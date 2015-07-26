import contextlib
import cherrypy

from . import base
from .. import models


def get_model_instance(model_id, model):
    try:
        return model.get(id=model_id)
    except model.DoesNotExist:
        raise cherrypy.NotFound()


def destr(strist):
    """Convert a thing that may be a string or a list into a list of strings"""
    if strist is None:
        return []
    elif isinstance(strist, str):
        return [strist]
    return [s for s in strist if s.strip()]


class SystemInterface(base.RestfulComponent):

    _cp_config = {
        'tools.database_connect.on': True
    }

    def get(self):
        return self.template('admin/systems.html', systems=models.System.select())

    def post(self):
        return self.template('admin/modify_system.html')

    def do_post(self, form):
        form['links'] = zip(destr(form.get('l-name')), destr(form.get('l-url')))
        system = models.System.create(
            name=form.get('name'),
            bite_md=form.get('bite'),
            bite=self.app.markdown(form.get('bite', '')),
            data_md=form.get('desc'),
            data=self.app.markdown(form.get('desc', '')))

        for name, link in form['links']:
            models.Link.insert(system=system, name=name, link=link).execute()
        raise cherrypy.HTTPRedirect("/systems/" + str(system.id))

    def put(self, system_id):
        return self.template('admin/modify_system.html',
                             system=get_model_instance(system_id, models.System))

    def do_put(self, system_id, form):
        form['links'] = zip(destr(form.get('l-name')), destr(form.get('l-url')))
        system = get_model_instance(system_id, models.System)
        if form.get('name') and form['name'].strip():
            system.name = form['name']
        if form.get('bite') and form['bite'].strip():
            system.bite_md = form['bite']
            system.bite = self.app.markdown(form['bite'])
        if form.get('desc') and form['desc'].strip():
            system.data_md = form['desc']
            system.data = self.app.markdown(form['desc'])

        system.save()

        models.Link.delete().where(models.Link.system == system).execute()
        for name, link in form['links']:
            models.Link.insert(system=system, name=name, link=link).execute()

        raise cherrypy.HTTPRedirect('/admin/systems/' + str(system_id) + '/put')

    def delete(self, system_id):
        return self.template('admin/delete_system.html',
                             system=get_model_instance(system_id, models.System))

    def do_delete(self, system_id, form):
        if form.get('delete', '').lower() != 'yes':
            raise cherrypy.HTTPRedirect('/admin/systems/')

        get_model_instance(system_id, models.System).delete_instance(recursive=True)
        raise cherrypy.HTTPRedirect('/admin/systems/')


class QuestionInterface(base.RestfulComponent):

    _cp_config = {
        'tools.database_connect.on': True
    }

    def get(self):
        return self.template('admin/questions.html', questions=models.Question.select())

    def post(self):
        return self.template('admin/modify_question.html', systems=models.System.select())

    def put(self, question_id):
        return self.template('admin/modify_question.html',
                             systems=models.System.select(),
                             question=get_model_instance(question_id, models.Question))

    def do_put(self, question_id, form):
        from pprint import pprint
        pprint(form)
        return ''

    def delete(self, question_id):
        return self.template('admin/delete_question.html',
                             question=get_model_instance(question_id, models.Question))


class AdminInterface(base.AuthenticatedComponent):
    index = base.Static.factory(page='admin/index.html')
    systems = SystemInterface.factory()
    questions = QuestionInterface.factory()

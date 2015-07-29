import string
import json
from functools import lru_cache

import jinja2
import mistune
import hashids
import webassets
from webassets.ext.jinja2 import AssetsExtension

from . import models as m
from . import utils, assets, components
from .markdown_renderer import DewidowRenderer

conf_default = object()


class VoteApplication(object):

    def __init__(self, config):
        self._config = config
        self.PRODUCTION = self.conf('general', 'production', False)

        m.database.init(self.conf('database', 'file'))

        self.markdown = mistune.Markdown(renderer=DewidowRenderer())

        self.hasher = hashids.Hashids(
            salt=self.conf('hashids', 'salt', ''),
            alphabet=self.conf('hashids', 'alphabet', string.ascii_lowercase + string.digits),
            min_length=self.conf('hashids', 'length', 5))

        webassets.filter.register_filter(assets.CSSCompressorFilter)

        self.assets_env = webassets.Environment('static/generated', 'static/generated',
            debug=self.conf('static', 'debug', (not self.PRODUCTION)),
            auto_build=self.conf('static', 'auto_build', (not self.PRODUCTION)))
        self.assets_env.append_path('static/js', 'static/js')
        self.assets_env.append_path('static/css', 'static/css')
        self.assets_env.config['CLOSURE_COMPRESSOR_OPTIMIZATION'] = 'ADVANCED_OPTIMIZATIONS'
        self.assets_env.config['PYSCSS_DEBUG_INFO'] = False
        self._install_assets(self.assets_env)

        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.conf('templating', 'directory')),
            extensions=[AssetsExtension], undefined=jinja2.StrictUndefined)
        self.template_env.globals.update(
            site_name='Searching For The Perfect System',
            base_url=self.conf('general', 'base_url'))
        self.template_env.filters.update({
            'dewidow': utils.dewidow})
        self.template_env.assets_environment = self.assets_env

    def bind_routes(self, routes):
        for url, component_factory in routes.items():
            component = component_factory(app=self)
            setattr(self, url, component)

    @lru_cache(maxsize=None)
    def conf(self, section, key, default=conf_default):
        if default is not conf_default:
            if not (section in self._config and key in self._config[section]):
                return default

        return eval(self._config[section][key])

    def _install_assets(self, env):
        js_common = webassets.Bundle('common/libVoting.js')
        js_admin = webassets.Bundle('admin/modify_links.js', 'admin/modify_answers.js')
        env.register('js.admin', js_common, js_admin,
                     filters='closure_js', output='admin-%(version)s.js')

        css_common = webassets.Bundle('common/main.scss', output='scssbuild-%(version)s.css')
        env.register('css.main', css_common,
                     filters=['pyscss', 'compressor'], output='main-%(version)s.css')

    def drop_tables(self):
        m.drop_tables()

    def create_tables(self):
        m.create_tables()

    def dump_models(self):
        systems, questions = m.dump_models()
        return {'systems': systems, 'questions': questions}

    def load_models(self, data):
        systems, questions = data['systems'], data['questions']
        m.load_models(systems=systems, questions=questions, markdown=self.markdown)


def create_app(config):
    app = VoteApplication(config=config)
    app.bind_routes({
        'index': components.Static.factory(page='site/index.html'),
        'about': components.Static.factory(page='site/about.html'),
        'quiz': components.Quiz.factory(hasher=app.hasher),
        'results': components.Results.factory(hasher=app.hasher),
        'systems': components.Systems.factory(),
        'static': components.Assets.factory(),
        'admin': components.admin.AdminInterface.factory()})
    return app

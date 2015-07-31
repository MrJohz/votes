from votes.components import base

try:
    from unittest import mock
except ImportError:
    import mock
import pytest
import cherrypy


class TestBaseComponent:

    def test_initialises_config(self):
        test_object = object()

        class SubComponent(base.BaseComponent):
            _cp_config = {'key1': 'test', 'key': 'ovewritten'}

        bc = base.BaseComponent(object(), config={'key': test_object})
        assert bc._cp_config == {'key': test_object}

        sc = SubComponent(object(), config={'key': test_object})
        assert sc._cp_config == {'key1': 'test', 'key': test_object}

    def test_sets_factories(self):

        class SubComponent(base.BaseComponent):
            pass

        class TestComponent(base.BaseComponent):
            component1 = SubComponent.factory()
            component2 = SubComponent.factory()

        assert TestComponent.component1.exposed is False
        assert TestComponent.component2.exposed is False

        tc = TestComponent(object())
        assert tc.component1.exposed is True
        assert tc.component2.exposed is True

    def test_factory_method(self):
        factory = base.BaseComponent.factory(config={'set in': 'factory'})
        assert factory(object())._cp_config == {'set in': 'factory'}

        factory = base.BaseComponent.factory(unrecognised='fails on initialiation')
        with pytest.raises(TypeError):
            factory(object())


class TestRestfulComponent:

    def test_calls_correct_methods(self):
        calls = []

        class TestRestful(base.RestfulComponent):

            def get(self):
                calls.append('get')

            def post(self):
                calls.append('post')

            def do_post(self, form):
                calls.append(('do_post', form))

            def put(self, id):
                calls.append(('put', id))

            def do_put(self, id, form):
                calls.append(('do_put', id, form))

            def delete(self, id):
                calls.append(('delete', id))

            def do_delete(self, id, form):
                calls.append(('do_delete', id, form))

        tr = TestRestful(object())

        tr.GET()
        assert calls[-1] == 'get'
        tr.GET('get')
        assert calls[-1] == 'get'
        tr.GET('post')
        assert calls[-1] == 'post'
        tr.GET('7', 'put')
        assert calls[-1] == ('put', 7)
        tr.GET('4', 'delete')
        assert calls[-1] == ('delete', 4)
        with pytest.raises(cherrypy.NotFound):
            tr.GET('get', '4')
        with pytest.raises(cherrypy.NotFound):
            tr.GET('put', '4')
        with pytest.raises(cherrypy.NotFound):
            tr.GET('put')
        with pytest.raises(cherrypy.NotFound):
            tr.GET('delete')
        with pytest.raises(cherrypy.NotFound):
            tr.GET('unknown method')

        tr.POST('post', **{'form': True})
        assert calls[-1] == ('do_post', {'form': True})
        tr.POST('1', 'put', **{'form': True})
        assert calls[-1] == ('do_put', 1, {'form': True})
        tr.POST('1', 'delete', **{'form': True})
        assert calls[-1] == ('do_delete', 1, {'form': True})
        with pytest.raises(cherrypy.HTTPError) as e:
            tr.POST('get')
        assert e.value.status == 405
        with pytest.raises(cherrypy.NotFound):
            tr.POST('delete')
        with pytest.raises(cherrypy.NotFound):
            tr.POST('unknown_method')


class TestStaticComponent:

    def test_returns_template_with_args(self):
        static = base.Static(app=object(), page='template.html', args={'one': 1})
        static.template = mock.Mock()
        static.GET()

        static.template.assert_called_once_with('template.html', one=1)

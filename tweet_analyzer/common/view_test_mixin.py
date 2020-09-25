
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

class ViewRequestFactoryTestMixin(object):
    longMessage = True  # More verbose messages
    view_class = None
    def get_response(self, method):
        factory = RequestFactory()
        req = getattr(factory, method)('/')
        req.user = AnonymousUser()
        return self.view_class.as_view()(req, *[], **{})

    def is_callable(self):
        resp = self.get_response('get')
        self.assertEqual(resp.status_code, 200)
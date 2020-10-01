
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

class ViewRequestFactoryTestMixin(object):
    longMessage = True  # More verbose messages
    view_class = None
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', email='tester@tester.com', password='top_secret')


        
    def get_response(self, method):
        factory = RequestFactory()
        req = getattr(factory, method)('/')
        req.user = self.user
        return self.view_class.as_view()(req, *[], **{})

    def is_callable(self):
        resp = self.get_response('get')
        self.assertEqual(resp.status_code, 200)

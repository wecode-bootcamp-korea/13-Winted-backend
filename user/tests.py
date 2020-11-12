from django.test import TestCase,Client

from .models import User

class UserTest(TestCase):
    def setUp(self):
        client = client()
        user.objects.create(name='john')

    def tearDown(self):
        User.objects.all().delete()

    def test_getuser_view(self):

        response = self.client.get('//user/1')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),  { 'name': 'john'})
        }

# Create your tests here.

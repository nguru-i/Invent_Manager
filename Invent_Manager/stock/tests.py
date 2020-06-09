from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from datetime import date, datetime, timedelta, time as dtime
import unittest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from .views import *
from .models import *
import unittest
from django.test import Client

User = get_user_model()

# Create your tests here.
class InventManagerTests(TestCase):
    def setUp(self):
        user = User.objects.get_or_create(username='testy')[0]
        user.is_staff = True
        user.is_superuser = True
        user.set_password('pass')
        user.save()
        self.client = Client()
        self.client.login(username='testy', password='pass')

    def test_log_in_attemp_while_already_logged_in(self):
        response = self.client.get('login')
        # self.client.login(username='testy', password='pass')
        self.assertRedirects(response, '')

    # def setUpCustomerUser(self):
    #     user2 = User.objects.get_or_create(username='pesty')[0]
    #     user2.is_staff = False
    #     user2.is_superuser = False
    #     user2.set_password('pass')
    #     group = Group.objects.get(name='customer')
    #     user2.save()
    #     # self.client.login(username='pesty', password='pass')
    def test_index_loads_properly(self):
        response = self.client.get('localhost:8000')
        self.assertEqual(response.status_code, 200)

    # def test_dashboard_is_only_accessible_to_admin_group(self):
    #     response = self.client.
    #     # self.client.login(username='testy', password='pass')
    #     # self.assertTrue(self.user.is_authenticated)
    #     self.assertRedirects('/',status_code=200)


    def test_registration_form_fields(self):
        # self.assertFieldOutput(EmailField, {'a@a.com': 'a@a.com'}, {'aaa': ['Enter a valid email address.']})
        pass



from .views import home

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        self

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('stock-home')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = home(request)
        # Use this syntax for class-based views.

        self.assertEqual(response.status_code, 200)





class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('stock-home')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        self.assertEqual(len(response.context['customers']), 5)
# tests/test_users.py


import unittest

from flask_login import LoginManager
from flask import request

from base import BaseTestCase
from project import bcrypt
from project.models import User
class UserViewsTests(BaseTestCase):

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertIn(b'Please login', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="admin@d.com", password="admin"),
                follow_redirects=True
            )

            self.assertIn(b'You were logged in', response.data)
            self.assertTrue(current_user.email == "admin@d.com")
            self.assertTrue(current_user.is_active())

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(email="wrong@d.com", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid username or password.', response.data)

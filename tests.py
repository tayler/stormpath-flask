"""
Our Flask-Stormpath tests.

Why are these in a single file instead of a directory?  Honestly, it's because
this extension is so simple, it didn't warrant a proper directory / module.  So
we'll just follow Flask conventions and have single file stuff going on.
"""


from os import environ
from unittest import TestCase

from flask.ext.stormpath import User

from stormpath.client import Client
from stormpath.resources.account import Account


class TestUser(TestCase):
    """Our User test suite."""

    def setUp(self):
        self.client = Client(
            id = environ.get('STORMPATH_API_KEY_ID'),
            secret = environ.get('STORMPATH_API_KEY_SECRET'),
        )
        self.application = self.client.applications.create({
            'name': 'flask-stormpath-tests',
            'description': 'This application is ONLY used for testing the Flask-Stormpath library. Please do not use this for anything serious.',
        }, create_directory=True)
        self.user = self.application.accounts.create({
            'given_name': 'Randall',
            'surname': 'Degges',
            'email': 'randall@stormpath.com',
            'password': 'woot1LoveCookies!',
        })
        self.user.__class__ = User

    def test_subclass(self):
        account = Account(client=self.client, properties={
            'given_name': 'Randall',
            'surname': 'Degges',
            'email': 'randall@stormpath.com',
            'password': 'woot1LoveCookies!',
        })
        self.assertEqual(type(account), Account)

        user = account
        user.__class__ = User
        self.assertTrue(user.writable_attrs)

    def test_get_id(self):
        self.assertEqual(self.user.get_id(), self.user.href)

    def test_is_active(self):
        self.assertEqual(self.user.is_active(), self.user.status == 'ENABLED')

    def tearDown(self):
        self.application.delete()
        self.client.directories.search('flask-stormpath-tests')[0].delete()

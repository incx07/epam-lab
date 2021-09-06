from unittest.mock import patch
from django.test import SimpleTestCase
from ..forms import RatingForm, LoginForm, RegisterForm


class FormsTest(SimpleTestCase):

    def test_rating_form_with_invalid_data(self):
        form_data = {'rating': '6'}
        form = RatingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Select a valid choice. 6 is not one of the available choices.',
            str(form.errors.as_data()['rating'])
        )

    def test_rating_form_with_valid_data(self):
        form_data = {'rating': '5'}
        form = RatingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_field_labels(self):
        form = LoginForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Username: ')
        self.assertTrue(form.fields['password'].label is None or form.fields['password'].label == 'Password: ')

    def test_login_form_with_invalid_long_username(self):
        form_data = {
            'username': 'long_long_long_long_long_long_long_long_long_long_\
                long_long_long_long_long_long_long_long_long_long_long_long_\
                long_username',
            'password': '123qwddd'
            }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Ensure this value has at most 150 characters (it has 155).',
            str(form.errors.as_data()['username'])
        )

    def test_login_form_with_invalid_long_password(self):
        form_data = {
            'username': 'test_user',
            'password': 'very_very_very_very_strong_password'
            }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Ensure this value has at most 30 characters (it has 35).',
            str(form.errors.as_data()['password'])
        )

    @patch('myshowsapp.forms.client')
    def test_login_form_with_invalid_credentian_data(self, mock_client):
        mock_client.is_authenticated = False
        mock_client.error = 'No active account found with the given credentials'
        form_data = {
            'username': 'test_user',
            'password': 'strong_password'
            }
        form = LoginForm(data=form_data)
        #mock_client.login.assert_called_once_with('test_user', 'strong_password')
        self.assertFalse(form.is_valid())
        self.assertIn(
            'No active account found with the given credentials',
            str(form.errors.as_data()['__all__'])
        )

    @patch('myshowsapp.forms.client')
    def test_login_form_with_valid_credentian_data(self, mock_client):
        mock_client.is_authenticated = True
        form_data = {
            'username': 'test_user',
            'password': 'strong_password'
            }
        form = LoginForm(data=form_data)
        #mock_client.login.assert_called_once_with('test_user', 'strong_password')
        self.assertTrue(form.is_valid())

    def test_register_form_field_labels(self):
        form = RegisterForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Username: ')
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'Email address: ')
        self.assertTrue(form.fields['password'].label is None or form.fields['password'].label == 'Password: ')
        self.assertTrue(form.fields['re_password'].label is None or form.fields['re_password'].label == 'Password confirmation: ')

    def test_register_form_with_invalid_long_username(self):
        form_data = {
            'username': 'long_long_long_long_long_long_long_long_long_long_\
                long_long_long_long_long_long_long_long_long_long_long_long_\
                long_username',
            'email': '12@12.com',
            'password': '123qwddd',
            're_password': '123qwddd'
            }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Ensure this value has at most 150 characters (it has 155).',
            str(form.errors.as_data()['username'])
        )

    def test_register_form_with_invalid_long_email(self):
        form_data = {
            'username': 'test_user',
            'email': 'long_long_long_long_long_long_long_long_long_long_\
                long_long_long_long_long_long_long_long_long_long_long_long_\
                long_long_long_long_long_long_long@email.com',
            'password': '123qwddd',
            're_password': '123qwddd'
            }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', str(form.errors.as_data()['email']))

    def test_register_form_with_invalid_long_password(self):
        form_data = {
            'username': 'test_user',
            'email': '12@12.com',
            'password': 'very_very_very_very_strong_password',
            're_password': 'very_very_very_very_strong_password'
            }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Ensure this value has at most 30 characters (it has 35).',
            str(form.errors.as_data()['password'])
        )

    @patch('myshowsapp.forms.register')
    def test_register_form_with_invalid_credentian_data(self, mock_register):
        mock_register.return_value = {
            'errors': {
                'password': [
                    'This password is too short. It must contain at least 8 characters.',
                    'This password is too common.',
                    'This password is entirely numeric.'
                ]
            }
        }
        form_data = {
            'username': 'test_user',
            'email': '12@12.com',
            'password': '123',
            're_password': '123'
            }
        form = RegisterForm(data=form_data)
        #mock_register.assert_called_once_with('test_user', '12@12.com', '123', '123')
        self.assertFalse(form.is_valid())
        self.assertIn(
            'This password is too short. It must contain at least 8 characters.',
            str(form.errors.as_data()['password'])
        )

from django.forms import Form, CharField, PasswordInput, ChoiceField, EmailField, ValidationError
from .service.auth_api_service import client, register


class RatingForm(Form):
    rating = ChoiceField(
        choices= [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5')
        ], 
        required=False
    )


class LoginForm(Form):
    username = CharField(max_length=150, label='Username: ')
    password = CharField(max_length=30, label='Password: ', widget=PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        client.login(username, password)
        if not client.is_authenticated:
            raise ValidationError(client.error)
        return cleaned_data


class RegisterForm(Form):
    username = CharField(max_length=150, label='Username: ')
    email = EmailField(max_length=200, label='Email address: ', required=False)
    password = CharField(max_length=30, label='Password: ', widget=PasswordInput)
    re_password = CharField(max_length=30, label='Password confirmation: ', widget=PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        response = register(username, email, password, re_password)
        if 'errors' in response:
            for error_field, error_value in response['errors'].items():
                if 'non_field_errors' in error_field:
                    raise ValidationError(error_value)
                else:
                    self.add_error(error_field, error_value)
        return cleaned_data

class PasswordResetForm(Form):
    email = EmailField(max_length=200, label='Email address: ')


class PasswordResetConfirmForm(Form):
    password = CharField(max_length=30, label='New password: ', widget=PasswordInput)
    re_password = CharField(max_length=30, label='New password confirmation: ', widget=PasswordInput)

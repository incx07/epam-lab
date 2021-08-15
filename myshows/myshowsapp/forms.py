from django.forms import Form, CharField, PasswordInput, ChoiceField, EmailField


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


class RegisterForm(Form):
    username = CharField(max_length=150, label='Username: ')
    email = EmailField(max_length=200, label='Email address: ', required=False)
    password = CharField(max_length=30, label='Password: ', widget=PasswordInput)
    re_password = CharField(max_length=30, label='Password confirmation: ', widget=PasswordInput)


class PasswordResetForm(Form):
    email = EmailField(max_length=200, label='Email address: ')


class PasswordResetConfirmForm(Form):
    password = CharField(max_length=30, label='New password: ', widget=PasswordInput)
    re_password = CharField(max_length=30, label='New password confirmation: ', widget=PasswordInput)

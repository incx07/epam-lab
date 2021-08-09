from django.forms import Form, CharField, PasswordInput, ChoiceField, EmailField


class RatingForm(Form):
    rating = ChoiceField(
        choices= [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5')
        ]
    )


class Loginform(Form):
    username = CharField(max_length=150, label='Username: ')
    password = CharField(max_length=30, label='Password: ', widget=PasswordInput)


class Registerform(Form):
    username = CharField(max_length=150, label='Username: ')
    email = EmailField(max_length=200, label='Email address: ', required=False)
    password = CharField(max_length=30, label='Password: ', widget=PasswordInput)
    re_password = CharField(max_length=30, label='Password confirmation: ', widget=PasswordInput)

from django.forms import ModelForm, Select, Form, CharField, PasswordInput
from .models.full_watched_show import FullWatchedShow


RATING_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
]


class RatingForm(ModelForm):
    class Meta:
        model = FullWatchedShow
        fields = ['rating']
        widgets = {
            'rating': Select(
                choices=RATING_CHOICES,
                attrs={'class':'custom-select custom-select-sm'}
            )    
        }


class Loginform(Form):
    username = CharField(max_length= 25, label="Enter username")
    password = CharField(max_length= 30, label='Password', widget=PasswordInput)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    name = forms.CharField(label='성명', max_length=30, required=True, help_text='이름을 입력하세요.')
    email = forms.EmailField(max_length=254, help_text='유효한 이메일 주소를 입력하세요.')

    class Meta:
        model = User
        fields = ['name', 'username', 'password1', 'password2', 'email']

class FindUsernameForm(forms.Form):
    email = forms.EmailField(label='이메일')

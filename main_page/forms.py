from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


### 회원가입 폼 ###
class SignUpForm(UserCreationForm):
    name = forms.CharField(
        label="성명", max_length=30, required=True, help_text="이름을 입력하세요."
    )
    email = forms.EmailField(max_length=254, help_text="유효한 이메일 주소를 입력하세요.")
    first_name = forms.CharField(
        label="이름", max_length=60, required=True, help_text="이름을 입력하세요."
    )
    username = forms.CharField(
        label="아이디", max_length=30, required=True, help_text="ID를 입력하세요."
    )
    email = forms.EmailField(max_length=254, help_text="유효한 이메일 주소를 입력하세요.")

    class Meta:
        model = User
        fields = ["name", "username", "password1", "password2", "email"]


### 아이디 찾기 폼 ###
class FindUsernameForm(forms.Form):
    email = forms.EmailField(label="이메일")
    # first_name = forms.CharField(max_length=60, required=True, help_text='성명을 입력하세요.')
    username = forms.CharField(
        label="ID", max_length=30, required=True, help_text="ID를 입력하세요."
    )
    email = forms.EmailField(max_length=254, help_text="유효한 이메일 주소를 입력하세요.")
    # password1 = forms.CharField(widget=forms.PasswordInput, help_text='비밀번호를 입력하세요.')
    # password2 = forms.CharField(widget=forms.PasswordInput, help_text='비밀번호를 다시 입력하세요.')

    class Meta:
        model = User
        fields = ["first_name", "username", "password1", "password2", "email"]
        labels = ["이름", "아이디", "비밀번호", "비밀번호 확인", "이메일"]


class FindUsernameForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True, label="성명")
    email = forms.EmailField(max_length=254, required=True, label="이메일")
    first_name = forms.CharField(max_length=30, required=True, label="성명")
    email = forms.EmailField(max_length=254, required=True, label="이메일")


### 회원 정보 폼 ###
class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text="유효한 이메일 주소를 입력하세요.")

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder': '아이디'}))
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
    class Meta:
        model = User
        fields = ['username', 'password']


class UserForm(forms.ModelForm):
    username = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder': '아이디'}))
    email = forms.CharField(label='email',widget=forms.EmailInput(attrs={'placeholder': '이메일'}))
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']




class SignUpForm(UserCreationForm):
   # email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.')
   username = forms.CharField(label='username', widget=forms.TextInput(attrs={'placeholder': '아이디'}))
   password1 = forms.CharField(label='password1', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
   password2 = forms.CharField(label='password2', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
   class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

#
# class BoardForm(forms.Form):
#     title = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#     message = forms.CharField(
#         widget=forms.Textarea(
#             attrs={
#                 'class':'form-fontrol',
#             }
#         )
#     )
class BoardForm(forms.ModelForm):
    board_title = forms.CharField(label='title',
                    widget=forms.TextInput(attrs={'placeholder': '제목'}))
    message = forms.CharField(label='title',
                    widget=forms.Textarea(attrs={'placeholder': '내용'}))

    class Meta:
        model = Board
        fields = ('board_title', 'message',)




class contact_form(forms.Form):
    contact_name = forms.CharField(label='Contact Name', max_length=255,)
    contact_email = forms.CharField(label='Contact Email',max_length=255)
    contact_message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
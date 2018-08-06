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
   email = forms.EmailField(max_length=255,label='email', widget=forms.TextInput(attrs={'placeholder': '이메일'}))
   password1 = forms.CharField(label='password1', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
   password2 = forms.CharField(label='password2', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
   class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2', )

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

    CHOICES1 = (('선택', '선택'),('기업', '기업'),('일반인', '일반인'))
    CHOICES2 = (('분류', '분류'),('가맹 및 제휴', '가맹 및 제휴'),('서비스 문의', '서비스 문의'),('채용', '채용'),('기타', '기타'))
    customer_select = forms.ChoiceField(choices=CHOICES1)
    question_select = forms.ChoiceField(choices=CHOICES2)
    contact_name = forms.CharField(label='Contact Name', max_length=255,widget=forms.TextInput(attrs={'placeholder': ' 성명 (업체명)'}))
  #  contact_email = forms.CharField(label='Contact Email',max_length=255)
    contact_message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )


class TestContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    # the new bit we're adding
    def __init__(self, *args, **kwargs):
        super(TestContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"
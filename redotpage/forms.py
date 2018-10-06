from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Board


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder': '아이디'}))
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))

    class Meta:
        model = User
        fields = ['username', 'password']




class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255, label='email', widget=forms.EmailInput(attrs={'placeholder': '이메일'}))
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'placeholder': '아이디'}))
    password1 = forms.CharField(label='password1', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput(attrs={'placeholder': '재확인'}))


    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("이메일이 비어있습니다.")
        if User.objects.filter(email=self.cleaned_data['email']).count():
            raise ValidationError("이미 등록된 이메일 입니다.")
        return self.cleaned_data['email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not ValidationError:
            raise ValidationError("이메일이 비어있습니다.")
        if User.objects.filter(email=self.cleaned_data['username']).count():
            raise ValidationError("이미 등록된 아이디 입니다.")
        return self.cleaned_data['username']

    class Meta:
        model = User
        fields = ['email', 'username', 'password1','password2' ]


class BoardForm(forms.ModelForm):
    board_title = forms.CharField(label='title',
                    widget=forms.TextInput(attrs={'placeholder': '제목','class':'form-control title'}))
    message = forms.CharField(label='title',
                    widget=forms.Textarea(attrs={'placeholder': '내용','class': 'form-control text'}))

    class Meta:
        model = Board
        fields = ('board_title', 'message',)


class contact_form(forms.Form):

    CHOICES1 = (('선택', '선택'),('기업', '기업'),('일반인', '일반인'))
    CHOICES2 = (('분류', '분류'),('가맹 및 제휴', '가맹 및 제휴'),('서비스 문의', '서비스 문의'),('채용', '채용'),('기타', '기타'))
    customer_select = forms.ChoiceField(choices=CHOICES1)
    question_select = forms.ChoiceField(choices=CHOICES2)
    contact_name = forms.CharField(label='Contact Name', max_length=255,widget=forms.TextInput(attrs={'placeholder': ' 성명 (업체명)'}))
    contact_email = forms.CharField(label='Contact Email', max_length=255,widget=forms.EmailInput(attrs={'placeholder': ' 이메일'}))

    contact_message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

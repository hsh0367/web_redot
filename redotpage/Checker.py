from .models import TestUser


class Checker:

    def validate_email(self,value):

        if TestUser.objects.filter(email=value).exists():
            #raise Test_SignupForm.error_messages("이메일이 이미 등록되어 있습니다.")
            return False
        else:
            return True

    def validate_username(self,value):
        if TestUser.objects.filter(username=value).exists():
            #raise Test_SignupForm.error_messages(" 이미 등록된 아이디입니다.")
            return False
        else:
            return True

    def validate_passord(self, value):
        if len(value) <8:
            return False
        else:
            return True
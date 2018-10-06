from django.contrib.auth.models import User


class Checker:

    def validate_value(self,email,username,password1,password2):

        errors = []

        if User.objects.filter(email=email).exists():
            errors.append("이미 등록된 이메일 입니다.")
        else:
            errors.append("옳바른 이메일 입니다.")

        if User.objects.filter(username=username).exists():
            errors.append("이미 등록된 아이디 입니다.")
        else:
            errors.append("옳바른 아이디 입니다.")

        if password1 != password2:
            errors.append("비밀번호가 서로 일치하지 않습니다.")
        else:
            errors.append("옳바른 비밀번호2 입니다.")

        if len(password1) < 8 :
            errors.append("비밀번호는 최소 8자리 이상되야 합니다.")
        else:
            errors.append("옳바른 비밀번호 입니다.")

        return errors
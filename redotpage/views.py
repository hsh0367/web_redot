from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template, render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import *
from .models import Board,TestUser
from .token import account_activation_token
from .Checker import *
def main(request):
    return render(request,"redotweb/main_redot.html")


def main_business(request):
    return render(request,"redotweb/main_redot_business.html")


def board(request):
    board_obeject = Board.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(board_obeject, 10)
    try:
        boards = paginator.page(page)
    except PageNotAnInteger:
        boards = paginator.page(1)
    except EmptyPage:
        boards = paginator.page(paginator.num_pages)
    return render(request, "redotweb/board_redot.html", {'boards': boards})


def board_view(request,pk):
    board = get_object_or_404(Board, number=pk)
    board.hit += 1
    board.save()
    return render(request, "redotweb/board_view_redot.html",{'board':board})


@login_required
def board_new(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = Board()
           # board = form.save(commit=False)
            board.author = request.user
            board.board_title = form.cleaned_data['board_title']
            board.message = form.cleaned_data['message']
            board.user_id = request.user.username
            board.create_date = timezone.now()
            board.save()
            return redirect('board_view', pk=board.pk)
    else:
        form = BoardForm()
    return render(request, 'redotweb/board_new_redot.html', {'form': form})


def contact(request):
    form_class = contact_form

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            # customer = request.POST.get('customer_select', '')
            # question = request.POST.get('question_select', '')

            customer = form.cleaned_data['customer_select']
            question = form.cleaned_data['question_select']

            contact_name =form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            form_content = form.cleaned_data['contact_message']

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
        context = {
            'customer': customer,
            'question': question,
            'contact_name': contact_name,
            'contact_email': contact_email,
            'form_content': form_content,
        }
        content = template.render(context)

        email = EmailMessage(
            "고객 "+contact_name+"이 새로운 접촉 제출되었습니다.",
            content,
            contact_email,
            ['redot.help@gmail.com'],
        )
        email.send()
        return redirect('contact')
    return render(request, 'redotweb/contact_redot.html', {'form': form_class, })


def download(request):
    return render(request,"redotweb/download_redot.html")


def pr(request):
    return render(request,"redotweb/pr_redot.html")


def signIn(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        # user = authenticate(request)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
            return render(request, 'redotweb/login_redot.html', {'form': login_form})
    else:
        login_form = LoginForm()
        return render(request, 'redotweb/login_redot.html', {'form': login_form})



#이메일인증 리캡챠 구현전까지 회원가입 차단


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = SignUpForm()
    return render(request, 'redotweb/signup.html', {'form': form})



# 이메일 인증 회원가입 테스트


def test_signup(request):
    if request.method == 'POST':
        form = Test_SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            # email, username, password check vaild value
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('account_activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )

            email.send()
            return HttpResponse('Please confirm your email address to complete the registration',)
    else:
        form = Test_SignupForm()
    return render(request, 'redotweb/testsignup.html', {'form': form})

    """
        class UserActivate(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self,requset, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user,token):
                user.active = True
                user.save()
                return Response(user.user_id + ' 계정이 활성화 되었습니다.', status=status.HTTP_200_OK)
            else:
                return Response('만료된 링크입니다.', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(traceback.format_exc())


class UserActivateView(TemplateView):
    logger = logging.getLogger(__name__)
    template_name = 'template/account_activate_complate.html'

    def get(self, request, *args, **kwargs):
        self.logger.debug('UserActivateView.get()')

        uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
        token = self.kwargs['token']

        self.logger.debug('uid: %s, token: %s' % (uid, token))

        try:
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.logger.warning('User %s not found' % uid)
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            self.logger.info('User %s(pk=%s) has been activated.' % (user, user.pk))

        return super(UserActivateView, self).get(request, *args, **kwargs)
        """


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, TestUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
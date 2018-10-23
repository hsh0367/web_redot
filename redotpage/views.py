import mimetypes

import os
import urllib
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import *
from .models import Board
from django.contrib.auth.models import User
from .token import account_activation_token
from .Checker import *


def main(request):
    return render(request,"redotweb/main_redot.html")


def main_business(request):
   return render(request,"redotweb/main_biz_redot.html")


def require(request):
    return render(request,"redotweb/login_require.html")


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


@login_required(login_url='/error/login/')
def board_view(request,pk):
    board = get_object_or_404(Board, number=pk)
    board.hit += 1
    board.save()
    return render(request, "redotweb/board_view_redot.html",{'board':board})


@login_required(login_url='/error/login/')
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


@login_required(login_url='/error/login/')
def board_edit(request, pk):
    board = get_object_or_404(Board, number=pk)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            board.published_date = timezone.now()
            board.save()
            return redirect('board_view', pk=board.pk)
    else:
        form = BoardForm(instance=board)
    return render(request, 'redotweb/board_new_redot.html', {'form': form})

@login_required(login_url='/error/login/')
def board_delete(request, pk):
    board = Board.objects.get(number=pk)
    board.delete()
    return redirect('board')


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
            return redirect('/')
        else:
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
            return render(request, 'redotweb/login_redot.html', {'form': login_form})
    else:
        login_form = LoginForm()
        return render(request, 'redotweb/login_redot.html', {'form': login_form})


# test download function

def testdownload(request):

    respond_as_attachment(request, '/Users/heosanghun/Desktop/redot/redotweb/redotpage/static/asset/app.png', 'app.png')
    return redirect('download')

# email athutication signup

def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)


        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False

            # email, username, password check vaild value#
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            #check = Checker()
            #checks = check.validate_value(email,username,password1,password2)
            #if len(checks) == 0:
            user.save()
            current_site = get_current_site(request)
            mail_subject = '리닷사이트 계정등록 이메일 인증 링크'
            message = render_to_string('account_activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
            })
            #to_email = form.cleaned_data['email']
            email = EmailMessage(
                        mail_subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return HttpResponse('이메일주소에서 리닷사이트 회원가입을 위한 링크를 확인해주세요',)

           # else:
           #     form = SignupForm()
            #    return render(request, 'redotweb/register_redot.html', {'form': form, 'checks': checks,})
    else:
        form = SignupForm()
    return render(request, 'redotweb/register_redot.html', {'form': form, })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request,'account_activate_complate.html')
    else:
        return HttpResponse('올바르지 않은 링크입니다.')


#file download test
def respond_as_attachment(request, file_path, original_filename):
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response
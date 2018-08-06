from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template

from .forms import *
from .models import *

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
            contact_name = request.POST.get('contact_name', '')
            form_content = request.POST.get('contact_message', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
        context = {
            'customer': customer,
            'question': question,
            'contact_name': contact_name,
            'form_content': form_content,
        }
        content = template.render(context)

        email = EmailMessage(
            "New contact form submission",
            content,
            "Your website" + 'redot.kr',
            ['redot.help@gmail.com'],
        )
        email.send()
        return redirect('contact')
    return render(request, 'redotweb/contact_redot.html', {'form': form_class, })


def email_contact(request):
    form_class = contact_form

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            #customer = request.POST.get('customer_select', '')
            #question = request.POST.get('question_select', '')

            customer = form.cleaned_data['customer_select']
            question = form.cleaned_data['question_select']
            contact_name = request.POST.get('contact_name', '')
            form_content = request.POST.get('contact_message', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
        context = {
            'customer': customer,
            'question': question,
            'contact_name': contact_name,
            'form_content': form_content,
        }
        content = template.render(context)

        email = EmailMessage(
            "New contact form submission",
            content,
            "Your website" + '',
            ['redot.help@gmail.com'],
        )
        email.send()
        return redirect('email')
    return render(request, 'test.html', {'form': form_class,})


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


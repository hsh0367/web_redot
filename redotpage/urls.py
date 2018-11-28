from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import logout
from .import views


urlpatterns = [
    #홈페이지 리뉴얼 작업 완료전까지 url 수정

    #리뉴얼전까지 막아두기
    url(r'^$', views.block, name='block'),
    url(r'test/business/$', views.main_business, name='business'),
    url(r'test/pr/$', views.pr, name='pr'),
    url(r'test/$', views.main, name='main'),
    url(r'test/contact/$', views.contact, name='contact'),
    url(r'test/download/$', views.download, name='download'),
    url(r'test/signin/$', views.signIn, name='signin'),
    url(r'test/error/login/$', views.require, name='require'),
    url(r'test/error/user/$', views.user_error, name='errorUser'),
    url(r'test/board/(?P<pk>\d+)/check/$', views.board_user_check, name='board_user_check'),
    url(r'test/board/$', views.board, name='board'),
    url(r'test/board/view/(?P<pk>\d+)/$', views.board_view, name='board_view'),
    url(r'test/board/new/$', views.board_new, name='board_new'),
    url(r'test/board/(?P<pk>\d+)/edit/$', views.board_edit, name='board_edit'),
    url(r'test/board/(?P<pk>\d+)/delete/$', views.board_delete, name='board_delete'),
    # 이메일인증 및 리갭챠 구현전까지 회원가입 막음
    # 이메일 인증 회원가입 테스트
    url(r'test/register/$', views.signup, name='register'),
    url(r'test/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'test/signout/$', logout, {'next_page': 'main'}, name='logout'),
    # url(r'^testdownload/$', views.testdownload, name='testdownload'),


]
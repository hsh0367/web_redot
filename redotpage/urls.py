from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import logout
from .import views


urlpatterns = [

    url(r'^business/$', views.main_business, name='business'),
    url(r'^pr/$', views.pr, name='pr'),
    url(r'^$', views.main, name='main'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^download/$', views.download, name='download'),
    url(r'^signin/$', views.signIn, name='signin'),
    url(r'^error/login/$', views.require, name='require'),
    url(r'^board/$', views.board, name='board'),
    url(r'^board/view/(?P<pk>\d+)/$', views.board_view, name='board_view'),
    url(r'^board/new/$', views.board_new, name='board_new'),
    url(r'^board/(?P<pk>\d+)/edit/$', views.board_edit, name = 'board_edit'),
    url(r'^board/(?P<pk>\d+)/delete/$', views.board_delete, name = 'board_delete'),
    # 이메일인증 및 리갭챠 구현전까지 회원가입 막음
    # 이메일 인증 회원가입 테스트
    url( r'^register/$', views.signup, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^signout/$', logout, {'next_page': 'main'}, name='logout'),
    #url(r'^testdownload/$', views.testdownload, name='testdownload'),

]
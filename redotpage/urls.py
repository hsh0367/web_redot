from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^business/$', views.main_business, name='business'),
    # path('board', views.board, name='board'),
    # path('board/view', views.board_view, name='board_view'),
    # path('board/new', views.board_new, name='board_new'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^download/$', views.download, name='download'),
    url(r'^signin/$', views.signIn, name='signin'),
    url(r'^pr/$', views.pr, name='pr'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^board/$', views.board, name='board'),
    url(r'^board/view/(?P<pk>\d+)/$', views.board_view, name='board_view'),
    url(r'^board/new/$', views.board_new, name='board_new'),

]
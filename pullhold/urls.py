from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'pullhold'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^addtitle/$', views.AddNewComicTitleView.as_view(), name='addtitle'),
    url(r'^newcomicsearch/$', views.ComicTitleSearchView.as_view(), name='newcomicsearch'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^$', views.PullHoldMenuView.as_view(), name='index'),
    url(r'^pulladd/$', views.PullHoldAddView.as_view(), name='pulladd'),
    url(r'^holdlist/$', views.HoldListView.as_view(), name='holdlist'),
    url(r'^login/$', views.UserSignIn.as_view(), name='login'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
]

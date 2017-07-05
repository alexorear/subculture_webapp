from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'pullhold'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^$', views.PullHoldView.as_view(), name='index'),
    url(r'^login/$', views.UserSignIn.as_view(), name='login'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
]

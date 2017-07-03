from django.conf.urls import url
from . import views

app_name = 'pullhold'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
]

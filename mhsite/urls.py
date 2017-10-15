from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

urlpatterns =[
    url(r'^$', views.home),
    url(r'^login/$', views.loginf),
    url(r'^logout/$', views.logoutf),
    url(r'^register/$', views.registration),
    url(r'^application/$', views.application),
]

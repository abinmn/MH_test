from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

urlpatterns =[
    url(r'^$', views.home),
    url(r'^login/$', login, {'template_name': 'mhsite/login.html'}),
    url(r'^register/$', views.registration),
    url(r'^application/$', views.application),
]

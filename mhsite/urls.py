from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

urlpatterns =[
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.loginf, name='log'),
    url(r'^logout/$', views.logoutf, name='log'),
    url(r'^register/$', views.registration, name='register'),
    url(r'^application/$', views.application, name='application'),
    url(r'^allocation/$', views.allocation, name='alloc'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^mess/$', views.mess, name='mess'),
]

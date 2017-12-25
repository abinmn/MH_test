from django.conf.urls import url
from mhsite import views
from django.contrib.auth.views import login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns =[
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.loginf, name='log'),
    url(r'^accounts/login/$', views.loginf, name='log'),
    url(r'^logout/$', views.logoutf, name='log'),
    url(r'^register/$', views.registration, name='register'),
    url(r'^application/$', views.application, name='application'),
    url(r'^allocation/$', views.allocation, name='alloc'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^mess/$', views.mess, name='mess'),
    url(r'^pwdreset/$', views.pwdreset, name='mess'),
    url(r'^reset-password/$', password_reset,{'template_name':'mhsite/forget.html'}, name='login'),
    url(r'^reset-password/done/$', password_reset_done,{'template_name':'mhsite/forgetview.html'}, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$', password_reset_confirm,{'template_name':'mhsite/forgetupdate.html'}, name='password_reset_confirm'),
    url(r'^reset-password/complete/$', password_reset_complete,{'template_name':'mhsite/forgetview2.html'}, name='password_reset_complete'),
    url(r'^studentscorner/$', views.students, name='students'),
    url(r'^expense_tracker/(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})/$', views.expense, name='expense'),
    url(r'report/$', views.Report.as_view(), name='report'),
    url(r'report/(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})/$',views.ReportDetails.as_view(), name='report_details'),

]

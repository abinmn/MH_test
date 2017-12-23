from django.conf.urls import url
from mhsite import views
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
    url(r'^studentscorner/$', views.students, name='students'),
    url(r'^expense_tracker/(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})/$', views.expense, name='expense'),
    url(r'^report/$', views.Report.as_view(), name='report'),
    url(r'^report/(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})/$',views.ReportDetails.as_view(), name='report_details'),
    url(r'^mess_cut/$',views.mess_cut,name='mess_cut'),
    url(r'^mess_cut/processing/$', views.processing, name='mess_cut_processing'),
    url(r'^mess_cut/processing/(?P<mess_id>[0-9]+)/$', views.approval, name='mess_cut_approval'),
    url(r'^mess_cut/processing/(?P<mess_id>[0-9]+)/submit$', views.final, name='mess_cut_final')
]

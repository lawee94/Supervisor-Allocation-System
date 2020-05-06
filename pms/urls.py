from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name="pms"

urlpatterns = [
    url(r'^index', views.index, name="index"),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^student_reg', views.register , name="student_reg"),
    url(r'^supervisor_reg', views.sup_register , name="supervisor_reg"),
    url(r'^std_reg', views.std_register , name="std_reg"),
    url(r'^admin_reg', views.admin_register , name="admin_reg"),
    url(r'^student_profile', views.student_profile , name="student_profile"),
    url(r'^cord', views.cord , name="cord"),
    url(r'^reg_done', views.reg_done , name="reg_done"),
    url(r'^eligible', views.eligible.as_view() , name="eligible"),
    url(r'^student', views.student , name="student"),
    url(r'^student_profile/', views.student_profile , name="student_profile"),
    url(r'^supervisor', views.supervisor , name="supervisor"),
    url(r'^super_profile', views.super_profile , name="super_profile"),
    url(r'^cord', views.cord , name="cord"),
    url(r'^upload', views.upload , name="upload"),
    url(r'^std_upload', views.std_upload , name="std_upload"),
    
    url(r'^upload_view/', views.uploadview, name="upload_view"),
    path('sup/<slug:surname>', views.super_detail, name='super_detail'),
    path('std/<slug:username>', views.student_detail, name='student_detail'),
    path('about_us', views.about, name='about_us'),
    path('contact', views.contact, name='contact'),
    path('sup_list', views.allsup, name='sup_list'),
    path('std_list', views.allstudent, name='std_list'),
    path('admin_list', views.alladmin, name='admin_list'),
    path('allocate', views.allocate, name='allocate'),
    path('page', views.mypage, name='page'),
    url(r'^searchs/$', views.searchs, name='searchs'),
    path('page/faq_search/', views.faq_search_autocomplete, name='faq_search'),

    path('<int:pk><group>', views.deactivate, name='deactivate'),
    url(r'^user/(?P<pk>\d+)/delete/$', views.delete_user, name='delete_user'),
    url(r'^user/(?P<pk>\d+)/update/$', views.edit_user, name='update_user'),

]


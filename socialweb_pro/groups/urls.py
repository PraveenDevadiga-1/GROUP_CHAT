from django.urls import path
from django.conf.urls import url
from . import views

app_name='groups'

urlpatterns = [

   path('',views.ListGroups.as_view(),name='all'),
   url(r'^new/$',views.CreateGroup.as_view(),name='create'),
   path('posts/in/<slug>/',views.GroupDetail,name='single'),
   url(r'^join/(?P<slug>[-\w]+)/$',views.JoinGroup.as_view(),name='join'),
   url(r'^leave/(?P<slug>[-\w]+)/$',views.LeaveGroup.as_view(),name='leave'),
   url(r'^delete/(?P<slug>[-\w]+)/$',views.DeleteGroup.as_view(),name='delete'),

]

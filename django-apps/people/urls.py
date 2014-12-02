from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(r'^$', views.list_interactions),
                       url(r'^list_people/$', views.list_people),
                       url(r'^list_interactions/$', views.list_interactions),
                       url(r'^(?P<person_id>\d+)/person/$', views.person),
                       url(r'^(?P<interaction_id>\d+)/interaction/$', views.interaction),
                       )

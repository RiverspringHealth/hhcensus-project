'''
Created on Jul 6, 2019

@author: fsells
'''
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
from webapp import views


app_name = 'webapp'  #required to use  as a qualifying namespace in template



#use generic viewsobsolete

urlpatterns = [

    path('census_edit', views.census_edit, name='census_edit'),
    path('daily_error_details', views.daily_error_details, name='daily_error_details'),
    path('monthly_summary', views.monthly_summary, name='monthly_summary'),
    path('notifications', views.notifications, name='notifications'),
    path('resident_location', views.resident_location, name='resident_location'),
    path('save_changes', views.save_changes, name='save_changes'),
    path('home', views.home, name='home'),
 ###   path('daily_census_report', views.daily_census_report, name='daily_census_report'),
    path('logout', views.logout, name='logout'),


]


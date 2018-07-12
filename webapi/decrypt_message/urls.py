'''
Created on 17-Jun-2018

@author: priyesh
'''
from . import views
from django.conf.urls import url

urlpatterns = [url(r'decryptMessage/$', views.decrypt_message, name='decrypt_message')
               ]
from django.urls import path, include
from . import views
import djoser

urlpatterns = [
    path('gettime', views.get_time, name='getTime'),
    path('getRepo', views.get_repo, name='getRepo'),
    path('addRepo', views.add_repo, name='addRepo'),
    path('getallrepo', views.get_all_repo, name='get_all_repo')
]

from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.repos, name='index'),
    path('<int:repo_id>/', views.repos_detail, name='repos_detail')

]

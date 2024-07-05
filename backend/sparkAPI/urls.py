from django.urls import path

from . import views

urlpatterns = [
    path('generate_repo_json/', views.generate_target_repos_json, name='create_repo_json'),
    path('view_repo_json/', views.view_target_repos_json, name='view_repo_json')
]



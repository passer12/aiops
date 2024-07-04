from django.urls import path

from . import views

urlpatterns = [
    path('create_repo_json/', views.generate_target_repos_json, name='repo_json'),
    path('update_repo_json/', views.update_target_repos_json, name='update_repo_json')
]



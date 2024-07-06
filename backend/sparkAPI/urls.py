from django.urls import path

from . import views

urlpatterns = [
    # path('generate_repo_json/', views.generate_target_repos_json, name='create_repo_json'),
    # path('view_repo_json/', views.view_target_repos_json, name='view_repo_json'),
    path('generate_repo_json_secure/', views.generate_target_repos_json_secure, name='create_repo_json_secure'),
    path('view_repo_json_secure/', views.view_target_repos_json_secure, name='view_repo_json_secure'),
    path('update_aiOps_config/', views.update_aiops_config, name='update_aiOps_config')
]



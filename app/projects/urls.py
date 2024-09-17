from django.urls import path
from . import views


urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.project, name='project'),
    path('create-projects/', views.create_project, name='create-project'),
    path('update-projects/<str:pk>/',
        views.update_project, name='update-project'),
    path('delete-projects/<str:pk>/',
        views.delete_project, name='delete-project'),
]

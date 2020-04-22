from django.urls import path

from .views import listprojects,addproject,project



urlpatterns = [
    path('new', addproject,name="new_project"),
    path('/<id>', project,name="project"),
    path('', listprojects,name="all_projects"),
]
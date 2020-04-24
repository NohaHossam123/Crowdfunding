from django.urls import path

from .views import listprojects,addproject,project,adddonate,addreport



urlpatterns = [
    path('new', addproject,name="new_project"),
    path('/<id>', project,name="project"),
    path('', listprojects,name="all_projects"),
    path('/donate/<id>', adddonate,name="add_donate"),
    path('/report/<id>', addreport,name="add_report"),
]
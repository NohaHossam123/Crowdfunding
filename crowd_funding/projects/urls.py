from django.urls import path
from .views import *

urlpatterns = [
    path('create', project_create_view,name="create_project"),
    path('<id>', project,name="project"),
    path('', listprojects,name="all_projects"),
    path('donate/<id>', adddonate,name="add_donate"),
    path('report/<id>', addreport,name="add_report"),
    path('<id>/comment',add_comment,name="add_comment"),
    path('<id>/comment/<c_id>',add_reply,name="add_reply"),
    path('<id>/deletecomment',delete_comment,name="delete_comment"),
    path('<id>/c_report',report_comment,name="report_comment"),
    path('<id>/<p_id>/deletereply',delete_reply,name="delete_reply"),
    path('<id>/e_comment',edit_comment,name="edit_comment"),
    path('<id>/rate',rate_project,name="rate_project"),
    path('cancel/<id>',remove_project,name="remove_project"),
    
]
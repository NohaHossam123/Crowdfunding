from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import *
from django.template.response import TemplateResponse
from django.urls import path
from .views import *
from django.contrib import messages
# Register your models here.
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(ProjectPictures)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Reply)
admin.site.register(Donate)
admin.site.register(ReportProject)
admin.site.register(ReportComment)



class SelectedToShowAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if SelectedToShow.objects.all().count() >4: 
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Featured cannot be more than 5 projects....')
            return
        elif SelectedToShow.objects.filter(project=obj.project.id).exists():
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Project already Exists....')
            return
        else:
            obj.save()
            return super(SelectedToShowAdmin, self).save_model(request, obj, form, change)


# admin.site.unregister(SelectedToShow)
admin.site.register(SelectedToShow, SelectedToShowAdmin)

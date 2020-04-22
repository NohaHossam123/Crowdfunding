from django.shortcuts import render
from .models import *
# Create your views here.


def listprojects(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, "allprojects.html", context)


def addproject(request):
    pass


def project(request, id):
    project = Project.objects.get(id=id)
    rate = project.rate_set.only("body")
    average = 0
    for r in rate:
        average += int(str(r))
    average = average / len(rate)
    imgs = project.projectpictures_set.only("image_path")
    for r in imgs:
        print (r.image_path)
    context = {"project": project, "totalRate": average,"imgs":imgs}
    return render(request, "project.html", context)

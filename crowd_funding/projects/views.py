from django.shortcuts import render
from django.shortcuts import redirect
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
    donates = project.donate_set.only("amount")
    total_donate = 0
    for d in donates:
        total_donate += float(str(d))
    rate = project.rate_set.only("body")
    average = 0
    for r in rate:
        average += int(str(r))
    average = average / len(rate)
    imgs = project.projectpictures_set.only("image_path")
    for r in imgs:
        print (r.image_path)
    
    try:
        report = ReportProject.objects.get(project=project, user=request.user)
    except ReportProject.DoesNotExist:
        report = ""
    context = {"project": project, "totalRate": average,
               "totalDonate": total_donate, "imgs": imgs, "report": report}
    return render(request, "project.html", context)


def adddonate(request, id):
    if request.method.lower() == "post":
        newdonate = Donate()
        newdonate.amount = request.POST['amount']
        newdonate.project = Project.objects.get(id=id)
        newdonate.user = request.user
        newdonate.save()
        return redirect(f'/project/{id}')


def addreport(request, id):
    if request.method.lower() == "post":
        try:
            updateReport = ReportProject.objects.get(user=request.user)
            updateReport.body = request.POST['body']
            updateReport.save()
        except ReportProject.DoesNotExist:
            newReport = ReportProject()
            newReport.body = request.POST['body']
            newReport.project = Project.objects.get(id=id)
            newReport.user = request.user
            newReport.save()
    return redirect(f'/project/{id}')

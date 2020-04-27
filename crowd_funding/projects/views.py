from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from authenticate.decorators import unauthenticated_user
# Create your views here.


# create Form

def project_create_view(request):
    # form_class = FileFieldForm
    # template_name = 'project_create.html'  # Replace with your template.
    form = ProjectForm(request.POST or None, initial = {'category_name': Category.objects.all()})
    print(request.FILES.getlist('images'))
    if form.is_valid():
        project = form.save(commit=False)
        project.user = request.user
        project.save()
    
    context = {
        'form': form
    }

    #get files from req
    for file in request.FILES.getlist('images'):
                instance = ProjectPictures(
                    project=project,
                    image_path=file
                )
                instance.save()

    return render(request, "project_create.html",context)


# if request.method.lower()=="get":
# book_form = AddBookForm()
# return render(request, "newbook.html", {"form": book_form})
# elif request.method.lower()=="post":
# form = AddBookForm(request.POST, request.FILES)
# if form.is_valid():
# form.save()
# return redirect('/')
# else:
# return render(request, "newbook.html", {"form": book_form}) 



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
    if len(rate) != 0:
        average = average / len(rate)
    else:
        average = 0
    imgs = project.projectpictures_set.only("image_path")
    for r in imgs:
        print (r.image_path)
    if not request.user.is_authenticated or Rate.objects.filter(user_id=request.user) is None:
        user_rate = 0
    else:
        user_rate =  project.rate_set.get(user_id=request.user.id).body
    
    if not request.user.is_authenticated or ReportProject.objects.filter(user_id=request.user) is None:
        report = ''
    else:
        report = ReportProject.objects.get(project=project, user=request.user)
   
    context = {"project": project, "totalRate": average,
               "totalDonate": total_donate, 
               "imgs": imgs, "report": report,
               "user_rate": user_rate
               }
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


@login_required(login_url='login')
def add_comment(request,id):
    if request.method == 'POST':
        user_id = request.user.id
        body = request.POST.get('body')
        Comment.objects.create(body=body,user_id=user_id, project_id=id)
    return redirect('project' , id)

@login_required(login_url='login')
def edit_comment(request, id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=id)
        comment.body = request.POST.get('body')
        project_id = comment.project_id
        comment.save()
    return redirect('project', project_id)

@login_required(login_url='login')
def add_reply(request,id,c_id):
    if request.method == 'POST':
        user_id = request.user.id
        body = request.POST.get('body')
        Reply.objects.create(body=body,user_id=user_id,comment_id=c_id)
    return redirect('project' , id)

@login_required(login_url='login')
def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    project_id = comment.project_id
    comment.delete()
    return redirect('project', project_id)


@login_required(login_url='login')
def report_comment(request, id):
    try:
        if request.method == 'POST':
            user_id = request.user.id
            comment = Comment.objects.get(id=id)
            project_id = comment.project_id
            body = request.POST.get('body')
            ReportComment.objects.create(user_id=user_id,comment_id=id, body=body)
    except:
        pass

    return redirect('project', project_id)


@login_required(login_url='login')
def delete_reply(request, id, p_id):
    Reply.objects.get(id=id).delete()
    return redirect('project', p_id)

@login_required(login_url='login')
def rate_project(request, id):
    try:
        if request.method == 'POST':
            user_id = request.user.id
            rate = int(request.POST.get('rating'))
            Rate.objects.create(user_id=user_id, project_id=id, body=rate)
    except:
        rate = Rate.objects.get(user_id= request.user.id)
        rate.body = int(request.POST.get('rating')) 
        rate.save()
    return redirect('project',id)

    


from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from authenticate.decorators import unauthenticated_user
from django.contrib import messages

# Create your views here.

# create Form
@login_required(login_url='login')
def project_create_view(request):
    form = ProjectForm(request.POST or None, initial = {'category_name': Category.objects.all()})
    if form.is_valid():
        project = form.save(commit=False)
        project.user = request.user
        project.save()
        print("inserted")
    
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
   
    # get tags
    fetched = request.POST.get('tags')
    if fetched is not None:
        new_tags = fetched.split(',')
        saved_tags = list(Tag.objects.all())
        saved_tags_data = [tag.name for tag in saved_tags]
        new_unique_tags = [tag for tag in new_tags if tag not in saved_tags_data]
        print(len (new_unique_tags))

        #check for comming new unique tags
        if len (new_unique_tags) != 0:
            # insert in project-tags Only
            for value in new_unique_tags:
                    instance = Tag(name= value)
                    instance.save()
                    instance.projects.add(project)
                    



        

    return render(request, "project_create.html",context)


def listprojects(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, "allprojects.html", context)

def project(request, id):
    project = Project.objects.get(id=id)
    donates = project.donate_set.only("amount")
    total_donate = 0
    for d in donates:
        total_donate += float(str(d))
    rate = project.rate_set.only("body")
    average = 0
    totalRate=0
    for r in rate:
        average += int(str(r))
    if len(rate) != 0:
        average = average / len(rate)
        totalRate=round(average)
    else:
        average = 0
    imgs = project.projectpictures_set.only("image_path")
    for r in imgs:
        print (r.image_path)
    try:
        user_rate = project.rate_set.get(user_id=request.user.id).body
    except:
        user_rate = 0
    try:
        report = ReportProject.objects.get(project=project, user=request.user)
    except:
        report=""
   
    context = {"project": project, "totalRate": totalRate   ,
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
        if  request.POST.get('body') == '':
            messages.error(request, "Comment cannot be empty, Try again!")
        else:  
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
        if comment.body == '':
            messages.error(request, "Comment cannot be empty, Try again!")
        else:  
            comment.save()
    return redirect('project', project_id)


@login_required(login_url='login')
def add_reply(request,id,c_id):
    if request.method == 'POST':
        if request.POST.get('body') == '':
            messages.error(request, "Reply cannot be empty, Try again!")
        else:    
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
            if body == '':
                messages.error(request, "Report cannot be empty, Try again!")
            else:    
                ReportComment.objects.create(user_id=user_id,comment_id=id, body=body)
    except:
        messages.error(request, "You reported this comment before!")
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
    return redirect('project', id)

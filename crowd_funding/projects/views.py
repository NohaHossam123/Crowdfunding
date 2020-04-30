from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from authenticate.decorators import unauthenticated_user
from django.contrib import messages
import datetime

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
        for i in new_tags:
            obj, created = Tag.objects.get_or_create(name=i)
            project.tag_projects_set.create(tag=obj)
        # new_tags = fetched.split(',')
        # saved_tags = list(Tag.objects.all())
        # saved_tags_data = [tag.name for tag in saved_tags]
        # new_unique_tags = [tag for tag in new_tags if tag not in saved_tags_data]
        # print(new_tags)
        # print(len (new_unique_tags))
        


    #     #check for comming new unique tags
    #     if len (new_unique_tags) != 0:
    #         # insert in project-tags Only
    #         for value in new_unique_tags:
    #                 instance = Tag(name= value)
    #                 instance.save()
                    
    # for tag in new_tags:
    #      instance = Tag_projects(
    #                 project=project,
    #                 image_path=file
    #             )
    #             instance.save()

    return render(request, "project_create.html",context)


def listprojects(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, "allprojects.html", context)

def project(request, id):
    try:
        project = Project.objects.get(id=id)
        total_donate = 0
        donates = project.donations.only("amount")
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
        try:
            user_rate = project.rate_set.get(user_id=request.user.id).body
        except:
            user_rate = 0
        try:
            report = ReportProject.objects.get(project=project, user=request.user)
        except:
            report=""
        
        relatedProjects=Project.objects.raw('select *,count(title) as r from projects_project as p RIGHT JOIN projects_tag_projects on project_id where projects_tag_projects.tag_id in (select tp.tag_id from projects_tag_projects as tp where tp.project_id=p.id) and p.id <> %s GROUP BY title ORDER by r DESC LIMIT 4',[id])

        context = {"project": project, "totalRate": totalRate   ,
                "totalDonate": total_donate, 
                "report": report,
                "relatedProjects": relatedProjects,
                "user_rate": user_rate
                }
        return render(request, "project.html", context)
    except:
        return redirect("/")

@login_required(login_url='login')
def adddonate(request, id):
    if request.method.lower() == "post":
        newdonate = Donate()
        newdonate.amount = request.POST['amount']
        newdonate.project = Project.objects.get(id=id)
        newdonate.user = request.user
        newdonate.save()
        return redirect(f'/project/{id}')

@login_required(login_url='login')
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
		messages.info(request, " We've received your report and we\'re working on it.")
                messages.info(request, "Please keep in mind that reporting something does not guarantee that it will be removed")
    except:
        messages.error(request, "You reported this comment before!we\'re working on it.")
    return redirect('project', project_id)

@login_required(login_url='login')
def remove_project(request, id):
    try:
        project = Project.objects.get(id=id, user=request.user)
        project.delete()
        return redirect('/', id)
    except:
        return redirect('/', id)

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
        rate = Rate.objects.get(user_id= request.user.id,project_id=id)
        rate.body = int(request.POST.get('rating')) 
        rate.save()
    return redirect('project', id)

from django.db import models
# from authenticate.models import CFAccountManager

class Category(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length = 50)
    details = models.TextField()
    start_date = models.DateTimeField(auto_now = False , auto_now_add = True)
    end_date = models.DateTimeField()
    total_target = models.FloatField()
    category = models.ForeignKey(Category , on_delete = models.CASCADE)
    # user = models.ForeignKey(CFAccountManager, on_delete = models.CASCADE)
    # donates = models.ManyToManyField(CFAccountManager, through='User_Donate_Project')
    def __str__(self):
        return self.title

class Tage(models.Model):
    name = models.CharField(max_length = 50)
    projects = models.ManyToManyField(Project)

    def __str__(self):
        return self.name

class Project_Pictures(models.Model):
    image_path = models.ImageField(null = True , blank = True)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

    def __str__(self):
        return self.image_path

class Selected_To_Show(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

# class report(models.Model):
#     report_body = models.TextField(null = True , blank = True)
#     project = models.ForeignKey(Project , on_delete = models.CASCADE)
#     report_on_type = 
#     def __str__(self):
#         return self.report_body 

# class User_Donate_Project(models.Model):
#     project = models.ForeignKey(Project , on_delete = models.CASCADE)
#     user = models.ForeignKey(CFAccountManager , on_delete = models.CASCADE)
#     amount_donated = models.FloatField()
#     def __str__(self):
#         return self.user.username





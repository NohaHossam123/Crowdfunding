from django.db import models
from authenticate.models import Account

class Category(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length = 50)
    details = models.TextField()
    start_date = models.DateTimeField( null = True , blank = True )
    end_date = models.DateTimeField( null = True , blank = True )
    total_target = models.FloatField()
    category = models.ForeignKey(Category , on_delete = models.CASCADE)
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    # donate = models.ManyToManyField(Account,related_name='user' )
    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length = 50)
    projects = models.ManyToManyField(Project)

    def __str__(self):
        return self.name

class ProjectPictures(models.Model):
    image_path = models.ImageField(null = True , blank = True)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

    def __str__(self):
        return self.image_path

class SelectedToShow(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    body = models.TextField()
    class Meta:
        unique_together = ('user', 'project')
    
class Rate(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    body = models.IntegerField(range(1, 5))
    class Meta:
        unique_together = ('user', 'project')
    def __str__(self):
        return str(self.body)

class Donate(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    amount = models.FloatField()
    def __str__(self):
        return str(self.amount)


class ReportProject(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    body = models.TextField()
    class Meta:
        unique_together = ('user', 'project')

class ReportComment(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    body = models.TextField()
    class Meta:
        unique_together = ('user', 'comment')


# class User_Donate_Project(models.Model):
#     project = models.ForeignKey(Project , on_delete = models.CASCADE)
#     user = models.ForeignKey(CFAccountManager , on_delete = models.CASCADE)
#     amount_donated = models.FloatField()
#     def __str__(self):
#         return self.user.username





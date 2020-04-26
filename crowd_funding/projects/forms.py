# from django import froms
from django import  forms

from .models import Project, Category


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'details',
            'total_target',
            'start_date',
            'end_date',
            'category'
        ]
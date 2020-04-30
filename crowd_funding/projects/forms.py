# from django import froms
from django import  forms
from django.utils import timezone

from .models import Project, Category

import datetime

class DateInput(forms.DateInput):
      input_type = 'date'


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput,initial=datetime.date.today,required=True)
    end_date = forms.DateField(widget=DateInput,initial=datetime.date.today,required=True)

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

        def clean_project_title(self):
                    title = self.cleaned_data['title']
                    if len(project_title) == 0:
                        raise forms.ValidationError("project title can't be empty ")
                    if len(project_title) >100:
                        raise forms.ValidationError("project title excedded length ")
                    return project_title
      
        def clean_details(self):
                details = self.cleaned_data['details']
                if len(details) == 0:
                    raise forms.ValidationError("project title can't be empty ")
                return details
      
        def clean_category(self):
                category = self.cleaned_data['category']
                try:
                    Category.objects.get(name = category)
                except:
                    raise forms.ValidationError("please choose from list")
                return category
      
        def clean_target(self):
                total_target = self.cleaned_data['total_target']
                if target <= 1000:
                    raise forms.ValidationError("project title can't lower than 1000 ")
                if target > 1000000000:
                    raise forms.ValidationError("project title can't be more than 1000000000 ")
                return target
                  
      
        def clean_start_date(self):
                start_date = self.cleaned_data['start_date']
                print("Date = ",start_date)
                if (start_date-datetime.date.today()).days < 0:
                    raise forms.ValidationError("Start date can't be in the past")
                return start_date

        def clean_end_date(self):
                end_date = self.cleaned_data['end_date']
                if self.cleaned_data.get('start_date')==None:
                    return end_date
                start_date = self.cleaned_data['start_date']
                print("Date = ",end_date)
                if (end_date-start_date).days <= 0:
                    raise forms.ValidationError("Wrong End Date")
                return end_date
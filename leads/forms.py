from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm , UsernameField
from django.http import request
from . models import Lead, User, Agent, Task

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
            'location',
            'Lead_status',
            'spendings'
        )

class Task(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'task_name',
            'task_descrption'
        )


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)




class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    #based on the request user we can filter on all agents that belong to this organization
    #every time the form is renderd is dynamcally updating the field based on the requested user
    def __init__(self,*args, **kwargs):
        request = kwargs.pop("request")
        agents=Agent.objects.filter(organisation=request.user.userprofile)
        #calling the original init method with the original expected keyword args
        super(AssignAgentForm, self). __init__(*args, **kwargs)
        self.fields["agent"].queryset=agents

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )


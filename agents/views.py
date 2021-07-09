from django.http import request
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent,Task
from django.shortcuts import reverse
from .forms import AgentModelForm
from .mixin import OrganisorAndLoginRequiredMixin

class AgentListView(OrganisorAndLoginRequiredMixin,generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)



class AgentCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
    template_name = "agents/agent_create.html" 
    form_class  = AgentModelForm 

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form ):
        agent = form.save(commit=False)
        agent.organisation = self.request.user.userprofile 
        agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin , generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        return Agent.objects.all()

class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name="agents/agent_update.html"
    form_class =AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name = "agents/agent_delete.html"


    def get_queryset(self):
        organisation = self.request.user.userprofile
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)



class TaskView(LoginRequiredMixin,generic.ListView):
    template_name="agents/tasks.html"
    context_object_name = "task"
    def get_queryset(self):
       user = self.request.user        
       if user.is_organisor:
            queryset = Task.objects.filter(task_name__isnull= False)
            queryset1= Task.objects.filter(task_descrption__isnull= False)
       else:
            queryset= Task.objects.filter(agent=user.agent).filter(done=False)
            return queryset
  
    # def get_context_data(self,**kwargs):
    #     context = super(TaskView , self).get_context_data(**kwargs)
    #     user = self.request.user

    #     context.update({
    #      "task_name":queryset,
    #      'task_desc':queryset1
    #     })


    
    #     return context
 


class TaskCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
        template_name="create_task.html"
        context_object_name="create_task"
        def form_valid(self, form):
            form.save(commit=False)
            Task.save()
            return super(TaskCreateView, self).form_valid(form)

from typing import ContextManager
from django.core.mail import send_mail
from django.shortcuts import render , redirect 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic 
from django.views.generic import TemplateView , DetailView, CreateView , UpdateView , DeleteView 
from django.views.generic.list import ListView
from .models import Category, Lead ,Agent , Task
from .forms import LeadForm , LeadModelForm , CustomerUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from agents.mixin import OrganisorAndLoginRequiredMixin

#class based views - create , retrieve , update and Delete + LIST


class SignupView(generic.CreateView):
    template_name = "signup.html"
    form_class = CustomerUserCreationForm

    def get_success_url(self):
        return reverse("login")



class LandingPageView(TemplateView):
    template_name = "landing.html"



class DashboardView(ListView):
    template_name = "dashboard.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"

    def get_context_data(self,**kwargs):
        context = super(DashboardView , self).get_context_data(**kwargs)
        user = self.request.user
        queryset = Lead.objects.all()
        queryset1 = Agent.objects.all()
        context["qs"] = Lead.objects.all() 
        Smouha = Lead.objects.filter(location="smouha")
        lauran = Lead.objects.filter(location="lauran")

        uncategorized = Lead.objects.filter(category_id=0)
        Unconverted = Lead.objects.filter(category_id=1)
        Converted = Lead.objects.filter(category_id=2)
        Contacted = Lead.objects.filter(category_id=3)
        Tasks = Task.objects.filter(agent=user.agent).filter(done=False)
        task1= Task.objects.all().count()
        task2 = Task.objects.filter(done=True).count()
        result = (task2/task1)*100


        if user.is_organisor:
            queryset2= Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset2= Lead.objects.filter(organisation=user.agent.organisation)
        context.update({
            "leads_count": queryset.count(),
            "agent_count": queryset1.count(),
            "uncategorized_lead_count":queryset2.filter(category__isnull=True).count(),
            "unassigned_lead_count":queryset2.filter(agent__isnull=True).count(),
            "smouha": Smouha.count(),
            "lauran": lauran.count(),
           "unconverted": Unconverted.count(),
            "converted": Converted.count(),
            "contacted": Converted.count(),
            "uncategorized": uncategorized.count(),
            "task_count":Tasks.count(),
            "progress" :result


        })
        return context



class LeadListView(LoginRequiredMixin,ListView):
    template_name = "leads_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        #initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset= Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            #filter for agent that is logged in
            queryset = queryset.filter(agent__user=user)
 
        return queryset
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context=super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile,agent__isnull=True)
            queryset1=Agent.objects.all()
            context.update({
            "unassigned_leads":queryset,
            "agent_name":queryset1
        })


        return context


class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name = "lead_detail.html"
    context_object_name = "lead"
    def get_queryset(self):
        user = self.request.user
        #initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset= Lead.objects.filter(organisation=user.agent.organisation)
            #filter for agent that is logged in
            queryset = queryset.filter(agent__user=user)
 
        return queryset
 

 

class LeadCreateView(OrganisorAndLoginRequiredMixin,CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead=form.save(commit=False)
        lead.organisation=self.request.user.userprofile
        lead.save()
        #TODO send email
        send_mail(
            subject="A lead has been created", 
            message="Go to the site to see the new lead",
            from_email="oomaya1@gmail.com",
            recipient_list=["oomaya1@gmail.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset= Lead.objects.filter(organisation=user.agent.organisation)
        
        return queryset

    def get_success_url(self):
         return reverse("leads:lead-list")
 
class LeadDeleteView(OrganisorAndLoginRequiredMixin,DeleteView):
    template_name = "lead_Delete.html"
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")
 

def landing_page(request):
    return render(request, "landing.html")




class UnassignedleadsView(LoginRequiredMixin,ListView):
    template_name = "unassigned_leads.html"
    context_object_name = "leads"
    def get_queryset(self):
        user = self.request.user
        #initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset= Lead.objects.filter(organisation=user.agent.organisation)
            #filter for agent that is logged in
 
        return queryset

    def get_context_data(self,**kwargs):
        user = self.request.user
        context = super(UnassignedleadsView,self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile,agent__isnull=True)
            context.update({
                "unassigned_leads":queryset
            })
            return context




def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads") 


class AssignAgentView(OrganisorAndLoginRequiredMixin,generic.FormView):
    template_name = "assign_agent.html"
    form_class=AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update ({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form) :
        #getting the choosed agent
        agent=form.cleaned_data["agent"]
        #getting the lead that need to be assigned
        lead =Lead.objects.get(id=self.kwargs["pk"])
        lead.agent=agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class  CategoryListView(LoginRequiredMixin,generic.ListView):
    template_name ="category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs) :
        context=super(CategoryListView,self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset= Lead.objects.filter(organisation=user.agent.organisation)

        context.update({
            "unassigned_lead_count": Lead.objects.filter(category__isnull=True).count()
       })
        return context

    def get_queryset(self):
        user = self.request.user
        #initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset= Category.objects.filter(organisation=user.userprofile)
        else:
            queryset= Category.objects.filter(organisation=user.agent.organisation)
 
        return queryset

class CategoryDetailView(LoginRequiredMixin,generic.DetailView):
    template_name="category_detail.html"
    context_object_name = "category"



    def get_queryset(self):
        user = self.request.user
        #initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset= Category.objects.filter(organisation=user.userprofile)
        else:
            queryset= Category.objects.filter(organisation=user.agent.organisation)
 
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "lead_category_update.html"
    form_class = LeadCategoryUpdateForm


    def get_queryset(self):
        user = self.request.user
        #initial Queryset of leads for the entire organisation
        if user.is_organisor:
            queryset= Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset= Lead.objects.filter(organisation=user.agent.organisation)
            #filter for agent that is logged in
            queryset = queryset.filter(agent__user=user)
 
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail",kwargs={"pk":self.get_object().id})



#    def lead_create(request):
#     form = LeadModelForm()
#     if request.method == "POST":
#         print('Receiving a post request ')
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             print("the form is valid")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name = last_name,
#                 age=age,
#                 agent=agent
#             )
#             print("the lead has been created")
#             return redirect("/leads")
#     context = {
#         "form": form
#     }
#     return render(request, "lead_create.html", context)



# Create your views here

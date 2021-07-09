from django.urls import path
from agents.views import TaskView
from .views import ( 
    LeadListView , LeadDetailView , LeadCreateView , LeadUpdateView , LeadDeleteView ,AssignAgentView,
    CategoryListView , CategoryDetailView, LeadCategoryUpdateView,UnassignedleadsView
)


app_name = "leads"
urlpatterns = [
    path('',LeadListView.as_view(), name='lead-list'),
    path('leads/unassinged/',UnassignedleadsView.as_view(), name='unassigend-leads'),
    path('<int:pk>/',LeadDetailView.as_view(),name='lead-detail'),
    path('<int:pk>/update/',LeadUpdateView.as_view(),name='lead-update'),
    path('<int:pk>/delete/',LeadDeleteView.as_view(),name='lead-delete'),
    path('<int:pk>/assign-agent/',AssignAgentView.as_view(),name='assign-agent'),
    path('<int:pk>/category/',LeadCategoryUpdateView.as_view(),name='lead-category-update'),
    path('create/',LeadCreateView.as_view(),name='lead-create'),
    path('categories/',CategoryListView.as_view(),name='category-list'),
    path('categories/<int:pk>/',CategoryDetailView.as_view(),name='category-detail')
]

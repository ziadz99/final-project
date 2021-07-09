from django.urls import path
from .views import AgentListView, AgentCreateView ,AgentDetailView , AgentUpdateView , AgentDeleteView,TaskView,TaskCreateView


app_name = 'agents'

urlpatterns = [
    path('',AgentListView.as_view(), name='agent-list'),
    path('<int:pk>/',AgentDetailView.as_view(),name='agent-detail'),
    path('view-task/',TaskView.as_view(),name='task-view'),
    path('<int:pk>/assign-task',TaskCreateView.as_view(),name='agent-tasks'),
    path('<int:pk>/update/',AgentUpdateView.as_view(),name='agent-update'),
    path('<int:pk>/delete/',AgentDeleteView.as_view(),name='agent-delete'),
    path('create/',AgentCreateView.as_view(), name='agent-create')
    

]

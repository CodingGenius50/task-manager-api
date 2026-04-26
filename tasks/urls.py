from django.urls import path
from . import views 
urlpatterns = [
    path('taskscreate/',views.TaskCreateView.as_view()),
    path("taskslist/",views.TaskListView.as_view()),
    path("taskdetails/<int:pk>/",views.TaskDetailView.as_view()),
    path("taskedit/<int:pk>/",views.TaskUpdateView.as_view()),
    path("taskremove/<int:pk>/",views.TaskDeleteView.as_view()),
]

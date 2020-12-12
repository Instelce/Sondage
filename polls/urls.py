from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('user/<str:username>', views.UserIndexView.as_view(), name='user'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('question/new/', views.QuestionCreateView.as_view(), name='create'),
    path('choice/new/', views.ChoiceCreateView.as_view(), name='create-choice'),
    path('<int:pk>/update/', views.QuestionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='delete'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
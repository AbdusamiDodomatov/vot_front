from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('', views.vote_list, name='vote_list'),
    path('<int:election_id>/', views.vote_detail, name='vote_detail'),
]

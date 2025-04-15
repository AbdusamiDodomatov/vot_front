from django.urls import path
from voting import views

app_name = 'voting'

urlpatterns = [
    path('', views.index, name='index'),
    path('poll/<int:pk>/', views.detail, name='detail'),
    path('poll/<int:pk>/vote/', views.vote, name='vote'),
    path('poll/<int:pk>/results/', views.results, name='results'),
    path('create/', views.create_poll, name='create_poll'),

]

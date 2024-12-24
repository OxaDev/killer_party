from django.urls import path
from . import views
from django.shortcuts import render

def index(request):
    return render(request, "index.html")


urlpatterns = [
    path('create-game/', views.create_game, name='create_game'),
    path('add-players/', views.add_players, name='add_players'),
    path('assign-targets/', views.assign_targets, name='assign_targets'),
    path('get-target/', views.get_player_target, name='get_player_target'),
    path('', index, name='index'),
]
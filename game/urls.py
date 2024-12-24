from django.urls import path
from . import views
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def player(request):
    return render(request, "player.html")

urlpatterns = [
    path('create-game/', views.create_game, name='create_game'),
    path('add-players/<str:game_code>/', views.add_players, name='add_players'),
    path('assign-targets/<str:game_code>/', views.assign_targets, name='assign_targets'),
    path('get-target/<str:game_code>/<str:player_name>/', views.get_player_target, name='get_player_target'),
    path('get-players/<str:game_code>/', views.get_players, name='get_players'),
    path('get-players-codes/<str:game_code>/', views.get_players_codes, name='get_players_code'),
    path('killer_admin', index, name='index'),
    path('killer', player, name='player-view'),
]
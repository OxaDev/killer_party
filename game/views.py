from django.shortcuts import render
import random
import json
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Game
from django.core.exceptions import ObjectDoesNotExist
from .killing_methods import methods as killing_methods

def create_player_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))

def create_master_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=20))


@csrf_exempt
def create_game(request):
    if request.method == 'POST':
        game_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        master_code = create_master_code()
        Game.objects.create(code=game_code, master_code=master_code)
        return JsonResponse({"game_code": game_code, "master_code": master_code})

@csrf_exempt
def add_players(request,game_code):
    try:
        game = Game.objects.get(code=game_code)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    if request.method == 'POST':
        if game.targets:
            return JsonResponse({"message": "Targets are already assigned, don't add other players"})
        data = json.loads(request.body)
        player_list = [
            player.replace(" ","").replace("\r","").lower()
            for player in data.get('players',[""])[0].split("\n")
        ]
        clean_player_list = []
        for i in range(len(player_list)):
            player = player_list[i]
            if player in game.players or player in player_list[i+1:]:
                return JsonResponse({"message": f"player {player} already in game or has a duplicate in the given list"})
            if player:
                clean_player_list.append(player)
        
        for player in clean_player_list:
            player_code = create_player_code()
            game.players_codes[player] = player_code
        game.players.extend(clean_player_list)
        game.save()
        return JsonResponse(
            {
                "message": "Players added successfully",
                "players_codes" : game.players_codes
            }
        )


@csrf_exempt
def assign_targets(request,game_code):
    try:
        game = Game.objects.get(code=game_code)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    if len(game.players) < 2:
        return JsonResponse({"error": "Not enough players"}, status=400)

    if request.method == 'POST':
        if game.targets:
            return JsonResponse({"message": "Targets are already assigned"})
        players = game.players
        random.shuffle(players)
        targets = {players[i]: players[(i + 1) % len(players)] for i in range(len(players))}
        assigned_methods = {player: random.choice(killing_methods) for player in players}

        game.targets = targets
        game.methods = assigned_methods
        game.save()

        return JsonResponse({"message": "Targets assigned successfully"})

@csrf_exempt
def get_player_target(request,game_code,player_name):
    try:
        game = Game.objects.get(code=game_code)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)
    if player_name not in game.targets or player_name not in game.players_codes:
        return JsonResponse({"error": "Player not found in game"}, status=404)

    player_code = request.GET.get("player-code")
    if game.players_codes[player_name] != player_code:
        return JsonResponse({"error": "Invalid given code"}, status=400)

    target = game.targets[player_name]
    method = game.methods[player_name]

    return JsonResponse({"target": target, "method": method})

@csrf_exempt
def get_players(request, game_code):
    try:
        game = Game.objects.get(code=game_code)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    return JsonResponse({"players": list(game.targets.keys())})

@csrf_exempt
def get_players_codes(request, game_code):
    try:
        game = Game.objects.get(code=game_code)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    master_code = request.GET.get("master-code")
    if game.master_code != master_code:
        return JsonResponse({"error": "Invalid master code"}, status=400)
    
    return JsonResponse({"players_codes": game.players_codes})
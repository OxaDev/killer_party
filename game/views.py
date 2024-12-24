from django.shortcuts import render
import random
import json
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Game
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def create_game(request):
    if request.method == 'POST':
        game_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        game = Game.objects.create(code=game_code)
        return JsonResponse({"game_code": game_code})

@csrf_exempt
def add_players(request):
    game_code = request.POST.get("game_code")
    breakpoint()
    try:
        game = Game.objects.get(code=game_code)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    if request.method == 'POST':
        players_body  = request.POST.get("players")
        players_list = players_body.replace("\r","").split("\n")
        game.players.extend(players_list)
        game.save()
        return JsonResponse({"message": "Players added successfully"})

@csrf_exempt
def assign_targets(request):
    game_code = request.POST.get("game_code")
    try:
        game = Game.objects.get(code=game_code)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    if len(game.players) < 2:
        return JsonResponse({"error": "Not enough players"}, status=400)

    if request.method == 'POST':
        players = game.players
        random.shuffle(players)
        methods = [
            "take a selfie with them", "make them eat a chip", "shake their hand",
            "make them laugh", "sing a song together", "give them a small item",
            "ask them to say a specific word", "offer them a glass of water",
            "ask them for directions to somewhere", "convince them to sit on a specific chair",
            "ask them to guess a number", "share a fun fact with them",
            "teach them a dance move", "give them a high-five", "ask them to hold something for you",
            "pretend to interview them", "make them draw a simple picture",
            "ask them to tell a joke", "ask them to help you find an object",
            "ask them to join you for a short walk", "make them mimic an animal sound",
            "play rock-paper-scissors with them", "show them a magic trick",
            "ask them to clap their hands", "ask them to do a quick stretch",
            "ask them to identify a color around you", "ask them to smile for a photo",
            "get them to hum a tune", "ask them to read something aloud",
            "share a secret handshake", "ask them to do a small favor for you",
            "make them count something nearby", "ask them to point at a random object",
            "ask them to compliment someone", "ask them to tell you a fun memory",
            "make them describe their favorite food", "ask them to write down their favorite color",
            "ask them to recite a tongue twister", "ask them to do a small hop",
            "ask them to play a guessing game", "ask them to list three things they like",
            "pretend to give them an award", "ask them to mimic your gesture",
            "ask them to describe the weather", "ask them to help you rearrange something",
            "ask them to count down from 10", "ask them to spell a word backward",
            "ask them to name a type of flower", "ask them to describe a sound",
            "make them fold a paper airplane", "ask them to whistle",
            "ask them to pretend to pick a fruit", "ask them to touch something soft",
            "ask them to stand in a specific spot", "ask them to perform a quick dance step",
            "ask them to draw a circle in the air", "ask them to imagine a scenario",
            "ask them to play a word association game", "ask them to identify a smell",
            "ask them to close their eyes for 5 seconds", "ask them to name their favorite animal",
            "ask them to imitate a famous character", "ask them to balance on one foot",
            "ask them to pretend to throw a ball", "ask them to say a random number",
            "ask them to identify a nearby sound", "ask them to touch something cold",
            "ask them to imitate a bird call", "ask them to describe a tree",
            "ask them to mimic a drumbeat", "ask them to identify a fruit",
            "ask them to say the alphabet backward", "ask them to touch something green",
            "ask them to describe their favorite holiday", "ask them to clap a rhythm",
            "ask them to pretend to hold an invisible object", "ask them to wave at someone nearby",
            "ask them to tap their foot", "ask them to blink rapidly",
            "ask them to name a historical figure", "ask them to draw a shape with their finger",
            "ask them to describe their dream destination", "ask them to mimic a robot",
            "ask them to pretend to be a statue", "ask them to share a trivia fact",
            "ask them to name a type of tree", "ask them to hum a familiar tune",
            "ask them to imagine a favorite place", "ask them to mime eating a fruit",
            "ask them to tap their nose", "ask them to mimic a car engine"
        ]
        targets = {players[i]: players[(i + 1) % len(players)] for i in range(len(players))}
        assigned_methods = {player: random.choice(methods) for player in players}

        game.targets = targets
        game.methods = assigned_methods
        game.save()

        return JsonResponse({"message": "Targets assigned successfully"})

@csrf_exempt
def get_player_target(request):
    game_code = request.GET.get("game_code")
    player_name = request.GET.get("player_name")
    try:
        game = Game.objects.get(code=game_code)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)
    if player_name not in game.targets:
        return JsonResponse({"error": "Player not found in game"}, status=404)

    target = game.targets[player_name]
    method = game.methods[player_name]

    return JsonResponse({"target": target, "method": method})

import json

# Comment out the actual model loading
# print("Loading Phi-2 model...")
# from transformers import pipeline
# pipe = pipeline("text-generation", model="microsoft/phi-2")
# print("Phi-2 model loaded successfully!")

print("Using template-based game generation (Phi-2 model simulation)")

# Template game logics
GAME_TEMPLATES = {
    "tic": {
        "gameType": "turnBased",
        "name": "Tic-Tac-Toe",
        "description": "Classic Tic-Tac-Toe game for two players",
        "board": {
            "size": 3,
            "cells": 9
        },
        "players": {
            "count": 2,
            "symbols": ["X", "O"]
        },
        "rules": {
            "winCondition": "3 in a row (horizontal, vertical, or diagonal)",
            "drawCondition": "All cells filled with no winner"
        },
        "assets": {
            "background": "plain",
            "markers": ["X", "O"]
        }
    },
    "snake": {
        "gameType": "continuous",
        "name": "Snake",
        "description": "Classic snake game where you collect food and grow longer",
        "controls": {
            "type": "directional",
            "keys": ["UP", "DOWN", "LEFT", "RIGHT"]
        },
        "rules": {
            "winCondition": "Score as many points as possible",
            "loseCondition": "Hit walls or your own tail"
        },
        "assets": {
            "background": "plain",
            "player": "snake",
            "collectibles": ["food"]
        }
    },
    "pong": {
        "gameType": "realtime",
        "name": "Pong",
        "description": "Two-player paddle game where you hit a ball back and forth",
        "controls": {
            "type": "vertical",
            "player1": ["W", "S"],
            "player2": ["UP", "DOWN"]
        },
        "rules": {
            "winCondition": "First player to reach 11 points",
            "scoreCondition": "When opponent misses the ball"
        },
        "assets": {
            "background": "plain",
            "paddles": 2,
            "ball": 1
        }
    },
    "breakout": {
        "gameType": "continuous",
        "name": "Breakout",
        "description": "Destroy bricks by bouncing a ball off a paddle",
        "controls": {
            "type": "horizontal",
            "keys": ["LEFT", "RIGHT"]
        },
        "rules": {
            "winCondition": "Destroy all bricks",
            "loseCondition": "Ball falls below paddle"
        },
        "assets": {
            "background": "plain",
            "paddle": 1,
            "ball": 1,
            "bricks": "multiple rows"
        }
    }
}

def generate_game_logic(prompt):
    """Generate game logic JSON from a text prompt using templates instead of Phi-2 model"""
    
    prompt_lower = prompt.lower()
    
    # Select template based on keywords in prompt
    if "tic" in prompt_lower or "tac" in prompt_lower or "toe" in prompt_lower:
        template = "tic"
    elif "snake" in prompt_lower:
        template = "snake"
    elif "pong" in prompt_lower or "paddle" in prompt_lower:
        template = "pong"
    elif "breakout" in prompt_lower or "brick" in prompt_lower or "arkanoid" in prompt_lower:
        template = "breakout"
    else:
        # Default to tic-tac-toe if no match
        template = "tic"
    
    print(f"Using template: {template} for prompt: {prompt}")
    return GAME_TEMPLATES[template] 
import enum

class GameState:
    """
    Enum for the card game's state machine
    """    
    unknown = "unknown" # Indicate possible error or misconfiguration
    initializing = "initializing"
    initialized = "initialized"
    game_play = "game_play"
    game_end = "game_end"
    quitting = "quitting"

class StateError(Exception):
    """
    Raised if the game is in an unexpected game state
    """

class EnergyType:
    """
    Enum for the different types represented by the TCG
    """
    unknown = "unknown"
    colorless = "colorless" # ⚪
    grass = "grass" # 🌿
    fire = "fire" # 🔥
    water = "water" # 💧
    lightning = "lightning" # ⚡
    psychic = "psychic" # 🔮
    fighting = "fighting" # ✊
    dark = "dark" # 🌙
    metal = "metal" # ⚙️
    dragon = "dragon" # 🐉 There is no dragon type energy, but there are dragon type cards

class EnergyError(Exception):
    """
    Raised if an unknown energy type is encountered while
    interacting with a card
    """

import enum

class GameState:
    """
    Enum for the card game's state machine
    """    
    # Unknown state, indicating possible error or misconfiguration
    unknown = "unknown"
    initializing = "initializing"
    initialized = "initialized"
    game_play = "game_play"
    game_end = "game_end"
    quitting = "quitting"

class StateError(Exception):
    """
    Raised if the game is in an unexpected game state
    """

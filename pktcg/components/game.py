from dataclasses import dataclass
from components.gui import run_gui
from components.enums import GameState

@dataclass
class CardGame:
    state: GameState
    # Add board state object
    # Add GUI object that uses the Textual library

    @classmethod
    def create(cls):
        game = cls(state=GameState.initializing)
        game.init()
        return game

    def init(self):
        self.assert_state(GameState.initializing)
        # Load decks and create board
        self.set_state(GameState.initialized)

    def start(self):
        self.assert_state(GameState.initialized)
        self.set_state(GameState.game_play)
        #self.loop()
        run_gui()
    
    def quit(self):
        self.assert_state(GameState.quitting)

    def loop(self):
        while self.state != GameState.quitting:
            if self.state == GameState.game_play:
                game = GameLoop(game=self, turn=0)
                game.loop()
            self.set_state(GameState.quitting)
        self.quit()

    def set_state(self, new_state):
        self.state = new_state

    def assert_state(self, *expected: GameState):
        if not self.state in expected:
            raise StateError(
                f"Expected the game state to be one of {expected}, not {self.state}"
            )

@dataclass
class GameLoop:
    game: CardGame
    turn: int

    def handle_events(self):
        self.set_state(GameState.quitting)

    def loop(self):
        while self.state != GameState.quitting:
            # Setup if turn number is 0
            # After setup, determine turn order
            # Then take turns, and handle actions until game ends
            self.handle_events()

    def set_state(self, new_state):
        self.game.set_state(new_state)

    @property
    def state(self):
        return self.game.state

    def board(self):
        return

    def gui(self):
        return

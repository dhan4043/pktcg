from dataclasses import dataclass
from components.enums import GameState

@dataclass
class CardGame:
    state: GameState
    @classmethod
    def create(cls):
        game = cls(state=GameState.initializing)
        game.init()
        return game
    def set_state(self, new_state):
        self.state = new_state
    def assert_state(self, *expected: GameState):
        if not self.state in expected:
            raise StateError(
                f"Expected the game state to be one of {expected}, not {self.state}"
            )
    def loop(self):
        while self.state != GameState.quitting:
            if self.state != GameState.game_play:
                print("Game start!")
                return
            elif self.state != GameState.game_end:
                print("Game over!")
                return
        self.quit()
    def quit(self):
        self.assert_state(GameState.game_quitting)
    def start(self):
        self.assert_state(GameState.initialized)
        self.set_state(GameState.game_play)
        self.loop()
    def init(self):
        self.assert_state(GameState.initializing)
        self.set_state(GameState.initialized)

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

    def init(self):
        self.assert_state(GameState.initializing)
        self.set_state(GameState.initialized)

    def start(self):
        self.assert_state(GameState.initialized)
        self.set_state(GameState.game_play)
        self.loop()
    
    def quit(self):
        self.assert_state(GameState.quitting)

    def loop(self):
        while self.state != GameState.quitting:
            if self.state != GameState.game_play:
                print("Game start!")
                loop = GameLoop(game=self)
                loop.loop()
            elif self.state != GameState.game_end:
                print("Game over!")
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

    def handle_events(self):
        print("Closing game")
        self.set_state(GameState.quitting)

    def loop(self):
        while self.state != GameState.quitting:
            self.handle_events()

    def set_state(self, new_state):
        self.game.set_state(new_state)

    @property
    def state(self):
        return self.game.state

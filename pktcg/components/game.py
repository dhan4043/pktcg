from dataclasses import dataclass
from components.board import BoardState, GameInfo, draw_gui, render_layout, Card
from components.enums import GameState

@dataclass
class CardGame:
    state: GameState
    board: BoardState

    @classmethod
    def create(cls):
        empty_board = BoardState( # Board states should actually be initialized in the game loop
            active=Card("Pikachu", 40, 60, 2),
            bench=[
                Card("Charmander", 50, 50, 1),
                Card("Squirtle", 30, 50, 0),
                Card("Bulbasaur", 50, 50, 3)
            ]
        )
        game = cls(state=GameState.initializing,board=empty_board)
        game.init()
        return game

    def init(self):
        self.assert_state(GameState.initializing)
        # Determine turn order
        # Load decks from JSON
        self.set_state(GameState.initialized)

    def start(self):
        self.assert_state(GameState.initialized)
        self.set_state(GameState.game_play)
        self.loop()
    
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
        info = GameInfo(
            current_player="Player 1", 
            turn_number=1,
            player1_hp=100,
            player2_hp=100,
            prizes_p1=0,
            prizes_p2=0
        )
        commands = {
            "A": "Show Hand",
            "S": "Show Active",
            "D": "Show Hand",
            "B": "Show Bench",
            "D": "Show Discard",
            "F": "Use Trainer",
            "I": "Use Item",
            "J": "Attach Energy",
            "K": "Use Ability",
            "L": "Attack",
            "R": "Retreat",
            "Q": "Quit"
        }
        view_mode = "board"
        #draw_gui(info, self.board, self.board, commands, view_mode)
        render_layout(self.board, self.board, turn_number=5, current_player="Player 1")
        
        # Then proceed with logic: handle events, input, actions...
        self.set_state(GameState.quitting)

    def loop(self):
        while self.state != GameState.quitting:
            # First phase (turns 0a and 0b), is setup
            # Then take turns, and handle events until game ends 
            self.handle_events()

    def set_state(self, new_state):
        self.game.set_state(new_state)

    @property
    def state(self):
        return self.game.state

    @property
    def board(self):
        return self.game.board

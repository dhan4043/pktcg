from dataclasses import dataclass
from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.reactive import reactive

@dataclass
class BoardState:
    active: str
    bench: list[str]
    hand: list[str]

# Widgets
class BoardView(Static):
    active_card = reactive("No Active Card")
    bench = reactive([])
    hand = reactive([])

    def render(self):
        bench_str = ", ".join(self.bench) if self.bench else "(empty)"
        hand_str = ", ".join(self.hand) if self.hand else "(empty)"
        return (
            f"[b]Active:[/b] {self.active_card}\n"
            f"[b]Bench:[/b] {bench_str}\n"
            f"[b]Hand:[/b] {hand_str}"
        )

class InfoPane(Static):
    card_info = reactive("Select a card to see details.")

    def render(self):
        return f"[b]Card Info:[/b]\n{self.card_info}"

# Textual app 
class PokemonTUI(App):
    CSS = """
    Screen {
        layout: horizontal;
    }
    BoardView {
        width: 60%;
        padding: 1;
        border: solid green;
    }
    InfoPane {
        width: 40%;
        padding: 1;
        border: solid yellow;
    }
    """

    BINDINGS = [
        ("1", "show_card_info('Pikachu')", "Show Pikachu"),
        ("2", "show_card_info('Bulbasaur')", "Show Bulbasaur"),
        ("3", "show_card_info('Charmander')", "Show Charmander"),
    ]

    def __init__(self, board_state: BoardState):
        super().__init__()
        self.board_state = board_state

    def compose(self) -> ComposeResult:
        yield BoardView(id="board")
        yield InfoPane(id="info")

    def on_mount(self):
        self.refresh_board()

    def refresh_board(self):
        board_widget = self.query_one("#board", BoardView)
        board_widget.active_card = self.board_state.active
        board_widget.bench = self.board_state.bench
        board_widget.hand = self.board_state.hand

    def action_show_card_info(self, card_name: str):
        info_widget = self.query_one("#info", InfoPane)
        info_widget.card_info = f"{card_name} — Example Pokémon — 50 HP"

def run_gui():
    state = BoardState(
        active="Pikachu",
        bench=["Bulbasaur", "Charmander"],
        hand=["Squirtle", "Potion", "Energy"]
    )
    app = PokemonTUI(state)  # Create instance with board state
    app.run()  # Run the instance, not the class

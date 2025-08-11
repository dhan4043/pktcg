from dataclasses import dataclass
from typing import List, Dict
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.console import Console
from dataclasses import dataclass
from typing import List
console = Console()

@dataclass
class Card:
    name: str
    current_hp: int
    max_hp: int
    energy_count: int

@dataclass
class BoardState:
    active: Card
    bench: List[Card]  # up to 3

@dataclass
class GameInfo:
    current_player: str
    turn_number: int
    player1_hp: int
    player2_hp: int
    prizes_p1: int
    prizes_p2: int


def make_header(game_info: GameInfo) -> Panel:
    title = Text(f"{game_info.current_player}, Turn {game_info.turn_number}")
    title.stylize("bold white")
    return Panel(Align.center(title),title="Pokémon TCG Pocket", style="bold blue")


def make_game_info_panel(info: GameInfo) -> Panel:
    table = Table(title="Game Info", expand=True)
    # show current energy generated and energy generated next turn
    table.add_column("Player", style="bold cyan")
    table.add_column("HP", justify="center")
    table.add_column("Prizes", justify="center")

    table.add_row("Player 1", str(info.player1_hp), str(info.prizes_p1))
    table.add_row("Player 2", str(info.player2_hp), str(info.prizes_p2))

    return Panel(table, border_style="yellow")


def make_commands_panel(commands: Dict[str, str]) -> Panel:
    command_text = "\n".join(f"[bold]{k}[/bold]: {v}" for k, v in commands.items())
    return Panel(command_text, border_style="white", title="Commands")


# ----- LEFT PANEL VIEWS -----
def view_board(board: BoardState) -> Panel:
    table = Table.grid(expand=True)
    table.add_column(justify="center")
    table.add_row(f"[bold yellow]{board.active}[/bold yellow] (Active)")
    bench_display = " | ".join(f"[cyan]{card}[/cyan]" for card in board.bench) if board.bench else "(empty)"
    table.add_row(bench_display)
    return Panel(table, title="Your Board", border_style="green")


def view_hand(board: BoardState) -> Panel:
    hand_display = "\n".join(f"[bold]{card}[/bold]" for card in board.hand) if board.hand else "(empty)"
    return Panel(hand_display, title="Your Hand", border_style="magenta")


def view_active(board: BoardState) -> Panel:
    return Panel(f"[bold yellow]{board.active}[/bold yellow]\n(HP: 50, Example Pokémon)", title="Active Pokémon", border_style="yellow")


def view_opponent_active(opponent_board: BoardState) -> Panel:
    return Panel(f"[red]{opponent_board.active}[/red]\n(HP: 60, Example Pokémon)", title="Opponent Active", border_style="red")


def view_opponent_bench(opponent_board: BoardState) -> Panel:
    bench_display = "\n".join(f"[red]{card}[/red]" for card in opponent_board.bench) if opponent_board.bench else "(empty)"
    return Panel(bench_display, title="Opponent Bench", border_style="red")


# ----- MAIN DRAW -----
def draw_gui(game_info: GameInfo, board_state: BoardState, opponent_board: BoardState, commands: dict, view_mode: str):
    layout = Layout()

    # Top level split
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1)
    )

    # Split body into left (view) and right (info+commands)
    layout["body"].split_row(
        Layout(name="left", ratio=2),
        Layout(name="right", ratio=1)
    )

    layout["right"].split_column(
        Layout(name="game_info", ratio=2),
        Layout(name="commands", size=16),
        Layout(name="output", size=4)
    )

    # Header
    layout["header"].update(make_header(game_info))

    # Left panel: choose view based on mode
    if view_mode == "board":
        layout["left"].update(view_board(board_state))
    elif view_mode == "hand":
        layout["left"].update(view_hand(board_state))
    elif view_mode == "active":
        layout["left"].update(view_active(board_state))
    elif view_mode == "opp_active":
        layout["left"].update(view_opponent_active(opponent_board))
    elif view_mode == "opp_bench":
        layout["left"].update(view_opponent_bench(opponent_board))
    else:
        layout["left"].update(Panel("Invalid view", border_style="red"))

    # Right panels
    layout["game_info"].update(make_game_info_panel(game_info))
    layout["commands"].update(make_commands_panel(commands))

    console.clear()
    console.print(layout)


def render_card(card: Card) -> Panel:
    """Small panel for board display."""
    if not card:
        return Panel("Empty", border_style="dim", expand=False)
    name_line = Text(card.name, style="bold cyan")
    hp_line = f"HP: {card.current_hp}/{card.max_hp}"
    energy_line = f"Energy: {card.energy_count}"
    return Panel(Text(f"{name_line}\n{hp_line}\n{energy_line}", justify="left"),
                 padding=(0,1), border_style="white", expand=False)

def render_full_board(your_board: BoardState, opp_board: BoardState) -> Panel:
    """Full board view for both players."""
    grid = Table.grid(expand=True)
    grid.add_column(justify="center")

    # Opponent bench
    bench_row = Table.grid()
    for _ in opp_board.bench:
        bench_row.add_column()
    bench_row.add_row(*[render_card(c) for c in opp_board.bench])
    grid.add_row(bench_row)

    # Opponent active
    grid.add_row(render_card(opp_board.active))

    # Your active
    grid.add_row(render_card(your_board.active))

    # Your bench
    bench_row2 = Table.grid()
    for _ in your_board.bench:
        bench_row2.add_column()
    bench_row2.add_row(*[render_card(c) for c in your_board.bench])
    grid.add_row(bench_row2)

    return Panel(grid, title="View", border_style="green")

def render_game_info(turn_number: int, current_player: str) -> Panel:
    """Top right panel: game stats/info."""
    info_table = Table.grid(padding=1)
    info_table.add_column()
    info_table.add_row(f"Turn: {turn_number}")
    info_table.add_row(f"Current Player: {current_player}")
    return Panel(info_table, title="Game Info", border_style="blue")

def render_commands() -> Panel:
    """Bottom right panel: available commands."""
    cmds = Table.grid(padding=1)
    cmds.add_column()
    cmds.add_row("[1] Show Active")
    cmds.add_row("[2] Show Bench")
    cmds.add_row("[3] Show Opponent Active")
    cmds.add_row("[4] Show Opponent Bench")
    cmds.add_row("[Q] End Turn")
    return Panel(cmds, title="Commands", border_style="magenta")

def render_layout(your_board: BoardState, opp_board: BoardState, turn_number: int, current_player: str):
    """Full layout with header, left, right, footer."""
    # Header
    header = Panel(f"Pokemon TCG Pocket — Turn {turn_number} — {current_player}'s Turn",
                   style="bold white")

    # Left = Board, Right = Game info + commands stacked
    right_col = Table.grid(expand=True)
    right_col.add_row(render_game_info(turn_number, current_player))
    right_col.add_row(render_commands())
    right_col.add_row(Panel("Select an Action", title="Messages", border_style="magenta"))

    main = Table.grid(expand=True)
    main.add_column(ratio=2)
    main.add_column(ratio=2)
    main.add_row(render_full_board(your_board, opp_board), right_col)

    console.clear()
    console.print(header)
    console.print(main)

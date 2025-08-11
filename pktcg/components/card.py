from dataclasses import dataclass
from components.enums import EnergyType
import uuid

@dataclass
class Card:
    name: str
    uuid: str

@dataclass
class Item(Card):
    effect: str

@dataclass
class Supporter(Card):
    effect: str

@dataclass
class Pokemon(Card):
    hp: int
    stage: int
    evolves_from: str | None
    attacks: [str]
    weakness: EnergyType
    retreat: [(EnergyType, int)]
    points: int

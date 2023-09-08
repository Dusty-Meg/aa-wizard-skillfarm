# Standard Library
import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class characters_character:
    def __init__(self):
        self.name = ""

    name: str
    last_update: datetime.datetime
    total_extract_sp: float
    total_large_extractors: float


@dataclass
class characters_main:
    def __init__(self):
        self.characters = []

    characters: List[characters_character]

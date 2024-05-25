# Standard Library
import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class characters_character_skill:
    def __init__(self):
        self.skill_name = ""

    skill_id: float
    skill_name: str
    skill_level: float
    sp_in_skill: float


@dataclass
class characters_character:
    def __init__(self):
        self.name = ""
        self.skills = []

    name: str
    last_update: datetime.datetime
    total_large_extractors: float

    skills: List[characters_character_skill]

    def total_extract_sp(self):
        total = 0

        for skill in self.skills:
            total += skill.sp_in_skill

        return total


@dataclass
class characters_main:
    def __init__(self):
        self.characters = []

    characters: List[characters_character]


@dataclass
class index_skill_queue:
    def __init__(self):
        self.name = ""

    name: str
    skill_queue_end: datetime.datetime


@dataclass
class index_main:
    def __init__(self):
        self.low_skill_queue = []
        self.paused_skill_queue = []
        self.has_characters = False
        self.has_skills = False
        self.has_omega = False

    low_skill_queue: List[index_skill_queue]
    paused_skill_queue: List[index_skill_queue]
    has_characters: bool
    has_skills: bool
    has_omega: bool


@dataclass
class account_time_character:
    def __init__(self):
        self.name = ""

    name: str
    id: str
    type: str
    expiry: datetime.datetime
    remaining: str


@dataclass
class account_time_main:
    def __init__(self):
        self.characters = []

    characters: List[account_time_character]


@dataclass
class settings_characters_character:
    def __init__(self):
        self.name = ""
        self.id = ""

    name: str
    id: str


@dataclass
class settings_characters_main:
    def __init__(self):
        self.not_included_characters = []
        self.included_characters = []

    not_included_characters: List[settings_characters_character]
    included_characters: List[settings_characters_character]


@dataclass
class settings_skills_skill:
    def __init__(self):
        self.name = ""
        self.id = ""

    name: str
    id: str


@dataclass
class settings_skills_main:
    def __init__(self):
        self.not_included_skills = []
        self.included_skills = []

    not_included_skills: List[settings_skills_skill]
    included_skills: List[settings_skills_skill]


@dataclass
class settings_omegatime_character:
    def __init__(self):
        self.name = ""

    name: str
    id: str
    expiry: datetime.datetime


@dataclass
class settings_omegatime_main:
    def __init__(self):
        self.not_included_characters = []
        self.omega_characters = []
        self.mct_characters = []

    not_included_characters: List[settings_omegatime_character]
    omega_characters: List[settings_omegatime_character]
    mct_characters: List[settings_omegatime_character]

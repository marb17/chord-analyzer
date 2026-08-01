from dataclasses import dataclass, field
from enum import Enum

class QualityType(Enum):
    # --- Triads ---
    MAJOR = ([0, 4, 7], "maj")
    MINOR = ([0, 3, 7], "min")
    AUGMENTED = ([0, 4, 8], "aug")
    DIMINISHED = ([0, 3, 6], "dim")
    SUSPENDED_2 = ([0, 2, 7], "sus2")
    SUSPENDED_4 = ([0, 5, 7], "sus4")

    def __init__(self, semitones: list[int], standard_name: str):
        self.semitones = semitones
        self.standard_name = standard_name

class ExtensionType(Enum):
    NINTH = (14, "9")
    ELEVENTH = (17, "11")
    THIRTEENTH = (21, "13")

    FLAT_9 = (13, "b9")
    SHARP_9 = (15, "#9")
    SHARP_11 = (18, "#11")
    FLAT_13 = (20, "b13")

    def __init__(self, semitone: int, standard_name: str):
        self.semitone = semitone
        self.standard_name = standard_name

class AlterationType(Enum):
    FLAT_5 = (6, "b5")
    SHARP_5 = (8, "#5")

    def __init__(self, semitone: int, standard_name: str):
        self.semitone = semitone
        self.standard_name = standard_name


@dataclass(frozen=True)
class Quality:
    quality: QualityType

    @property
    def semitones(self) -> list[int]:
        return self.quality.semitones

    @property
    def standard_name(self) -> str:
        return self.quality.standard_name

@dataclass(frozen=True)
class Extension:
    extension: ExtensionType
    add: bool = False

    @property
    def semitone(self) -> int:
        return self.extension.semitone

    @property
    def standard_name(self) -> str:
        return self.extension.standard_name

    @property
    def is_add(self) -> bool:
        return self.add

@dataclass(frozen=True)
class Alteration:
    alteration: AlterationType

    @property
    def semitone(self) -> int:
        return self.alteration.semitone

    @property
    def standard_name(self) -> str:
        return self.alteration.standard_name



@dataclass
class NoteInput:
    note: int
    state: bool

@dataclass
class Chord:
    key: int
    quality: Quality
    extensions: list[Extension] = field(default_factory=list)
    alterations: list[Alteration] = field(default_factory=list)

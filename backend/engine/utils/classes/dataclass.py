from dataclasses import dataclass, field
from enum import Enum
from typing import List

from backend.engine.utils.functions.midi import midi_to_name


class Quality(Enum):
    # Triads
    MAJOR = ([0, 4, 7], "")
    MINOR = ([0, 3, 7], "min")
    AUGMENTED = ([0, 4, 8], "aug")
    DIMINISHED = ([0, 3, 6], "dim")
    SUSPENDED_2 = ([0, 2, 7], "sus2")
    SUSPENDED_4 = ([0, 5, 7], "sus4")

    def __init__(self, semitones: List[int], standard_name: str):
        self.semitones = semitones
        self.standard_name = standard_name


class Extension(Enum):
    SIXTH = (8, "6")
    MAJ_SIXTH = (9, "maj6")

    SEVENTH = (10, "7")
    MAJ_SEVENTH = (11, "maj7")

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

    def with_add(self) -> tuple["Extension", bool]:
        return self, True

class Alteration(Enum):
    FLAT_5 = (6, "b5")
    SHARP_5 = (8, "#5")

    def __init__(self, semitone: int, standard_name: str):
        self.semitone = semitone
        self.standard_name = standard_name


class Omit(Enum):
    NO_3 = "no3"
    NO_5 = "no5"

    def __init__(self, standard_name: str):
        self.standard_name = standard_name



@dataclass
class NoteInput:
    note: int
    state: bool


@dataclass
class Chord:
    key: int
    quality: Quality
    extensions: List[Extension] = field(default_factory=list)
    alterations: List[Alteration] = field(default_factory=list)
    omits: List[Omit] = field(default_factory=list)
    inversion: int | None = None
    complexity: float = field(init=False)
    confidence: float = 0.0

    def __str__(self):
        final_name = ""

        final_name += midi_to_name(self.key)[0][:1] #TODO add proper accidental shit
        final_name += self.quality.standard_name
        for ext in self.extensions:
            final_name += ext.standard_name
        for alt in self.alterations: #TODO add exceptions liek C7Sus4
            final_name += alt.standard_name
        for omt in self.omits:
            final_name += omt.standard_name
        if self.inversion:
            final_name += "/" + midi_to_name(self.inversion)[0][:1]

        return final_name

    def __post_init__(self):
        cplx = 0.0

        cplx += len(self.extensions) * 1.0
        cplx += len(self.alterations) * 1.2
        cplx += len(self.omits) * 1.4
        cplx += 0.5 if self.inversion else 0

        self.complexity = cplx


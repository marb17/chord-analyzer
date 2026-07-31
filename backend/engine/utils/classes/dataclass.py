from dataclasses import dataclass
from enum import Enum

class Quality(Enum):
    MAJOR = 1
    MINOR = 2
    DIMINISHED = 3
    AUGMENTED = 4
    SUS4 = 5
    SUS2 = 6
    MINOR_MAJOR = 7
    HALF_DIMISHED = 8
    MAJOR_6TH = 9

@dataclass
class NoteInput:
    note: int
    state: bool

@dataclass
class Chord:
    key: int
    quality: Quality

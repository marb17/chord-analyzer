from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal

from backend.engine.utils.functions.midi import midi_to_name

@dataclass
class Quality:
    quality: Literal["maj", "min", "aug", "dim", "sus2", "sus4"]
    standard_name: str = field(init=False)
    semitones: List[int] = field(init=False)
    is_suspension: bool = field(init=False)

    def __post_init__(self):
        match self.quality:
            case "maj":
                self.semitones = [0, 4, 7]
                self.standard_name = ""
            case "min":
                self.semitones = [0, 3, 7]
                self.standard_name = self.quality
            case "aug":
                self.semitones = [0, 4, 7]
                self.standard_name = self.quality
            case "dim":
                self.semitones = [0, 3, 7]
                self.standard_name = self.quality
            case "sus2":
                self.semitones = [0, 4, 7]
                self.standard_name = self.quality
            case "sus4":
                self.semitones = [0, 5, 7]
                self.standard_name = self.quality

        if self.standard_name in ["sus2", "sus4"]:
            self.is_suspension = True
        else:
            self.is_suspension = False

EXTENSION_SEMITONE_MAPPING = {
    "6": 8,
    "maj6": 9,
    "7": 10,
    "maj7": 11,
    "b9": 13,
    "9": 14,
    "maj9": 15,
    "#9": 15,
    "11": 17,
    "maj11": 18,
    "#11": 18,
    "b13": 20,
    "13": 21,
    "maj13": 22,
}

@dataclass
class Extension:
    extension: Literal["6", "maj6", "7", "maj7", "9", "maj9", "11", "maj11", "13", "maj13", "b9", "#9", "#11", "b13"]
    add: bool = False
    semitone: int = field(init=False)
    prefer_accidental: bool = False
    hidden: bool = False
    def __post_init__(self):
        self.semitone = EXTENSION_SEMITONE_MAPPING[self.extension]

        if self.prefer_accidental:
            if self.extension in ["maj9", "maj11"]:
                if self.extension == "maj9":
                    self.extension = "#9"
                elif self.extension == "maj11":
                    self.extension = "#11"

    def __str__(self):
        return f"{"HIDDEN | " if self.hidden else ""}{"add" if self.add else ""}{self.extension}"

    def __eq__(self, other: int | str | Extension):
        if isinstance(other, int):
            if self.semitone == other:
                return True
        elif isinstance(other, str):
            if self.extension == other:
                return True
        elif isinstance(other, Extension):
            if self.extension == other.extension:
                return True

        return NotImplemented

    def __gt__(self, other):
        compare_value = None
        if isinstance(other, int):
            compare_value = other
        elif isinstance(other, str):
            compare_value = EXTENSION_SEMITONE_MAPPING[other]
        elif isinstance(other, Extension):
            compare_value = other.semitone

        return self.semitone > compare_value

    def __lt__(self, other):
        compare_value = None
        if isinstance(other, int):
            compare_value = other
        elif isinstance(other, str):
            compare_value = EXTENSION_SEMITONE_MAPPING[other]
        elif isinstance(other, Extension):
            compare_value = other.semitone

        return self.semitone < compare_value

    def __le__(self, other):
        compare_value = None
        if isinstance(other, int):
            compare_value = other
        elif isinstance(other, str):
            compare_value = EXTENSION_SEMITONE_MAPPING[other]
        elif isinstance(other, Extension):
            compare_value = other.semitone

        return self.semitone <= compare_value

    def __ge__(self, other):
        compare_value = None
        if isinstance(other, int):
            compare_value = other
        elif isinstance(other, str):
            compare_value = EXTENSION_SEMITONE_MAPPING[other]
        elif isinstance(other, Extension):
            compare_value = other.semitone

        return self.semitone >= compare_value

@dataclass
class Alteration:
    alteration: Literal["b5", "#5"]

    def __post_init__(self):
        pass

@dataclass
class Omit:
    omit: Literal["no3", "no5"]


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
        return self.chord_name

    def __post_init__(self):
        cplx = 0.0

        cplx += len(self.extensions) * 1.0
        cplx += len(self.alterations) * 1.2
        cplx += len(self.omits) * 1.4
        cplx += 0.5 if self.inversion else 0

        self.complexity = cplx

    @property
    def chord_name(self) -> str:
        final_name = ""

        final_name += midi_to_name(self.key)[0][:-1]  # TODO add proper accidental shit
        final_name += self.quality.standard_name
        for ext in self.extensions:
            if ext.add:
                final_name += "add" + ext.extension
            else:
                final_name += ext.extension
        for alt in self.alterations: #TODO add exceptions liek C7Sus4
            final_name += alt.alteration
        for omt in self.omits:
            final_name += omt.omit

        if self.inversion:
            final_name += "/" + midi_to_name(self.inversion)[0][:1]

        return final_name


from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal

from backend.engine.utils.functions.midi import midi_to_name

@dataclass
class Quality:
    quality: Literal["maj", "min", "aug", "dim", "sus2", "sus4", "5", "octave"]
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
            case "5":
                self.semitones = [0, 7]
                self.standard_name = self.quality
            case "octave":
                self.semitones = [0, 12]
                self.standard_name = self.quality

        if self.standard_name in ["sus2", "sus4"]:
            self.is_suspension = True
        else:
            self.is_suspension = False

EXTENSION_SEMITONE_MAPPING = {
    "6": 9,
    "7": 10,
    "maj7": 11,
    "b9": 13,
    "9": 14,
    "#9": 15,
    "11": 17,
    "#11": 18,
    "b13": 20,
    "13": 21,

    "maj9": 14,
    "maj11": 17,
    "maj13": 21
}

@dataclass
class Extension:
    extension: Literal["6", "maj6", "7", "maj7", "9", "maj9", "11", "maj11", "13", "maj13", "b9", "#9", "#11", "b13"]
    add: bool = False
    semitone: int = field(init=False)
    major_seventh_present: bool = False
    hidden: bool = False
    non_standard_extension: bool = field(init=False)

    def __post_init__(self):
        self._update_data()
        if self.major_seventh_present: self.convert_to_major_ext()


    def _update_data(self):
        self.semitone = EXTENSION_SEMITONE_MAPPING[self.extension]
        self.non_standard_extension = self.extension in ["b9", "#9", "#11", "b13"]

    def convert_to_major_ext(self):
        if self.extension in ("maj6", "maj7", "maj9", "maj11", "maj13"):
            pass
        elif self.extension in ("b9", "#9", "#11", "b13"):
            pass
        else:
            self.extension = f"maj{self.extension}"

        self._update_data()

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
    confidence: float = 0.0

    complexity: float = field(init=False)

    def __str__(self):
        return self.chord_name

    def __hash__(self):
        return hash(self.chord_name)

    def __post_init__(self):
        cplx = 0.0

        cplx += len(self.extensions) * 0.5
        cplx += len(self.alterations) * 1.2
        cplx += len(self.omits) * 1.5
        cplx += 0.5 if self.inversion else 0

        self.complexity = cplx

    @property
    def chord_name(self) -> str:
        final_name = ""

        final_name += midi_to_name(self.key)[0][:-1]  # TODO add proper accidental shit
        if self.quality.quality in ("sus2", "sus4"):
            if self.extensions:
                final_name += self.extensions[0].extension
            final_name += self.quality.standard_name

            if len(self.extensions) >= 2:
                for extension in self.extensions[1:]:
                    final_name += extension.extension

            for alt in self.alterations:
                final_name += alt.alteration

            for omt in self.omits:
                final_name += omt.omit
        else:
            final_name += self.quality.standard_name

            for extension in self.extensions:
                final_name += extension.extension

            for alt in self.alterations:
                final_name += alt.alteration

            for omt in self.omits:
                final_name += omt.omit

        if self.inversion:
            final_name += "/" + midi_to_name(self.inversion)[0][:1]

        return final_name


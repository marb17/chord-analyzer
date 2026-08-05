from __future__ import annotations

from dataclasses import dataclass, field
from math import log
from typing import List, Literal

import select

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
    "maj13": 21,
}

@dataclass
class Extension:
    extension: Literal["6", "maj6", "7", "maj7", "9", "maj9", "11", "maj11", "13", "maj13", "b9", "#9", "#11", "b13"]
    add: bool = False
    semitone: int = field(init=False)
    major_seventh_present: bool = False
    hidden: bool = False
    non_standard_extension: bool = field(init=False)
    priority_order: int = field(init=False)

    def __post_init__(self):
        self._update_data()
        if self.major_seventh_present: self.convert_to_major_ext()
        self.priority_order = EXTENSION_SEMITONE_MAPPING[self.extension]
        if self.priority_order in [10, 11]:
            self.priority_order = 0


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
        return f"{self.extension}"
        # return f"{"add" if self.add else ""}{self.extension}"

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
    hidden: bool = False

    def __str__(self):
        return self.alteration

@dataclass
class Omit:
    omit: Literal["no3", "no5"]
    hidden: bool = False

    def __str__(self):
        return self.omit


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
    raw_notes: list[int] = field(default_factory=list)

    complexity: float = field(init=False)
    final_score: float = field(init=False)

    def __str__(self):
        return self.chord_name

    def __hash__(self):
        return hash(self.chord_name)

    def __post_init__(self):
        cplx = 0.0

        cplx += len(self.extensions) * 0.5
        cplx += len(self.alterations) * 1.2
        cplx += len(self.omits) * 1.5
        cplx += 2.0 if self.inversion else 0

        root_note = min(self.raw_notes)
        chord_root_note = min(self.key, self.inversion if self.inversion else self.key)

        if root_note != chord_root_note:
            cplx += 0.3

        self.complexity = cplx

        self.final_score = round((self.confidence * 2) / (log(self.complexity + 1.8, 2)), 2)

    @property
    def chord_name(self) -> str:
        final_name = ""

        non_hidden_extensions = [ext for ext in self.extensions.copy() if not ext.hidden]
        is_add_present = any([ext.add for ext in non_hidden_extensions])
        standard_extension = [ext for ext in non_hidden_extensions if not ext.non_standard_extension]

        final_name += midi_to_name(self.key)[0][:-1]  # TODO add proper accidental shit
        if self.quality.quality in ("sus2", "sus4"):
            if non_hidden_extensions:
                biggest_standard = standard_extension[-1]
                final_name += biggest_standard.extension
                non_hidden_extensions.remove(biggest_standard)

            list_of_additions = non_hidden_extensions + self.alterations + self.omits

            final_name += self.quality.standard_name

            if len(list_of_additions) != 0 or self.alterations:
                final_name += f"({"add" if is_add_present else ""}{", ".join([str(add) for add in list_of_additions if not add.hidden])})"

        else:
            list_of_additions = non_hidden_extensions + self.alterations + self.omits

            final_name += self.quality.standard_name

            if list_of_additions:
                if (isinstance(list_of_additions[0], Extension) and list_of_additions[0].add or
                        isinstance(list_of_additions[0], Alteration)):
                    pass
                else:
                    final_name += str(list_of_additions[0])
                    list_of_additions.pop(0)

            if len(list_of_additions) != 0 or self.alterations:
                final_name += f"({"add" if is_add_present and len(list_of_additions) > 1 else ""}{", ".join([str(add) for add in list_of_additions if not add.hidden])})"

        if self.inversion:
            final_name += "/" + midi_to_name(self.inversion)[0][:-1]

        return final_name


from __future__ import annotations

from dataclasses import dataclass, field
from math import log
from typing import List, Literal

import select

from backend.engine.utils.functions.midi import midi_to_name
from backend.engine.utils.default.default_var import MODES

from dataclasses import dataclass, field
from typing import List, Literal

# Type literal including standard intervals and chord qualities
IntervalOrQuality = Literal[
    # Single Intervals
    "m2", "M2", "m3", "M3", "P4", "TT", "P5", "m6", "M6", "m7", "M7",
    # Common Triad & Dyad Qualities
    "maj", "min", "aug", "dim", "sus2", "sus4", "5", "octave"
]

@dataclass
class Quality:
    quality: IntervalOrQuality
    standard_name: str = field(init=False)
    semitones: List[int] = field(init=False)
    is_suspension: bool = field(init=False)

    def __post_init__(self):
        match self.quality:
            # Single Intervals
            # case "P1":
            #     self.semitones = [0]
            #     self.standard_name = "Perfect Unison"
            case "m2":
                self.semitones = [0, 1]
                self.standard_name = "Minor 2nd"
            case "M2":
                self.semitones = [0, 2]
                self.standard_name = "Major 2nd"
            case "m3":
                self.semitones = [0, 3]
                self.standard_name = "Minor 3rd"
            case "M3":
                self.semitones = [0, 4]
                self.standard_name = "Major 3rd"
            case "P4":
                self.semitones = [0, 5]
                self.standard_name = "Perfect 4th"
            case "TT":
                self.semitones = [0, 6]
                self.standard_name = "Tritone"
            case "P5":
                self.semitones = [0, 7]
                self.standard_name = "Perfect 5th"
            case "m6":
                self.semitones = [0, 8]
                self.standard_name = "Minor 6th"
            case "M6":
                self.semitones = [0, 9]
                self.standard_name = "Major 6th"
            case "m7":
                self.semitones = [0, 10]
                self.standard_name = "Minor 7th"
            case "M7":
                self.semitones = [0, 11]
                self.standard_name = "Major 7th"

            # Triad / Dyad Qualities
            case "maj":
                self.semitones = [0, 4, 7]
                self.standard_name = ""
            case "min":
                self.semitones = [0, 3, 7]
                self.standard_name = "min"
            case "aug":
                self.semitones = [0, 4, 8]
                self.standard_name = "aug"
            case "dim":
                self.semitones = [0, 3, 6]
                self.standard_name = "dim"
            case "sus2":
                self.semitones = [0, 2, 7]
                self.standard_name = "sus2"
            case "sus4":
                self.semitones = [0, 5, 7]
                self.standard_name = "sus4"
            case "5":
                self.semitones = [0, 7]
                self.standard_name = "5"
            case "octave":
                self.semitones = [0, 12]
                self.standard_name = "Octave"

        self.is_suspension = self.quality in ["sus2", "sus4"]

    def __eq__(self, other):
        if isinstance(other, Quality):
            return self.quality == other.quality
        elif isinstance(other, str):
            return self.quality == other
        raise NotImplementedError

EXTENSION_SEMITONE_MAPPING = {
    "6": 9,
    "dim7": 9,
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

    def __hash__(self):
        final_score = self.semitone
        final_score += self.add * 100
        final_score += self.major_seventh_present * 200
        final_score += self.hidden * 400
        final_score += self.non_standard_extension * 800
        final_score += self.priority_order * 1600

        return final_score

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

    def __hash__(self):
        return hash(f"{self.alteration}{self.hidden}")

@dataclass
class Omit:
    omit: Literal["no3", "no5"]
    hidden: bool = False

    def __str__(self):
        return self.omit

    def __hash__(self):
        return hash(f"{self.omit}{self.hidden}")


@dataclass
class NoteInput:
    note: int
    velocity: int
    released: bool = field(default=False)
    is_sustained: bool = field(default=False)

    def __hash__(self):
        return hash(f"{self.note}{self.is_sustained}{self.state}")

    def __eq__(self, other):
        if isinstance(other, NoteInput):
            return (self.note == other.note and
                    self.is_sustained == other.is_sustained and
                    self.released == other.released)
        elif isinstance(other, int):
            return self.note == other
        raise NotImplementedError


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

    def __repr__(self):
        return f"Chord({self.__class__} {self.chord_name})"

    def __hash__(self):
        return hash(self.chord_name)

    def __post_init__(self):
        cplx = 0.0

        cplx += len(self.extensions) * 0.5
        cplx += len(self.alterations) * 1.2
        cplx += len(self.omits) * 1.5
        cplx += 2.0 if self.inversion else 0

        if self.raw_notes:
            root_note = min(self.raw_notes)
            chord_root_note = min(self.key, self.inversion if self.inversion else self.key)

            if root_note != chord_root_note:
                cplx += 0.6
        else:
            if self.key != self.inversion:
                cplx += 0.6

        self.complexity = round(cplx, 2)
        self.confidence = round(self.confidence, 2)

        self.final_score = round((self.confidence * 2) / (log(self.complexity + 1.8, 3)), 2)

        # remove dups
        self.extensions = list(set(self.extensions))
        self.alterations = list(set(self.alterations))
        self.omits = list(set(self.omits))

    @property
    def chord_name(self) -> str:
        def get_default_note(index: int) -> str:
            enharmonic_notes = midi_to_name(index)
            index %= 12

            if len(enharmonic_notes) == 1:
                return enharmonic_notes[0][:-1]
            elif len(enharmonic_notes) == 2:
                match index:
                    case 1: return enharmonic_notes[0][:-1]
                    case 3: return enharmonic_notes[1][:-1]
                    case 6: return enharmonic_notes[0][:-1]
                    case 8: return enharmonic_notes[0][:-1]
                    case 10: return enharmonic_notes[1][:-1]
                    case _: raise Exception(index)
            return enharmonic_notes[0]


        root_str = get_default_note(self.key)

        active_exts = [e for e in self.extensions if not e.hidden]
        active_alts = [a for a in self.alterations if not a.hidden]
        active_omits = [o for o in self.omits if not o.hidden]

        qual_str = (" " if len(self.quality.semitones) == 2 else "") + self.quality.standard_name

        if qual_str == "dim" and any(e.extension in ("dim7", "7") for e in active_exts):
            qual_str = "dim7"
            active_exts = [e for e in active_exts if e.extension not in ("dim7", "7")]

        elif qual_str == "aug" and any(e.extension == "maj7" for e in active_exts):
            qual_str = "maj7"
            active_alts.append(Alteration("#5"))
            active_exts = [e for e in active_exts if e.extension != "maj7"]

        primary_ext = ""
        parenthetical_items = []

        for ext in active_exts:
            if not ext.add and not primary_ext:
                primary_ext = ext.extension
            else:
                label = f"{"add" if len(parenthetical_items) == 0 else ""}{ext.extension}" if ext.add else ext.extension
                parenthetical_items.append(label)

        parenthetical_items.extend([str(a) for a in active_alts])
        parenthetical_items.extend([str(o) for o in active_omits])

        if qual_str in ("sus4", "sus2"):
            final_name = f"{root_str}{primary_ext}{qual_str}"
        else:
            final_name = f"{root_str}{qual_str}{primary_ext}"

        if parenthetical_items:
            formatted_parens = ", ".join(parenthetical_items)
            if len(parenthetical_items) > 1 or primary_ext or qual_str:
                final_name += f"({formatted_parens})"
            else:
                final_name += f"({formatted_parens})"

        if self.inversion:
            bass_str = get_default_note(self.inversion)
            final_name += f"/{bass_str}"

        return final_name

    def is_major(self) -> bool:
        return self.quality in ["maj", "sus2", "sus4"]

    def is_minor(self) -> bool:
        return self.quality in ["min"]

    def is_dim(self) -> bool:
        return self.quality in ["dim"]

@dataclass
class Key:
    base_key: int
    mode: Literal["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"] = field(default="Ionian")
    diatonic_chords: list[Quality] = field(init=False)

    def __post_init__(self):
        standard_diatonic_chords = [Quality("maj"),
                                    Quality("min"),
                                    Quality("min"),
                                    Quality("maj"),
                                    Quality("maj"),
                                    Quality("min"),
                                    Quality("dim"),]

        shift = MODES.index(self.mode)
        order = list(range(shift, 7)) + list(range(shift))

        self.diatonic_chords = [standard_diatonic_chords[i] for i in order]
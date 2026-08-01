from backend.engine.utils.classes.dataclass import Chord


class ChordEngine:
    def __init__(self):
        pass

    def notes_to_chord(self, notes: list[int]) -> Chord:
        sorted_notes = sorted(notes)


if __name__ == "__main__":
    engine = ChordEngine()

    from backend.engine.utils.default.default_var import SIMPLE_MIDI_CHORDS

    engine.notes_to_chord(SIMPLE_MIDI_CHORDS["C_Major"])
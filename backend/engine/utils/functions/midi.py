from backend.engine.utils.default.default_var import PITCH_TO_NOTES_MAP, A4_STANDARD_FREQUENCY

def midi_to_name(midi_int: int) -> list[str]:
    octave = (midi_int // 12) - 1
    semitone = midi_int % 12

    return [f"{note}{octave}" for note in PITCH_TO_NOTES_MAP[semitone]]


def midi_to_frequency(midi_int: int) -> float:
    return round(A4_STANDARD_FREQUENCY * (2**((midi_int - 69) / 12)), 2)

def frequency_to_midi(freq: float) -> int:
    raise NotImplementedError
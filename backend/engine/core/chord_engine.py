from backend.engine.utils.classes.dataclass import Chord
from backend.engine.utils.default.default_var import MUSICAL_INTERVALS
from backend.engine.utils.functions.midi import midi_to_name


class ChordEngine:
    def __init__(self):
        pass

    def notes_to_chord(self, notes: list[int]) -> list[Chord]:
        no_dup_notes = sorted(list(set(notes)))

        for base_note in no_dup_notes:
            all_semitone_relative = [note - base_note for note in no_dup_notes]
            pitch_classes = [note % 12 for note in all_semitone_relative]

            all_intervals = list()
            for note, abs_note in zip(all_semitone_relative, pitch_classes):
                if note >= 0:
                    all_intervals.append(MUSICAL_INTERVALS[note])
                else:
                    all_intervals.append(MUSICAL_INTERVALS[abs_note])

            bass_note = no_dup_notes[0]
            candidate_note = base_note

            # --- THIRD / SUS DETECTION ---
            has_sus2 = 2 in pitch_classes
            has_minor_3rd = 3 in pitch_classes
            has_major_3rd = 4 in pitch_classes
            has_sus4 = 5 in pitch_classes

            # --- FIFTH DETECTION ---
            has_dim_5th = 6 in pitch_classes
            has_perf_5th = 7 in pitch_classes
            has_aug_5th = 8 in pitch_classes

            # TRIAD DETECTION
            is_major = 0.0
            is_minor = 0.0
            is_dim = 0.0
            is_aug = 0.0
            is_sus4 = 0.0
            is_sus2 = 0.0

            if has_sus2:
                is_major += 0.0
                is_minor += 0.0
                is_dim += 0.0
                is_aug += 0.0
                is_sus4 += 0.0
                is_sus2 += 0.5
            if has_minor_3rd:
                is_major += 0.0
                is_minor += 1.0
                is_dim += 0.5
                is_aug += 0.0
                is_sus4 += 0.0
                is_sus2 += 0.0
            if has_major_3rd:
                is_major += 1.0
                is_minor += 0.0
                is_dim += 0.0
                is_aug += 0.0
                is_sus4 += 0.0
                is_sus2 += 0.0
            if has_sus4:
                is_major += 0.0
                is_minor += 0.0
                is_dim += 0.0
                is_aug += 0.0
                is_sus4 += 0.5
                is_sus2 += 0.0
            if has_perf_5th:
                is_major += 0.5
                is_minor += 0.5
                is_dim += 0.0
                is_aug += 0.0
                is_sus4 += 0.5
                is_sus2 += 0.5
            if has_dim_5th:
                is_major += 0.0
                is_minor += 0.0
                is_dim += 0.5
                is_aug += 0.0
                is_sus4 += 0.0
                is_sus2 += 0.0
            if has_aug_5th:
                is_major += 0.0
                is_minor += 0.0
                is_dim += 0.0
                is_aug += 0.5
                is_sus4 += 0.0
                is_sus2 += 0.0

            if has_major_3rd and has_perf_5th:
                is_major += 2
            elif has_minor_3rd and has_perf_5th:
                is_minor += 2
            elif has_minor_3rd and has_dim_5th:
                is_dim += 2
            elif has_major_3rd and has_aug_5th:
                is_aug += 2
            elif has_sus4 and has_perf_5th and not (has_major_3rd or has_minor_3rd):
                is_sus4 += 2
            elif has_sus2 and has_perf_5th and not (has_major_3rd or has_minor_3rd):
                is_sus2 += 2

            scores = {
                "is_major": is_major,
                "is_minor": is_minor,
                "is_dim": is_dim,
                "is_aug": is_aug,
                "is_sus4": is_sus4,
                "is_sus2": is_sus2,
            }

            best_quality_name = max(scores, key=scores.get)
            highest_score = scores[best_quality_name]

            print(f"Top Quality: {best_quality_name} ({highest_score} points)")

            print(pitch_classes)
            print(midi_to_name(candidate_note), midi_to_name(bass_note))
            print(is_major, is_minor, is_dim, is_aug, is_sus4, is_sus2)
            print([midi_to_name(note + base_note) for note in all_semitone_relative])
            print()





            








if __name__ == "__main__":
    engine = ChordEngine()

    from backend.engine.utils.default.default_var import EXPANDED_MIDI_CHORDS

    for key, value in EXPANDED_MIDI_CHORDS.items():
        print(key)
        engine.notes_to_chord(value)
        print("--------------------------")
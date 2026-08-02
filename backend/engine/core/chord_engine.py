from backend.engine.utils.classes.dataclass import Chord, Omit, Alteration, Extension, Quality
from backend.engine.utils.default.default_var import MUSICAL_INTERVALS
from backend.engine.utils.functions.midi import midi_to_name


class ChordEngine:
    def __init__(self):
        pass

    def notes_to_chord(self, notes: list[int]) -> list[Chord]:
        no_dup_notes = sorted(list(set(notes)))

        chords = list()

        for base_note in no_dup_notes:
            all_semitone_relative = sorted([note - base_note for note in no_dup_notes])
            pitch_classes = sorted([note % 12 for note in all_semitone_relative])

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

            triad_mapping = {
                "is_major": [0, 4, 7],
                "is_minor": [0, 3, 7],
                "is_dim": [0, 3, 6],
                "is_aug": [0, 4, 8],
                "is_sus4": [0, 5, 7],
                "is_sus2": [0, 2, 7],
            }

            best_quality_name = max(scores, key=scores.get)
            highest_score = scores[best_quality_name]

            additional_notes = [note if note > 0 else note % 12 for note in all_semitone_relative if note % 12 not in triad_mapping[best_quality_name]]
            missing_notes = [note for note in triad_mapping[best_quality_name] if note not in pitch_classes]

            chord_omits = list()
            chord_alterations = list()
            chord_extensions = list()

            if 7 in missing_notes:
                if 6 in additional_notes:
                    chord_alterations.append(Alteration.FLAT_5)
                elif 8 in additional_notes:
                    chord_alterations.append(Alteration.SHARP_5)
                else:
                    chord_omits.append(Omit.NO_5)

            # standard adds or extentoins
            if 8 in additional_notes:
                chord_extensions.append(Extension.SIXTH)
            if 9 in additional_notes:
                chord_extensions.append(Extension.MAJ_SIXTH)
            if 10 in additional_notes:
                chord_extensions.append(Extension.SEVENTH)
            if 11 in additional_notes:
                chord_extensions.append(Extension.MAJ_SEVENTH)
            if 14 in additional_notes:
                chord_extensions.append(Extension.NINTH)
            if 17 in additional_notes:
                chord_extensions.append(Extension.ELEVENTH)
            if 21 in additional_notes:
                chord_extensions.append(Extension.THIRTEENTH)
            if 13 in additional_notes:
                chord_extensions.append(Extension.FLAT_9)
            if 15 in additional_notes:
                chord_extensions.append(Extension.SHARP_9)
            if 18 in additional_notes:
                chord_extensions.append(Extension.SHARP_11)
            if 20 in additional_notes:
                chord_extensions.append(Extension.FLAT_13)


            # print(f"Top Quality: {best_quality_name} ({highest_score} points)")

            # # print(pitch_classes)
            # # print(midi_to_name(candidate_note), midi_to_name(bass_note))
            # print(is_major, is_minor, is_dim, is_aug, is_sus4, is_sus2)
            # # print([midi_to_name(note + base_note) for note in all_semitone_relative])
            print(additional_notes)
            print(missing_notes)
            # print(chord_omits)
            # print(chord_alterations)
            # print(chord_extensions)
            # print()

            qualities = {
                "is_major": Quality.MAJOR,
                "is_minor": Quality.MINOR,
                "is_dim": Quality.DIMINISHED,
                "is_aug": Quality.AUGMENTED,
                "is_sus4": Quality.SUSPENDED_4,
                "is_sus2": Quality.SUSPENDED_2,
            }

            chords.append(Chord(
                key=candidate_note,
                quality=qualities[best_quality_name],
                extensions=chord_extensions,
                alterations=chord_alterations,
                omits=chord_omits,
                inversion=bass_note if bass_note != candidate_note else None,
                confidence=highest_score
            ))

        for chord in chords:
            print(str(chord), chord.confidence, chord.complexity)
        return chords





            








if __name__ == "__main__":
    engine = ChordEngine()

    from backend.engine.utils.default.default_var import EXPANDED_MIDI_CHORDS

    for key, value in EXPANDED_MIDI_CHORDS.items():
        print(key)
        engine.notes_to_chord(value)
        print("---------------------------------------------------")
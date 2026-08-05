from dataclasses import replace

from backend.engine.utils.classes.dataclass import Chord, Omit, Alteration, Extension, Quality
from backend.engine.utils.default.default_var import MUSICAL_INTERVALS
from backend.engine.utils.functions.midi import midi_to_name


class ChordEngine:
    def __init__(self):
        pass

    def notes_to_chord(self, notes: list[int]) -> list[Chord]:
        if len(notes) == 0:
            return []
        elif len(notes) == 1:
            return []

        no_dup_notes = sorted(list(set(notes)))

        chords = list()

        for idx, base_note in enumerate(no_dup_notes):
            for i in range(2):
                bass_note = no_dup_notes[0]
                candidate_note = base_note

                cleaned_list = no_dup_notes.copy()

                if bass_note != candidate_note and i == 1:
                    cleaned_list.remove(bass_note)
                if bass_note == candidate_note and i == 1:
                    continue

                all_semitone_relative = sorted([note - base_note for note in cleaned_list])
                pitch_classes = sorted([note % 12 for note in all_semitone_relative])

                if len(no_dup_notes) == 2:
                    if 0 in pitch_classes and 7 in pitch_classes:
                        return [Chord(
                            key=candidate_note,
                            quality=Quality(
                                "5"
                            )
                        )]
                    elif 0 in pitch_classes and 12 in all_semitone_relative:
                        return [Chord(
                            key=candidate_note,
                            quality=Quality(
                                "octave"
                            )
                        )]

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
                        chord_alterations.append(Alteration("b5"))
                    elif 8 in additional_notes:
                        chord_alterations.append(Alteration("#5"))
                    else:
                        chord_omits.append(Omit("no5"))

                # standard adds or extentoins
                if 21 in additional_notes:
                    chord_extensions.append(Extension("13"))
                if 20 in additional_notes:
                    chord_extensions.append(Extension("b13"))
                if 18 in additional_notes:
                    chord_extensions.append(Extension("#11"))
                if 17 in additional_notes:
                    chord_extensions.append(Extension("11"))
                if 15 in additional_notes:
                    chord_extensions.append(Extension("#9"))
                if 14 in additional_notes:
                    chord_extensions.append(Extension("9"))
                if 13 in additional_notes:
                    chord_extensions.append(Extension("b9"))
                if 11 in additional_notes:
                    chord_extensions.append(Extension("maj7"))
                if 10 in additional_notes:
                    chord_extensions.append(Extension("7"))
                if 9 in additional_notes:
                    chord_extensions.append(Extension("6"))

                qualities = {
                    "is_major": Quality("maj"),
                    "is_minor": Quality("min"),
                    "is_dim": Quality("dim"),
                    "is_aug": Quality("aug"),
                    "is_sus4": Quality("sus4"),
                    "is_sus2": Quality("sus2"),
                }

                formatted_extensions = list()
                chord_extensions = sorted(chord_extensions, key = lambda e: e.semitone)

                seventh_present = any(ext.extension in ("7", "maj7") for ext in chord_extensions)

                if seventh_present:
                    seventh_major = any(ext.extension == "maj7" for ext in chord_extensions)
                else: seventh_major = False

                sixth_present = any(ext.extension in ("6") for ext in chord_extensions)

                for extension in chord_extensions:
                    if extension.extension in ("6", "maj6"):
                        formatted_extensions.append(extension)
                    elif extension.extension in ("7", "maj7"):
                        formatted_extensions.append(extension)
                    # special cases
                    elif extension.extension == "9" and sixth_present:
                        formatted_extensions.append(extension)

                    else:
                        if seventh_present:
                            formatted_extensions.append(Extension(
                                extension.extension,
                                major_seventh_present=seventh_major,
                                add=False
                            ))
                        else:
                            formatted_extensions.append(Extension(
                                extension.extension,
                                major_seventh_present=seventh_major,
                                add=True
                            ))

                    # TODO continue

                try:
                    max_semitone_standard = max([ext.semitone for ext in formatted_extensions if ext.non_standard_extension == False])
                    second_formatted_extensions = list()

                    for extension in formatted_extensions:
                        if extension.semitone == max_semitone_standard:
                            second_formatted_extensions.append(extension)
                            continue

                        if extension.add:
                            second_formatted_extensions.append(extension)
                            continue


                        if extension.semitone in (10, 11, 14, 15, 17, 18, 21) and not extension.non_standard_extension:
                            second_formatted_extensions.append(replace(extension, hidden=True))
                        else:
                            second_formatted_extensions.append(extension)

                except ValueError:
                    second_formatted_extensions = formatted_extensions

                chords.append(Chord(
                    key=candidate_note,
                    quality=qualities[best_quality_name],
                    extensions=second_formatted_extensions,
                    alterations=chord_alterations,
                    omits=chord_omits,
                    inversion=bass_note if bass_note != candidate_note else None,
                    confidence=highest_score
                ))

        return sorted(list(set(chords)), key = lambda chrd: chrd.confidence, reverse=True)














if __name__ == "__main__":
    engine = ChordEngine()

    from backend.engine.utils.default.default_var import EXPANDED_MIDI_CHORDS

    for key, value in EXPANDED_MIDI_CHORDS.items():
        print(key)
        for chord in engine.notes_to_chord(value):
            print(str(chord))
        print()
from dataclasses import replace

from backend.engine.utils.classes.dataclass import Chord, Omit, Alteration, Extension, Quality
from backend.engine.utils.default.default_var import MUSICAL_INTERVALS, MASSIVE_EXPANDED_MIDI_CHORDS
from backend.engine.utils.functions.midi import midi_to_name


class ChordEngine:
    def __init__(self):
        pass

    @staticmethod
    def notes_to_chord(notes: list[int]) -> list[Chord]:
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

                if bass_note % 12 != candidate_note % 12 and i == 1:
                    cleaned_list.remove(bass_note)
                if bass_note % 12 == candidate_note % 12 and i == 1:
                    continue

                all_semitone_relative = sorted([note - base_note for note in cleaned_list])
                pitch_classes = sorted(list(set([note % 12 for note in all_semitone_relative])))

                if len(pitch_classes) == 1 and i != 1:
                    if 0 in pitch_classes and (12 in all_semitone_relative or not any([semi % 12 == 0 for semi in all_semitone_relative])):
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "octave"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))


                if len(pitch_classes) == 2 and i != 1:
                    if 0 in pitch_classes and 1 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "m2"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))
                    elif 0 in pitch_classes and 2 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "M2"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))
                    elif 0 in pitch_classes and 3 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "m3"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))
                    elif 0 in pitch_classes and 4 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "M3"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))
                    elif 0 in pitch_classes and 5 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "P4"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))
                    elif 0 in pitch_classes and 6 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "TT"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))
                    elif 0 in pitch_classes and 7 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "P5"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))
                    elif 0 in pitch_classes and 8 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "m6"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))
                    elif 0 in pitch_classes and 9 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "M6"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))
                    elif 0 in pitch_classes and 10 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "m7"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))
                    elif 0 in pitch_classes and 11 in pitch_classes:
                        chords.append(Chord(
                            key=candidate_note,
                            quality=Quality(
                                "M7"
                            ),
                            raw_notes=notes,
                            confidence=7.0
                        ))


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
                if 3 in missing_notes or 4 in missing_notes:
                    chord_alterations.append(Omit("no3"))

                # standard adds or extentoins
                skip_try = False
                for add_note in additional_notes:
                    if add_note == 21:
                        chord_extensions.append(Extension("13"))
                    elif add_note == 20:
                        chord_extensions.append(Extension("b13"))
                    elif add_note == 18:
                        chord_extensions.append(Extension("#11"))
                    elif add_note == 17:
                        chord_extensions.append(Extension("11"))
                    elif add_note == 15:
                        chord_extensions.append(Extension("#9"))
                    elif add_note == 14:
                        chord_extensions.append(Extension("9"))
                    elif add_note == 13:
                        chord_extensions.append(Extension("b9"))
                    elif add_note == 11:
                        chord_extensions.append(Extension("maj7"))
                    elif add_note == 10:
                        if best_quality_name == "is_dim":
                            best_quality_name = "is_minor"
                            chord_alterations.append(Alteration("b5"))
                        chord_extensions.append(Extension("7"))
                    elif add_note == 9:
                        if best_quality_name == "is_dim":
                            # chord_extensions.append(Extension("dim7"))
                            chord_extensions.append(Extension("7"))
                        else:
                            chord_extensions.append(Extension("6"))
                    # safety passes
                    elif add_note in (6, ):
                        pass

                    else:
                        skip_try = True
                        break

                if skip_try:
                    continue

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
                seventh_major = any(ext.extension == "maj7" for ext in chord_extensions)
                sixth_present = any(ext.extension == "6" for ext in chord_extensions)

                try:
                    max_semitone_standard = max([ext.semitone for ext in chord_extensions if ext.non_standard_extension == False])
                except ValueError:
                    max_semitone_standard = 0

                for extension in chord_extensions:
                    if extension.extension in ("6", "maj6"):
                        formatted_extensions.append(extension)
                    elif extension.extension in ("7", "maj7"):
                        formatted_extensions.append(replace(extension, hidden=extension.semitone < max_semitone_standard))
                    # special cases
                    elif extension.extension == "9" and sixth_present:
                        formatted_extensions.append(extension)

                    else:
                        formatted_extensions.append(Extension(
                            extension.extension,
                            major_seventh_present=seventh_major,
                            add=not seventh_present or extension.non_standard_extension
                        ))

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

                        if extension.semitone in (11, 14, 15, 17, 18, 21) and not extension.non_standard_extension:
                            second_formatted_extensions.append(replace(extension, hidden=True))
                        else:
                            second_formatted_extensions.append(extension)

                except ValueError:
                    second_formatted_extensions = formatted_extensions

                second_formatted_extensions = sorted(second_formatted_extensions, key=lambda e: e.priority_order, reverse=False)

                chords.append(Chord(
                    key=candidate_note,
                    quality=qualities[best_quality_name],
                    extensions=second_formatted_extensions,
                    alterations=chord_alterations,
                    omits=chord_omits,
                    inversion=bass_note if bass_note % 12 != candidate_note % 12 else None,
                    confidence=highest_score,
                    raw_notes=notes
                ))

        return sorted(list(set(chords)), key = lambda chrd: chrd.final_score, reverse=True)



if __name__ == "__main__":
    engine = ChordEngine()

    from backend.engine.utils.default.default_var import EXPANDED_MIDI_CHORDS

    # for key, value in MASSIVE_EXPANDED_MIDI_CHORDS.items():
    for key, value in {"broken maj chord": [51, 58, 62, 63, 67, 70, 74]}.items():
        print(key)
        for chord in engine.notes_to_chord(value):
            # print(str(chord), chord.final_score, chord.confidence, chord.complexity)
            print(chord.chord_name, chord.final_score, chord.confidence, chord.complexity)
            # print(chord)
            # break
        print()
    # for key, value in {"C_Add9": [60, 64, 67, 74]}.items():
    #     print(key)
    #     for chord in engine.notes_to_chord(value):
    #         print(str(chord))
    #         print()
    #     print()
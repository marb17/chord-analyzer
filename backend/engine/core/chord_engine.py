from dataclasses import replace

from backend.engine.utils.classes.dataclass import Chord, Omit, Alteration, Extension, Quality, Key, IntervalOrQuality
from backend.engine.utils.default.default_var import MODES
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

    def predict_key(self, chords: list[Chord]) -> Key:
        def predict_candidate_root(candidate_root: int, chords_to_analyze: list[Chord]) -> float:
            score = 0.0
            diatonic_root_notes = [0, 2, 4, 5, 7, 9, 11]

            for idx, chord in enumerate(chords_to_analyze):
                curr_rel = (chord.key - candidate_root) % 12
                curr_chord = chord
                try:
                    prev_1_chord = chords[idx - 1]
                    prev_1_rel = (prev_1_chord.key - candidate_root) % 12
                except IndexError:
                    prev_1_rel = None
                    prev_1_chord = None
                try:
                    prev_2_chord = chords[idx - 2]
                    prev_2_rel = (prev_2_chord.key - candidate_root) % 12
                except IndexError:
                    prev_2_rel = None
                    prev_2_chord = None
                try:
                    prev_3_chord = chords[idx - 3]
                    prev_3_rel = (prev_3_chord.key - candidate_root) % 12
                except IndexError:
                    prev_3_rel = None
                    prev_3_chord = None

                is_tonic = False

                # 1 chord

                    # Tonic present I/i
                if curr_rel == 0 and (curr_chord.is_minor() or curr_chord.is_major()):
                    score += 10
                    is_tonic = True

                # 2 chord

                    # IV-I cadance
                if (curr_rel == 0 and curr_chord.is_major()
                        and prev_1_rel == 5 and prev_1_chord.is_major()):
                    score += 100

                    # V-I/i cadence
                if is_tonic and prev_1_rel == 7 and prev_1_chord.is_major():
                    score += 200

                    # bVII - I cadence
                if prev_3_rel == 0 and prev_3_chord.is_major() and prev_1_rel == 10 and prev_1_chord.is_major():
                    score += 50

                # 3 chord

                    # ii-V-I/i cadence
                if (is_tonic and
                        prev_1_rel == 7 and prev_1_chord.is_major() and
                        prev_2_rel == 2 and prev_2_chord.is_minor()):
                    score += 300

                    # iidim-V-I/i cadence
                if (is_tonic and
                        prev_1_rel == 7 and prev_1_chord.is_major() and
                        prev_2_rel == 2 and prev_2_chord.is_dim()):
                    score += 300

                # chord progressions

                    # I - vi - IV - V
                if (curr_chord.is_major() and curr_rel == 0 and
                        prev_1_rel == 9 and prev_1_chord.is_minor() and
                        prev_2_rel == 5 and prev_2_chord.is_major() and
                        prev_3_rel == 7 and prev_3_chord.is_major()):
                    score += 250

                if (curr_chord.is_major() and curr_rel == 0 and
                        prev_1_rel == 7 and prev_1_chord.is_major() and
                        prev_2_rel == 9 and prev_2_chord.is_minor() and
                        prev_3_rel == 5 and prev_3_chord.is_major()):
                    score += 250

                    # IV - V - iii - vi
                if (curr_chord.is_major() and curr_rel == 5 and
                        prev_1_rel == 7 and prev_1_chord.is_major() and
                        prev_2_rel == 4 and prev_2_chord.is_minor() and
                        prev_3_rel == 9 and prev_3_chord.is_minor()):
                    score += 250

                    # vi - IV - V - I
                if (curr_chord.is_minor() and curr_rel == 9 and
                        prev_1_rel == 5 and prev_1_chord.is_major() and
                        prev_2_rel == 7 and prev_2_chord.is_major() and
                        prev_3_rel == 0 and prev_3_chord.is_major()):
                    score += 250


            return score

        chord_mapping = list()
        for chord in chords:
            if chord.is_major(): qual = 0
            elif chord.is_minor(): qual = 1
            elif chord.is_dim(): qual = 2
            else: qual = 3


            chord_mapping.append([
                chord.key % 12,
                qual
            ])

        cleaned_chords = list()
        prev_key = -1
        prev_qual = -1
        for chord, mapping in zip(chords, chord_mapping):
            if mapping[0] != prev_key and mapping[1] != prev_qual:
                cleaned_chords.append(chord)
                prev_key = mapping[0]
                prev_qual = mapping[1]


        results = list()
        for i in range(12):
            score1 = predict_candidate_root(i, chords)
            score2 = predict_candidate_root(i, cleaned_chords) // 3
            results.append(score1 + score2)
            print(score1 + score2)

        highest_scoring_index = max(results)
        return Key(results.index(highest_scoring_index))
        # TODO add other modes other than IONIAN, or just rewrite ts so buns



if __name__ == "__main__":
    engine = ChordEngine()


    def c(root: int, q: IntervalOrQuality) -> Chord:
        return Chord(key=root+24, quality=Quality(quality=q))


    FULL_SONG_TEST_CASES = {
        # --------------------------------------------------------------------------
        # 1. "Risk It All" - Bruno Mars
        # Key: D Major (Root: 2, Mode: Ionian)
        # Includes full sequence: Intro -> V1 -> Pre-Chorus -> Chorus -> V2 -> Pre-Chorus -> Chorus -> Bridge -> Solo -> Pre-Chorus -> Chorus
        # --------------------------------------------------------------------------
        # Add these to your FULL_SONG_TEST_CASES dictionary:

        "Yoasobi - Racing Into The Night / Yoru ni Kakeru (Full Song)": {
            "expected_root": 5,  # F Major (Ionian) - Uses Royal Road (Db - Eb - C - Fm in F)
            "expected_mode": "Ionian",
            "chords": [
                # Intro / Chorus Loop (Db - Eb - C - Fm -> Bb - C - F)
                c(1, "maj"), c(3, "maj"), c(0, "maj"), c(5, "min"),
                c(10, "min"), c(0, "maj"), c(5, "maj"),
                c(1, "maj"), c(3, "maj"), c(0, "maj"), c(5, "min"),
                c(10, "min"), c(0, "maj"), c(5, "maj"),

                # Verse 1
                c(1, "maj"), c(3, "maj"), c(0, "min"), c(5, "min"),
                c(10, "min"), c(0, "maj"), c(5, "maj"),
                c(1, "maj"), c(3, "maj"), c(0, "maj"), c(5, "min"),
                c(10, "min"), c(0, "maj"), c(5, "maj"),

                # Pre-Chorus
                c(10, "min"), c(0, "maj"), c(5, "min"),
                c(1, "maj"), c(3, "maj"), c(0, "maj"),
                c(10, "min"), c(0, "maj"), c(3, "maj"),

                # Chorus
                c(1, "maj"), c(3, "maj"), c(0, "maj"), c(5, "min"),
                c(10, "min"), c(0, "maj"), c(5, "maj"),
                c(1, "maj"), c(3, "maj"), c(0, "maj"), c(5, "min"),
                c(10, "min"), c(0, "maj"), c(5, "maj")
            ]
        },

        "Taylor Swift - Cruel Summer (Full Song)": {
            "expected_root": 9,  # A Major (Ionian) - Classic A - C#m - F#m - D Loop
            "expected_mode": "Ionian",
            "chords": [
                # Intro
                c(9, "maj"), c(1, "min"), c(6, "min"), c(2, "maj"),
                c(9, "maj"), c(1, "min"), c(6, "min"), c(2, "maj"),

                # Verse 1 & 2
                c(9, "maj"), c(1, "min"), c(6, "min"), c(2, "maj"),
                c(9, "maj"), c(1, "min"), c(6, "min"), c(2, "maj"),

                # Chorus
                c(9, "maj"), c(1, "min"), c(6, "min"), c(2, "maj"),
                c(9, "maj"), c(1, "min"), c(6, "min"), c(2, "maj"),

                # Bridge
                c(6, "min"), c(2, "maj"), c(9, "maj"), c(4, "maj"),
                c(6, "min"), c(2, "maj"), c(9, "maj"), c(4, "maj"),

                # Outro
                c(9, "maj"), c(1, "min"), c(6, "min"), c(2, "maj"),
                c(9, "maj")
            ]
        },

        "The Beatles - Let It Be (Full Song)": {
            "expected_root": 0,  # C Major (Ionian) - Textbook I - V - vi - IV
            "expected_mode": "Ionian",
            "chords": [
                # Verse 1
                c(0, "maj"), c(7, "maj"), c(9, "min"), c(5, "maj"),
                c(0, "maj"), c(7, "maj"), c(5, "maj"), c(0, "maj"),

                # Chorus
                c(9, "min"), c(7, "maj"), c(5, "maj"), c(0, "maj"),
                c(0, "maj"), c(7, "maj"), c(5, "maj"), c(0, "maj"),

                # Verse 2
                c(0, "maj"), c(7, "maj"), c(9, "min"), c(5, "maj"),
                c(0, "maj"), c(7, "maj"), c(5, "maj"), c(0, "maj"),

                # Guitar Solo (F - C - G - F - C)
                c(5, "maj"), c(0, "maj"), c(7, "maj"), c(5, "maj"), c(0, "maj"),
                c(5, "maj"), c(0, "maj"), c(7, "maj"), c(5, "maj"), c(0, "maj"),

                # Final Chorus & Outro
                c(9, "min"), c(7, "maj"), c(5, "maj"), c(0, "maj"),
                c(0, "maj"), c(7, "maj"), c(5, "maj"), c(0, "maj")
            ]
        },

        "Earth, Wind & Fire - September (Full Song)": {
            "expected_root": 9,  # A Major (Ionian) - Heavy IV - V - iii - vi (D - E - C#m - F#m)
            "expected_mode": "Ionian",
            "chords": [
                # Intro
                c(2, "maj"), c(4, "maj"), c(1, "min"), c(6, "min"),
                c(2, "maj"), c(4, "maj"), c(1, "min"), c(6, "min"),

                # Verse
                c(2, "maj"), c(4, "maj"), c(1, "min"), c(6, "min"),
                c(2, "maj"), c(4, "maj"), c(1, "min"), c(6, "min"),
                c(2, "maj"), c(4, "maj"), c(1, "min"), c(6, "min"),

                # Chorus
                c(2, "maj"), c(4, "maj"), c(1, "min"), c(6, "min"),
                c(2, "maj"), c(4, "maj"), c(1, "min"), c(6, "min"),
                c(2, "maj"), c(4, "maj"), c(9, "maj"),  # Resolves to A Major!

                # Outro Loop
                c(2, "maj"), c(4, "maj"), c(1, "min"), c(6, "min"),
                c(2, "maj"), c(4, "maj"), c(9, "maj")
            ]
        },

        "Radiohead - High and Dry (Full Song)": {
            "expected_root": 4,  # E Major (Ionian) - F#m11 - Aadd9 - E Loop (ii - IV - I)
            "expected_mode": "Ionian",
            "chords": [
                # Verse 1
                c(6, "min"), c(9, "maj"), c(4, "maj"), c(4, "maj"),
                c(6, "min"), c(9, "maj"), c(4, "maj"), c(4, "maj"),

                # Chorus
                c(6, "min"), c(9, "maj"), c(4, "maj"), c(4, "maj"),
                c(6, "min"), c(9, "maj"), c(4, "maj"), c(4, "maj"),

                # Verse 2
                c(6, "min"), c(9, "maj"), c(4, "maj"), c(4, "maj"),
                c(6, "min"), c(9, "maj"), c(4, "maj"), c(4, "maj"),

                # Guitar Solo / Bridge
                c(6, "min"), c(9, "maj"), c(4, "maj"), c(4, "maj"),
                c(6, "min"), c(9, "maj"), c(4, "maj"), c(4, "maj"),

                # Outro
                c(6, "min"), c(9, "maj"), c(4, "maj")
            ]
        },
        "Bruno Mars - Risk It All (Full Song)": {
            "expected_root": 2,  # D
            "expected_mode": "Ionian",
            "chords": [
                # Intro
                c(4, "min"), c(9, "maj"), c(2, "maj"), c(11, "maj"),
                c(4, "min"), c(9, "maj"),
                # Verse 1
                c(4, "min"), c(9, "maj"), c(2, "maj"), c(11, "maj"),
                c(4, "min"), c(9, "maj"), c(9, "maj"), c(6, "min"), c(6, "min"), c(11, "maj"),
                # Pre-Chorus
                c(4, "min"), c(10, "min"), c(6, "min"), c(11, "maj"),
                # Chorus
                c(4, "min"), c(9, "maj"), c(2, "maj"),
                # Verse 2
                c(4, "min"), c(9, "maj"), c(2, "maj"), c(11, "maj"),
                c(4, "min"), c(9, "maj"), c(9, "maj"), c(6, "min"), c(6, "min"), c(11, "maj"),
                c(1, "dim"), c(3, "dim"),
                # Pre-Chorus
                c(4, "min"), c(10, "min"), c(6, "min"), c(11, "maj"),
                # Chorus
                c(4, "min"), c(9, "maj"), c(2, "maj"), c(2, "sus4"), c(2, "maj"), c(4, "dim"), c(6, "dim"),
                # Bridge
                c(10, "min"), c(0, "maj"), c(0, "maj"), c(9, "min"), c(10, "maj"),
                c(3, "maj"), c(9, "maj"), c(9, "maj"), c(11, "min"), c(9, "maj"), c(2, "maj"),
                # Guitar Solo
                c(4, "min"), c(9, "maj"), c(2, "maj"), c(11, "maj"),
                c(4, "min"), c(9, "maj"), c(9, "maj"), c(6, "min"), c(6, "min"), c(11, "maj"),
                c(1, "dim"), c(3, "dim"),
                # Pre-Chorus
                c(4, "min"), c(10, "min"), c(6, "min"), c(11, "maj"),
                c(1, "dim"), c(3, "dim"),
                # Chorus
                c(4, "min"), c(9, "maj"), c(9, "maj"), c(6, "min"), c(6, "min"), c(11, "maj"),
                c(1, "dim"), c(3, "dim"), c(4, "min"), c(9, "maj"), c(2, "maj")
            ]
        },

        # --------------------------------------------------------------------------
        # 2. "We'll shine brighter than any other stars" - LeeHi
        # Key: Db Major (Root: 1, Mode: Ionian)
        # Full Sequence: Intro -> Verse -> Pre-Chorus -> Chorus -> Bridge -> Interlude -> Verse -> Chorus -> Break -> Piano Solo -> Up-Chorus -> Ending
        # --------------------------------------------------------------------------
        "LeeHi - We'll shine brighter than any other stars (Full Song)": {
            "expected_root": 1,  # Db
            "expected_mode": "Ionian",
            "chords": [
                # Intro
                c(3, "min"), c(8, "sus4"), c(1, "maj"), c(1, "maj"), c(1, "maj"), c(1, "maj"), c(10, "sus4"),
                c(3, "min"), c(8, "maj"), c(8, "maj"), c(1, "maj"),
                # Verse
                c(3, "min"), c(1, "maj"), c(3, "min"), c(8, "sus4"), c(8, "sus4"), c(1, "maj"),
                c(3, "min"), c(8, "sus4"), c(8, "maj"), c(8, "sus4"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "sus4"), c(8, "maj"), c(1, "maj"),
                # Pre-Chorus
                c(3, "min"), c(8, "sus4"), c(8, "sus4"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(8, "maj"), c(1, "maj"),
                c(3, "min"), c(8, "sus4"), c(8, "maj"), c(8, "sus4"), c(1, "maj"), c(8, "maj"), c(8, "maj"),
                c(3, "min"), c(8, "sus4"), c(8, "sus4"), c(1, "maj"),
                # Chorus
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"),
                # Bridge
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"),
                # Interlude
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"),
                # Verse
                c(3, "min"), c(1, "maj"), c(3, "min"), c(8, "sus4"), c(8, "sus4"), c(1, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(1, "maj"),
                c(3, "min"), c(8, "sus4"), c(8, "sus4"), c(1, "maj"),
                # Chorus
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"),
                # Break
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"),
                # Piano Solo
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"),
                # Slow - Up Chorus
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(11, "min"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"),
                # Ending
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj"), c(10, "maj"),
                c(3, "min"), c(8, "maj"), c(1, "maj")
            ]
        },

        # --------------------------------------------------------------------------
        # 3. "オレンジ (Orange)" - 7!! (Your Lie in April ED 2)
        # Key: G Major (Root: 7, Mode: Ionian)
        # Full Progression across all lines
        # --------------------------------------------------------------------------
        "7!! - Orange (Full Song)": {
            "expected_root": 7,  # G
            "expected_mode": "Ionian",
            "chords": [
                # Line 1
                c(9, "min"), c(0, "maj"), c(2, "maj"), c(2, "maj"), c(2, "maj"),
                # Line 2
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(10, "maj"),
                # Line 3
                c(9, "min"), c(0, "maj"), c(2, "maj"), c(2, "maj"), c(2, "maj"),
                # Line 4
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(2, "maj"), c(2, "maj"), c(7, "maj"),
                # Line 5
                c(0, "min"), c(2, "maj"), c(2, "maj"), c(9, "min"),
                # Line 6
                c(0, "maj"), c(2, "maj"), c(7, "maj"),
                # Line 7
                c(0, "min"), c(2, "maj"), c(2, "maj"), c(9, "min"),
                # Line 8
                c(0, "maj"), c(0, "min"), c(2, "maj"), c(2, "sus4"), c(2, "maj"),
                # Line 9
                c(7, "maj"), c(2, "maj"), c(9, "min"), c(0, "min"), c(2, "maj"),
                # Line 10
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(2, "maj"),
                # Line 11
                c(7, "maj"), c(2, "maj"), c(9, "min"), c(0, "min"), c(2, "maj"),
                # Line 12
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(2, "maj"), c(7, "maj"),
                # Line 13
                c(9, "min"), c(0, "maj"), c(2, "maj"), c(2, "maj"), c(2, "maj"),
                # Line 14
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(2, "maj"), c(2, "maj"), c(7, "maj"),
                # Line 15
                c(0, "min"), c(2, "maj"), c(2, "maj"), c(9, "min"),
                # Line 16
                c(0, "maj"), c(2, "maj"), c(7, "maj"),
                # Line 17
                c(0, "min"), c(2, "maj"), c(2, "maj"), c(9, "min"),
                # Line 18
                c(0, "maj"), c(0, "min"), c(2, "maj"), c(2, "sus4"), c(2, "maj"),
                # Line 19
                c(7, "maj"), c(2, "maj"), c(9, "min"), c(0, "min"), c(2, "maj"),
                # Line 20
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(2, "maj"),
                # Line 21
                c(7, "maj"), c(2, "maj"), c(9, "min"), c(0, "min"), c(2, "maj"),
                # Line 22
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(2, "maj"), c(7, "maj"),
                # Line 23
                c(9, "min"), c(7, "maj"), c(0, "min"), c(2, "maj"), c(7, "maj"), c(2, "maj"),
                # Line 24
                c(9, "min"), c(0, "maj"), c(2, "maj"), c(2, "sus4"), c(2, "maj"),
                # Line 25
                c(7, "maj"), c(2, "maj"), c(9, "min"), c(0, "min"), c(2, "maj"),
                # Line 26
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(2, "maj"),
                # Line 27
                c(7, "maj"), c(2, "maj"), c(9, "min"), c(0, "min"), c(2, "maj"),
                # Line 28
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(2, "maj"), c(7, "maj"), c(2, "maj"),
                # Line 29
                c(0, "maj"), c(0, "min"), c(7, "maj"),
                # Outro
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(2, "maj"), c(7, "maj"),
                c(0, "maj"), c(2, "maj"), c(11, "min"), c(9, "min"), c(0, "min"), c(0, "min"), c(7, "maj")
            ]
        },
        "Ima Nan Janai? (Hiroo) (Full Song)": {
            "expected_root": 8,  # Ab / G# Major
            "expected_mode": "Ionian",
            "chords": [
                # Intro
                c(1, "maj"),  # C#
                c(1, "min"),  # C#m
                c(0, "min"),  # Cm
                c(0, "maj"),  # C7
                c(5, "min"),  # Fm
                c(0, "maj"),  # C
                c(8, "maj"),  # G#
                c(2, "dim"),  # Dm7b5
                c(10, "min"),  # A#m
                c(1, "maj"),  # C#
                c(3, "maj"),  # D#
                c(8, "maj"),  # G#

                # Interlude 1
                c(10, "min"), c(3, "maj"), c(8, "maj"),
                c(10, "min"), c(3, "maj"), c(8, "maj"), c(5, "min"),

                # Verse 1
                c(10, "min"), c(3, "maj"), c(5, "min"),
                c(10, "min"), c(3, "maj"), c(5, "min"), c(0, "maj"),

                # Pre-Chorus 1
                c(10, "min"), c(3, "maj"), c(8, "maj"), c(0, "maj"),
                c(10, "min"), c(0, "min"), c(1, "maj"), c(3, "maj"),

                # Chorus 1
                c(2, "dim"),  # Dm7b5
                c(1, "maj"),  # C#
                c(1, "min"),  # C#m
                c(0, "min"),  # Cm
                c(5, "min"),  # Fm
                c(1, "maj"),  # C#
                c(1, "min"),  # C#m
                c(7, "dim"),  # Gm7b5
                c(0, "maj"),  # C7
                c(5, "min"),  # Fm
                c(8, "maj"),  # G#
                c(1, "maj"),  # C#
                c(1, "min"),  # C#m
                c(0, "min"),  # Cm
                c(0, "maj"),  # C7
                c(5, "min"),  # Fm
                c(10, "min"),  # A#m
                c(1, "min"),  # C#m
                c(8, "maj"),  # G#

                # Interlude 2
                c(10, "min"), c(3, "maj"), c(8, "maj"),
                c(10, "min"), c(3, "maj"), c(8, "maj"), c(5, "min"),

                # Verse 2
                c(10, "min"), c(1, "min"), c(8, "maj"), c(0, "min"),
                c(10, "min"), c(0, "maj"), c(8, "maj"), c(0, "maj"),

                # Pre-Chorus 2
                c(10, "min"), c(3, "maj"), c(8, "maj"), c(0, "maj"),
                c(10, "min"), c(0, "min"), c(1, "maj"), c(3, "maj"),
                c(1, "maj"), c(0, "maj"), c(5, "min"),

                # Interlude 3
                c(1, "maj"), c(0, "maj"), c(5, "min"),
                c(1, "maj"), c(0, "maj"), c(5, "min"),
                c(10, "min"), c(0, "min"), c(1, "min"), c(6, "maj"), c(6, "maj"),

                # Bridge (Modulates: E / Em -> B -> D)
                c(4, "maj"),  # E
                c(4, "min"),  # Em
                c(10, "dim"),  # A#m7b5
                c(3, "maj"),  # D#
                c(8, "min"),  # G#m
                c(1, "min"),  # C#m
                c(6, "maj"),  # F#
                c(11, "maj"),  # B
                c(6, "min"),  # F#m
                c(11, "maj"),  # B
                c(4, "min"),  # Em
                c(9, "maj"),  # A
                c(2, "maj"),  # D
                c(3, "dim"),  # D#m7b5
                c(4, "min"),  # Em
                c(4, "maj"),  # E
                c(9, "maj"),  # A
                c(3, "maj"),  # D#

                # Chorus 2 (Returns to Ab Major)
                c(1, "maj"),  # C#
                c(1, "min"),  # C#m
                c(0, "min"),  # Cm
                c(5, "min"),  # Fm
                c(1, "maj"),  # C#
                c(1, "min"),  # C#m
                c(7, "dim"),  # Gm7b5
                c(0, "maj"),  # C7
                c(5, "min"),  # Fm
                c(0, "maj"),  # C
                c(8, "maj"),  # G#
                c(2, "dim"),  # Dm7b5
                c(1, "maj"),  # C#
                c(1, "min"),  # C#m
                c(7, "dim"),  # Gm7b5
                c(0, "maj"),  # C7
                c(5, "min"),  # Fm
                c(10, "min"),  # A#m
                c(1, "min"),  # C#m
                c(8, "maj"),  # G#
                c(10, "min"),  # A#m
                c(1, "min"),  # C#m
                c(8, "maj"),  # G#

                # Outro
                c(10, "min"), c(3, "maj"), c(8, "maj"),
                c(10, "min"), c(3, "maj"), c(8, "maj"), c(5, "min"),
                c(10, "min"), c(3, "maj"), c(7, "dim"), c(0, "maj"), c(5, "min"),
                c(10, "min"), c(0, "min"), c(1, "min"), c(3, "maj"),
                c(8, "maj")  # G# (Final resolution)
            ]
        }
    }
    print("=== FULL SONG KEY PREDICTION TESTS ===\n")
    for name, data in FULL_SONG_TEST_CASES.items():
        def run_full_song_tests(predict_fn):
            predicted = predict_fn(data["chords"])
            expected = Key(data["expected_root"], mode=data["expected_mode"])

            status = "PASSED" if predicted == expected else f"FAILED (Expected {expected}, got {predicted})"
            print(f"[{status}] {name} ({len(data['chords'])} total chords)")

        run_full_song_tests(engine.predict_key)

    from backend.engine.utils.default.default_var import EXPANDED_MIDI_CHORDS

    # for key, value in MASSIVE_EXPANDED_MIDI_CHORDS.items():
    # # for key, value in {"broken maj chord": [51, 58, 62, 63, 67, 70, 74]}.items():
    #     print(key)
    #     for chord in engine.notes_to_chord(value):
    #         # print(str(chord), chord.final_score, chord.confidence, chord.complexity)
    #         print(chord.chord_name, chord.final_score, chord.confidence, chord.complexity)
    #         # print(chord)
    #         # break
    #     print()

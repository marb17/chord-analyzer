A4_STANDARD_FREQUENCY = 440

PITCH_TO_NOTES_MAP = {
    0: ["C"],
    1: ["C#", "Db"],
    2: ["D"],
    3: ["D#", "Eb"],
    4: ["E"],
    5: ["F"],
    6: ["F#", "Gb"],
    7: ["G"],
    8: ["G#", "Ab"],
    9: ["A"],
    10: ["A#", "Bb"],
    11: ["B"],
}

MUSICAL_INTERVALS = {
    0: "P1",
    1: "m2",
    2: "M2",
    3: "m3",
    4: "M3",
    5: "P4",
    6: "TT",
    7: "P5",
    8: "m6",
    9: "M6",
    10: "m7",
    11: "M7",
    12: "P8",
    13: "m9",
    14: "M9",
    15: "m10",
    16: "M10",
    17: "P11",
    18: "A11",
    19: "P12",
    20: "m13",
    21: "M13",
    22: "m14",
    23: "M14",
    24: "P15",
}

# TEST AREA

EXPANDED_MIDI_CHORDS = {
    # --- BASIC TRIADS & INVERSIONS ---
    "C_Major": [60, 64, 67],  # Root: C4, E4, G4
    "C_Major_1st_Inv": [64, 67, 72],  # 1st Inv (C/E): E4, G4, C5
    "C_Major_2nd_Inv": [67, 72, 76],  # 2nd Inv (C/G): G4, C5, E5
    "C_Minor": [60, 63, 67],  # Root: C4, Eb4, G4
    "C_Minor_1st_Inv": [63, 67, 72],  # 1st Inv (Cm/Eb): Eb4, G4, C5
    "C_Minor_2nd_Inv": [67, 72, 75],  # 2nd Inv (Cm/G): G4, C5, Eb5
    "C_Diminished": [60, 63, 66],  # Root: C4, Eb4, Gb4
    "C_Diminished_1st_Inv": [63, 66, 72],  # 1st Inv (Cdim/Eb): Eb4, Gb4, C5
    "C_Diminished_2nd_Inv": [66, 72, 75],  # 2nd Inv (Cdim/Gb): Gb4, C5, Eb5
    "C_Augmented": [60, 64, 68],  # Root: C4, E4, G#4
    "C_Augmented_1st_Inv": [64, 68, 72],  # 1st Inv (C+/E): E4, G#4, C5
    "C_Augmented_2nd_Inv": [68, 72, 76],  # 2nd Inv (C+/G#): G#4, C5, E5
    "C_Flat_5": [60, 64, 66],  # Root: C4, E4, Gb4 (C(b5))
    "C_Flat_5_1st_Inv": [64, 66, 72],  # 1st Inv: E4, Gb4, C5
    "C_Flat_5_2nd_Inv": [66, 72, 76],  # 2nd Inv: Gb4, C5, E5
    # --- SUSPENDED CHORDS ---
    "C_Sus2": [60, 62, 67],  # Root: C4, D4, G4
    "C_Sus2_1st_Inv": [62, 67, 72],  # 1st Inv (Csus2/D): D4, G4, C5
    "C_Sus2_2nd_Inv": [67, 72, 74],  # 2nd Inv (Csus2/G): G4, C5, D5
    "C_Sus4": [60, 65, 67],  # Root: C4, F4, G4
    "C_Sus4_1st_Inv": [65, 67, 72],  # 1st Inv (Csus4/F): F4, G4, C5
    "C_Sus4_2nd_Inv": [67, 72, 77],  # 2nd Inv (Csus4/G): G4, C5, F5
    "C_Sus2_Add13": [60, 62, 67, 81],  # Csus2(add13): C4, D4, G4, A5
    "C_Sus4_Add13": [60, 65, 67, 81],  # Csus4(add13): C4, F4, G4, A5
    # --- 7TH CHORDS & INVERSIONS ---
    "C_Dominant_7": [60, 64, 67, 70],  # Root: C4, E4, G4, Bb4
    "C_Dominant_7_1st_Inv": [64, 67, 70, 72],  # 1st Inv (C7/E): E4, G4, Bb4, C5
    "C_Dominant_7_2nd_Inv": [67, 70, 72, 76],  # 2nd Inv (C7/G): G4, Bb4, C5, E5
    "C_Dominant_7_3rd_Inv": [70, 72, 76, 79],  # 3rd Inv (C7/Bb): Bb4, C5, E5, G5
    "C_Major_7": [60, 64, 67, 71],  # Root: C4, E4, G4, B4
    "C_Major_7_1st_Inv": [64, 67, 71, 72],  # 1st Inv (Cmaj7/E): E4, G4, B4, C5
    "C_Major_7_2nd_Inv": [67, 71, 72, 76],  # 2nd Inv (Cmaj7/G): G4, B4, C5, E5
    "C_Major_7_3rd_Inv": [71, 72, 76, 79],  # 3rd Inv (Cmaj7/B): B4, C5, E5, G5
    "C_Minor_7": [60, 63, 67, 70],  # Root: C4, Eb4, G4, Bb4
    "C_Minor_7_1st_Inv": [63, 67, 70, 72],  # 1st Inv (Cm7/Eb): Eb4, G4, Bb4, C5
    "C_Minor_7_2nd_Inv": [67, 70, 72, 75],  # 2nd Inv (Cm7/G): G4, Bb4, C5, Eb5
    "C_Minor_7_3rd_Inv": [70, 72, 75, 79],  # 3rd Inv (Cm7/Bb): Bb4, C5, Eb5, G5
    "C_Half_Diminished_7": [60, 63, 66, 70],  # Root: C4, Eb4, Gb4, Bb4 (Cø7)
    "C_Half_Diminished_7_1st_Inv": [63, 66, 70, 72],  # 1st Inv (Cø7/Eb)
    "C_Half_Diminished_7_2nd_Inv": [66, 70, 72, 75],  # 2nd Inv (Cø7/Gb)
    "C_Half_Diminished_7_3rd_Inv": [70, 72, 75, 78],  # 3rd Inv (Cø7/Bb)
    "C_Diminished_7": [60, 63, 66, 69],  # Root: C4, Eb4, Gb4, Bbb4 (MIDI 69 = A4 enharmonic)
    "C_Diminished_7_1st_Inv": [63, 66, 69, 72],  # 1st Inv (C°7/Eb)
    "C_Diminished_7_2nd_Inv": [66, 69, 72, 75],  # 2nd Inv (C°7/Gb)
    "C_Diminished_7_3rd_Inv": [69, 72, 75, 78],  # 3rd Inv (C°7/Bbb)
    "C_Minor_Major_7": [60, 63, 67, 71],  # Root: C4, Eb4, G4, B4
    "C_Minor_Major_7_1st_Inv": [63, 67, 71, 72],  # 1st Inv (Cm(maj7)/Eb)
    "C_Minor_Major_7_2nd_Inv": [67, 71, 72, 75],  # 2nd Inv (Cm(maj7)/G)
    "C_Minor_Major_7_3rd_Inv": [71, 72, 75, 79],  # 3rd Inv (Cm(maj7)/B)
    "C_7_Sus4": [60, 65, 67, 70],  # Root: C4, F4, G4, Bb4
    "C_7_Sus4_1st_Inv": [65, 67, 70, 72],  # 1st Inv (C7sus4/F)
    "C_7_Sus4_2nd_Inv": [67, 70, 72, 77],  # 2nd Inv (C7sus4/G)
    "C_7_Sus4_3rd_Inv": [70, 72, 77, 79],  # 3rd Inv (C7sus4/Bb)
    "C_9_Sus4": [60, 65, 67, 70, 74],  # Root: C4, F4, G4, Bb4, D5
    "C_13_Sus4": [60, 65, 67, 70, 74, 81],  # Root: C4, F4, G4, Bb4, D5, A5
    "C_7_Sus4_Flat_9": [60, 65, 67, 70, 73],  # Root: C4, F4, G4, Bb4, Db5
    # --- 6THS, ADD CHORDS & VOICINGS (Formerly "Extended Inversions") ---
    "C_Major_6": [60, 64, 67, 69],  # Root: C4, E4, G4, A4
    "C_Major_6_1st_Inv": [64, 67, 69, 72],  # 1st Inv (C6/E): E4, G4, A4, C5
    "C_Major_6_2nd_Inv": [67, 69, 72, 76],  # 2nd Inv (C6/G): G4, A4, C5, E5
    "C_Major_6_3rd_Inv": [69, 72, 76, 79],  # 3rd Inv (C6/A): A4, C5, E5, G5 (Am7)
    "C_Minor_6": [60, 63, 67, 69],  # Root: C4, Eb4, G4, A4
    "C_Minor_6_1st_Inv": [63, 67, 69, 72],  # 1st Inv (Cm6/Eb): Eb4, G4, A4, C5
    "C_Minor_6_2nd_Inv": [67, 69, 72, 75],  # 2nd Inv (Cm6/G): G4, A4, C5, Eb5
    "C_Minor_6_3rd_Inv": [69, 72, 75, 79],  # 3rd Inv (Cm6/A): A4, C5, Eb5, G5 (Am7b5)
    "C_69": [60, 64, 67, 69, 74],  # Root: C4, E4, G4, A4, D5
    "C_Add9": [60, 64, 67, 74],  # Root: C4, E4, G4, D5
    "C_Add9_slash_E": [
        64,
        67,
        74,
        72,
    ],  # Voicing: E4, G4, D5, C5 (Reclassified from 1st Inv)
    "C_Add9_slash_G": [
        67,
        74,
        72,
        76,
    ],  # Voicing: G4, D5, C5, E5 (Reclassified from 2nd Inv)
    "C_Add11": [60, 64, 67, 77],  # Root: C4, E4, G4, F5
    "C_Add13": [60, 64, 67, 81],  # Root: C4, E4, G4, A5
    "C_Minor_Add9": [60, 63, 67, 74],  # Root: C4, Eb4, G4, D5
    "C_Add9_Add11": [60, 64, 67, 74, 77],  # Root: C4, E4, G4, D5, F5
    "C7_Flat9_Add9": [
        60,
        64,
        67,
        73,
        74,
    ],  # Reclassified from C_Add_Flat9_Add9 (Adds dominant tension context)
    "C_7_Add9_Add13": [60, 64, 67, 70, 74, 81],  # Root: C4, E4, G4, Bb4, D5, A5
}
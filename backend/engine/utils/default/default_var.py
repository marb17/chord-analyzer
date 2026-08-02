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
    "C_Major": [60, 64, 67],  # 1st: Root (C4, E4, G4)
    "C_Major_1st_Inv": [64, 67, 72],  # 1st Inv: E4, G4, C5
    "C_Major_2nd_Inv": [67, 72, 76],  # 2nd Inv: G4, C5, E5
    "C_Minor": [60, 63, 67],  # Root: C4, Eb4, G4
    "C_Minor_1st_Inv": [63, 67, 72],  # 1st Inv: Eb4, G4, C5
    "C_Minor_2nd_Inv": [67, 72, 75],  # 2nd Inv: G4, C5, Eb5
    "C_Diminished": [60, 63, 66],  # Root: C4, Eb4, Gb4
    "C_Diminished_1st_Inv": [63, 66, 72],  # 1st Inv: Eb4, Gb4, C5
    "C_Diminished_2nd_Inv": [66, 72, 75],  # 2nd Inv: Gb4, C5, Eb5
    "C_Augmented": [60, 64, 68],  # Root: C4, E4, G#4
    "C_Augmented_1st_Inv": [64, 68, 72],  # 1st Inv: E4, G#4, C5
    "C_Augmented_2nd_Inv": [68, 72, 76],  # 2nd Inv: G#4, C5, E5
    "C_Flat_5": [60, 64, 66],  # Root: C4, E4, Gb4
    "C_Flat_5_1st_Inv": [64, 66, 72],  # 1st Inv: E4, Gb4, C5
    "C_Flat_5_2nd_Inv": [66, 72, 76],  # 2nd Inv: Gb4, C5, E5
    "C_Sus2": [60, 62, 67],  # Root: C4, D4, G4
    "C_Sus2_1st_Inv": [62, 67, 72],  # 1st Inv: D4, G4, C5
    "C_Sus2_2nd_Inv": [67, 72, 74],  # 2nd Inv: G4, C5, D5
    "C_Sus4": [60, 65, 67],  # Root: C4, F4, G4
    "C_Sus4_1st_Inv": [65, 67, 72],  # 1st Inv: F4, G4, C5
    "C_Sus4_2nd_Inv": [67, 72, 77],  # 2nd Inv: G4, C5, F5
    "C_Sus2_Add13": [60, 62, 67, 81],
    "C_Sus4_Add13": [60, 65, 67, 81],
    "C_Sus2_Add9": [60, 62, 67, 74],
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
    "C_Half_Diminished_7": [60, 63, 66, 70],  # Root: C4, Eb4, Gb4, Bb4
    "C_Half_Diminished_7_1st_Inv": [63, 66, 70, 72],  # 1st Inv
    "C_Half_Diminished_7_2nd_Inv": [66, 70, 72, 75],  # 2nd Inv
    "C_Half_Diminished_7_3rd_Inv": [70, 72, 75, 78],  # 3rd Inv
    "C_Diminished_7": [60, 63, 66, 69],  # Root: C4, Eb4, Gb4, A4
    "C_Diminished_7_1st_Inv": [63, 66, 69, 72],  # 1st Inv
    "C_Diminished_7_2nd_Inv": [66, 69, 72, 75],  # 2nd Inv
    "C_Diminished_7_3rd_Inv": [69, 72, 75, 78],  # 3rd Inv
    "C_Minor_Major_7": [60, 63, 67, 71],
    "C_Minor_Major_7_1st_Inv": [63, 67, 71, 72],
    "C_Minor_Major_7_2nd_Inv": [67, 71, 72, 75],
    "C_Minor_Major_7_3rd_Inv": [71, 72, 75, 79],
    "C_7_Sus4": [60, 65, 67, 70],
    "C_7_Sus4_1st_Inv": [65, 67, 70, 72],
    "C_7_Sus4_2nd_Inv": [67, 70, 72, 77],
    "C_7_Sus4_3rd_Inv": [70, 72, 77, 79],
    "C_9_Sus4": [60, 65, 67, 70, 74],
    "C_13_Sus4": [60, 65, 67, 70, 74, 81],
    "C_7_Sus4_Flat_9": [60, 65, 67, 70, 73],
    # --- ADD CHORDS, 6THS & INVERSIONS ---
    "C_Major_6": [60, 64, 67, 69],  # Root: C4, E4, G4, A4
    "C_Major_6_1st_Inv": [64, 67, 69, 72],  # 1st Inv: E4, G4, A4, C5
    "C_Major_6_2nd_Inv": [67, 69, 72, 76],  # 2nd Inv: G4, A4, C5, E5
    "C_Major_6_3rd_Inv": [69, 72, 76, 79],  # 3rd Inv: A4, C5, E5, G5
    "C_Minor_6": [60, 63, 67, 69],  # Root: C4, Eb4, G4, A4
    "C_Minor_6_1st_Inv": [63, 67, 69, 72],  # 1st Inv: Eb4, G4, A4, C5
    "C_Minor_6_2nd_Inv": [67, 69, 72, 75],  # 2nd Inv: G4, A4, C5, Eb5
    "C_Minor_6_3rd_Inv": [69, 72, 75, 79],  # 3rd Inv: A4, C5, Eb5, G5
    "C_69": [60, 64, 67, 69, 74],
    "C_Add9": [60, 64, 67, 74],
    "C_Add9_1st_Inv": [64, 67, 74, 72],
    "C_Add9_2nd_Inv": [67, 74, 72, 76],
    "C_Add11": [60, 64, 67, 77],
    "C_Add13": [60, 64, 67, 81],
    "C_Minor_Add9": [60, 63, 67, 74],
    "C_Add9_Add11": [60, 64, 67, 74, 77],
    "C_Add_Flat9_Add9": [60, 64, 67, 73, 74],
    "C_7_Add9_Add13": [60, 64, 67, 70, 74, 81],
    # --- CLEAN EXTENSIONS (9TH, 11TH, 13TH) & INVERSIONS ---
    "C_Dominant_9": [60, 64, 67, 70, 74],  # Root: C4, E4, G4, Bb4, D5
    "C_Dominant_9_1st_Inv": [
        64,
        67,
        70,
        74,
        72,
    ],  # 1st Inv (C9/E): E4, G4, Bb4, D5, C5
    "C_Dominant_9_2nd_Inv": [
        67,
        70,
        74,
        72,
        76,
    ],  # 2nd Inv (C9/G): G4, Bb4, D5, C5, E5
    "C_Dominant_9_3rd_Inv": [
        70,
        74,
        72,
        76,
        79,
    ],  # 3rd Inv (C9/Bb): Bb4, D5, C5, E5, G5
    "C_Dominant_9_4th_Inv": [
        74,
        72,
        76,
        79,
        82,
    ],  # 4th Inv (C9/D): D5, C5, E5, G5, Bb5
    "C_Dominant_11": [60, 64, 67, 70, 74, 77],
    "C_Dominant_13": [60, 64, 67, 70, 74, 81],
    "C_Minor_9": [60, 63, 67, 70, 74],
    "C_Minor_9_1st_Inv": [63, 67, 70, 74, 72],
    "C_Minor_9_2nd_Inv": [67, 70, 74, 72, 75],
    "C_Minor_11": [60, 63, 67, 70, 74, 77],
    "C_Minor_13": [60, 63, 67, 70, 74, 81],
    "C_Major_9": [60, 64, 67, 71, 74],
    "C_Major_9_1st_Inv": [64, 67, 71, 74, 72],
    "C_Major_9_2nd_Inv": [67, 71, 74, 72, 76],
    "C_Major_11": [60, 64, 67, 71, 74, 77],
    "C_Major_13": [60, 64, 67, 71, 74, 81],
    "C_Major_9_Add13": [60, 64, 67, 71, 74, 81],
    "C_11_Add13": [60, 64, 67, 70, 74, 77, 81],
    # --- ALTERED DOMINANTS & INVERSIONS ---
    "C_7_Flat_9": [60, 64, 67, 70, 73],
    "C_7_Flat_9_1st_Inv": [64, 67, 70, 73, 72],
    "C_7_Sharp_9": [60, 64, 67, 70, 75],
    "C_7_Sharp_9_1st_Inv": [64, 67, 70, 75, 72],
    "C_7_Flat_5": [60, 64, 66, 70],
    "C_7_Flat_5_1st_Inv": [64, 66, 70, 72],
    "C_7_Sharp_5": [60, 64, 68, 70],
    "C_7_Sharp_5_1st_Inv": [64, 68, 70, 72],
    "C_7_Flat_9_Sharp_9": [60, 64, 67, 70, 73, 75],
    "C_7_Sharp_9_Sharp_11": [60, 64, 67, 70, 75, 78],
    "C_7_Flat_9_Sharp_11": [60, 64, 67, 70, 73, 78],
    "C_7_Sharp_9_Flat_13": [60, 64, 67, 70, 75, 80],
    "C_7_Flat_9_Flat_13": [60, 64, 67, 70, 73, 80],
    "C_7_Sharp_9_Sharp_11_Flat_13": [60, 64, 67, 70, 75, 78, 80],
    "C_7_Flat_5_Sharp_5": [60, 64, 66, 68, 70],
    "C_7_Sharp_5_Sharp_11": [60, 64, 68, 70, 78],
    # --- ADVANCED JAZZ & EXTENDED MONSTERS ---
    "C_13_Flat_9_Sharp_11": [60, 64, 67, 70, 73, 78, 81],
    "C_Major_13_Sharp_11": [60, 64, 67, 71, 74, 78, 81],
    "C_Minor_9_Flat_5": [60, 63, 66, 70, 74],
    "C_Major_9_Sharp_11": [60, 64, 67, 71, 74, 78],
    "C_Minor_7_Flat_5_Flat_9": [60, 63, 66, 70, 73],
    "C_Minor_7_Flat_5_Flat_9_Flat_13": [60, 63, 66, 70, 73, 80],
    "C_7_Flat_9_Sharp_9_Sharp_11": [60, 64, 67, 70, 73, 75, 78],
    "C_7_Sharp_9_Flat_13_Sharp_11": [60, 64, 67, 70, 75, 78, 80],
    "C_13_Flat_9_Flat_13_Sharp_11": [60, 64, 67, 70, 73, 78, 80, 81],
    "C_7_Altered_Full": [60, 64, 68, 70, 73, 75, 78, 80],
    # --- DIMINISHED & MINOR/MAJOR EXTENSIONS ---
    "C_Diminished_7_Add9": [60, 63, 66, 69, 74],
    "C_Diminished_7_Flat_9": [60, 63, 66, 69, 73],
    "C_Half_Diminished_7_Add11": [60, 63, 66, 70, 77],
    "C_Minor_Major_9_Sharp_11": [60, 63, 67, 71, 74, 78],
    # --- OMISSIONS & HARD-MODE TEST CASES ---
    "C_Power_Chord": [60, 67],  # 1, 5 (Cno3)
    "C_No5": [60, 64],  # 1, 3
    "C_7_No5": [60, 64, 70],  # 1, 3, b7
    "C_7_No5_1st_Inv": [64, 70, 72],  # E4, Bb4, C5
    "C_9_No3": [60, 67, 70, 74],  # 1, 5, b7, 9
    "C_13_No9": [60, 64, 67, 70, 81],  # 1, 3, 5, b7, 13
    "C_7_No3_Flat_9": [60, 67, 70, 73],  # 1, 5, b7, b9
    "C_13_No5_Sharp_11": [60, 64, 70, 74, 78, 81],  # 1, 3, b7, 9, #11, 13
    "C_9_No3_No5": [60, 70, 74],  # 1, b7, 9
    "C_7_Sus4_Add3": [60, 64, 65, 67, 70],  # 1, 3, 4, 5, b7
    "C_FINAL_BOSS": [60, 64, 65, 70, 73, 75, 78, 80],
}
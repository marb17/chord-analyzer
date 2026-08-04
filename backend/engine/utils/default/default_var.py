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
    # --- 1. BASIC TRIADS & SUSPENSIONS ---
    "C_Major": [60, 64, 67],  # 1-3-5
    "C_Major_1st_Inv": [64, 67, 72],  # C/E (Root C moved up an octave)
    "C_Minor": [60, 63, 67],  # 1-b3-5
    "C_Diminished": [60, 63, 66],  # 1-b3-b5
    "C_Augmented": [60, 64, 68],  # 1-3-#5
    "C_Flat_5": [60, 64, 66],  # 1-3-b5 (C(b5))
    "C_Sus2": [60, 62, 67],  # 1-2-5
    "C_Sus4": [60, 65, 67],  # 1-4-5
    "C_Power_Chord": [60, 67],  # 1-5 (C5)

    # --- 2. CORE 7TH CHORDS ---
    "C_Dominant_7": [60, 64, 67, 70],  # C7: 1-3-5-b7
    "C_Dominant_7_3rd_Inv": [70, 72, 76, 79],  # C7/Bb (7th in bass, root/3rd/5th moved up an octave)
    "C_Major_7": [60, 64, 67, 71],  # Cmaj7: 1-3-5-7
    "C_Minor_7": [60, 63, 67, 70],  # Cm7: 1-b3-5-b7
    "C_Half_Diminished_7": [60, 63, 66, 70],  # Cm7b5 (Cø7): 1-b3-b5-b7
    "C_Diminished_7": [60, 63, 66, 69],  # Cdim7: 1-b3-b5-bb7
    "C_Minor_Major_7": [60, 63, 67, 71],  # Cm(maj7): 1-b3-5-7
    "C_Augmented_Major_7": [60, 64, 68, 71],  # Caug(maj7): 1-3-#5-7
    "C_Augmented_7": [60, 64, 68, 70],  # C7#5: 1-3-#5-b7

    # --- 3. SUSPENDED EXTENSIONS (No 3rd) ---
    "C_7_Sus4": [60, 65, 67, 70],  # C7sus4
    "C_9_Sus4": [60, 65, 67, 70, 74],  # C9sus4 (1-4-5-b7-9)
    "C_13_Sus4": [60, 65, 67, 70, 74, 81],  # C13sus4 (1-4-5-b7-9-13)
    "C_7_Sus4_Flat_9": [60, 65, 67, 70, 73],  # C7sus4(b9)

    # --- 4. 6TH CHORDS & EXTENSIONS (No 7th) ---
    "C_Major_6": [60, 64, 67, 69],  # C6 (1-3-5-6)
    "C_Minor_6": [60, 63, 67, 69],  # Cm6 (1-b3-5-6)
    "C_69": [60, 64, 67, 69, 74],  # C6/9 (1-3-5-6-9)
    "C_Minor_69": [60, 63, 67, 69, 74],  # Cm6/9
    "C_6_Add11": [60, 64, 67, 69, 77],  # C6add11 (6th + 11th, NO 7th)

    # --- 5. ADD CHORDS (Extensions WITHOUT a 7th) ---
    "C_Add9": [60, 64, 67, 74],  # Cadd9 (1-3-5-9)
    "C_Minor_Add9": [60, 63, 67, 74],  # Cmadd9
    "C_Add11": [60, 64, 67, 77],  # Cadd11 (1-3-5-11)
    "C_Add13": [60, 64, 67, 81],  # Cadd13 (1-3-5-13)
    "C_Add9_Add11": [60, 64, 67, 74, 77],  # Cadd9add11

    # --- 6. EXTENDED CONTIGUOUS CHORDS ---
    "C_Dominant_9": [60, 64, 67, 70, 74],  # C9 (1-3-5-b7-9)
    "C_Major_9": [60, 64, 67, 71, 74],  # Cmaj9 (1-3-5-7-9)
    "C_Minor_9": [60, 63, 67, 70, 74],  # Cm9 (1-b3-5-b7-9)
    "C_Dominant_11": [60, 64, 67, 70, 74, 77],  # C11
    "C_Minor_11": [60, 63, 67, 70, 74, 77],  # Cm11 (1-b3-5-b7-9-11)
    "C_Dominant_13": [60, 64, 67, 70, 74, 77, 81],  # C13 (Full stack)
    "C_Major_13": [60, 64, 67, 71, 74, 81],  # Cmaj13 (Omits 11th)

    # --- 7. OMISSIONS & SPARSITY EXCEPTIONS (Jazz Shells) ---
    "C_Dominant_13_Shell": [60, 64, 70, 81],  # C13 Shell (1-3-b7-13)
    "C_Major_13_Shell": [60, 64, 71, 81],  # Cmaj13 Shell (1-3-7-13)
    "C7_No5": [60, 64, 70],  # C7(no5)
    "C9_No5": [60, 64, 70, 74],  # C9(no5)
    "C13_No11": [60, 64, 67, 70, 74, 81],  # C13(no11) - Correct name for 1-3-5-b7-9-13
    "C13_No9_No11": [60, 64, 67, 70, 81],  # C13(no9,no11) - Correct name for 1-3-5-b7-13

    # --- 8. ALTERED EXTENSIONS & ALTERED CHORDS ---
    "C7_Flat9": [60, 64, 67, 70, 73],  # C7(b9)
    "C7_Sharp9": [60, 64, 67, 70, 75],  # C7(#9)
    "C7_Sharp11": [60, 64, 67, 70, 78],  # C7(#11)
    "C7_Flat13": [60, 64, 67, 70, 80],  # C7(b13)
    "C7_Alt_Complete": [60, 64, 70, 73, 80],  # C7alt (1-3-b7-b9-b13)
    "C7_Flat9_Sharp9": [60, 64, 67, 70, 73, 75],  # C7(b9,#9)
    "C7_Sharp9_Sharp11": [60, 64, 67, 70, 75, 78],  # C7(#9,#11)
    "C7_Flat9_Flat13": [60, 64, 67, 70, 73, 80],  # C7(b9,b13)
    "C_Major7_Sharp11": [60, 64, 67, 71, 78],  # Cmaj7(#11)

    # --- 9. SLASH CHORDS & HYBRID BASS NOTES ---
    "C_Major_slash_G": [55, 60, 64, 67],  # C/G (Root C triad over Low G bass [G2])
    "F_slash_C": [60, 65, 69, 72],  # F/C (F triad in 2nd inv with C in bass)
    "Fmaj7_slash_G": [55, 65, 69, 72, 76],  # Fmaj7/G (G bass note + Fmaj7)
    "Db_slash_C": [60, 61, 65, 68],  # Db/C (C bass note + Db major triad)
}
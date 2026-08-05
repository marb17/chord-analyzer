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
    "C_Octave": [60, 72],
}

MASSIVE_EXPANDED_MIDI_CHORDS = {
    # ==========================================
    # 1. BASIC TRIADS, INVERSIONS & SUSPENSIONS
    # ==========================================
    "C_Major": [60, 64, 67],
    "C_Major_1st_Inv": [64, 67, 72],  # C/E
    "C_Major_2nd_Inv": [67, 72, 76],  # C/G
    "C_Major_Open_Spread": [48, 64, 67, 72, 79],  # C2, E4, G4, C5, G5
    "C_Minor": [60, 63, 67],
    "C_Minor_1st_Inv": [63, 67, 72],  # Cm/Eb
    "C_Minor_2nd_Inv": [67, 72, 75],  # Cm/G
    "C_Diminished": [60, 63, 66],
    "C_Diminished_1st_Inv": [63, 66, 72],  # Cdim/Eb
    "C_Diminished_2nd_Inv": [66, 72, 75],  # Cdim/Gb
    "C_Augmented": [60, 64, 68],
    "C_Augmented_1st_Inv": [64, 68, 72],
    "C_Augmented_2nd_Inv": [68, 72, 76],
    "C_Flat_5": [60, 64, 66],  # C(b5)
    "C_Sus2": [60, 62, 67],
    "C_Sus2_1st_Inv": [62, 67, 72],  # Csus2/D
    "C_Sus4": [60, 65, 67],
    "C_Sus4_1st_Inv": [65, 67, 72],  # Csus4/F
    "C_Power_Chord": [60, 67],  # C5
    "C_Power_Chord_3Octaves": [36, 48, 55, 60, 67],  # Heavy C5 stack
    "C_Octave": [60, 72],
    "C_Octave_Wide": [48, 60, 72, 84],

    # ==========================================
    # 2. CORE 7TH CHORDS & ALL INVERSIONS
    # ==========================================
    "C_Dominant_7": [60, 64, 67, 70],
    "C_Dominant_7_1st_Inv": [64, 67, 70, 72],  # C7/E
    "C_Dominant_7_2nd_Inv": [67, 70, 72, 76],  # C7/G
    "C_Dominant_7_3rd_Inv": [70, 72, 76, 79],  # C7/Bb
    "C_Major_7": [60, 64, 67, 71],
    "C_Major_7_1st_Inv": [64, 67, 71, 72],  # Cmaj7/E
    "C_Major_7_2nd_Inv": [67, 71, 72, 76],  # Cmaj7/G
    "C_Major_7_3rd_Inv": [71, 72, 76, 79],  # Cmaj7/B
    "C_Minor_7": [60, 63, 67, 70],
    "C_Minor_7_1st_Inv": [63, 67, 70, 72],  # Cm7/Eb
    "C_Minor_7_2nd_Inv": [67, 70, 72, 75],  # Cm7/G
    "C_Minor_7_3rd_Inv": [70, 72, 75, 79],  # Cm7/Bb
    "C_Half_Diminished_7": [60, 63, 66, 70],  # Cm7b5
    "C_Half_Diminished_7_1st_Inv": [63, 66, 70, 72],
    "C_Half_Diminished_7_2nd_Inv": [66, 70, 72, 75],
    "C_Half_Diminished_7_3rd_Inv": [70, 72, 75, 78],
    "C_Diminished_7": [60, 63, 66, 69],  # Cdim7
    "C_Minor_Major_7": [60, 63, 67, 71],  # Cm(maj7)
    "C_Augmented_Major_7": [60, 64, 68, 71],  # Caug(maj7)
    "C_Augmented_7": [60, 64, 68, 70],  # C7#5

    # ==========================================
    # 3. SUSPENDED EXTENSIONS
    # ==========================================
    "C_7_Sus4": [60, 65, 67, 70],
    "C_7_Sus4_1st_Inv": [65, 67, 70, 72],
    "C_9_Sus4": [60, 65, 67, 70, 74],
    "C_9_Sus4_Open": [48, 58, 65, 67, 74],  # C2, Bb3, F4, G4, D5
    "C_13_Sus4": [60, 65, 67, 70, 74, 81],
    "C_13_Sus4_Jazz_Voicing": [48, 58, 65, 69, 74, 81],  # C2, Bb3, F4, A4, D5, A5
    "C_7_Sus4_Flat_9": [60, 65, 67, 70, 73],
    "C_7_Sus4_Flat_9_Open": [48, 58, 65, 70, 73],

    # ==========================================
    # 4. 6TH CHORDS & 6/9 EXTENSIONS
    # ==========================================
    "C_Major_6": [60, 64, 67, 69],
    "C_Major_6_1st_Inv": [64, 67, 69, 72],  # C6/E
    "C_Minor_6": [60, 63, 67, 69],
    "C_Minor_6_1st_Inv": [63, 67, 69, 72],  # Cm6/Eb
    "C_69": [60, 64, 67, 69, 74],
    "C_69_Open_Guitar_Style": [48, 60, 64, 69, 74, 79],  # C2, C4, E4, A4, D5, G5
    "C_Minor_69": [60, 63, 67, 69, 74],
    "C_Minor_69_Spread": [48, 58, 63, 69, 74],
    "C_6_Add11": [60, 64, 67, 69, 77],

    # ==========================================
    # 5. ADD CHORDS
    # ==========================================
    "C_Add9": [60, 64, 67, 74],
    "C_Add9_Low_5th": [48, 55, 64, 74],  # C2, G2, E4, D5
    "C_Minor_Add9": [60, 63, 67, 74],
    "C_Add11": [60, 64, 67, 77],
    "C_Add13": [60, 64, 67, 81],
    "C_Add9_Add11": [60, 64, 67, 74, 77],

    # ==========================================
    # 6. EXTENDED CONTIGUOUS & DIATONIC CHORDS
    # ==========================================
    "C_Dominant_9": [60, 64, 67, 70, 74],
    "C_Major_9": [60, 64, 67, 71, 74],
    "C_Minor_9": [60, 63, 67, 70, 74],
    "C_Dominant_11": [60, 64, 67, 70, 74, 77],
    "C_Minor_11": [60, 63, 67, 70, 74, 77],
    "C_Minor_11_Spread": [48, 58, 63, 67, 74, 77],  # C2, Bb3, Eb4, G4, D5, F5
    "C_Dominant_13": [60, 64, 67, 70, 74, 77, 81],
    "C_Major_13": [60, 64, 67, 71, 74, 81],
    "C_Minor_13": [60, 63, 67, 70, 74, 77, 81],

    # ==========================================
    # 7. JAZZ SHELLS, DROP-2 & DROP-4 VOICINGS
    # ==========================================
    "C_Dominant_7_Shell_3rd_Bass": [48, 64, 70],  # C2, E4, Bb4
    "C_Dominant_7_Shell_7th_Bass": [48, 58, 64],  # C2, Bb3, E4
    "C_Major_7_Shell": [48, 64, 71],  # C2, E4, B4
    "C_Minor_7_Shell": [48, 63, 70],  # C2, Eb4, Bb4
    "C_Dominant_13_Shell": [60, 64, 70, 81],
    "C_Major_13_Shell": [60, 64, 71, 81],
    "C7_No5": [60, 64, 70],
    "C9_No5": [60, 64, 70, 74],
    "C13_No11": [60, 64, 67, 70, 74, 81],
    "C13_No9_No11": [60, 64, 67, 70, 81],
    # Drop-2 (2nd highest note dropped down an octave)
    "C_Maj7_Drop2_Root_Pos": [48, 59, 64, 67],  # C2, B3, E4, G4
    "C_Min7_Drop2_Root_Pos": [48, 58, 63, 67],  # C2, Bb3, Eb4, G4
    "C_Dom7_Drop2_Root_Pos": [48, 58, 64, 67],  # C2, Bb3, E4, G4
    # Drop-3 (3rd highest note dropped down an octave)
    "C_Maj7_Drop3_Root_Pos": [48, 64, 59, 67],  # C2, E4, B3, G4 -> C2, B3, E4, G4
    "C_Dom7_Drop3_Root_Pos": [48, 64, 58, 67],  # C2, E4, Bb3, G4

    # ==========================================
    # 8. ROOTLESS JAZZ VOICINGS
    # ==========================================
    "C_Maj9_Rootless_TypeA": [64, 67, 71, 74],  # E, G, B, D (3-5-7-9)
    "C_Maj9_Rootless_TypeB": [71, 74, 76, 79],  # B, D, E, G (7-9-3-5)
    "C_Min9_Rootless_TypeA": [63, 67, 70, 74],  # Eb, G, Bb, D (b3-5-b7-9)
    "C_Min9_Rootless_TypeB": [70, 74, 75, 79],  # Bb, D, Eb, G (b7-9-b3-5)
    "C_Dom9_Rootless_TypeA": [64, 70, 74, 79],  # E, Bb, D, G (3-b7-9-13)
    "C_Dom9_Rootless_TypeB": [70, 74, 76, 81],  # Bb, D, E, A (b7-9-3-13)
    "C_Dom7alt_Rootless_TypeA": [64, 70, 73, 80],  # E, Bb, Db, Ab (3-b7-b9-b13)
    "C_Dom7alt_Rootless_TypeB": [70, 73, 76, 80],  # Bb, Db, E, Ab (b7-b9-3-b13)

    # ==========================================
    # 9. ALTERED EXTENSIONS & COMPLEX ALTERED
    # ==========================================
    "C7_Flat9": [60, 64, 67, 70, 73],
    "C7_Sharp9": [60, 64, 67, 70, 75],
    "C7_Sharp11": [60, 64, 67, 70, 78],
    "C7_Flat13": [60, 64, 67, 70, 80],
    "C7_Alt_Complete": [60, 64, 70, 73, 80],  # 1-3-b7-b9-b13
    "C7_Alt_Full_Stack": [60, 64, 70, 73, 75, 78, 80],  # 1-3-b7-b9-#9-#11-b13
    "C7_Flat9_Sharp9": [60, 64, 67, 70, 73, 75],
    "C7_Sharp9_Sharp11": [60, 64, 67, 70, 75, 78],
    "C7_Flat9_Flat13": [60, 64, 67, 70, 73, 80],
    "C7_Sharp9_Flat13": [60, 64, 67, 70, 75, 80],
    "C7_Flat9_Sharp11": [60, 64, 67, 70, 73, 78],
    "C_Major7_Sharp11": [60, 64, 67, 71, 78],
    "C_Major7_Sharp5": [60, 64, 68, 71],
    "C_Minor_Major7_Sharp11": [60, 63, 67, 71, 78],

    # ==========================================
    # 10. SLASH CHORDS, HYBRIDS & POLYCHORDS
    # ==========================================
    # Inversions/Slash Bass
    "C_Major_slash_G": [55, 60, 64, 67],  # C/G
    "F_slash_C": [60, 65, 69, 72],  # F/C
    "Fmaj7_slash_G": [55, 65, 69, 72, 76],  # Fmaj7/G
    "Db_slash_C": [60, 61, 65, 68],  # Db/C
    "D_slash_C": [60, 62, 66, 69],  # D/C (C7#11 sound)
    "Eb_slash_C": [60, 63, 67, 70],  # Eb/C (Cm7)
    "E_slash_C": [60, 64, 68, 71],  # E/C (Cmaj7#5)
    "F_slash_C_Clash": [60, 65, 69, 72],  # F/C
    "Fm_slash_C": [60, 65, 68, 72],  # Fm/C
    "G_slash_C": [60, 62, 67, 71],  # G/C (Cmaj9 no3)
    "Ab_slash_C": [60, 63, 68, 72],  # Ab/C (Fm/C or Ab/C)
    "Bb_slash_C": [60, 62, 65, 70],  # Bb/C (C9sus4 sound)
    "B_slash_C": [60, 63, 66, 71],  # B/C (Diminished/Altered clash)

    # Polychords (Upper Structure Triads over C7 Shell [C-E-Bb = 48, 64, 70])
    "C7_US_D_Major": [48, 64, 70, 74, 78, 81],  # D/C7 (Adds 9, #11, 13)
    "C7_US_Eb_Major": [48, 64, 70, 75, 79, 82],  # Eb/C7 (Adds #9, 5, #11)
    "C7_US_Fm_Minor": [48, 64, 70, 77, 80, 84],  # Fm/C7 (Adds 11, b13, R)
    "C7_US_Fsharp_Major": [48, 64, 70, 78, 82, 85],  # F#/C7 (Adds #11, b7, b9)
    "C7_US_Ab_Major": [48, 64, 70, 80, 84, 87],  # Ab/C7 (Adds b13, R, #9)
    "C7_US_A_Major": [48, 64, 70, 81, 85, 88],  # A/C7 (Adds 13, b9, 3)

    # ==========================================
    # 11. MODERN, QUARTAL, CLUSTER & EXOTIC
    # ==========================================
    # Quartal Voicings (Stacked 4ths)
    "C_Quartal_3Note": [60, 65, 70],  # C, F, Bb
    "C_Quartal_4Note": [60, 65, 70, 75],  # C, F, Bb, Eb (Cm11 sound)
    "C_Quartal_5Note": [60, 65, 70, 75, 80],  # C, F, Bb, Eb, Ab
    "C_Quartal_6Note": [48, 53, 58, 63, 68, 73],  # Stacked 4ths from C2

    # Quintal Voicings (Stacked 5ths)
    "C_Quintal_3Note": [60, 67, 74],  # C, G, D (Csus2)
    "C_Quintal_4Note": [60, 67, 74, 81],  # C, G, D, A (C6/9 no3)
    "C_Quintal_5Note": [48, 55, 62, 69, 76],  # C, G, D, A, E (Cmaj9)

    # Cluster Voicings (Tight adjacencies)
    "C_Semitone_Cluster": [60, 61, 62, 63],  # C, C#, D, Eb
    "C_Tone_Cluster": [60, 62, 64, 66],  # C, D, E, F#
    "C_Maj7_Inner_Cluster": [60, 71, 72, 76],  # C, B, C, E (B and C rubbing)
    "C_Add9_Cluster": [60, 62, 64, 67],  # C, D, E, G

    # Exotic & Synthetic Scales/Chords
    "C_Prometheus_Chord": [60, 66, 70, 76, 81, 86],  # C, F#, Bb, E, A, D
    "C_Tristan_Chord": [60, 66, 71, 76],  # C, F#, B, E
    "C_Mu_Major": [60, 62, 64, 67],  # Steely Dan Mu Major (C, D, E, G)
    "C_So_What_Voicing": [48, 53, 58, 63, 67],  # Stacked 4ths + 3rd (D min sound built on C)
}
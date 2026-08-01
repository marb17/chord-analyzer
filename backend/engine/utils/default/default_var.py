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

# TEST AREA

SIMPLE_MIDI_CHORDS = {
    # --- Basic Triads ---
    "C_Major": [60, 64, 67],  # C4, E4, G4
    "C_Minor": [60, 63, 67],  # C4, Eb4, G4
    "D_Minor": [62, 65, 69],  # D4, F4, A4
    "E_Minor": [64, 67, 71],  # E4, G4, B4
    "F_Major": [53, 57, 60],  # F3, A3, C4
    "G_Major": [55, 59, 62],  # G3, B3, D4
    "A_Minor": [57, 60, 64],  # A3, C4, E4
    "B_Diminished": [59, 62, 65],  # B3, D4, F4

    # --- Suspended Triads ---
    "C_Sus2": [60, 62, 67],  # C4, D4, G4
    "C_Sus4": [60, 65, 67],  # C4, F4, G4

    # --- Basic 7th Chords ---
    "C_Major_7": [60, 64, 67, 71],  # C4, E4, G4, B4
    "C_Dominant_7": [60, 64, 67, 70],  # C4, E4, G4, Bb4
    "A_Minor_7": [57, 60, 64, 67],  # A3, C4, E4, G4
    "D_Minor_7": [62, 65, 69, 72],  # D4, F4, A4, C5
    "G_Dominant_7": [55, 59, 62, 65],  # G3, B3, D4, F4
    "B_Half_Diminished_7": [59, 62, 65, 69],  # B3, D4, F4, A4

    # --- Common Inversions & Open Voicings ---
    "C_Major_1st_Inversion": [64, 67, 72],  # E4, G4, C5
    "C_Major_2nd_Inversion": [55, 60, 64],  # G3, C4, E4
    "G7_Drop_2": [55, 62, 65, 71],  # G3, D4, F4, B4
    "A_Minor_7_Spread": [45, 60, 64, 67],  # A2, C4, E4, G4
}
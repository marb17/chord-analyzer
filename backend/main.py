import helperfunc
from chord_database import *
import re
import json

def extract_chords(text_input: str) -> list[str]:
    qualities = sorted(
        (q for q in CHORD_INTERVALS.keys() if q),
        key=len,
        reverse=True
    )
    regex_quality_key = "|".join(re.escape(q) for q in qualities)

    chord_data = re.findall(
        rf'((?:[CDEFGAB][#b]?)(?:{regex_quality_key})?(?:(?:(?:[b#]|(?:no|omit|add|sus)?)(?:2|3|4|5|6|7|9|11|13)?)*)(?:\/(?:[CDEFGAB][#b]?))?)', text_input)

    return chord_data

def get_base_info(chords_input: list[str]) -> list[dict]:
    chords_data = []

    for chord in chords_input:
        main_data = helperfunc.get_chord_info(chord)
        interval_data = helperfunc.get_intervals(**main_data)
        note_data = helperfunc.get_chord_notes(main_data['base_key'], interval_data, main_data['inversion'])

        chords_data.append(
            {
                'chord': chord,
                'key_base': main_data['base_key'],
                'quality': main_data['quality'],
                'alterations': main_data['alterations'],
                'inversion': main_data['inversion'],
                'intervals': interval_data,
                'notes': note_data
            }
        )

    return chords_data

def get_roman_numerals(chords_input: list[dict], song_key: str) -> list[dict]:
    chords_data = []
    for counter in range(len(chords_input)):
        chord_data = chords_input[counter]
        key_number = ((int(KEY_TO_NUMBER[chord_data['key_base']]) - KEY_TO_NUMBER[song_key]) % 12) + 1

        maj_or_min = "maj"
        if "b3" in helperfunc.get_intervals("C", chord_data['quality'], [], ""):
            maj_or_min = "min"

        chord_data['roman_numeral'] = [NUMBER_TO_ROMAN[key_number] if maj_or_min == "maj" else NUMBER_TO_ROMAN[key_number].lower(), f"{chord_data["quality"]}{"".join(chord_data["alterations"])}"]

        chords_data.append(chord_data)

    return chords_data

if __name__ == "__main__":
    # for item in get_roman_numerals(get_base_info(extract_chords('Eb - Dm7b5 - G7 - Cm7 - Bbm7 - Eb7 - Abmaj7 - Bb7 - Gm7 - Cm7 - F7sus4 - Bmaj7 - Bb7 - Cm - Baug - Eb/Bb - Fsus4 - F - Fm - Gm - Ab - Bb - B -Db - D7')), "Eb"):
    for item in get_roman_numerals(get_base_info(extract_chords('Eb - Dm7b5 - G7 - Cm7 - Bbm7 - Eb7 - Abmaj7 - Bb7')), "Eb"):
        print(json.dumps(item, indent=4))
        pass
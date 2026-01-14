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
        chord_data = chords_input[counter].copy()
        key_number = ((int(KEY_TO_NUMBER[chord_data['key_base']]) - KEY_TO_NUMBER[song_key]) % 12) + 1

        maj_or_min = "maj"
        if "b3" in helperfunc.get_intervals("C", chord_data['quality'], [], ""):
            maj_or_min = "min"

        chord_data['roman_numeral'] = [NUMBER_TO_ROMAN[key_number] if maj_or_min == "maj" else NUMBER_TO_ROMAN[key_number].lower(), f"{chord_data["quality"]}{"".join(chord_data["alterations"])}"]

        chords_data.append(chord_data)

    return chords_data

def find_251_movement(chords_input: list[dict]) -> list[dict]:
    if len(chords_input) < 3:
        pass
    else:
        chords_data = []
        skip_counter = 0
        for counter in range(len(chords_input)):
            if skip_counter > 0:
                skip_counter -= 1
                pass
            else:
                try:
                    chord_1 = chords_input[counter].copy()
                    chord_2 = chords_input[counter + 1].copy()
                    chord_3 = chords_input[counter + 2].copy()

                    chords_roman = get_roman_numerals([chord_1, chord_2, chord_3], chord_3['key_base'])

                    roman_numerals = chords_roman[0]['roman_numeral'].copy(), chords_roman[1]['roman_numeral'].copy(), chords_roman[2]['roman_numeral'].copy()

                    #! add tritone sub in aswell
                    is_251 = []

                    for chord, correct in zip(roman_numerals, ['ii', 'V', 'I']):
                        if correct != 'I' and chord[0] == correct:
                            is_251.append(True)
                        elif correct == 'I' and chord[0].upper() == correct:
                            is_251.append(True)
                        else:
                            is_251.append(False)

                    if is_251 == [True, True, True]:
                        skip_counter += 2

                        (chord_1_roman,
                         chord_2_roman,
                         chord_3_roman,
                         chord_1_quality,
                         chord_2_quality,
                         chord_3_quality) = (roman_numerals[0][0],
                                             roman_numerals[1][0],
                                             roman_numerals[2][0],
                                             roman_numerals[0][1],
                                             roman_numerals[1][1],
                                             roman_numerals[2][1])

                        chord_1['roman_numeral_251'] = f"{chord_1_roman}{chord_1_quality}/{chord_3['roman_numeral'][0][0]}"
                        chord_2['roman_numeral_251'] = f"{chord_2_roman}{chord_2_quality}/{chord_3['roman_numeral'][0][0]}"

                        chords_data.append(chord_1)
                        chords_data.append(chord_2)
                        chords_data.append(chord_3)
                    else:
                        chord_1 = chords_input[counter].copy()
                        chords_data.append(chord_1)
                except IndexError:
                    chord_1 = chords_input[counter].copy()
                    chords_data.append(chord_1)

        return chords_data

if __name__ == "__main__":
    # for item in get_roman_numerals(get_base_info(extract_chords('Eb - Dm7b5 - G7 - Cm7 - Bbm7 - Eb7 - Abmaj7 - Bb7 - Gm7 - Cm7 - F7sus4 - Bmaj7 - Bb7 - Cm - Baug - Eb/Bb - Fsus4 - F - Fm - Gm - Ab - Bb - B -Db - D7')), "Eb"):
    asdfjkl = get_roman_numerals(get_base_info(extract_chords('Eb - Dm7b5 - G7 - Cm7 - Bbm7 - Eb7 - Abmaj7 - Bb7')), "Eb")

    # for item in asdfjkl:
    #     print(json.dumps(item, indent=4))
    #     pass

    print('-----')

    for item in find_251_movement(asdfjkl):
        print(json.dumps(item, indent=4))
        pass
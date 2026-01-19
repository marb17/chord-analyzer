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
        note_data_alt = helperfunc.get_chord_notes(main_data['base_key'], interval_data, main_data['inversion'], lower_octave=True)

        chords_data.append(
            {
                'chord': chord,
                'key_base': main_data['base_key'],
                'quality': main_data['quality'],
                'alterations': main_data['alterations'],
                'inversion': main_data['inversion'],
                'intervals': interval_data,
                'notes': note_data,
                'notes_alt': note_data_alt
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

def find_251_movement(chords_input: list[dict]) -> list[dict] | None:
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

                    is_251 = []
                    is_251_tritone = []

                    for chord, correct in zip(roman_numerals, ['ii', 'V', 'I']):
                        if correct != 'I' and chord[0] == correct:
                            is_251.append(True)
                        elif correct == 'I' and chord[0].upper() == correct:
                            is_251.append(True)
                        else:
                            is_251.append(False)

                    for chord, correct in zip(roman_numerals, ['ii', 'I#', 'I']):
                        if correct != 'I' and chord[0] == correct:
                            is_251_tritone.append(True)
                        elif correct == 'I' and chord[0].upper() == correct:
                            is_251_tritone.append(True)
                        else:
                            is_251_tritone.append(False)

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

                        chord_1['roman_numeral_251'] = f"{chord_1_roman}{chord_1_quality}/{chord_3['roman_numeral'][0]}"
                        chord_2['roman_numeral_251'] = f"{chord_2_roman}{chord_2_quality}/{chord_3['roman_numeral'][0]}"
                        chord_3['roman_numeral_251'] = ""

                        chord_1['roman_numeral_251_tritone'] = ""
                        chord_2['roman_numeral_251_tritone'] = ""
                        chord_3['roman_numeral_251_tritone'] = ""

                        chords_data.append(chord_1)
                        chords_data.append(chord_2)
                        chords_data.append(chord_3)

                    elif is_251_tritone == [True, True, True]:
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

                        chord_1['roman_numeral_251_tritone'] = f"{chord_1_roman}{chord_1_quality}/{chord_3['roman_numeral'][0][0]}"
                        chord_2['roman_numeral_251_tritone'] = f"{SHARP_TO_FLAT_ROMAN[chord_2_roman]}{chord_2_quality}/{chord_3['roman_numeral'][0][0]}"
                        chord_3['roman_numeral_251_tritone'] = ""

                        chord_1['roman_numeral_251'] = ""
                        chord_2['roman_numeral_251'] = ""
                        chord_3['roman_numeral_251'] = ""

                        chords_data.append(chord_1)
                        chords_data.append(chord_2)
                        chords_data.append(chord_3)

                    else:

                        chord_1 = chords_input[counter].copy()
                        chord_1['roman_numeral_251'] = ""
                        chord_1['roman_numeral_251_tritone'] = ""
                        chords_data.append(chord_1)
                except IndexError:
                    chord_1 = chords_input[counter].copy()
                    chord_1['roman_numeral_251'] = ""
                    chord_1['roman_numeral_251_tritone'] = ""
                    chords_data.append(chord_1)

        return chords_data

def find_51_movement(chords_input: list[dict]) -> list[dict] | None:
    if len(chords_input) < 2:
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

                    chords_roman = get_roman_numerals([chord_1, chord_2], chord_2['key_base'])

                    roman_numerals = chords_roman[0]['roman_numeral'].copy(), chords_roman[1]['roman_numeral'].copy()

                    is_51 = []
                    is_51_tritone = []

                    for chord, correct in zip(roman_numerals, ['V', 'I']):
                        if correct != 'I' and chord[0] == correct:
                            is_51.append(True)
                        elif correct == 'I' and chord[0].upper() == correct:
                            is_51.append(True)
                        else:
                            is_51.append(False)

                    for chord, correct in zip(roman_numerals, ['I#', 'I']):
                        if correct != 'I' and chord[0] == correct:
                            is_51_tritone.append(True)
                        elif correct == 'I' and chord[0].upper() == correct:
                            is_51_tritone.append(True)
                        else:
                            is_51_tritone.append(False)

                    if is_51 == [True, True]:
                        skip_counter += 1

                        (chord_1_roman,
                         chord_2_roman,
                         chord_1_quality,
                         chord_2_quality,) = (roman_numerals[0][0],
                                             roman_numerals[1][0],
                                             roman_numerals[0][1],
                                             roman_numerals[1][1],)

                        chord_1['roman_numeral_51'] = f"{chord_1_roman}{chord_1_quality}/{chord_2['roman_numeral'][0]}"
                        chord_2['roman_numeral_51'] = ""

                        chord_1['roman_numeral_51_tritone'] = ""
                        chord_2['roman_numeral_51_tritone'] = ""

                        chords_data.append(chord_1)
                        chords_data.append(chord_2)

                    elif is_51_tritone == [True, True]:
                        skip_counter += 1

                        (chord_1_roman,
                         chord_2_roman,
                         chord_1_quality,
                         chord_2_quality,) = (roman_numerals[0][0],
                                              roman_numerals[1][0],
                                              roman_numerals[0][1],
                                              roman_numerals[1][1],)

                        chord_1['roman_numeral_51_tritone'] = f"{SHARP_TO_FLAT_ROMAN[chord_1_roman]}{chord_1_quality}/{chord_2['roman_numeral'][0][0]}"
                        chord_2['roman_numeral_51_tritone'] = ""

                        chord_1['roman_numeral_51'] = ""
                        chord_2['roman_numeral_51'] = ""

                        chords_data.append(chord_1)
                        chords_data.append(chord_2)
                    else:

                        chord_1 = chords_input[counter].copy()
                        chord_1['roman_numeral_51'] = ""
                        chord_1['roman_numeral_51_tritone'] = ""
                        chords_data.append(chord_1)
                except IndexError:
                    chord_1 = chords_input[counter].copy()
                    chord_1['roman_numeral_51'] = ""
                    chord_1['roman_numeral_51_tritone'] = ""
                    chords_data.append(chord_1)

        return chords_data

def find_chord_relative_to_next(chords_input: list[dict]) -> list[dict] | None:
    chords_data = []

    for counter in range(len(chords_input)):
        chord_data = {}
        chord = chords_input[counter].copy()

        for counter_2 in range(1, 5):
            try:
                chord_precede = chords_input[counter + counter_2].copy()

                chord_roman = get_roman_numerals([chord], chord_precede['key_base'])[0]

                chord_data[f'{counter_2}_ahead'] = f"{chord_roman['roman_numeral'][0]}{chord_roman['roman_numeral'][1]}/{chord_precede['roman_numeral'][0]}"
            except IndexError:
                break

        chord['chord_next_relative'] = chord_data
        chords_data.append(chord)

    return chords_data

def find_parallel_minor(chords_input: list[dict]) -> list[dict] | None:
    chords_data = []

    for counter in range(len(chords_input) - 1):
        chord_1 = chords_input[counter].copy()
        chord_2 = chords_input[counter + 1].copy()

        chord_1_key_base = chord_1['key_base']
        chord_2_key_base = chord_2['key_base']

        chord_1_interval = chord_1['intervals']
        chord_2_interval = chord_2['intervals']

        if 'b3' in chord_1_interval:
            chord_1_quality = 'min'
        elif '3' in chord_1_interval:
            chord_1_quality = 'maj'
        else:
            chord_1_quality = ''

        if 'b3' in chord_2_interval:
            chord_2_quality = 'min'
        elif '3' in chord_2_interval:
            chord_2_quality = 'maj'
        else:
            chord_2_quality = ''

        is_same_key = True if chord_1_key_base == chord_2_key_base else False

        if chord_1_quality == 'maj' and chord_2_quality == 'min' and is_same_key:
            chord_1['parallel_mode_shift'] = f'I/{chord_2['roman_numeral'][0]}'
            chords_data.append(chord_1)
        elif chord_1_quality == 'min' and chord_2_quality == 'maj' and is_same_key:
            chord_1['parallel_mode_shift'] = f'i/{chord_2['roman_numeral'][0]}'
            chords_data.append(chord_1)
        else:
            chord_1['parallel_mode_shift'] = ''
            chords_data.append(chord_1)

    chords_data.append(chords_input[-1])

    return chords_data

def find_neighbouring_next_notes(chords_input: list[dict]) -> list[dict] | None:
    chords_data = []

    for counter in range(len(chords_input) - 1):
        chord_1 = chords_input[counter].copy()
        chord_2 = chords_input[counter + 1].copy()

        chord_1_notes = chord_1['notes']
        chord_1_notes_alt = chord_1['notes_alt']
        chord_2_notes = chord_2['notes']
        chord_2_notes_alt = chord_2['notes_alt']

        chord_1_number = [KEY_OCTAVE_TO_NUMBER[note] for note in chord_1_notes]
        chord_1_number_alt = [KEY_OCTAVE_TO_NUMBER[note] for note in chord_1_notes_alt]
        chord_2_number = [KEY_OCTAVE_TO_NUMBER[note] for note in chord_2_notes]
        chord_2_number_alt = [KEY_OCTAVE_TO_NUMBER[note] for note in chord_2_notes_alt]

        difference_list = []
        difference_list_strict = []
        difference_list_very_strict = []

        for chord_1_note, chord_1_note_alt in zip(chord_1_number, chord_1_number_alt):
            holding_number = chord_2_number[0] - chord_1_note
            holding_number_strict = chord_2_number[0] - chord_1_note

            for chord_2_note, chord_2_note_alt in zip(chord_2_number, chord_2_number_alt):
                if abs(holding_number) > abs(chord_2_note - chord_1_note):
                    holding_number = chord_2_note - chord_1_note
                if abs(holding_number) > abs(chord_2_note_alt - chord_1_note):
                    holding_number = chord_2_note_alt - chord_1_note
                if abs(holding_number) > abs(chord_2_note - chord_1_note_alt):
                    holding_number = chord_2_note - chord_1_note_alt
                if abs(holding_number) > abs(chord_2_note_alt - chord_1_note_alt):
                    holding_number = chord_2_note_alt - chord_1_note_alt

                if abs(holding_number_strict) > abs(chord_2_note - chord_1_note):
                    holding_number_strict = chord_2_note - chord_1_note

            difference_list.append(holding_number)
            difference_list_strict.append(holding_number_strict)

        for chord_1_note, chord_2_note in zip(chord_1_number, chord_2_number):
            difference_list_very_strict.append(chord_2_note - chord_1_note)

        for _ in range(len(chord_1_number) - len(difference_list_very_strict)):
            difference_list_very_strict.append(None)

        chord_1['next_chord_note_difference'] = difference_list
        chord_1['next_chord_note_difference_strict'] = difference_list_strict
        chord_1['next_chord_note_difference_very_strict'] = difference_list_very_strict
        chords_data.append(chord_1)

    return chords_data

# ill make it pretty later....
def pretty_print_chords(chords_data: list[dict]) -> None:
    lines_to_print = []

    keys_chord_dict = chords_data[0].keys()

    for key in keys_chord_dict:
        lines_to_print.append([])

    for chord, counter_1 in zip(chords_data, range(len(keys_chord_dict))):
        for key, counter_2 in zip(keys_chord_dict, range(len(keys_chord_dict))):
            try:
                lines_to_print[counter_2].append(chord[key].copy())
            except AttributeError:
                lines_to_print[counter_2].append(chord[key])

    for item in lines_to_print:
        print(item)

if __name__ == "__main__":
    # asdfjkl = get_roman_numerals(get_base_info(extract_chords('Eb - Dm7b5 - G7 - Cm7 - Bbm7 - Eb7 - Abmaj7 - Bb7 - Gm7 - Cm7 - F7sus4 - Bmaj7 - Bb7 - Cm - Baug - Eb/Bb - Fsus4 - F - Fm - Gm - Ab - Bb - B - Db - D7')), "Eb")
    asdfjkl = get_roman_numerals(get_base_info(extract_chords('Eb - Dm7b5 - G7 - Cm7 - Bbm7 - Eb7 - Abmaj7 - Bb7')), "Eb")
    # asdfjkl = get_roman_numerals(get_base_info(extract_chords('Dm - G - C')), "Bb")
    # asdfjkl = get_roman_numerals(get_base_info(extract_chords('C - F - Fm - C - Fm - F - C')), "C")
    # for item in asdfjkl:
    #     print(json.dumps(item, indent=4))
    #     pass

    print('-----')

    asdfjkl = find_251_movement(asdfjkl)
    asdfjkl = find_51_movement(asdfjkl)
    asdfjkl = find_parallel_minor(asdfjkl)
    asdfjkl = find_neighbouring_next_notes(asdfjkl)
    asdfjkl = find_chord_relative_to_next(asdfjkl)

    for item in asdfjkl:
        print(json.dumps(item, indent=4))
        pass

    # pretty_print_chords(asdfjkl)
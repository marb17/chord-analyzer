import re
from chord_database import *

def get_chord_info(chord: str) -> dict:
    """
    :param chord: The input chord to be extracted
    :return: Base key, Quality, Alterations, Inversion
    """

    qualities = sorted(
        (q for q in CHORD_INTERVALS.keys() if q),
        key=len,
        reverse=True
    )
    regex_quality_key = "|".join(re.escape(q) for q in qualities)

    chord_data = re.findall(rf'([CDEFGAB][#b]?)({regex_quality_key})?((?:(?:[b#]|(?:no|omit|add|sus)?)(?:2|3|4|5|6|7|9|11|13)?)*)(?:\/([CDEFGAB][#b]?))?', chord)
    alterations = re.findall(r'(?:no|omit|sus|add|[#b])?(?:2|3|4|5|6|7|9|11|13)', chord_data[0][2])

    try:
        base_key = chord_data[0][0]
    except IndexError:
        Exception("Not a valid chord")

    try:
        quality = chord_data[0][1]
    except IndexError:
        quality = ''

    try:
        inversion = chord_data[0][3]
    except IndexError:
        inversion = ''

    return {
        "base_key": base_key,
        "quality": quality,
        "alterations": alterations,
        "inversion": inversion,
    }

def get_intervals(base_key: str, quality: str, alterations: list[str], inversion: str) -> list:
    """
    :param base_key: key of chord
    :param quality: quality of chord
    :param alterations: alterations to chord (list)
    :param inversion: inversion of chord
    :return: the intervals for a chord (inversions do not change order, always in note order, not chord order)
    """
    output_list = CHORD_INTERVALS[quality].copy()

    for alt in alterations:
        alt_group = re.findall(r"([b#])?(2|3|4|5|6|7|9|11|13)", alt)
        alt_acc = alt_group[0][0]
        alt_number = alt_group[0][1]

        try:
            output_list.remove(alt_number)
        except ValueError:
            pass

        if re.match(r"sus", alt):
            output_list.remove("3")

        if re.match(r"no|omit", alt):
            try:
                output_list.remove(str(alt_number))
            except ValueError:
                pass
        else:
            output_list.append(f"{alt_acc}{alt_number}")

    output_list.sort(key=lambda x: INTERVAL_ORDER[x])

    return output_list

if __name__ == "__main__":
    chord_interval_tests = [

        # =============================
        # BASIC TRIADS
        # =============================
        ("C", ['1', '3', '5']),
        ("Db", ['1', '3', '5']),
        ("F#", ['1', '3', '5']),
        ("Am", ['1', 'b3', '5']),
        ("Ebm", ['1', 'b3', '5']),
        ("Bdim", ['1', 'b3', 'b5']),
        ("F#dim", ['1', 'b3', 'b5']),
        ("Eaug", ['1', '3', '#5']),
        ("Bbaug", ['1', '3', '#5']),

        # =============================
        # SUSPENDED
        # =============================
        ("Csus2", ['1', '2', '5']),
        ("Csus4", ['1', '4', '5']),
        ("Gsus2", ['1', '2', '5']),
        ("Gsus4", ['1', '4', '5']),
        ("Fsus2add13", ['1', '2', '5', '13']),

        # =============================
        # BASIC 7THS
        # =============================
        ("C7", ['1', '3', '5', 'b7']),
        ("F7", ['1', '3', '5', 'b7']),
        ("Bb7", ['1', '3', '5', 'b7']),
        ("Cmaj7", ['1', '3', '5', '7']),
        ("Fmaj7", ['1', '3', '5', '7']),
        ("Bmaj7", ['1', '3', '5', '7']),
        ("Am7", ['1', 'b3', '5', 'b7']),
        ("Ebm7", ['1', 'b3', '5', 'b7']),
        ("Bm7b5", ['1', 'b3', 'b5', 'b7']),
        ("Cø7", ['1', 'b3', 'b5', 'b7']),
        ("Adim7", ['1', 'b3', 'b5', 'bb7']),

        # =============================
        # EXTENSIONS (CLEAN)
        # =============================
        ("C9", ['1', '3', '5', 'b7', '9']),
        ("C11", ['1', '3', '5', 'b7', '9', '11']),
        ("C13", ['1', '3', '5', 'b7', '9', '13']),
        ("Cm9", ['1', 'b3', '5', 'b7', '9']),
        ("Cm11", ['1', 'b3', '5', 'b7', '9', '11']),
        ("Cm13", ['1', 'b3', '5', 'b7', '9', '13']),
        ("Cmaj9", ['1', '3', '5', '7', '9']),
        ("Cmaj11", ['1', '3', '5', '7', '9', '11']),
        ("Cmaj13", ['1', '3', '5', '7', '9', '13']),

        # =============================
        # ALTERED DOMINANTS (HELL)
        # =============================
        ("C7b9", ['1', '3', '5', 'b7', 'b9']),
        ("C7#9", ['1', '3', '5', 'b7', '#9']),
        ("C7b5", ['1', '3', 'b5', 'b7']),
        ("C7#5", ['1', '3', '#5', 'b7']),
        ("C7b9#9", ['1', '3', '5', 'b7', 'b9', '#9']),
        ("C7#9#11", ['1', '3', '5', 'b7', '#9', '#11']),
        ("C7b9#11", ['1', '3', '5', 'b7', 'b9', '#11']),
        ("C7#9b13", ['1', '3', '5', 'b7', '#9', 'b13']),
        ("C7b9b13", ['1', '3', '5', 'b7', 'b9', 'b13']),
        ("C7#9#11b13", ['1', '3', '5', 'b7', '#9', '#11', 'b13']),

        # =============================
        # SUSPENDED DOMINANTS
        # =============================
        ("G7sus4", ['1', '4', '5', 'b7']),
        ("G9sus4", ['1', '4', '5', 'b7', '9']),
        ("G13sus4", ['1', '4', '5', 'b7', '9', '13']),
        ("D7sus4b9", ['1', '4', '5', 'b7', 'b9']),

        # =============================
        # ADD CHORDS
        # =============================
        ("Cadd9", ['1', '3', '5', '9']),
        ("Cadd11", ['1', '3', '5', '11']),
        ("Cadd13", ['1', '3', '5', '13']),
        ("Cmadd9", ['1', 'b3', '5', '9']),
        ("Csus2add9", ['1', '2', '5', '9']),
        ("Csus4add13", ['1', '4', '5', '13']),

        # =============================
        # INVERSIONS (IGNORE BASS)
        # =============================
        ("C/E", ['1', '3', '5']),
        ("C/G", ['1', '3', '5']),
        ("Am/C", ['1', 'b3', '5']),
        ("G7/B", ['1', '3', '5', 'b7']),
        ("G7/F", ['1', '3', '5', 'b7']),
        ("Cmaj9/E", ['1', '3', '5', '7', '9']),
        ("C13/Bb", ['1', '3', '5', 'b7', '9', '13']),

        # =============================
        # JAZZ MONSTERS
        # =============================
        ("Bb13b9#11", ['1', '3', '5', 'b7', 'b9', '#11', '13']),
        ("Gb7#9#11/Bb", ['1', '3', '5', 'b7', '#9', '#11']),
        ("E7#9#11b13", ['1', '3', '5', 'b7', '#9', '#11', 'b13']),
        ("Abmaj13#11", ['1', '3', '5', '7', '9', '#11', '13']),
        ("F#m9b5", ['1', 'b3', 'b5', 'b7', '9']),
        ("Dbmaj9#11", ['1', '3', '5', '7', '9', '#11']),

        # =============================
        # OMISSIONS (OPTIONAL SUPPORT)
        # =============================
        ("Cno3", ['1', '5']),
        ("Cno5", ['1', '3']),
        ("C7no5", ['1', '3', 'b7']),
        ("C9no3", ['1', '5', 'b7', '9']),
        ("G13no9", ['1', '3', '5', 'b7', '13']),

        # =============================
        # PURE EVIL
        # =============================
        ("C7#9#11#5b13", ['1', '3', '#5', 'b7', '#9', '#11', 'b13']),
        ("F#m7b5b9b13", ['1', 'b3', 'b5', 'b7', 'b9', 'b13']),
        ("Bb7#9b9#11", ['1', '3', '5', 'b7', 'b9', '#9', '#11']),

        # =============================
        # ALTERATION STACKING HELL
        # =============================
        ("C7b9#9", ['1', '3', '5', 'b7', 'b9', '#9']),
        ("C7#9b13#11", ['1', '3', '5', 'b7', '#9', '#11', 'b13']),
        ("C13b9b13#11", ['1', '3', '5', 'b7', 'b9', '#11', 'b13']),
        ("C7b5#5", ['1', '3', 'b5', '#5', 'b7']),
        ("C7#11#5", ['1', '3', '#5', 'b7', '#11']),

        # =============================
        # DOUBLE-CONFLICT INTERVALS
        # =============================
        ("C7sus4add3", ['1', '3', '4', '5', 'b7']),  # illegal but real
        ("Cadd9add11", ['1', '3', '5', '9', '11']),
        ("Caddb9add9", ['1', '3', '5', 'b9', '9']),
        ("C7add13add9", ['1', '3', '5', 'b7', '9', '13']),

        # =============================
        # DIMINISHED NIGHTMARES
        # =============================
        ("Cdim7add9", ['1', 'b3', 'b5', 'bb7', '9']),
        ("Cdim7b9", ['1', 'b3', 'b5', 'bb7', 'b9']),
        ("Cø7add11", ['1', 'b3', 'b5', 'b7', '11']),

        # =============================
        # MAJOR / MINOR IDENTITY CRISIS
        # =============================
        ("Cmaj7b3", ['1', 'b3', '5', '7']),
        ("CmMaj7", ['1', 'b3', '5', '7']),
        ("CmMaj9#11", ['1', 'b3', '5', '7', '9', '#11']),

        # =============================
        # EXTENSION COLLISIONS
        # =============================
        ("C9add13", ['1', '3', '5', 'b7', '9', '13']),
        ("C11add13", ['1', '3', '5', 'b7', '9', '11', '13']),
        ("Cmaj9add13", ['1', '3', '5', '7', '9', '13']),
        ("C13add11", ['1', '3', '5', 'b7', '9', '11', '13']),

        # =============================
        # OMISSION + ALTERATION COMBOS
        # =============================
        ("C7no3b9", ['1', '5', 'b7', 'b9']),
        ("C13no5#11", ['1', '3', 'b7', '9', '#11', '13']),
        ("C9no3no5", ['1', 'b7', '9']),

        # =============================
        # SLASH + CHAOS
        # =============================
        ("C7#9/Eb", ['1', '3', '5', 'b7', '#9']),
        ("Cmaj13#11/Gb", ['1', '3', '5', '7', '9', '#11', '13']),
        ("F#m7b5b9/E", ['1', 'b3', 'b5', 'b7', 'b9']),

        # =============================
        # JAZZ THEORY WAR CRIMES
        # =============================
        # ("C7alt", ['1', '3', 'b7', 'b9', '#9', 'b5', '#5']),  # if you support "alt"
        # ("C13alt", ['1', '3', 'b7', 'b9', '#9', '#11', 'b13']),
        ("C7#9b9#11b13", ['1', '3', '5', 'b7', 'b9', '#9', '#11', 'b13']),

        # =============================
        # PURE EVIL FINAL BOSS
        # =============================
        ("C7sus4add3b9#9#11b13no5",
         ['1', '3', '4', 'b7', 'b9', '#9', '#11', 'b13']),
    ]

    for chord, expected in chord_interval_tests:
        print(get_chord_info(chord), chord)

    print('-----')

    correct = 0

    for chord, expected in chord_interval_tests:
        result = get_intervals(**get_chord_info(chord))
        print(chord, result, "OK" if result == expected else "FAIL", "expected:" if result != expected else "", expected if result != expected else "")
        if result == expected:
            correct += 1

    print(f"{correct}/{len(chord_interval_tests)} is right")

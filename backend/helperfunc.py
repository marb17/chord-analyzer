import re

GET_EQUIV_ACCIDENTAL = {
    "C#": "Db",
    "Db": "C#",

    "D#": "Eb",
    "Eb": "D#",

    "F#": "Gb",
    "Gb": "F#",

    "G#": "Ab",
    "Ab": "G#",

    "A#": "Bb",
    "Bb": "A#"
}

KEY_TO_NUMBER = {
    "C" : 1, "C#" : 2, "Db" : 2,
    "D" : 3, "D#" : 4, "Eb" : 4,
    "E" : 5,
    "F" : 6, "F#" : 7, "Gb" : 7,
    "G" : 8, "G#" : 9, "Ab" : 9,
    "A" : 10, "A#" : 11, "Bb" : 11,
    "B" : 12,
}

def get_chord_info(chord: str) -> tuple[str, str, list[str], str]:
    """
    :param chord: The input chord to be extracted
    :return: Base key, Quality, Alterations, Inversion
    """
    chord_data = re.findall(r'([CDEFGAB][#b]?)(7sus4|7sus|sus2|sus4|sus|m7b5|maj7|maj9|maj13|M7|m7|Δ7|m9|m|dim7|dim|aug|7|ø7|ø|9)?(?:(?:[b#]|(?:add)?)(?:2|3|5|6|7|9|11|13))*(?:\/([CDEFGAB][#b]?))?', chord)
    alterations = re.findall(r'(?:add|[#b])(?:2|3|5|6|7|9|11|13)', chord)

    return chord_data[0], chord_data[1], alterations, chord_data[2]

if __name__ == "__main__":
    get_chord_info("Gb7#9#11/Bb")
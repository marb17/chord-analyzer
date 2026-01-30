import helperfunc
import chord_database
import rtmidi

midiin = rtmidi.RtMidiIn()

def write_notes_to_set_from_midi(midi, notes: set[int]) -> list[int]:
    if midi.isNoteOn():
        notes.add(midi.getNoteNumber())
    elif midi.isNoteOff():
        try:
            notes.remove(midi.getNoteNumber())
        except KeyError:
            notes.clear()

def main(midi_port=0) -> None:
    notes = set()

    ports = range(midiin.getPortCount())
    if ports:
        for i in ports:
            print(midiin.getPortName(i))
        print('--------------')
        midiin.openPort(midi_port)
        while True:
            m = midiin.getMessage(10)  # some timeout in ms
            if m:
                write_notes_to_set_from_midi(m, notes)
                notes_list = sorted(notes)
                print(notes_list)
    else:
        print('NO MIDI INPUT PORTS!')

if __name__ == '__main__':
    main(midi_port=1)
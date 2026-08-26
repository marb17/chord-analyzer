from collections.abc import Generator
from pathlib import Path
import time
from typing import AsyncGenerator, Any

from backend.engine.core.chord_engine import ChordEngine
from backend.engine.utils.classes.dataclass import *

import asyncio

from mido import MidiFile
import mido
import tinysoundfont
import pyaudio

from backend.engine.utils.classes.dataclass import Chord


class Engine:
    def __init__(self, sound_file: Path = None):
        self.current_notes: list[int] = list()
        self.current_chord: list[Chord] = list()
        self.last_time: float = time.time()
        self.last_time_delta: float = 0.0
        self.chord_debounce_time: float = 0.005
        self.debounce_chord: list[Chord] = list()

        self._chord_analyzer: ChordEngine = ChordEngine()

        self.sound_file = sound_file

    async def note_input_receive(self, data: NoteInput):
        if data.state:
            self.current_notes.append(data.note)
        else:
            if data.note in self.current_notes:
                self.current_notes.remove(data.note)
            else:
                pass

        await self.get_current_chord()


    async def get_current_chord(self):
        self.current_chord = self._chord_analyzer.notes_to_chord(self.current_notes)


    async def read_midi_file(self, midi_file: Path, play_sound: bool = False) -> AsyncGenerator[list[Chord], None]:
        mid = MidiFile(str(midi_file))

        absolute_seconds = 0.0

        if play_sound and self.sound_file:
            fs = tinysoundfont.Synth()
            sfid = fs.sfload(str(self.sound_file))
            fs.program_select(0, sfid, 0, 0)
            fs.start()

        for msg in mid:
            absolute_seconds += msg.time

            if msg.type == 'note_on':
                if msg.velocity > 0:
                    await self.note_input_receive(NoteInput(msg.note, True))
                    if play_sound and self.sound_file:
                        fs.noteon(0, msg.note, msg.velocity)
                else:
                    await self.note_input_receive(NoteInput(msg.note, False))
                    if play_sound and self.sound_file:
                        fs.noteoff(0, msg.note)

            await asyncio.sleep(msg.time)
            yield self.current_chord



async def main():
    engine = Engine(sound_file=Path(r"/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/piano.sf2"))

    async for chords in engine.read_midi_file(Path("/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/Merry_Go_Round_of_Life_(Howl's_Moving_Castle).midi"), play_sound=True):
        # 'chords' will contain your list[Chord] yielded on every MIDI message
        print(f"{[chord.chord_name for chord in chords]} | {engine.current_notes}")
        # pass

    # await engine.note_input_receive(NoteInput(60, True))
    # await engine.note_input_receive(NoteInput(64, True))
    # await engine.note_input_receive(NoteInput(67, True))
    # print("C Major Chord Down:", engine.current_notes)
    # await asyncio.sleep(0.5)
    # print(engine.current_chord)
    #
    # # Release Chord
    # await engine.note_input_receive(NoteInput(60, False))
    # await engine.note_input_receive(NoteInput(64, False))
    # await engine.note_input_receive(NoteInput(67, False))
    # print("Chord Released:", engine.current_notes)
    # await asyncio.sleep(0.2)
    # print(engine.current_chord)
    #
    # # Quick Scale Run: C4 -> D4 -> E4 -> F4 -> G4
    # notes = [60, 62, 64, 65, 67]
    # for note in notes:
    #     await engine.note_input_receive(NoteInput(note, True))
    #     print(f"Note {note} Down:", engine.current_notes)
    #     await asyncio.sleep(0.1)
    #     await engine.note_input_receive(NoteInput(note, False))
    #     print(f"Note {note} Up:", engine.current_notes)
    #     print(engine.current_chord)

if __name__ == "__main__":
    asyncio.run(main())
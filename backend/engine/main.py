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
        self.current_notes: dict[int, NoteInput] = dict()
        self.current_chord: list[Chord] = list()
        self.is_sustained: bool = False

        self._chord_analyzer: ChordEngine = ChordEngine()

        self.sound_file = sound_file

    async def get_current_chord(self):
        self.current_chord = self._chord_analyzer.notes_to_chord([note.note for note in self.current_notes.values()])

    async def note_on(self, note: int):
        self.current_notes[note] = (NoteInput(note, released=False, is_sustained=self.is_sustained))

    async def note_off(self, note: int):
        self.current_notes[note].released = True

        await self._cleanup_notes()

    async def set_sustain(self, value):
        self.is_sustained = value

        for key in self.current_notes.keys():
            self.current_notes[key].is_sustained = value

        await self._cleanup_notes()

    async def _cleanup_notes(self):
        self.current_notes = {
            k: v for k, v in self.current_notes.items()
            if (not v.released) or v.is_sustained
        }

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
                    if play_sound and self.sound_file:
                        fs.noteon(0, msg.note, msg.velocity)

                    await self.note_on(msg.note)
                else:
                    if play_sound and self.sound_file:
                        fs.noteoff(0, msg.note)

                    await self.note_off(msg.note)
            elif msg.is_cc(64):
                if msg.value > 64:
                    await self.set_sustain(True)
                else:
                    await self.set_sustain(False)


            await asyncio.sleep(msg.time)
            await self.get_current_chord()
            yield self.current_chord




async def main():
    engine = Engine(sound_file=Path(r"/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/piano.sf2"))

    # async for chords in engine.read_midi_file(Path("/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/Happy_Birthday_Song_in_Jazz_｜Arr_By_Jonny_May.midi"), play_sound=True):
    async for chords in engine.read_midi_file(Path("/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/Merry_Go_Round_of_Life_(Howl's_Moving_Castle).midi"),
                                              play_sound=True):
        # 'chords' will contain your list[Chord] yielded on every MIDI message
        # print(f"{[chord.chord_name for chord in chords]} | {[note.note for note in engine.current_notes.values()]}")
        # print(engine.current_notes)
        pass

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
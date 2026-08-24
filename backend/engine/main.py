from collections.abc import Generator
from pathlib import Path
import time
from typing import AsyncGenerator

from backend.engine.core.chord_engine import ChordEngine
from backend.engine.utils.classes.dataclass import *

import asyncio

from mido import MidiFile
import mido

from backend.engine.utils.classes.dataclass import Chord


class Engine:
    def __init__(self):
        self.current_notes: list[int] = list()
        self.current_chord: list[Chord] = list()
        self.last_time: float = time.time()
        self.last_time_delta: float = 0.0

        self._chord_analyzer: ChordEngine = ChordEngine()

    async def note_input_receive(self, data: NoteInput):
        if data.state:
            self.current_notes.append(data.note)
        else:
            if data.note in self.current_notes:
                self.current_notes.remove(data.note)
            else:
                pass

        await self.get_current_chord()
        self.last_time_delta = time.time() - self.last_time_delta
        self.last_time = time.time()


    async def get_current_chord(self):
        self.current_chord = self._chord_analyzer.notes_to_chord(self.current_notes)

    async def read_midi_file(self, midi_file: Path) -> AsyncGenerator[list[Chord], None]:
        mid = MidiFile(str(midi_file))

        absolute_seconds = 0.0

        for msg in mid:
            absolute_seconds += msg.time

            if msg.type == 'note_on':
                if msg.velocity > 0:
                    await self.note_input_receive(NoteInput(msg.note, True))
                else:
                    await self.note_input_receive(NoteInput(msg.note, False))

            await asyncio.sleep(msg.time)
            yield self.current_chord


        # for i, track in enumerate(mid.tracks):
        #     print(f'Track {i}: {track.name}')
        #     for msg in track:
        #         if msg.type == 'note_on':
        #             if msg.velocity > 0:
        #                 await self.note_input_receive(NoteInput(msg.note, True))
        #             else:
        #                 await self.note_input_receive(NoteInput(msg.note, False))
        #
        #         await self.get_current_chord()
        #         try: print(self.current_chord[0].chord_name)
        #         except IndexError: pass

async def main():
    engine = Engine()

    async for chords in engine.read_midi_file(Path("/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/Merry_Go_Round_of_Life_(Howl's_Moving_Castle).midi")):
        # 'chords' will contain your list[Chord] yielded on every MIDI message
        print(f"Current detected chords: {chords}")

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
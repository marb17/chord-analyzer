from collections.abc import Generator
from pathlib import Path
import time
from typing import AsyncGenerator, Any

from backend.engine.core.chord_engine import ChordEngine
from backend.engine.utils.classes.dataclass import *

import asyncio

from mido import MidiFile
import mido
# import tinysoundfont
import fluidsynth
import pyaudio

from backend.engine.utils.classes.dataclass import Chord


class Engine:
    def __init__(self,
                 sound_file: Path = None,
                 max_notes: int = -1):
        self.current_notes: dict[int, NoteInput] = dict()
        self.current_chord: list[Chord] = list()
        self.is_sustained: bool = False
        self.currently_playing_notes: set[int] = set()

        self._chord_analyzer: ChordEngine = ChordEngine()
        self._sound_file = sound_file
        self._max_notes = max_notes

        self.fs = None

    async def get_current_chord(self):
        self.current_chord = self._chord_analyzer.notes_to_chord([note.note for note in self.current_notes.values()])

    async def note_on(self, note: int, velocity: int = 64):
        self.current_notes[note] = (NoteInput(note, velocity=velocity, released=False, is_sustained=self.is_sustained))

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

        self._sync_audio_player()

    def _sync_audio_player(self, force_play_notes: list[NoteInput] = None):
        print(self.currently_playing_notes)
        if force_play_notes:
            for note in force_play_notes:
                if note.note in self.currently_playing_notes:
                    self.fs.noteon(0, note.note, note.velocity)

        target_pitches = set(self.current_notes.keys())
        notes_to_start = target_pitches - self.currently_playing_notes

        for pitch in notes_to_start:
            note_data = self.current_notes[pitch]
            self.fs.noteon(0, pitch, note_data.velocity)
            self.currently_playing_notes.add(pitch)

        notes_to_stop = self.currently_playing_notes - target_pitches
        for pitch in list(notes_to_stop):
            self.fs.noteoff(0, pitch)
            self.currently_playing_notes.remove(pitch)

    async def read_midi_file(self, midi_file: Path, play_sound: bool = False) -> AsyncGenerator[list[Chord], None]:
        mid = list(MidiFile(str(midi_file)))
        absolute_seconds = 0.0

        if play_sound and self._sound_file:
            self.fs = fluidsynth.Synth()
            sfid = self.fs.sfload(str(self._sound_file))
            self.fs.program_select(0, sfid, 0, 0)
            self.fs.start()

        start_time = time.perf_counter()

        for msg in mid:
            state_changed = False

            absolute_seconds += msg.time

            target_time = start_time + absolute_seconds
            delay = target_time - time.perf_counter()

            if delay > 0.002:
                await asyncio.sleep(delay)
                pass

            if msg.type == 'note_on':
                if msg.velocity > 0:
                    await self.note_on(msg.note, msg.velocity)
                    self._sync_audio_player(force_play_notes=[NoteInput(msg.note, msg.velocity)])
                elif msg.velocity == 0:
                    await self.note_off(msg.note)
                    self._sync_audio_player()
                state_changed = True
            elif msg.type == 'note_off':
                print(msg.value)
                state_changed = True


            elif msg.is_cc(64):
                if msg.value > 64:
                    await self.set_sustain(True)
                else:
                    await self.set_sustain(False)
                state_changed = True
            elif msg.is_cc(121) or msg.is_cc(123):
                self.current_notes = dict()
                self.current_chord = list()
                self.is_sustained = False
                state_changed = True

            if state_changed:
                await self.get_current_chord()
                yield self.current_chord




async def main():
    engine = Engine(sound_file=Path(r"/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/piano.sf2"))

    # async for chords in engine.read_midi_file(Path("/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/Happy_Birthday_Song_in_Jazz_｜Arr_By_Jonny_May.midi"), play_sound=True):
    # async for chords in engine.read_midi_file(Path("/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/Merry_Go_Round_of_Life_(Howl's_Moving_Castle).midi"), play_sound=True):
    async for chords in engine.read_midi_file(Path("/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/Merry-Go-Round_of_Life_Howl's_Moving_Castle_Piano_Tutorial.midi"), play_sound=True):
    # async for chords in engine.read_midi_file(Path("/Users/marb/PycharmProjects/chord-analyzer/backend/engine/database/不可思議のカルテ《Fukashigi_no_Carte》.midi"), play_sound=True):
    #     print(f"{[chord.chord_name for chord in chords]} | {[note.note for note in engine.current_notes.values()]}")
        # print(engine.current_notes)
        # print(len(engine.current_notes))
        pass

if __name__ == "__main__":
    asyncio.run(main())
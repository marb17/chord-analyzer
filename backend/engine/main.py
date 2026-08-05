from backend.engine.core.chord_engine import ChordEngine
from backend.engine.utils.classes.dataclass import *

import asyncio


class Engine:
    def __init__(self):
        self.current_notes: list[int] = list()
        self.current_chord: list[Chord] = None

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

    async def get_current_chord(self):
        self.current_chord = self._chord_analyzer.notes_to_chord(self.current_notes)

async def main():
    engine = Engine()

    await engine.note_input_receive(NoteInput(60, True))
    await engine.note_input_receive(NoteInput(64, True))
    await engine.note_input_receive(NoteInput(67, True))
    print("C Major Chord Down:", engine.current_notes)
    await asyncio.sleep(0.5)
    print(engine.current_chord)

    # Release Chord
    await engine.note_input_receive(NoteInput(60, False))
    await engine.note_input_receive(NoteInput(64, False))
    await engine.note_input_receive(NoteInput(67, False))
    print("Chord Released:", engine.current_notes)
    await asyncio.sleep(0.2)
    print(engine.current_chord)

    # Quick Scale Run: C4 -> D4 -> E4 -> F4 -> G4
    notes = [60, 62, 64, 65, 67]
    for note in notes:
        await engine.note_input_receive(NoteInput(note, True))
        print(f"Note {note} Down:", engine.current_notes)
        await asyncio.sleep(0.1)
        await engine.note_input_receive(NoteInput(note, False))
        print(f"Note {note} Up:", engine.current_notes)
        print(engine.current_chord)

if __name__ == "__main__":
    asyncio.run(main())
from backend.engine.utils.classes.dataclass import *

import asyncio


class Engine:
    def __init__(self):
        self.current_notes: list[int] = list()

    async def note_input_receive(self, data: NoteInput):
        if data.state:
            self.current_notes.append(data.note)
        else:
            if data.note in self.current_notes:
                self.current_notes.remove(data.note)
            else:
                pass

    async def get_current_chord(self) -> :


async def main():
    engine = Engine()

    print(engine.current_notes)
    await engine.note_input_receive(NoteInput(10, True))
    print(engine.current_notes)

if __name__ == "__main__":
    asyncio.run(main())
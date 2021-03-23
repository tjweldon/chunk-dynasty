import json
from persistence.migrations import init_db
from persistence import db
from persistence import chunk_repository
from chunk_dynasty.core.chunk import Chunk

data = {420: "blaze it", "big beats": "bigger vibes", "demands": ["Free", "Bob", "Marley"]}


def run():
    chunk = Chunk(json.dumps(data).encode(), b"0000", b"0001", b"alphabet-spaghet")
    chunk_repository.save(chunk)

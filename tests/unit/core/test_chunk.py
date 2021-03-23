import json
import unittest

from chunk_dynasty.core.chunk import get_salter, Chunk
from tests.unit.core.fixtures.chunk_factory import ChunkFactory


class ChunkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = b'skateboards'
        self.parent_header = b'birds'
        self.salt = b'rollers'

    def get_serialized_chunk(self) -> str:
        salter = get_salter(data=self.data, parent_header=self.parent_header)
        new_header: bytes = salter(self.salt)
        serialized_chunk = json.dumps({
            'data': self.data.decode(),
            'parent_header': self.parent_header.decode(),
            'header': new_header.decode(),
            'salt': self.salt.decode()
        })
        return serialized_chunk

    def validate_json(self, serialized_chunk) -> bool:
        is_json = False
        try:
            json.loads(serialized_chunk)
            is_json = True
        except Exception:
            pass
        return is_json

    def test_create_chunk(self):
        chunk = ChunkFactory.get_valid_chunk(self.data, self.parent_header, self.salt)

        self.assertTrue(
            chunk.verify(),
            "Chunk.verify() returned false for a valid chunk"
        )

    def test_invalid_chunk(self):
        new_header = b'wrong'
        chunk = Chunk(self.data, self.parent_header, new_header, self.salt)

        self.assertFalse(
            chunk.verify(),
            "Chunk.verify() returned true for an invalid chunk"
        )

    def test_serialization_to_json(self):
        chunk = ChunkFactory.get_valid_chunk(self.data, self.parent_header, self.salt)
        serialized_chunk = chunk.serialize()

        is_valid = self.validate_json(serialized_chunk)

        self.assertTrue(
            is_valid,
            "json.loads raised an exception while parsing the serialized chunk."
        )

    def test_deserialization_from_json(self):
        serialized_chunk = self.get_serialized_chunk()

        chunk = None
        error = ''
        try:
            chunk = Chunk.deserialize(serialized_chunk)
        except Exception as error:
            pass

        self.assertIsNotNone(
            chunk,
            "An exception was thrown during deserialization. The message was {}"
                .format(str(error))
        )

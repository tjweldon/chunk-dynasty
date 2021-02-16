import unittest

from chunk_dynasty.core.chunk import get_salter, Chunk


class ChunkTest(unittest.TestCase):
    def test_create_chunk(self):
        data = b'skateboards'
        parent_header = b'birds'
        salter = get_salter(data=data, parent_header=parent_header)
        salt = b'rollers'
        new_header = salter(salt)
        chunk = Chunk(data, parent_header, new_header, salt)

        self.assertTrue(chunk.verify())

    def test_invalid_chunk(self):
        data = b'not skateboard'
        parent_header = b'not birds'
        salt = b'not rollers'
        new_header = b'wrong'
        chunk = Chunk(data, parent_header, new_header, salt)

        self.assertFalse(chunk.verify())

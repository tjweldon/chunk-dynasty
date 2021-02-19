import unittest

from chunk_dynasty.core.dynasty import Dynasty
from tests.unit.core.fixtures.chunk_factory import ChunkFactory


class DynastyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.first_chunk = ChunkFactory.get_valid_chunk(
            b'skateboards',
            b'birds',
            b'rollers',
        )

    def test_valid_dynasty(self):
        chunk_list = ChunkFactory.get_successors(self.first_chunk, 8)
        dynasty = Dynasty(chunk_list)

        self.assertTrue(
            dynasty.validate(),
            "Dynasty.validate() returned false for a valid dynasty"
        )

    def test_invalid_dynasty(self):
        chunk_list = [self.first_chunk] * 8
        dynasty = Dynasty(chunk_list)

        self.assertFalse(
            dynasty.validate(),
            "Dynasty.validate() returned false for a invalid Dynasty"
        )

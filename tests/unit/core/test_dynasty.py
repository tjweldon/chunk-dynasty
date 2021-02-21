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

        self.assertIs(
            False,
            dynasty.validate(),
            "Dynasty.validate() returned false for a invalid Dynasty"
        )

    def test_get_tail(self):
        chunk_list = ChunkFactory.get_successors(self.first_chunk, 8)
        dynasty = Dynasty(chunk_list)

        expected_tail_length = 2
        tail = dynasty.get_tail(expected_tail_length)
        expected_ultimate_successor = chunk_list[-1]
        actual_ultimate_successor = tail.get_chunk_list()[-1]

        self.assertEqual(expected_ultimate_successor, actual_ultimate_successor)
        self.assertEqual(expected_tail_length, len(tail.get_chunk_list()))

    def test_append(self):
        chunk_list = ChunkFactory.get_successors(self.first_chunk, 8)
        dynasty = Dynasty(chunk_list[:-1])

        dynasty = dynasty.append(chunk_list[-1])
        expected_ultimate_successor = chunk_list[-1]
        actual_ultimate_successor = dynasty.get_chunk_list()[-1]

        self.assertEqual(expected_ultimate_successor, actual_ultimate_successor)

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
        print(len(chunk_list))

        expected_tail_length = 2
        tail = dynasty.get_tail(expected_tail_length)
        expected_ultimate_successor = chunk_list[-1]
        actual_ultimate_successor = tail.get_chunk_list()[-1]

        self.assertEqual(expected_ultimate_successor.header, actual_ultimate_successor.header)
        self.assertEqual(expected_tail_length, len(tail.get_chunk_list()))

    def test_invalid_tail_length(self):
        length = 8
        chunk_list = ChunkFactory.get_successors(self.first_chunk, length - 1)
        dynasty = Dynasty(chunk_list)

        self.assertRaises(ValueError, dynasty.get_tail, length + 5,)

    def test_append(self):
        chunk_list = ChunkFactory.get_successors(self.first_chunk, 8)
        dynasty = Dynasty(chunk_list[:-1])

        dynasty = dynasty.append(chunk_list[-1])
        expected_ultimate_successor = chunk_list[-1]
        actual_ultimate_successor = dynasty.get_chunk_list()[-1]

        self.assertEqual(expected_ultimate_successor, actual_ultimate_successor)

    def test_intersection_exists(self):
        chunk_list = ChunkFactory.get_successors(self.first_chunk, 8)
        intersecting_chunk_list = chunk_list[5:-1] + ChunkFactory.get_successors(chunk_list[-1], 3)
        dynasty = Dynasty(chunk_list)
        intersecting_dynasty = Dynasty(intersecting_chunk_list)

        intersection = dynasty.intersection(intersecting_dynasty)

        self.assertListEqual(dynasty.get_chunk_list()[5:], intersection.get_chunk_list())

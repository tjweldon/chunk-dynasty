from __future__ import annotations
from typing import List, Optional

from chunk_dynasty.core.chunk import Chunk


class Dynasty:
    _chunks: List[Chunk]

    @classmethod
    def deserialize(cls, dynasty_json: str) -> Dynasty:
        pass

    def __init__(self, chunks: Optional[List[Chunk]] = None):
        if chunks is None:
            chunks = []
        self._chunks = chunks

    def validate(self) -> bool:
        """
        This validates the entire chain, each chunk must be valid and
        the order of chunks must be preserved.
        :return:
        """
        all_chunks_valid = all(chunk.verify() for chunk in self._chunks)
        succession_is_valid = self._succession_is_valid()
        dynasty_is_valid = all_chunks_valid and succession_is_valid

        return dynasty_is_valid

    def _succession_is_valid(self):
        ordering_is_valid = True
        for i in range(0, len(self._chunks) - 1):
            current_succession_verified = self._chunks[i].header == self._chunks[i + 1].parent_header
            ordering_is_valid = ordering_is_valid and current_succession_verified
        return ordering_is_valid

    def get_chunk_list(self):
        return self._chunks

    def get_tail(self, length: int) -> Dynasty:
        """
        Returns the sub-dynasty whose ultimate successor is the same as this dynasty's
        and whose length is the length provided.
        :param length:
        :return:
        """
        if length > len(self._chunks):
            msg = "Provide a length less than or equal to the total dynasty length, total dynasty length was {}, tail length requested was {}"
            raise ValueError(msg.format(len(self._chunks), length))
        chunk_subset = self._chunks[-length:]
        return Dynasty(chunk_subset)

    def append(self, chunk: Chunk) -> Dynasty:
        """
        Fluently appends a chunk to the dynasty
        :param chunk:
        :return:
        """
        self._chunks.append(chunk)

        return self

    def serialize(self) -> str:
        pass

    def intersection(self, other: Dynasty) -> Optional[Dynasty]:
        """
        This function returns the intersection of two dynasties if it exists.
        if it doesn't exist it returns None
        :param other:
        :return:
        """
        if not other.validate():
            raise ValueError("The dynasty passed was not valid")

        other_header_list = [chunk.header for chunk in other.get_chunk_list()]
        this_header_list = [chunk.header for chunk in self._chunks]

        this_dynasty_is_older = other_header_list[0] in this_header_list[1:]
        other_dynasty_older = this_header_list[0] in other_header_list[1:]
        simultaneous_start = this_header_list[0] == other_header_list[0]

        case = (this_dynasty_is_older, other_dynasty_older, simultaneous_start)
        no_intersection = (False, False, False)

        if case == no_intersection:
            return None

        if this_dynasty_is_older:
            other_header_list = self._pad_other_list(other_header_list, this_header_list)
            # EXAMPLE
            # this_header_list = [h1, h2, h3, h4]
            # other header_list = [b'', b'', b'', h4, h5, h6]

        if other_dynasty_older:
            other_header_list = self._truncate_other_list(other_header_list, this_header_list)
            # EXAMPLE
            # this_header_list = [h4, h5, h6, h7]
            # other header_list = [h4, h5, h6]

        intersection_indices = []
        for index, header in enumerate(this_header_list):
            if index not in range(0, len(other_header_list)):
                break
            if header == other_header_list[index]:
                intersection_indices.append(index)

        chunk_list = [self._chunks[i] for i in intersection_indices]

        return Dynasty(chunk_list)

    def _truncate_other_list(self, other_header_list, this_header_list):
        # Here we truncate the beginning of the other header list
        # to give it the same indexing as this_header_list
        offset = other_header_list.index(this_header_list[0])
        other_header_list = other_header_list[offset:]
        return other_header_list

    def _pad_other_list(self, other_header_list, this_header_list):
        # Here we pad the beginning of the other header list with trivial
        # hashes to give it the same indexing as this_header_list
        offset = this_header_list.index(other_header_list[0])
        other_header_list = [b''] * offset + other_header_list
        return other_header_list

    def __eq__(self, other):
        pass

    def __len__(self) -> int:
        pass

    def _truncate_to_match_start(self, other_header_list, this_header_list):
        offset = other_header_list.index(this_header_list[0])
        return other_header_list[offset:]

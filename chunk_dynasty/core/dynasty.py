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
        pass

    def append(self, chunk: Chunk) -> Dynasty:
        """
        Fluently appends a chunk to the dynasty
        :param chunk:
        :return:
        """
        pass

    def serialize(self) -> str:
        pass

    def head_index(self, other: Dynasty) -> Optional[int]:
        """
        This function gives relative index of the the head of the other dynasty with respect
        to the dynasty instance on which it is invoked.
        :param other:
        :return:
        """
        pass

    def __eq__(self, other):
        pass

    def __len__(self) -> int:
        pass

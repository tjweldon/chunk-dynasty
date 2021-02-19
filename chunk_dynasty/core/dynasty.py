from __future__ import annotations
from chunk import Chunk
from typing import List, Optional


class Dynasty:

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
        pass

    def get_tail(self, length: int) -> Dynasty:
        """
        Returns a Dynasty of the length provided
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

from typing import List

from chunk_dynasty.core.chunk import get_salter, Chunk


class ChunkFactory:

    @staticmethod
    def get_valid_chunk(data: bytes, parent_header: bytes, salt: bytes) -> Chunk:
        salter = get_salter(data=data, parent_header=parent_header)
        new_header = salter(salt)
        chunk = Chunk(data, parent_header, new_header, salt)
        return chunk

    @classmethod
    def get_successors(cls, chunk: Chunk, number_of_successors: int) -> List[Chunk]:
        dynasty = [chunk]
        for i in range(0, number_of_successors):
            dynasty.append(cls.get_successor(dynasty[i], i))

        return dynasty

    @classmethod
    def get_successor(cls, chunk: Chunk, data: int) -> Chunk:
        salt = b'oof'
        return cls.get_valid_chunk(bytes(data), chunk.header, salt)

#!/usr/bin/env python

from typing import Callable
from Cryptodome.Hash import SHA256


def get_salter(data: bytes, parent_header: bytes) -> Callable:
    unsalted = data + parent_header
    return lambda salt: SHA256.new(data=unsalted + salt).hexdigest().encode()


class Chunk:
    def __init__(
            self, data: bytes, parent_header: bytes, header: bytes, salt: bytes
    ) -> None:
        self._data = data
        self._parent_header = parent_header
        self._header = header
        self._salt = salt

    def __str__(self) -> str:
        return str(bytes(self))

    def __bytes__(self) -> bytes:
        return self._data + self._parent_header + self._salt

    @property
    def data(self) -> bytes:
        return self._data

    @property
    def header(self) -> bytes:
        return self._header

    @property
    def parent_header(self) -> bytes:
        return self._parent_header

    @property
    def salt(self) -> bytes:
        return self._salt

    def verify(self):
        return hash_chunk(self) == self._header


def hash_chunk(chunk: Chunk) -> bytes:
    chunk_hash = SHA256.new(data=bytes(chunk)).hexdigest()
    return chunk_hash.encode()

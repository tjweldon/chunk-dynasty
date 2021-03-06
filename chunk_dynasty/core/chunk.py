#!/usr/bin/env python
from __future__ import annotations

import json
from typing import Callable
from Cryptodome.Hash import SHA256


def get_salter(data: bytes, parent_header: bytes) -> Callable:
    unsalted = data + parent_header
    return lambda salt: SHA256.new(data=unsalted + salt).hexdigest().encode()


class Chunk:

    @classmethod
    def deserialize(cls, json_chunk: str) -> Chunk:
        chunk_dict = json.loads(json_chunk)
        return cls(**chunk_dict)

    def __init__(
            self, data: bytes, parent_header: bytes, header: bytes, salt: bytes
    ) -> None:
        self._data = data if type(data) == bytes else data.encode()
        self._parent_header = parent_header if type(parent_header) == bytes else parent_header.encode()
        self._header = header if type(header) == bytes else header.encode()
        self._salt = salt if type(salt) == bytes else salt.encode()

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

    def serialize(self) -> str:
        return json.dumps(self.get_dict())

    def get_dict(self) -> dict:
        return {
            'data': self._data.decode(),
            'parent_header': self._parent_header.decode(),
            'header': self._header.decode(),
            'salt': self._salt.decode(),
        }

def hash_chunk(chunk: Chunk) -> bytes:
    chunk_hash = SHA256.new(data=bytes(chunk)).hexdigest()
    return chunk_hash.encode()

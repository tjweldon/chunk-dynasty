import json
from typing import List

from Cryptodome.PublicKey import RSA

from chunk_dynasty.core.transaction import Transaction
from persistence import chunk_repository
from chunk_dynasty.core.chunk import Chunk, get_salter

my_key = RSA.generate(1024)


def serialize_transactions(transactions: List[Transaction]) -> bytes:
    serialized_transactions = ", ".join(map(str, transactions))

    return serialized_transactions.encode()


def satisfies_constraint(new_hash: bytes):
    return new_hash.decode().startswith('0')


def run(iterations: int) -> None:
    transactions = [
        Transaction(0.69, sender=None, recipient=my_key.publickey().export_key())
    ]
    data = serialize_transactions(transactions)
    parent_header = b"0" * 64
    salter = get_salter(data=data, parent_header=parent_header)
    spaghet = b"alphabet-spaghet"
    new_hash = None
    salt = spaghet
    for i in range(iterations):
        if new_hash is None:
            new_hash = salter(spaghet)
        else:
            salt = new_hash
            new_hash = salter(new_hash)

        if satisfies_constraint(new_hash):
            chunk = Chunk(data, parent_header, new_hash, salt)
            chunk_repository.save(chunk)
            parent_header = chunk.header






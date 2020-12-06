from __future__ import annotations

import json
import time
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome import Signature

def _sign(sk: bytes, message: bytes) -> bytes:
    key = RSA.import_key(sk)
    signer = Signature.pkcs1_15.new(key)
    hash_object = SHA256.new(data = message)
    return signer.sign(hash_object)

def _verify(pk: bytes, message: bytes, signature: bytes) -> None:
    key = RSA.import_key(pk)
    verifier = Signature.pkcs1_15.new(key)
    hash_object = SHA256.new(data = message)
    verifier.verify(hash_object, signature)


class Transaction:
    def __init__(self, amount: float, sender: bytes, recipient: bytes):
        self._timestamp = time.time()
        self._amount = amount
        self._recipient = recipient
        self._sender = sender

    def __str__(self) -> str:
        dict_transaction = {
            'timestamp': self._timestamp,
            'amount': self._amount,
            'sender': self._sender,
            'recipient': self._recipient
        }

        return json.dumps(dict_transaction)

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def recipient(self) -> bytes:
        return self._recipient

    @property
    def sender(self) -> bytes:
        return self._sender

    def sign(self, sk: bytes) -> SignedTransaction:
        return SignedTransaction(self, sk)


class SignedTransaction(Transaction):
    def __init__(self, transaction: Transaction, sk: bytes):
        super().__init__(transaction.amount, transaction.sender, transaction.recipient)
        self._signature = _sign(sk, str(transaction).encode())

    @property
    def signature(self) -> bytes:
        return self._signature

    def verify(self, pk: bytes) -> None:
        _verify(pk, str(self).encode(), self.signature)








from __future__ import annotations

import json
import time
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pss


def _sign(key: RSA.RsaKey, message: bytes) -> bytes:
    signer = pss.new(key)
    hash_object = SHA256.new(data=message)
    return signer.sign(hash_object)


def _verify(pk: bytes, message: bytes, signature: bytes) -> None:
    key = RSA.import_key(pk)
    verifier = pss.new(key)
    hash_object = SHA256.new(data=message)
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
            'sender': self._sender.decode(),
            'recipient': self._recipient.decode()
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

    @property
    def timestamp(self) -> float:
        return self._timestamp

    def sign(self, signature: bytes) -> SignedTransaction:
        return SignedTransaction(self, signature)


class SignedTransaction:
    def __init__(self, transaction: Transaction, signature: bytes):
        self._transaction = transaction
        self._signature = signature

    def __str__(self):
        return str(self._transaction)

    @property
    def signature(self) -> bytes:
        return self._signature

    @property
    def transaction(self) -> Transaction:
        return self._transaction

    def verify(self) -> bool:
        verified = False
        try:
            _verify(self._transaction.sender, str(self).encode(), self.signature)
            verified = True
        except ValueError as e:
            pass

        return verified


def get_transaction_signature(transaction: Transaction, key: RSA.RsaKey) -> bytes:
    return _sign(key, str(transaction).encode())

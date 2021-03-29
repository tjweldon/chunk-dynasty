from __future__ import annotations

import json
import time
from typing import Optional

from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pss


def _sign(key: RSA.RsaKey, message: bytes) -> bytes:
    """
    This is an internal module function that returns
    a PSS signature, given a key and a message.
    :param RSA.RsaKey key:
    :param bytes message:
    :rtype: bytes
    """
    signer = pss.new(key)
    hash_object = SHA256.new(data=message)
    return signer.sign(hash_object)


def _verify(pk: bytes, message: bytes, signature: bytes) -> None:
    """
    This is a module internal function that verifies a
    PSS signed message against a public key. This function
    raises an error if the verification fails. None returned
    on success.
    :param bytes pk:
    :param bytes message:
    :param signature:
    """
    key = RSA.import_key(pk)
    verifier = pss.new(key)
    hash_object = SHA256.new(data=message)
    verifier.verify(hash_object, signature)


class Transaction:
    def __init__(self, amount: float, sender: Optional[bytes], recipient: bytes):
        self._timestamp = time.time()
        self._amount = amount
        self._recipient = recipient
        self._sender = sender

    def __str__(self) -> str:
        dict_transaction = {
            'timestamp': self._timestamp,
            'amount': self._amount,
            'sender': self._sender.decode() if self._sender else None,
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
    """
    This is the public interface for signature creation, and should be used
    in order to ensure that transactions are correctly signed.
    :param transaction:
    :param key:
    :rtype bytes:
    """
    return _sign(key, str(transaction).encode())

import unittest

from Cryptodome.PublicKey import RSA
from chunk_dynasty.core.transaction import Transaction, SignedTransaction, get_transaction_signature


class TransactionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sender_key = RSA.generate(1024)
        self.recipient_key = RSA.generate(1024)

    def test_get_signature(self):
        transaction = self.get_transaction()

        signature = get_transaction_signature(transaction, self.sender_key)

        self.assertIsInstance(signature, bytes)

    def get_transaction(self):
        return Transaction(
            0.69,
            self.sender_key.publickey().export_key(),
            self.recipient_key.publickey().export_key()
        )

    def test_construct_signed_transaction(self):
        transaction = self.get_transaction()
        signature = get_transaction_signature(transaction, self.sender_key)
        signed_transaction = transaction.sign(signature)

        self.assertTrue(signed_transaction.verify())

    def test_invalid_signature(self):
        transaction = self.get_transaction()
        signature = b'some invalid signature'
        signed_transaction = transaction.sign(signature)

        self.assertFalse(signed_transaction.verify())

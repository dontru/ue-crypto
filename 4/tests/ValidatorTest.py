import unittest

from crypto.Asymmetric import Asymmetric
from crypto.CryptoError import CryptoError
from crypto.Symmetric import Symmetric
from crypto.Validator import Validator


class ValidatorTest(unittest.TestCase):

    def test_symmetric_key(self):
        key = Symmetric.generate_key()
        try:
            Validator.symmetric_key(key)
        except CryptoError:
            self.fail()

        with self.assertRaises(CryptoError):
            Validator.symmetric_key('aaaa')

        with self.assertRaises(CryptoError):
            Validator.symmetric_key('asdf')

    def test_asymmetric_test(self):
        private_key, public_key = Asymmetric.generate_key()
        try:
            Validator.asymmetric_key(private_key=private_key, public_key=public_key)
        except CryptoError:
            self.fail()

        with self.assertRaises(CryptoError):
            Validator.asymmetric_key('aaaa', 'aaaa')

        with self.assertRaises(CryptoError):
            Validator.asymmetric_key('asdf', 'asdf')


if __name__ == '__main__':
    unittest.main()

import unittest

from cipher import validate_text, validate_rot, prepare, shift, encrypt, decrypt


class MyTestCase(unittest.TestCase):
    def test_validate_text(self):
        self.assertTrue(validate_text('asdf'))
        self.assertFalse(validate_text(''))
        self.assertFalse(validate_text('ąśdf'))

    def test_validate_rot(self):
        self.assertTrue(validate_rot(10))
        self.assertFalse(validate_rot(3.14))
        self.assertFalse(validate_rot(-10))

    def test_prepare(self):
        self.assertEqual(prepare('asdf'), 'asdf')
        self.assertEqual(prepare('As df'), 'asdf')

    def test_shift(self):
        self.assertEqual(shift('abcyz', 1), 'bcdza')
        self.assertEqual(shift('asdf', 13), 'nfqs')

    def test_encrypt(self):
        self.assertEqual(encrypt('Hello World'), 'uryybjbeyq')
        self.assertEqual(encrypt('Hello World', 16), 'xubbemehbt')

    def test_decrypt(self):
        self.assertEqual(decrypt('uryybjbeyq'), 'helloworld')
        self.assertEqual(decrypt('xubbemehbt', 16), 'helloworld')


if __name__ == '__main__':
    unittest.main()

import re
import string


ASCII_PATTERN = re.compile('^[\x00-\x7F]*$')
ALPHABET = string.ascii_lowercase
ALPHABET_LENGTH = len(string.ascii_lowercase)


def validate_text(text: str) -> bool:
    '''Check if the text contains only ASCII characters'''
    flag = True

    if len(text) == 0:
        flag = False
        print('empty text')

    if not ASCII_PATTERN.match(text):
        flag = False
        print('non-ASCII character(s)')

    return flag


def validate_rot(rot: int) -> bool:
    '''Check if the rot is integer between 0 and len(alphabet)'''
    flag = True

    if not isinstance(rot, int):
        print('rot is not integer value')
        flag = False

    if not (0 <= rot < ALPHABET_LENGTH):
        print('rot is not between 0 and len(alphabet)')
        flag = False

    return flag


def prepare(text: str) -> str:
    '''Lowercase + delete all characters except the English alphabet'''
    lower_text = text.lower()
    return ''.join([c for c in lower_text if c in ALPHABET])


def shift(text: str, rot: int) -> str:
    '''Caesar cipher shift'''
    return ''.join([ALPHABET[(ALPHABET.index(c) + rot) % ALPHABET_LENGTH] for c in text])


def encrypt(text: str, rot: int = 13) -> str:
    '''Encrypt the text with Caesar cipher'''
    encrypted = ''

    if validate_text(text) and validate_rot(rot):
        prepared = prepare(text)
        encrypted = shift(prepared, rot)

    return encrypted


def decrypt(text: str, rot: int = 13) -> str:
    '''Decrypt the text with Caesar cipher'''
    return encrypt(text, ALPHABET_LENGTH - rot)

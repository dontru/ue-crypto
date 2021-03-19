from .cipher import ALPHABET_LENGTH, decrypt


def display(text: str) -> str:
    '''If the text is longer than 24 characters, add ...'''
    return text if len(text) <= 24 else text[:24] + '...'


def break_code(text: str) -> None:
    '''Manual Caesar cipher breaker '''

    print(f'Manual decryption of the text: {display(text)}')
    for rot in range(1, ALPHABET_LENGTH):
        encrypted = decrypt(text, rot)
        print(f'rot={rot:2} {display(encrypted)}')

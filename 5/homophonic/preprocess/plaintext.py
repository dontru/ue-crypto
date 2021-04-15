import string


def plaintext(text: str) -> str:
    return ''.join(c for c in text.lower() if c in string.ascii_lowercase)

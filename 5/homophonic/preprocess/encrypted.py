def encrypted(text: str) -> str:
    return ''.join(c for c in text.strip() if c != '\n')

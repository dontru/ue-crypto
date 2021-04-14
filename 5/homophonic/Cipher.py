from typing import Dict, List, Tuple


class Cipher:
    WIDTH = 8
    HEIGHT = 8

    def __init__(
            self,
            substitution: Dict[str, List[str]],
            col_transpositions: List[Tuple[int, int]],
            row_transpositions: List[Tuple[int, int]],
    ):
        pass

    def encrypt(self, plaintext: str) -> str:
        pass

    def decrypt(self, encrypted: str) -> str:
        pass

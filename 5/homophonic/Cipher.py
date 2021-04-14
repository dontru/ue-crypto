from typing import Dict, List, Optional, Tuple


class Cipher:
    WIDTH = 8
    HEIGHT = 8

    def __init__(
            self,
            substitution: Dict[str, List[str]],
            col_transpositions: Optional[List[Tuple[int, int]]] = None,
            row_transpositions: Optional[List[Tuple[int, int]]] = None,
    ):
        self.substitution = substitution
        self.col_transpositions = [] if col_transpositions is None else col_transpositions
        self.row_transpositions = [] if row_transpositions is None else row_transpositions

    def encrypt(self, plaintext: str) -> str:
        pass

    def decrypt(self, encrypted: str) -> str:
        pass

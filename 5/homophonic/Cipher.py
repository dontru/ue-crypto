import random
from typing import Dict, List, Optional, Tuple

from . import preprocess
from .Grids import Grids


class Cipher:
    def __init__(
            self,
            substitution: Dict[str, List[str]],
            num_cols: int = 8,
            num_rows: int = 8,
            col_transpositions: Optional[List[Tuple[int, int]]] = None,
            row_transpositions: Optional[List[Tuple[int, int]]] = None,
    ):
        self.substitution = substitution
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.col_transpositions = [] if col_transpositions is None else col_transpositions
        self.row_transpositions = [] if row_transpositions is None else row_transpositions

    def encrypt(self, plaintext: str) -> str:
        plaintext = preprocess.plaintext(plaintext)
        substituted = ''.join([self.substitute(c) for c in plaintext])
        grids = Grids(text=substituted, num_cols=self.num_cols, num_rows=self.num_rows)
        grids.transpose(col_transpositions=self.col_transpositions, row_transpositions=self.row_transpositions)
        return str(grids)

    def substitute(self, character: str) -> str:
        return random.choice(self.substitution[character]) if character in self.substitution else character

    def decrypt(self, encrypted: str) -> str:
        encrypted = preprocess.encrypted(encrypted)
        unsubstituted = ''.join([self.unsubstitute(c) for c in encrypted])
        grids = Grids(text=unsubstituted, num_cols=self.num_cols, num_rows=self.num_rows)
        grids.transpose(col_transpositions=self.col_transpositions, row_transpositions=self.row_transpositions)
        return str(grids)

    def unsubstitute(self, character: str) -> str:
        for k, v in self.substitution.items():
            if character in v:
                return k
        else:
            return character

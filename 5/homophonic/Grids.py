from typing import List, Tuple


class Grids:
    def __init__(self, text: str, num_cols: int, num_rows: int):
        self.num_cols = num_cols
        self.num_rows = num_rows

        rows = [text[i:i + num_cols] for i in range(0, len(text), num_cols)]
        rows[-1] = rows[-1].ljust(num_cols)
        grids = [rows[i:i + num_rows] for i in range(0, len(rows), num_rows)]
        grids[-1].extend([' ' * 8] * (num_rows - len(grids[-1])))
        self.grids = grids

    def transpose(self, col_transpositions: List[Tuple[int, int]], row_transpositions: List[Tuple[int, int]]):
        for i, grid in enumerate(self.grids):
            for pos_a, pos_b in row_transpositions:
                self.grids[i][pos_a], self.grids[i][pos_b] = self.grids[i][pos_b], self.grids[i][pos_a]

            for j, row in enumerate(self.grids[i]):
                for pos_a, pos_b in col_transpositions:
                    pos_a, pos_b = min(pos_a, pos_b), max(pos_a, pos_b)
                    start = self.grids[i][j][:pos_a]
                    a = self.grids[i][j][pos_a]
                    mid = self.grids[i][j][pos_a+1:pos_b]
                    b = self.grids[i][j][pos_b]
                    end = self.grids[i][j][pos_b+1:]
                    self.grids[i][j] = start + b + mid + a + end

    def __str__(self):
        return '\n'.join([row for grid in self.grids for row in grid]).strip()

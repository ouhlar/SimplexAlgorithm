from typing import Optional, Tuple

from matrix import Matrix
from rational_number import RationalNumber
from vector import Vector


class SimplexMethod:
    def __init__(self, a_matrix: Matrix, b_vector: Vector, c_vector: Vector) -> None:
        self.a = a_matrix
        self.b = b_vector
        self.c = c_vector

    def run_simplex_method(self) -> Tuple[Vector, RationalNumber]:
        simplex_table: Matrix = self.to_simplex_table()
        pivot_c_idx: Optional[int] = self.pivot_col_index(simplex_table[-1])
        pivot_r_idx: Optional[int] = self.pivot_row_index(simplex_table, pivot_c_idx)
        while pivot_c_idx is not None and pivot_r_idx is not None:
            simplex_table = self.pivot_gauss_jordan(simplex_table, pivot_r_idx, pivot_c_idx)
            pivot_c_idx = self.pivot_col_index(simplex_table[-1])
            if pivot_c_idx is None:
                break
            pivot_r_idx = self.pivot_row_index(simplex_table, pivot_c_idx)
        return self.get_result(simplex_table), simplex_table[-1][-1]

    def to_simplex_table(self) -> Matrix:
        """
            # # # # # # #
            #       #   #
            #   a   # b #
            #       #   #
            # # # # # # #
            #   c   # 0 #
            # # # # # # #
        """
        simplex_table: Matrix = self.a
        simplex_table.add_col(self.b)
        simplex_table.add_row(self.c + RationalNumber(0))
        return simplex_table

    @staticmethod
    def pivot_col_index(c_vector: Vector) -> Optional[int]:
        pivot: RationalNumber = min(c_vector[:-1])  # without result
        if pivot < RationalNumber(0):
            c_vector_len = len(c_vector) - 1
            for idx in range(c_vector_len):
                if c_vector[idx] == pivot:
                    return idx

    @staticmethod
    def pivot_row_index(simplex_table: Matrix, pivot_c_index: int) -> int:
        min_ratio: RationalNumber = RationalNumber(0, 1)
        min_ratio_idx: Optional[int] = None
        simplex_table_len: int = len(simplex_table) - 1  # without last row (z row)
        for idx in range(simplex_table_len):
            row_pivot: RationalNumber = simplex_table[idx][pivot_c_index]
            if row_pivot > 0:
                ratio = simplex_table[idx][-1] / row_pivot
                if min_ratio == 0:
                    min_ratio = ratio
                    min_ratio_idx = idx
                elif ratio < min_ratio:
                    min_ratio = ratio
                    min_ratio_idx = idx
        return min_ratio_idx

    @staticmethod
    def pivot_gauss_jordan(simplex_table: Matrix, pivot_r_idx: int, pivot_c_idx: int) -> Matrix:
        result_matrix: Matrix = Matrix(*simplex_table)
        pivot: RationalNumber = simplex_table[pivot_r_idx][pivot_c_idx]
        result_matrix[pivot_r_idx] = simplex_table[pivot_r_idx] / pivot
        simplex_table_len: int = len(simplex_table)
        for idx in range(simplex_table_len):
            if idx != pivot_r_idx:
                ratio: RationalNumber = simplex_table[idx][pivot_c_idx]
                if ratio != 0:
                    result_matrix[idx] = result_matrix[idx] - result_matrix[pivot_r_idx] * ratio
        return result_matrix

    def get_result(self, simplex_table: Matrix):
        result: Vector = Vector(*(0 for _ in range(simplex_table.m_dimension()[1] - 1)))
        simplex_table_cols: int = simplex_table.m_dimension()[1] - 1  # without last col (b col)
        for idx in range(simplex_table_cols):
            idx_base: Optional[int] = self.is_base(simplex_table.get_col(idx))
            if idx_base is not None:
                result[idx] = simplex_table[idx_base][-1]
        return result

    @staticmethod
    def is_base(col: Vector):
        if sum(col) == 1 and (x in (0, 1) for x in col):
            return [idx for idx in range(len(col) - 1) if col[idx] == 1][0]

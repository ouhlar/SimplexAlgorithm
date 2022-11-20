from typing import Optional, Tuple

from matrix import Matrix
from rational_number import RationalNumber
from vector import Vector


class SimplexMethod:
    def __init__(self, a_matrix: Matrix, b_vector: Vector, z_vector: Vector, p_number: int) -> None:
        self.a: Matrix = a_matrix
        self.b: Vector = b_vector + RationalNumber(0)
        self.z: Vector = z_vector
        self.p: int = p_number
        self.u: int = 0

    def run_simplex_method(self) -> Tuple[Vector, RationalNumber]:
        simplex_table: Matrix = self.to_simplex_table()
        pivot_c_idx: Optional[int] = self.pivot_col_index(simplex_table[-1])
        if pivot_c_idx is None:
            return self.get_result(simplex_table), simplex_table[-1][-1]
        pivot_r_idx: Optional[int] = self.pivot_row_index(simplex_table, pivot_c_idx, 1)
        if pivot_r_idx is None:
            return self.get_result(simplex_table), simplex_table[-1][-1]
        while pivot_c_idx is not None and pivot_r_idx is not None:
            simplex_table = self.pivot_gauss_jordan(simplex_table, pivot_r_idx, pivot_c_idx)
            pivot_c_idx = self.pivot_col_index(simplex_table[-1])
            if pivot_c_idx is None:
                break
            pivot_r_idx = self.pivot_row_index(simplex_table, pivot_c_idx, 1)
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
        simplex_table: Matrix = Matrix(*self.a.matrix)                # add A matrix
        simplex_table.add_row(self.z)                                 # add z row
        simplex_table = self.add_artificial_and_b_col(simplex_table)  # add artificial u + b col if needed
        return simplex_table
    
    def add_artificial_and_b_col(self, m: Matrix) -> Matrix:
        rows, cols = self.a.m_dimension()
        w_row: Vector = Vector().create_empty(cols)
        w_in_b_col: RationalNumber = RationalNumber(0)
        added_w_row: bool = False
        for r in range(rows):
            if sum((self.a[r])[-self.p:]) != 1:  # sum of p1, p2, ...pn
                self.u += 1
                if not added_w_row:
                    m.add_row(w_row)
                    added_w_row = True
                u: Vector = Vector().create_empty(rows + 2)  # +2 z,w row
                u[r] = RationalNumber(1)
                u[-1] = RationalNumber(1)  # w row = 1
                m.add_col(u)
                m[-1] -= m[r]  # modify w row without b col
                w_in_b_col -= self.b[r]  # modify w value for b col 
        if added_w_row:
            m.add_col(self.b + w_in_b_col)
            m = self.first_phase(m)
        else:
            m.add_col(self.b)
        return m
    
    def first_phase(self, simplex_table: Matrix) -> Matrix:
        pivot_c_idx: Optional[int] = self.pivot_col_index(simplex_table[-1])
        pivot_r_idx: Optional[int] = self.pivot_row_index(simplex_table, pivot_c_idx, 2)
        while pivot_c_idx is not None and pivot_r_idx is not None:
            simplex_table = self.pivot_gauss_jordan(simplex_table, pivot_r_idx, pivot_c_idx)
            pivot_c_idx = self.pivot_col_index(simplex_table[-1])
            if pivot_c_idx is None:
                if simplex_table[-1][-1] == 0 and not self.base_contains_artificial(simplex_table):
                    break
                else:
                    raise ValueError("Simplex method has no solution")
            pivot_r_idx = self.pivot_row_index(simplex_table, pivot_c_idx, 2)
        return self.remove_w_and_artificial(simplex_table)

    def base_contains_artificial(self, simplex_table: Matrix) -> bool:
        cols: int = simplex_table.m_dimension()[1]
        first_artificial_idx: int = cols - self.u
        for c in range(first_artificial_idx, cols):
            if self.is_base(simplex_table.get_col(c)):
                return True
        return False
    
    def remove_w_and_artificial(self, simplex_table: Matrix) -> Matrix:
        b_col: Vector = simplex_table.get_col(-1)
        simplex_table = simplex_table[:-1]  # remove w row
        for _ in range(self.u + 1):
            simplex_table.del_col()
        simplex_table.add_col(b_col)
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
    def pivot_row_index(simplex_table: Matrix, pivot_c_index: int, phase: int) -> int:
        min_ratio: Optional[RationalNumber] = None
        min_ratio_idx: Optional[int] = None
        simplex_table_len: int = len(simplex_table) - phase  # without last z or z + w row
        for idx in range(simplex_table_len):
            row_pivot: RationalNumber = simplex_table[idx][pivot_c_index]
            if row_pivot > 0:
                ratio = simplex_table[idx][-1] / row_pivot
                if min_ratio is None:
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

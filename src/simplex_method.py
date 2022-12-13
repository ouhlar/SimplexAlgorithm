from typing import Optional, Tuple, List
from prettytable import PrettyTable

from matrix import Matrix
from rational_number import RationalNumber
from vector import Vector


class SimplexMethod:
    def __init__(self, a_matrix: Matrix, b_vector: Vector, z_vector: Vector, p_number: int) -> None:
        self.a: Matrix = a_matrix
        self.b: Vector = b_vector + RationalNumber(0)
        self.z: Vector = Vector(*z_vector, *(p_number * [RationalNumber(0)])) * (-1)
        self.p: int = p_number
        self.u: int = 0

    def run_simplex_method(self) -> Tuple[Vector, RationalNumber]:
        simplex_table: Matrix = self.to_simplex_table()
        pivot_c_idx: Optional[int] = self.pivot_col_index(simplex_table[-1])
        if pivot_c_idx is None:
            result = self.get_result(simplex_table)
            self.print_nice_result(simplex_table, result)
            return result, simplex_table[-1][-1]
        pivot_r_idx: Optional[int] = self.pivot_row_index(simplex_table, pivot_c_idx, 1)
        if pivot_r_idx is None:
            result = self.get_result(simplex_table)
            self.print_nice_result(simplex_table, result)
            return result, simplex_table[-1][-1]
        while pivot_c_idx is not None and pivot_r_idx is not None:
            self.get_result(simplex_table)
            simplex_table = self.pivot_gauss_jordan(simplex_table, pivot_r_idx, pivot_c_idx)
            pivot_c_idx = self.pivot_col_index(simplex_table[-1])
            if pivot_c_idx is None:
                break
            pivot_r_idx = self.pivot_row_index(simplex_table, pivot_c_idx, 1)
        result = self.get_result(simplex_table)
        self.print_nice_result(simplex_table, result)
        return result, simplex_table[-1][-1]

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
        self.get_result(simplex_table)
        pivot_c_idx: Optional[int] = self.pivot_col_index(simplex_table[-1])
        pivot_r_idx: Optional[int] = self.pivot_row_index(simplex_table, pivot_c_idx, 2)
        while pivot_c_idx is not None and pivot_r_idx is not None:
            simplex_table = self.pivot_gauss_jordan(simplex_table, pivot_r_idx, pivot_c_idx)
            self.get_result(simplex_table)
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
    def is_lexicographically_greater(x: Vector, y: Vector, pivot_idx: int) -> bool:
        x = x / x[pivot_idx]
        y = y / y[pivot_idx]
        cols: int = len(x)
        for i in range(cols):
            if x[i] > 0 and y[i] > 0:
                if x[i] > y[i]:
                    return True
                elif x[i] == y[i]:
                    continue
                return False
        return False

    def pivot_row_index(self, simplex_table: Matrix, pivot_c_index: int, phase: int) -> int:
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
                elif ratio == min_ratio:
                    if self.is_lexicographically_greater(simplex_table[min_ratio_idx],
                                                         simplex_table[idx],
                                                         pivot_c_index):
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
        base_idx: List[int] = [0] * len(self.a)
        for idx in range(simplex_table_cols):
            idx_base: Optional[int] = self.is_base(simplex_table.get_col(idx))
            if idx_base is not None:
                base_idx[idx_base] = idx
                result[idx] = simplex_table[idx_base][-1]
        self.print_nice_table(simplex_table, base_idx)
        return result

    @staticmethod
    def is_base(col: Vector):
        if sum(col) == 1 and (x in (0, 1) for x in col):
            return [idx for idx in range(len(col) - 1) if col[idx] == 1][0]

    def print_nice_table(self, simplex_table: Matrix, base_idx: List[int]) -> None:
        # adding header
        x_header: List[str] = self.nice_header(self.a.m_dimension()[1] - self.p, 'x') 
        p_header: List[str] = self.nice_header(self.p, 'p')
        u_header: List[str] = self.nice_header(simplex_table.m_dimension()[1] - len(x_header) - len(p_header) - 1, 'u')  # -1 b
        table_header = x_header + p_header + u_header + ['b']
        table = PrettyTable(table_header, title="SIMPLEX METHOD TABLE")

        # adding data
        table.add_rows(simplex_table)

        # adding base col
        is_w: bool = len(u_header) > 0
        base_col = self.nice_base(base_idx, table_header, is_w)
        fieldname: str = ''
        table._field_names.insert(0, fieldname)
        table._align[fieldname] = 'c'
        table._valign[fieldname] = 't'
        for i in range(len(base_col)): 
            table._rows[i].insert(0, base_col[i])
        print(table)
        print()
        return table_header
    
    def print_nice_result(self, simplex_table: Matrix, result: Vector) -> None:
        x_header: List[str] = self.nice_header(self.a.m_dimension()[1] - self.p, 'x')
        p_header: List[str] = self.nice_header(self.p, 'p')
        table_header = x_header + p_header
        # format nice result
        z_line = [str(a) + ' * ' + str(x) for a, x in zip(-self.z, x_header)]
        z_line = ' + '.join(z_line)
        z_line_values = [str(a) + ' * ' + str(x) for a, x in zip(-self.z, result[:-self.p])]
        z_line_values = ' + '.join(z_line_values)
        print(f'x = ({str(table_header)[1:-1]})\n'
              f'x = ({str(list(result))[1:-1]}) => ({str(list(result[:-self.p]))[1:-1]})\n\n'
              f'z(x) = {z_line}\n'
              f'z(x) = {z_line_values}\n'
              f'z(x) = {simplex_table[-1][-1]}\n')

    @staticmethod
    def nice_header(num_var: int, symbol: str) -> List[str]:
        return [symbol + "_" + str(i) for i in range(1,num_var+1)]

    @staticmethod
    def nice_base(base_idx: List[int], table_header: List[str], is_w: bool) -> PrettyTable:
        first_col: List[str] = []
        for i in base_idx:
            first_col.append(table_header[i])
        first_col.append('z(x)')
        if is_w:
            first_col.append('w(x)')
        return first_col

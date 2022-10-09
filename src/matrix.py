import json
from typing import Optional, Tuple, Union
from rational_number import RationalNumber
from vector import Vector


class Matrix:
    def __init__(self, *values: Union[Vector, object]) -> None:
        self.matrix = Vector(*values)
    
    @classmethod
    def from_json_file(cls, filename):
        with open(filename) as json_file:
            return cls(*json.load(json_file))

    def __getitem__(self, item) -> Vector:
        return self.matrix[item]
    
    def __setitem__(self, place_num: int, item: Vector) -> None:
        self.matrix[place_num] = item

    def __len__(self) -> int:
        return len(self.matrix)
    
    def __repr__(self) -> str:
        return str(self.matrix)
    
    def __str__(self) -> str:
        return '[' + '\n '.join((map(str, self.matrix))) + ']'
    
    def __iter__(self):
        return self.matrix.__iter__()
    
    def __neg__(self) -> "Matrix":
        return Matrix(*(-v for v in self.matrix))

    def m_dimension(self) -> Tuple[int, int]:
        return len(self), len(self[0])

    def __add__(self, other: "Matrix") -> "Matrix":
        if self.m_dimension() != other.m_dimension():
            raise ValueError("Different dimension of matrices")
        return Matrix(*(a + b for a, b in zip(self.matrix, other.matrix)))
    
    def __sub__(self, other: "Matrix") -> "Matrix":
        return self.__add__(-other)
    
    def __mul__(self, other: Union["Matrix", RationalNumber, int, Vector]) -> "Matrix":
        if isinstance(other, Vector):
            other = Matrix(*(Vector(other)))
        if isinstance(other, Matrix):
            if self.m_dimension()[1] != len(other):
                raise ValueError("Wrong dimension of matrices for multiplication")
            return Matrix(*((Vector(*(sum(a * b for a, b in zip(A_row, B_col))
                                      for B_col in zip(*other))) for A_row in self)))
        if isinstance(other, Union[int, RationalNumber]):
            return Matrix(*(a * other for a in self.matrix))
        else:
            raise TypeError("wrong type of number for multiplication")
    
    def __truediv__(self, other: Union[RationalNumber, int]) -> "Matrix":
        if not isinstance(other, Union[RationalNumber, int]):
            raise TypeError("wrong type of number for division")
        return Matrix(*(a / other for a in self))
    
    def swap_rows(self, a_row: int, b_row: int) -> Optional["Matrix"]:
        if a_row < 0 or a_row > len(self) or b_row < 0 or b_row > len(self):
            raise ValueError("Index of row is out of range")
        self[a_row], self[b_row] = self[b_row], self[a_row]
        return self

    def swap_cols(self, a_col: int, b_col: int) -> Optional["Matrix"]:
        if a_col < 0 or a_col > self.m_dimension()[1] or b_col < 0 or b_col > self.m_dimension()[1]:
            raise ValueError("Index of row is out of range")
        for row in self:
            row[a_col], row[b_col] = row[b_col], row[a_col]
        return self

    def gauss_jordan(self) -> None:
        m_size: Tuple[int, int] = self.m_dimension()
        pivot = 0
        rows: int = m_size[0]
        cols: int = m_size[1]
        for r in range(rows):
            if pivot >= cols:
                return
            i = r
            while self[i][pivot] == 0:
                i += 1
                if rows == i:
                    i = r
                    pivot += 1
                    if cols == pivot:
                        return
            if i != r:
                self.swap_rows(i, r)
            self[r] = self[r] / self[r][pivot]
            for j in range(rows):
                if j != r:
                    ratio: RationalNumber = self[j][pivot]
                    if ratio != 0:
                        self[j] = self[j] - self[r] * self[j][pivot]
            pivot += 1

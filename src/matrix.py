from typing import Tuple, Union
from rational_number import RationalNumber
from vector import Vector


class Matrix:
    def __init__(self, *values: Vector) -> None:
        self.matrix = Vector(*values)

    def __getitem__(self, item) -> Vector:
        return self.matrix[item]

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
        return Matrix(*(a + b for a,b in zip(self.matrix, other.matrix)))
    
    def __sub__(self, other: "Matrix") -> "Matrix":
        return self.__add__(-other)
    
    def __mul__(self, other: Union["Matrix", RationalNumber, int, Vector]) -> "Matrix":
        if isinstance(other, Vector):
            other = Matrix(*(Vector(other)))
        if isinstance(other, Matrix):
            if self.m_dimension()[1] != len(other):
                raise ValueError("Wrong dimension of matrices for multiplication")
            return Matrix(*((Vector(*(sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*other))) for A_row in self)))
        if isinstance(other, Union[int, RationalNumber]):
            return Matrix(*(a * other for a in self.matrix))
        else:
            raise TypeError("wrong type of number for multiplication")
    
    def __truediv__(self, other: Union[RationalNumber, int]) -> "Matrix":
        if not isinstance(other, Union[RationalNumber, int]):
            raise TypeError("wrong type of number for division")
        return Matrix(*(a / other for a in self))
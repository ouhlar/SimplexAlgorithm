from typing import Tuple
from rational_number import RationalNumber
from vector import Vector


class Matrix:
    def __init__(self, *values: Vector) -> None:
        self.matrix = Vector(*values)

    def __getitem__(self, item) -> "Vector":
        return self.matrix[item]

    def __len__(self) -> int:
        return len(self.matrix)
    
    def __repr__(self) -> str:
        return str(self.matrix)
    
    def __str__(self) -> str:
        return str(self.matrix)

    def size(self) -> Tuple[int, int]:
        return len(self), len(self[0])

from typing import Tuple, Union

from rational_number import RationalNumber


class Vector:
    def __init__(self, values: Tuple[RationalNumber, ...]) -> None:
        self.vector = values

    def __len__(self):
        return len(self.vector)
    
    def __mul__(self, other: Union[int, RationalNumber]) -> "Vector":
        if isinstance(other, Union[int, RationalNumber]):
            return Vector(tuple(i * other for i in self))
        else:
            raise TypeError("Wrong type of values for multiplication")
    
    def __rmul__(self, other: Union[int, RationalNumber]) -> "Vector":
        return self.__mul__(other)
    
    def __add__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            if len(self) == len(other):
                return Vector(tuple(a + b for a, b in zip(self, other)))
        else:
            raise TypeError("Wrong type of values for addition")
    
    def __sub__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            if len(self) == len(other):
                result: Vector = Vector(tuple(a - b for a, b in zip(self, other)))
                return result
        else:
            raise TypeError("Wrong type of values for substraction")
    
    def __truediv__(self, other: Union[int, RationalNumber]) -> "Vector":
        if other == 0:
            raise ZeroDivisionError("Division by 0")
        if isinstance(other, Union[int, RationalNumber]):
            return Vector(tuple(i / other for i in self))
        else:
            raise TypeError("Wrong type of values for division")
    
    def __iter__(self):
        return self.vector.__iter__()
    
    def __getitem__(self, key):
        return self.vector[key]

    def __repr__(self):
        return str(self.vector)
    
    def __str__(self):
        return str(self.vector)

from typing import Tuple, Union

from rational_number import RationalNumber


class Vector:
    def __init__(self, *values: Union[RationalNumber, "Vector"]) -> None:
        self.vector = values

    def __len__(self):
        return len(self.vector)
    
    # Dot products
    def __mul__(self, other: Union[int, RationalNumber, "Vector"]) -> Union[RationalNumber, "Vector"]:
        if isinstance(other, Union[int, RationalNumber]):
            return Vector(*(i * other for i in self))
        if isinstance(other, Vector):
            return sum(a * b for a, b in zip(self, other))
        else:
            raise TypeError("Wrong type of values for multiplication")
    
    def __rmul__(self, other: Union[int, RationalNumber]) -> "Vector":
        return self.__mul__(other)
    
    def __add__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            if len(self) == len(other):
                return Vector(*(a + b for a, b in zip(self, other)))
        else:
            raise TypeError("Wrong type of values for addition")
    
    def __sub__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            if len(self) == len(other):
                return Vector(*(a - b for a, b in zip(self, other)))
        else:
            raise TypeError("Wrong type of values for substraction")
    
    def __truediv__(self, other: Union[int, RationalNumber]) -> "Vector":
        if other == 0:
            raise ZeroDivisionError("Division by 0")
        if isinstance(other, Union[int, RationalNumber]):
            return Vector(*(i / other for i in self))
        else:
            raise TypeError("Wrong type of values for division")

    def __eq__(self, other: "Vector") -> bool:
        return self.vector == other.vector

    def __getitem__(self, item) -> Union["Vector", RationalNumber]:
        return self.vector[item]

    def __repr__(self) -> str:
        return str(self.vector)
    
    def __str__(self) -> str:
        return str(self.vector)

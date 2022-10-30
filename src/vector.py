from typing import List, Union

from rational_number import RationalNumber


class Vector:
    def __init__(self, *values: Union[RationalNumber, "Vector"]) -> None:
        self.vector = values

    def __len__(self):
        return len(self.vector)

    # Dot products
    def __mul__(self, other: Union[int, RationalNumber, "Vector"]) -> Union[RationalNumber, "Vector"]:
        if isinstance(other, Union[int, RationalNumber]):
            return Vector(*(i * other for i in self.vector))
        if isinstance(other, Vector):
            return sum(a * b for a, b in zip(self.vector, other.vector))
        else:
            raise TypeError("Wrong type of values for multiplication")

    def __rmul__(self, other: Union[int, RationalNumber, "Vector"]) -> "Vector":
        return self.__mul__(other)

    def __add__(self, other: Union["Vector", RationalNumber]) -> "Vector":
        if isinstance(other, Vector):
            if len(self) == len(other):
                return Vector(*(a + b for a, b in zip(self.vector, other.vector)))
        if isinstance(other, RationalNumber):
            return Vector(*self.vector, other)
        else:
            raise TypeError("Wrong type of values for addition")

    def __neg__(self) -> "Vector":
        return Vector(*(-rn for rn in self.vector))

    def __sub__(self, other: "Vector") -> "Vector":
        return self.__add__(-other)

    def __truediv__(self, other: Union[int, RationalNumber]) -> "Vector":
        if isinstance(other, Union[int, RationalNumber]):
            if isinstance(other, int):
                other: RationalNumber = RationalNumber(other, 1)
            return Vector(*(i / other for i in self.vector))
        else:
            raise TypeError("Wrong type of values for division")

    def __eq__(self, other: "Vector") -> bool:
        return self.vector == other.vector

    def __getitem__(self, place_num: int) -> Union["Vector", RationalNumber]:
        return self.vector[place_num]

    def __setitem__(self, place_num: int, item: Union[RationalNumber, "Vector"]) -> None:
        list_vector: List[Union[RationalNumber, "Vector"]] = list(self.vector)
        list_vector[place_num] = item
        self.vector = tuple(list_vector)

    def __iter__(self):
        return self.vector.__iter__()

    def __repr__(self) -> str:
        return str(self.vector)

    def __str__(self) -> str:
        return '[' + '  '.join((map(str, self.vector))) + ']'

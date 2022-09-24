from typing import Tuple, Union


class RationalNumber:
    def __init__(self, numerator: int, denominator: int) -> None:
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("Wrong type of numerator or denominator, must be int")
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be 0")
        if numerator == 0:
            self._numerator = 0
            self._denominator = 1
        else:
            if (numerator < 0 and denominator > 0) or (numerator >= 0 and denominator < 0):
                minus: int = -1
            else:
                minus: int = 1
            self._numerator, self._denominator = self._reduce(abs(numerator), abs(denominator), minus)

    def __str__(self) -> str:
        return "{}/{}".format(str(self._numerator), str(self._denominator))

    def _gcd(self, n: int, d: int) -> int:
        if n == 0:
            return d
        return self._gcd(d % n, n)

    def _reduce(self, numerator: int, denominator: int, minus: int) -> Tuple[int, int]:
        gcd_num: int = self._gcd(numerator, denominator)
        return (numerator // gcd_num * minus), (denominator // gcd_num)

    def get_numerator(self):
        return self._numerator

    def get_denominator(self):
        return self._denominator

    def __eq__(self, rn: "RationalNumber") -> bool:
        return self.__dict__ == rn.__dict__

    def __gt__(self, rn: "RationalNumber") -> bool:
        return self._numerator * rn.get_denominator() > \
            rn.get_numerator() * self.get_denominator()

    def __ge__(self, rn: "RationalNumber") -> bool:
        return not self < rn

    def __neg__(self):
        return RationalNumber(self._numerator * (-1), self._denominator)

    def __add__(self, rn: Union["RationalNumber", int]) -> "RationalNumber":
        if isinstance(rn, int):
            new_rn: RationalNumber = RationalNumber(rn, 1)
        else:
            new_rn: RationalNumber = rn
        new_numerator: int = self._numerator * new_rn.get_denominator() + new_rn.get_numerator() * self._denominator
        new_denominator: int = self._denominator * new_rn.get_denominator()
        return RationalNumber(new_numerator, new_denominator)

    def __mul__(self, rn: Union["RationalNumber", int]) -> "RationalNumber":
        if isinstance(rn, int):
            new_rn: RationalNumber = RationalNumber(rn, 1)
        else:
            new_rn: RationalNumber = rn
        new_numerator: int = self._numerator * new_rn.get_numerator()
        new_denominator: int = self._denominator * new_rn.get_denominator()
        return RationalNumber(new_numerator, new_denominator)

    def __sub__(self, rn: Union["RationalNumber", int]) -> "RationalNumber":
        if isinstance(rn, int):
            new_rn: RationalNumber = (-RationalNumber(rn, 1))
        else:
            new_rn: RationalNumber = (-rn)
        return self + new_rn

    def __truediv__(self, rn: Union["RationalNumber", int]) -> "RationalNumber":
        if isinstance(rn, int):
            new_rn: RationalNumber = RationalNumber(1, rn)
        else:
            new_rn: RationalNumber = RationalNumber(rn.get_denominator(), rn.get_numerator())
        return self * new_rn

    def __pow__(self, power_number: int) -> "RationalNumber":
        if power_number == 0:
            return RationalNumber(1, 1)
        if power_number < 0:
            return RationalNumber(self._denominator ** abs(power_number), self._numerator ** abs(power_number))
        return RationalNumber(self._numerator ** power_number, self._denominator ** power_number)

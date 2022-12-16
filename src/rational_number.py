from typing import Tuple, Union
import re


class RationalNumber:
    def __init__(self, *var: Union[int, str]) -> None:
        if len(var) == 1:
            if isinstance(var[0], str):
                r_number: str = var[0].replace('-', '')
                numerator, denominator = [int(x) for x in r_number.split('/')]
                if re.match(r"-\d/\d", var[0]):
                    numerator *= -1
            else:
                numerator = var[0]
                denominator = 1
        else:
            numerator, denominator = var
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be 0")
        if numerator == 0:
            self._numerator: int = 0
            self._denominator: int = 1
        else:
            if (numerator < 0 and denominator > 0) or (numerator >= 0 and denominator < 0):
                minus: int = -1
            else:
                minus: int = 1
            self._numerator, self._denominator = self._reduce(abs(numerator), abs(denominator), minus)

    def __str__(self) -> str:
        if self.get_denominator() == 1:
            return str(self._numerator)
        return "{}/{}".format(str(self._numerator), str(self._denominator))

    def __repr__(self) -> str:
        if self.get_denominator() == 1:
            return str(self._numerator)
        return "{}/{}".format(str(self._numerator), str(self._denominator))

    def _gcd(self, n: int, d: int) -> int:
        if n == 0:
            return d
        return self._gcd(d % n, n)

    def _reduce(self, numerator: int, denominator: int, minus: int) -> Tuple[int, int]:
        gcd_num: int = self._gcd(numerator, denominator)
        return (numerator // gcd_num * minus), (denominator // gcd_num)

    def get_numerator(self) -> int:
        return self._numerator

    def get_denominator(self) -> int:
        return self._denominator

    def __eq__(self, rn: Union["RationalNumber", int]) -> bool:
        if isinstance(rn, RationalNumber):
            return self.__dict__ == rn.__dict__
        return self.__eq__(RationalNumber(rn, 1))

    def __gt__(self, rn: Union["RationalNumber", int]) -> bool:
        if isinstance(rn, RationalNumber):
            return self._numerator * rn.get_denominator() > \
                   rn.get_numerator() * self.get_denominator()
        return self.__gt__(RationalNumber(rn, 1))

    def __ge__(self, rn: Union["RationalNumber", int]) -> bool:
        if isinstance(rn, RationalNumber):
            return not self < rn
        return self.__ge__(RationalNumber(rn, 1))

    def __neg__(self) -> "RationalNumber":
        return RationalNumber(self._numerator * (-1), self._denominator)

    def __add__(self, rn: Union["RationalNumber", int]) -> "RationalNumber":
        if isinstance(rn, int):
            new_rn: RationalNumber = RationalNumber(rn, 1)
        else:
            new_rn: RationalNumber = rn
        new_numerator: int = self._numerator * new_rn.get_denominator() + new_rn.get_numerator() * self._denominator
        new_denominator: int = self._denominator * new_rn.get_denominator()
        return RationalNumber(new_numerator, new_denominator)

    def __radd__(self, rn: Union["RationalNumber", int]) -> "RationalNumber":
        return self.__add__(rn)

    def __mul__(self, rn: Union["RationalNumber", int]) -> "RationalNumber":
        if isinstance(rn, int):
            new_rn: RationalNumber = RationalNumber(rn, 1)
        else:
            new_rn: RationalNumber = rn
        new_numerator: int = self._numerator * new_rn.get_numerator()
        new_denominator: int = self._denominator * new_rn.get_denominator()
        return RationalNumber(new_numerator, new_denominator)

    def __rmul__(self, rn: Union["RationalNumber", int]) -> "RationalNumber":
        return self.__mul__(rn)

    def __sub__(self, rn: Union["RationalNumber", int]) -> "RationalNumber":
        if isinstance(rn, int):
            new_rn: RationalNumber = (-RationalNumber(rn, 1))
        else:
            new_rn: RationalNumber = (-rn)
        return self + new_rn

    def __rsub__(self, rn: Union["RationalNumber", int]) -> "RationalNumber":
        return -self.__sub__(rn)

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

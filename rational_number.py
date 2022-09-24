from typing import Tuple


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
        return str(self._numerator) + "/" + str(self._denominator)

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
        if not isinstance(rn, RationalNumber):
            raise TypeError("Wrong type of comparing number")
        return self.__dict__ == rn.__dict__

    def __gt__(self, rn: "RationalNumber") -> bool:
        if not isinstance(rn, RationalNumber):
            raise TypeError("Wrong type of comparing number")
        return self._numerator * rn.get_denominator() > \
            rn.get_numerator() * self.get_denominator()

    def __ge__(self, rn: "RationalNumber") -> bool:
        if not isinstance(rn, RationalNumber):
            raise TypeError("Wrong type of comparing number")
        return not self < rn

    def __add__(self, rn: "RationalNumber") -> "RationalNumber":
        new_numerator: int = self._numerator * rn.get_denominator() + rn.get_numerator() * self._denominator
        new_denominator: int = self._denominator * rn.get_denominator()
        return RationalNumber(new_numerator, new_denominator)

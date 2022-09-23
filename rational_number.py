from typing import Tuple


class RationalNumber:
    def __init__(self, numerator: int, denominator: int) -> None:
        self._minus: bool = False
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("Wrong type of numerator or denominator, must be int")
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be 0")
        if numerator == 0:
            self._numerator = 0
            self._denominator = 1
        else:
            if (numerator < 0 and denominator > 0) or (numerator >= 0 and denominator < 0):
                self._minus = True
            else:
                self._minus = False
            self._numerator, self._denominator = self._reduce(abs(numerator), abs(denominator))

    def __str__(self) -> str:
        return (self._minus and '-' or '') + str(self._numerator) + "/" + str(self._denominator)

    def _gcd(self, n: int, d: int) -> int:
        if n == 0:
            return d
        return self._gcd(d % n, n)

    def _reduce(self, numerator: int, denominator: int) -> Tuple[int, int]:
        gcd_num: int = self._gcd(numerator, denominator)
        return numerator // gcd_num, denominator // gcd_num

    def get_numerator(self):
        return self._numerator

    def get_denominator(self):
        return self._denominator

    def get_minus(self):
        return self._minus

    def __eq__(self, rn: "RationalNumber") -> bool:
        if not isinstance(rn, RationalNumber):
            raise TypeError("Wrong type of comparing number")
        return self.__dict__ == rn.__dict__

    def __gt__(self, rn: "RationalNumber") -> bool:
        if not isinstance(rn, RationalNumber):
            raise TypeError("Wrong type of comparing number")
        if rn.get_minus() == self._minus:
            sign: int = self._minus and -1 or 1
            return self._numerator * rn.get_denominator() * sign > \
                rn.get_numerator() * self.get_denominator() * sign
        return rn.get_minus()

    def __ge__(self, rn: "RationalNumber") -> bool:
        if not isinstance(rn, RationalNumber):
            raise TypeError("Wrong type of comparing number")
        return not self < rn

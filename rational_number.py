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
        return (self._minus and '-' or ' ') + str(self._numerator) + "/" + str(self._denominator)

    def _gcd(self, n: int, d: int) -> int:
        if n == 0:
            return d
        return self._gcd(d % n, n)

    def _reduce(self, numerator: int, denominator: int) -> Tuple[int, int]:
        gcd_num: int = self._gcd(numerator, denominator)
        return numerator // gcd_num, denominator // gcd_num

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
            self._numerator: int = abs(numerator)
            self._denominator: int = abs(denominator)

    def __str__(self) -> str:
        return (self._minus and '-' or ' ') + str(self._numerator) + "/" + str(self._denominator)

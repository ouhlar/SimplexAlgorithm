import unittest

from rational_number import RationalNumber


class TestRationalNumber(unittest.TestCase):
    def test_basics(self):
        self.assertEqual(str(RationalNumber(5, 3)), "5/3")
        self.assertEqual(str(RationalNumber(3, 10)), "3/10")
    
    def test_wrong_input(self):
        self.assertRaises(TypeError, RationalNumber, "str", 8)
        self.assertRaises(TypeError, RationalNumber, "str", 0)
        self.assertRaises(TypeError, RationalNumber, "9", 8)
        self.assertRaises(TypeError, RationalNumber, 9.5, 8)

    def test_minus_sign(self):
        self.assertEqual(str(RationalNumber(-5, 3)), "-5/3")
        self.assertEqual(str(RationalNumber(5, -3)), "-5/3")
        self.assertEqual(str(RationalNumber(-5, -3)), "5/3")

    def test_zero_numerator(self):
        self.assertEqual(str(RationalNumber(0, 150)), "0/1")
        self.assertEqual(str(RationalNumber(-0, 150)), "0/1")
        self.assertEqual(str(RationalNumber(0, -150)), "0/1")
        self.assertEqual(str(RationalNumber(-0, -150)), "0/1")

    def test_zero_denominator(self):
        self.assertRaises(ZeroDivisionError, RationalNumber, 8, 0)
        self.assertRaises(ZeroDivisionError, RationalNumber, -8, 0)
        self.assertRaises(ZeroDivisionError, RationalNumber, 8, -0)
        self.assertRaises(ZeroDivisionError, RationalNumber, -8, -0)
        self.assertRaises(ZeroDivisionError, RationalNumber, 0, 0)

    def test_reducing(self):
        self.assertEqual(str(RationalNumber(3, 9)), "1/3")
        self.assertEqual(str(RationalNumber(-3, 9)), "-1/3")
        self.assertEqual(str(RationalNumber(3, -9)), "-1/3")
        self.assertEqual(str(RationalNumber(-3, -9)), "1/3")
        self.assertEqual(str(RationalNumber(157092776646, 366549812174)), "3/7")

    def test_is_equal(self):
        self.assertEqual(RationalNumber(3, 9) == RationalNumber(1, 3), True)
        self.assertEqual(RationalNumber(-3, 9) == RationalNumber(1, 3), False)
        self.assertEqual(RationalNumber(3, -9) == RationalNumber(1, 3), False)
        self.assertEqual(RationalNumber(-3, -9) == RationalNumber(1, 3), True)

    def test_greater_then(self):
        self.assertEqual(RationalNumber(1, 2) > RationalNumber(1, 9), True)
        self.assertEqual(RationalNumber(-1, 2) > RationalNumber(1, 9), False)
        self.assertEqual(RationalNumber(1, 2) > RationalNumber(-1, 9), True)
        self.assertEqual(RationalNumber(-1, -2) > RationalNumber(1, 9), True)
        self.assertEqual(RationalNumber(1, 2) > RationalNumber(-1, -9), True)
        self.assertEqual(RationalNumber(-1, 2) > RationalNumber(-1, 9), False)

    def test_greater_then_or_equal(self):
        self.assertEqual(RationalNumber(1, 2) >= RationalNumber(1, 9), True)
        self.assertEqual(RationalNumber(1, 2) >= RationalNumber(1, 2), True)
        self.assertEqual(RationalNumber(-1, 2) >= RationalNumber(-1, 9), False)
        self.assertEqual(RationalNumber(-1, 2) >= RationalNumber(-1, 2), True)
        self.assertEqual(RationalNumber(1, 2) >= RationalNumber(-1, -2), True)
        self.assertEqual(RationalNumber(-1, -2) >= RationalNumber(-1, -2), True)

    def test_addition(self):
        self.assertEqual(RationalNumber(1, 9) + RationalNumber(1, 2), RationalNumber(11, 18))
        self.assertEqual(RationalNumber(-1, 9) + RationalNumber(1, 2), RationalNumber(7, 18))
        self.assertEqual(RationalNumber(1, 9) + RationalNumber(-1, 2), RationalNumber(-7, 18))
        self.assertEqual(RationalNumber(-1, 9) + RationalNumber(-1, 2), RationalNumber(-11, 18))


if __name__ == '__main__':
    unittest.main()

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


if __name__ == '__main__':
    unittest.main()

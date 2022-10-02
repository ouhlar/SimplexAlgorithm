import unittest
from rational_number import RationalNumber
from vector import Vector

V_POS: Vector = Vector((RationalNumber(1, 3), RationalNumber(3, 2), RationalNumber(4, 7)))
V_NEG: Vector = Vector((RationalNumber(-1, 3), RationalNumber(-3, 2), RationalNumber(-4, 7)))


class TestRationalNumber(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(str(V_POS + V_POS), "(2/3, 3/1, 8/7)")
        self.assertEqual(str(V_POS + V_NEG), "(0/1, 0/1, 0/1)")
        self.assertEqual(str(V_NEG + V_POS), "(0/1, 0/1, 0/1)")
        self.assertEqual(str(V_NEG + V_NEG), "(-2/3, -3/1, -8/7)")

    def test_substraction(self):
        self.assertEqual(str(V_POS - V_POS), "(0/1, 0/1, 0/1)")
        self.assertEqual(str(V_POS - V_NEG), "(2/3, 3/1, 8/7)")
        self.assertEqual(str(V_NEG - V_POS), "(-2/3, -3/1, -8/7)")
        self.assertEqual(str(V_NEG - V_NEG), "(0/1, 0/1, 0/1)")
    
    def test_multiplication(self):
        self.assertEqual(str(V_POS * 8), "(8/3, 12/1, 32/7)")
        self.assertEqual(str(8 * V_POS), "(8/3, 12/1, 32/7)")
        self.assertEqual(str(V_NEG * 8), "(-8/3, -12/1, -32/7)")
        self.assertEqual(str(8 * V_NEG), "(-8/3, -12/1, -32/7)")
    
    def test_division(self):
        self.assertEqual(str(V_POS / 8), "(1/24, 3/16, 1/14)")
        self.assertEqual(str(V_NEG / 8), "(-1/24, -3/16, -1/14)")
        self.assertRaises(ZeroDivisionError, Vector.__truediv__, V_POS, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)

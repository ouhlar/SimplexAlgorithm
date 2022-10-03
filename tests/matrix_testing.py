import unittest
from matrix import Matrix
from rational_number import RationalNumber
from vector import Vector

M1_POS: Matrix = Matrix(
                        Vector(RationalNumber(1, 3), RationalNumber(3, 2), RationalNumber(4, 7))
                    )
M2_POS: Matrix = Matrix(
                        Vector(RationalNumber(1, 3)),
                        Vector(RationalNumber(3, 2)),
                        Vector(RationalNumber(4, 7))
                    )

M1_NEG: Matrix = Matrix(
                        Vector(RationalNumber(-1, 3), RationalNumber(-3, 2), RationalNumber(-4, 7))
                    )
M2_NEG: Matrix = Matrix(
                        Vector(RationalNumber(-1, 3)),
                        Vector(RationalNumber(-3, 2)),
                        Vector(RationalNumber(-4, 7))
                    )

class TestMatrix(unittest.TestCase):
    def test_len(self):
        self.assertEqual(len(M1_POS), 1)
        self.assertEqual(len(M2_POS), 3)
    
    def test_size(self):
        self.assertEqual(M1_POS.size(), (1,3))
        self.assertEqual(M2_POS.size(), (3,1))

if __name__ == '__main__':
    unittest.main(verbosity=2)

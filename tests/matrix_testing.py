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

V_POS: Vector = Vector(RationalNumber(1, 3), RationalNumber(3, 2), RationalNumber(4, 7))


class TestMatrix(unittest.TestCase):
    def test_len(self):
        self.assertEqual(len(M1_POS), 1)
        self.assertEqual(len(M2_POS), 3)
    
    def test_dimension(self):
        self.assertEqual(M1_POS.m_dimension(), (1,3))
        self.assertEqual(M2_POS.m_dimension(), (3,1))
    
    def test_get_item(self):
        self.assertEqual(str(M1_POS[0][1]), "3/2")
    
    def test_addition(self):
        self.assertEqual(str(M1_POS + M1_POS), "[[2/3  3/1  8/7]]")
        self.assertRaises(ValueError, Matrix.__add__, M1_POS, M2_POS)
        self.assertEqual(str(M1_POS + M1_NEG), "[[0/1  0/1  0/1]]")
        self.assertEqual(str(M1_NEG + M1_POS), "[[0/1  0/1  0/1]]")
        self.assertEqual(str(M1_NEG + M1_NEG), "[[-2/3  -3/1  -8/7]]")
        self.assertEqual(str(M2_POS + M2_POS), "[[2/3]\n [3/1]\n [8/7]]")
        self.assertEqual(str(M2_POS + M2_NEG), "[[0/1]\n [0/1]\n [0/1]]")
        self.assertEqual(str(M2_NEG + M2_NEG), "[[-2/3]\n [-3/1]\n [-8/7]]")
    
    def test_substraction(self):
        self.assertEqual(str(M1_POS - M1_POS), "[[0/1  0/1  0/1]]")
        self.assertRaises(ValueError, Matrix.__sub__, M1_POS, M2_POS)
        self.assertEqual(str(M1_POS - M1_NEG), "[[2/3  3/1  8/7]]")
        self.assertEqual(str(M1_NEG - M1_POS), "[[-2/3  -3/1  -8/7]]")
        self.assertEqual(str(M1_NEG - M1_NEG), "[[0/1  0/1  0/1]]")
        self.assertEqual(str(M2_POS - M2_POS), "[[0/1]\n [0/1]\n [0/1]]")
        self.assertEqual(str(M2_POS - M2_NEG), "[[2/3]\n [3/1]\n [8/7]]")
        self.assertEqual(str(M2_NEG - M2_NEG), "[[0/1]\n [0/1]\n [0/1]]")
    
    def test_multiplication(self):
        self.assertEqual(str(M1_POS * M2_POS), "[[4741/1764]]")
        self.assertEqual(str(M1_POS * M2_NEG), "[[-4741/1764]]")
        self.assertRaises(ValueError, Matrix.__mul__, M1_POS, M1_POS)
        self.assertEqual(str(M1_POS * 5), "[[5/3  15/2  20/7]]")
        self.assertEqual(str(M1_POS * RationalNumber(1,2)), "[[1/6  3/4  2/7]]")
        self.assertEqual(str(M2_POS * V_POS), "[[1/9  1/2  4/21]\n [1/2  9/4  6/7]\n [4/21  6/7  16/49]]")

if __name__ == '__main__':
    unittest.main(verbosity=2)

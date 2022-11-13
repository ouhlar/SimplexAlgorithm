import unittest

from matrix import Matrix
from rational_number import RationalNumber
from simplex_method import SimplexMethod
from vector import Vector


class TestSimplexMethod(unittest.TestCase):
    def test_run_simplex_method(self):
        m = Matrix.from_json_file('./tests/test_data/simplex_sample.json')
        b = Vector(RationalNumber(38), RationalNumber(55))
        z = Vector(RationalNumber(-5), RationalNumber(-7), RationalNumber(-12), RationalNumber(1),
                   RationalNumber(0), RationalNumber(0))
        p = 2
        simplex_result = SimplexMethod(m, b, z, p).run_simplex_method()
        self.assertEqual(str(simplex_result), "((0, 0, 31/2, 7/1, 0, 0), 179/1)")

    def test_run_simplex_2_phase(self):
        m = Matrix.from_json_file('./tests/test_data/simplex_two_phase.json')
        b = Vector(RationalNumber(14), RationalNumber(2), RationalNumber(19))
        z = Vector(RationalNumber(3), RationalNumber(2), RationalNumber(0), RationalNumber(0))
        p = 2
        simplex_result = SimplexMethod(m, b, z, p).run_simplex_method()
        self.assertEqual(str(simplex_result), "((4/1, 1/1, 2/1, 0), -14/1)")


if __name__ == '__main__':
    unittest.main(verbosity=2)

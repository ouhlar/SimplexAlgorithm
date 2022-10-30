import unittest

from matrix import Matrix
from rational_number import RationalNumber
from simplex_method import SimplexMethod
from vector import Vector


class TestSimplexMethod(unittest.TestCase):
    def test_run_simplex_method(self):
        m = Matrix.from_json_file('./tests/test_data/simplex_sample.json')
        b = Vector(RationalNumber(38), RationalNumber(55))
        c = Vector(RationalNumber(-5), RationalNumber(-7), RationalNumber(-12), RationalNumber(1),
                   RationalNumber(0), RationalNumber(0))
        simplex_result = SimplexMethod(m, b, c).run_simplex_method()
        self.assertEqual(str(simplex_result), "((0, 0, 31/2, 7/1, 0, 0), 179/1)")


if __name__ == '__main__':
    unittest.main(verbosity=2)

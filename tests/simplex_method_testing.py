import unittest

from simplex_method import SimplexMethod


class TestSimplexMethod(unittest.TestCase):
    def test_run_simplex_method(self):
        simplex_result = SimplexMethod('./tests/test_data/classic_simplex.json').run_simplex_method(False)
        self.assertEqual(str(simplex_result), "((0, 0, 31/2, 7, 0, 0), 179)")

    def test_run_simplex_2_phase(self):
        simplex_result = SimplexMethod('./tests/test_data/simplex_two_phase.json').run_simplex_method(False)
        self.assertEqual(str(simplex_result), "((4, 1, 2, 0), 11)")


if __name__ == '__main__':
    unittest.main(verbosity=2)

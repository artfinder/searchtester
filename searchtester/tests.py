import unittest2 as unittest
from searchtester.scoring import calculate_score

class FloatTestCase(unittest.TestCase):
    def assertRoughlyEqual(self, float1, float2, epsilon=0.0001):
        if abs(float1 - float2) < epsilon:
            return
        else:
            self.assertEqual(float1, float2)

class ScoringTests(FloatTestCase):
    def test_perfect(self):
        self.assertEqual(1.0, calculate_score([0]))
        self.assertEqual(1.0, calculate_score([0, 1]))
        self.assertEqual(1.0, calculate_score([0, 1, 2]))
        self.assertEqual(1.0, calculate_score([0, 1, 2, 3]))
        self.assertEqual(1.0, calculate_score([0, 1, 2, 3, 4]))

    def test_middling(self):
        self.assertRoughlyEqual(0.9926, calculate_score([0, 1, 2, 3, 5]))
        self.assertRoughlyEqual(0.9800, calculate_score([0, 1, 2, 4, 3]))
        self.assertRoughlyEqual(0.8520, calculate_score([0, 2, 1, 3, 4]))

        self.assertRoughlyEqual(0.7976, calculate_score([0, 3, 1, 2, 4]))
        self.assertRoughlyEqual(0.7775, calculate_score([0, 4, 1, 2, 3]))
        self.assertRoughlyEqual(0.7775, calculate_score([0, 3, 1, 4, 2]))

        self.assertRoughlyEqual(0.5977, calculate_score([1, 0, 2, 3, 4]))
        self.assertRoughlyEqual(0.5032, calculate_score([1, 0, 4, 3, 2]))
        self.assertRoughlyEqual(0.4497, calculate_score([2, 0, 1, 3, 4]))

        self.assertRoughlyEqual(0.4432, calculate_score([1, 2, 0, 3]))
        self.assertRoughlyEqual(0.3881, calculate_score([1, 3, 0, 2]))
        self.assertRoughlyEqual(0.2935, calculate_score([2, 1, 0, 3]))

        self.assertRoughlyEqual(0.2273, calculate_score([2, 1, 3, 4, 0]))

    def test_awful(self):
        self.assertEqual(0.0, calculate_score([None]))
        self.assertEqual(0.0, calculate_score([None, None]))
        self.assertEqual(0.0, calculate_score([None, None, None]))

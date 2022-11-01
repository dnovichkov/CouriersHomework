import unittest
from main import Point


class PointsTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_dist_to_center(self):
        point = Point(2, 0)
        dist_to_center = point.get_distance_to_center()
        self.assertEqual(2, dist_to_center)

    def test_bad_init(self):
        point = Point(2, 'o')
        self.assertRaises(TypeError, point.get_distance_to_center)


if __name__ == '__main__':
    unittest.main()

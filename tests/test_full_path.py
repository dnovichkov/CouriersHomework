import unittest
from main import get_full_plan_path, Point, Courier, Order


class FullPathTest(unittest.TestCase):
    def test_one_courier(self):
        courier = Courier('Courier1', Point(3, 4))
        couriers = [courier]
        order = Order('Order1', 6, 8, 0)
        plan = {courier.name: [order]}
        full_path = get_full_plan_path(plan, couriers)
        self.assertEqual(full_path, 15)


if __name__ == '__main__':
    unittest.main()

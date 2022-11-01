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

    def test_one_courier_two_orders(self):
        courier = Courier('Courier1', Point(3, 4))
        couriers = [courier]
        order_1 = Order('Order1', 6, 8, 0)
        order_2 = Order('Order2', 1, 0, 0)
        plan = {courier.name: [order_1, order_2]}
        full_path = get_full_plan_path(plan, couriers)
        self.assertEqual(full_path, 17)


if __name__ == '__main__':
    unittest.main()

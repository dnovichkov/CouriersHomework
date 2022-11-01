import math

import plotly.graph_objects as go
# import streamlit as st


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_distance_to_other(self, other_point):
        order_distance = math.dist((self.x, self.y), (other_point.x, other_point.y))
        return order_distance

    def get_distance_to_center(self):
        return self.get_distance_to_other(Point(0, 0))


class Courier:
    def __init__(self, name: str, point: Point):
        self.name = name
        self.point = point

    def __str__(self):
        return self.name


class Order:
    def __init__(self, name: str, x, y, price=0):
        self.name = name
        self.point = Point(x, y)
        self.price = price

    def __repr__(self):
        return self.name


def load_couriers():
    # Можно читать из файла
    _couriers = \
        [
            ("Курьер 1", 2, 2),
            ("Курьер 2", 7, 7),
            ("Курьер 3", 5, 5),
            ("Курьер 4", 21, 21),
        ]

    return [Courier(_c[0], Point(_c[1], _c[2])) for _c in _couriers]


def load_orders():
    _orders = \
        [
            ("A", 1, 1),
            ("B", 3, 3),
            ("C", 8, 5),
            ("D", 6, 6),
        ]

    return [Order(order[0], order[1], order[2], 0) for order in _orders]


def show_plot(orders, couriers):
    """
    Рисует расположение заказов и курьеров
    Запускать надо из терминала: streamlit run main.py
    :param orders:
    :param couriers:
    :return:
    """
    st.set_page_config(layout='wide')
    st.title('Тест-курьеры')
    st.subheader('Точки')
    fig = go.Figure()

    for name, x, y in zip(
            [point[0] for point in orders],
            [point[1] for point in orders],
            [point[2] for point in orders]
    ):
        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                name=name,
                mode='markers+text',
                marker=dict(size=20),
                text=name,
                marker_symbol=17
            )
        )

    for name, x, y in zip(
            [point[0] for point in couriers],
            [point[1] for point in couriers],
            [point[2] for point in couriers]
    ):
        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                name=name,
                mode='markers',
                marker=dict(size=20),
                marker_symbol=0
            )
        )
    fig['layout'].update(width=2000, height=1000, autosize=False)
    fig.update_layout(legend=dict(font=dict(family="Courier", size=50, color="black")))

    st.plotly_chart(fig)


def calculate_plan(couriers, orders):
    """
    Формирует план без учета истории перемещений курьера (неверно)
    :param couriers:
    :param orders:
    :return:
    """
    couriers_plan = {}
    for i in range(1):
        print(f'Запустили итерацию {i}')
        for order in orders:
            print(f'Ищем курьера для заказа {order}')
            order_distance = order.point.get_distance_to_center()
            print(f'Расстояние до центра составляет {order_distance}')

            possible_courier = None

            min_full_distance = 0
            for courier in couriers:
                print(f'Пробуем курьера {courier}')

                courier_distance = courier.point.get_distance_to_other(order.point)

                print(f'Суммарное расстояние до заказа составляет {courier_distance}')

                fill_distance = courier_distance + order_distance
                print(f'Полное расстояние для заказа составляет {fill_distance}')
                if min_full_distance == 0 or min_full_distance > fill_distance:
                    possible_courier = courier
                    min_full_distance = fill_distance
            print(f'Для заказа {order} лучший курьер - {possible_courier}')
            if possible_courier and possible_courier.name not in couriers_plan:
                couriers_plan[possible_courier.name] = []
            couriers_plan[possible_courier.name].append(order)
    return couriers_plan


def calculate_plan_using_full_path_couriers_orders(couriers, orders):
    """
    Формирует план с учетом истории перемещения курьера - курьеры ищут себе заказы
    :param couriers:
    :param orders:
    :return:
    """
    couriers_plan = {}

    for courier in couriers:
        print(f'Пробуем курьера {courier}')
        # print(f'Ищем курьера для заказа {order}')

        for order in orders:

            order_distance = order.point.get_distance_to_center()
            print(f'Расстояние до центра составляет {order_distance}')

            possible_courier = None

            min_full_distance = 0

            print(f'Пробуем курьера {courier}')
            print(f'Ищем курьера для заказа {order}')
            courier_name = courier.name
            courier_distance = courier.point.get_distance_to_other(order.point)

            if courier_name in couriers_plan:
                # Курьер уже выполнил какой-то заказ и теперь находится в точке (0;0),
                # чтобы его доставить, надо сходить туда-обратно
                courier_distance = order_distance

                couriers_orders = couriers_plan[courier_name]

                # Надо посмотреть, какой путь он уже проделал
                for order_number, visited_order in enumerate(couriers_orders):
                    visited_order_distance = visited_order.point.get_distance_to_center()

                    # Добавляем в пройденный путь то, как мы шли с заказом
                    courier_distance += visited_order_distance

                    if order_number == 0:
                        # За первым заказом мы ходили из начальной точки курьера
                        courier_distance += courier.point.get_distance_to_other(visited_order.point)
                    else:
                        # За остальными заказами мы ходили из точки (0;0
                        courier_distance += visited_order_distance

            print(f'Суммарное расстояние до заказа составляет {courier_distance}')

            fill_distance = courier_distance + order_distance
            print(f'Полное расстояние для заказа составляет {fill_distance}')
            if min_full_distance == 0 or min_full_distance > fill_distance:
                possible_courier = courier
                min_full_distance = fill_distance
        print(f'Для заказа {order} лучший курьер - {possible_courier} с расстоянием {min_full_distance}')
        if possible_courier.name not in couriers_plan:
            couriers_plan[possible_courier.name] = []
        couriers_plan[possible_courier.name].append(order)
    return couriers_plan


def calculate_plan_using_full_path_order_couriers(couriers, orders):
    """
    Формирует план с учетом истории перемещения курьера - заказы ищут себе размещение
    :param couriers:
    :param orders:
    :return:
    """
    couriers_plan = {}

    for order in orders:
        print(f'Ищем курьера для заказа {order}')

        order_distance = order.point.get_distance_to_center()
        print(f'Расстояние до центра составляет {order_distance}')

        possible_courier = None

        min_full_distance = 0
        for courier in couriers:
            print(f'Пробуем курьера {courier}')
            courier_name = courier.name
            courier_distance = courier.point.get_distance_to_other(order.point)

            if courier_name in couriers_plan:
                # Курьер уже выполнил какой-то заказ и теперь находится в точке (0;0),
                # чтобы его доставить, надо сходить туда-обратно
                courier_distance = order_distance

                couriers_orders = couriers_plan[courier_name]

                # Надо посмотреть, какой путь он уже проделал
                for order_number, visited_order in enumerate(couriers_orders):
                    visited_order_distance = visited_order.point.get_distance_to_center()

                    # Добавляем в пройденный путь то, как мы шли с заказом
                    courier_distance += visited_order_distance

                    if order_number == 0:
                        # За первым заказом мы ходили из начальной точки курьера
                        courier_distance += courier.point.get_distance_to_other(visited_order.point)
                    else:
                        # За остальными заказами мы ходили из точки (0;0
                        courier_distance += visited_order_distance

            print(f'Суммарное расстояние до заказа составляет {courier_distance}')

            fill_distance = courier_distance + order_distance
            print(f'Полное расстояние для заказа составляет {fill_distance}')
            if min_full_distance == 0 or min_full_distance > fill_distance:
                possible_courier = courier
                min_full_distance = fill_distance
        print(f'Для заказа {order} лучший курьер - {possible_courier} с расстоянием {min_full_distance}')
        if possible_courier.name not in couriers_plan:
            couriers_plan[possible_courier.name] = []
        couriers_plan[possible_courier.name].append(order)
    return couriers_plan


def get_full_plan_path(plan, couriers):
    full_path = 0
    for courier in couriers:
        name = courier.name
        if name not in plan:
            continue
        for number, order in enumerate(plan[name]):
            # Добавляем в пройденный путь то, как мы шли с заказом
            full_path += order.point.get_distance_to_center()

            if number == 0:
                # За первым заказом мы ходили из начальной точки курьера
                full_path += courier.point.get_distance_to_other(order.point)
            else:
                # За остальными заказами мы ходили из точки (0;0
                full_path += order.point.get_distance_to_center()

    return full_path


def main():
    couriers = load_couriers()
    orders = load_orders()
    # show_plot(orders, couriers)

    # Ключ - имя курьера, значение - его заказы
    couriers_plan = calculate_plan(couriers, orders)

    print(f'{couriers_plan=}')
    plan_distance = get_full_plan_path(couriers_plan, couriers)
    print(f'{plan_distance=}')

    expected_plan = {'Курьер 1': [Order('A', 1, 1), Order('B', 3, 3)], 'Курьер 2': [Order('C', 8, 5), Order('D', 6, 6)]}
    print(expected_plan == couriers_plan)

    print("Запускаем расчет плана с историей перемещений")

    couriers_plan_using_full_path_order_couriers = calculate_plan_using_full_path_order_couriers(couriers, orders)
    best_plan = {'Курьер 1': [('A', 1, 1), ('D', 6, 6)], 'Курьер 3': [('B', 3, 3)], 'Курьер 2': [('C', 8, 5)]}
    print(f'{couriers_plan_using_full_path_order_couriers=}')
    print(expected_plan == couriers_plan_using_full_path_order_couriers)
    print(best_plan == couriers_plan_using_full_path_order_couriers)
    best_plan_distance_order_couriers = get_full_plan_path(couriers_plan_using_full_path_order_couriers, couriers)
    print(f'{best_plan_distance_order_couriers=}')
    print(f'{plan_distance=}')

    print("Запускаем расчет плана с историей перемещений - сначала курьеры")
    couriers_plan_using_full_path_couriers_orders = calculate_plan_using_full_path_couriers_orders(couriers, orders)
    best_plan = {'Курьер 1': [Order('A', 1, 1), Order('D', 6, 6)], 'Курьер 3': [Order('B', 3, 3)], 'Курьер 2': [Order('C', 8, 5)]}
    print(f'{couriers_plan_using_full_path_couriers_orders=}')
    print(expected_plan == couriers_plan_using_full_path_couriers_orders)
    print(best_plan == couriers_plan_using_full_path_order_couriers)
    best_plan_distance_couriers_orders = get_full_plan_path(couriers_plan_using_full_path_couriers_orders, couriers)
    print(f'{best_plan_distance_couriers_orders=}')
    print(f'{best_plan_distance_order_couriers=}')
    print(f'{plan_distance=}')

    possible_best_plan = {
        'Курьер 1': [Order('B', 3, 3), Order('A', 1, 1)],
        'Курьер 2': [Order('C', 8, 5)],
        'Курьер 3': [Order('D', 6, 6)],
    }
    possible_best_plan_distance = get_full_plan_path(possible_best_plan, couriers)
    print(f'{possible_best_plan_distance=}')


if __name__ == '__main__':
    main()


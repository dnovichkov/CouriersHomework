import math

import plotly.graph_objects as go
import streamlit as st


def load_couriers():
    _couriers = \
        [
            ("Курьер 1", 2, 2),
            ("Курьер 2", 7, 7),
            ("Курьер 3", 5, 5),
            ("Курьер 4", 21, 21),
        ]
    return _couriers


def load_orders():
    _orders = \
        [
            ("A", 1, 1),
            ("B", 3, 3),
            ("C", 8, 5),
            ("D", 6, 6),
        ]
    return _orders


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
                mode='markers',
                marker=dict(size=20),
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
            order_x = order[1]
            order_y = order[2]
            order_distance = math.dist((order_x, order_y), (0, 0))
            print(f'Расстояние до центра составляет {order_distance}')

            possible_courier = None

            min_full_distance = 0
            for courier in couriers:
                print(f'Пробуем курьера {courier}')

                courier_x = courier[1]
                courier_y = courier[2]
                courier_distance = math.dist((courier_x, courier_y), (order_x, order_y))

                print(f'Суммарное расстояние до заказа составляет {courier_distance}')

                fill_distance = courier_distance + order_distance
                print(f'Полное расстояние для заказа составляет {fill_distance}')
                if min_full_distance == 0 or min_full_distance > fill_distance:
                    possible_courier = courier
                    min_full_distance = fill_distance
            print(f'Для заказа {order} лучший курьер - {possible_courier}')
            if possible_courier[0] not in couriers_plan:
                couriers_plan[possible_courier[0]] = []
            couriers_plan[possible_courier[0]].append(order)
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

            order_x = order[1]
            order_y = order[2]
            order_distance = math.dist((order_x, order_y), (0, 0))
            print(f'Расстояние до центра составляет {order_distance}')

            possible_courier = None

            min_full_distance = 0

            print(f'Пробуем курьера {courier}')
            print(f'Ищем курьера для заказа {order}')
            courier_name = courier[0]

            courier_x = courier[1]
            courier_y = courier[2]
            courier_distance = math.dist((courier_x, courier_y), (order_x, order_y))

            if courier_name in couriers_plan:
                # Курьер уже выполнил какой-то заказ и теперь находится в точке (0;0),
                # чтобы его доставить, надо сходить туда-обратно
                courier_distance = order_distance

                couriers_orders = couriers_plan[courier_name]

                # Надо посмотреть, какой путь он уже проделал
                for order_number, visited_order in enumerate(couriers_orders):
                    visited_order_distance = math.dist((visited_order[1], visited_order[2]), (0, 0))

                    # Добавляем в пройденный путь то, как мы шли с заказом
                    courier_distance += visited_order_distance

                    if order_number == 0:
                        # За первым заказом мы ходили из начальной точки курьера
                        courier_distance += math.dist((courier_x, courier_y),
                                                         (visited_order[1], visited_order[2]))
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
        if possible_courier[0] not in couriers_plan:
            couriers_plan[possible_courier[0]] = []
        couriers_plan[possible_courier[0]].append(order)
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

        order_x = order[1]
        order_y = order[2]
        order_distance = math.dist((order_x, order_y), (0, 0))
        print(f'Расстояние до центра составляет {order_distance}')

        possible_courier = None

        min_full_distance = 0
        for courier in couriers:
            print(f'Пробуем курьера {courier}')
            courier_name = courier[0]

            courier_x = courier[1]
            courier_y = courier[2]
            courier_distance = math.dist((courier_x, courier_y), (order_x, order_y))

            if courier_name in couriers_plan:
                # Курьер уже выполнил какой-то заказ и теперь находится в точке (0;0),
                # чтобы его доставить, надо сходить туда-обратно
                courier_distance = order_distance

                couriers_orders = couriers_plan[courier_name]

                # Надо посмотреть, какой путь он уже проделал
                for order_number, visited_order in enumerate(couriers_orders):
                    visited_order_distance = math.dist((visited_order[1], visited_order[2]), (0, 0))

                    # Добавляем в пройденный путь то, как мы шли с заказом
                    courier_distance += visited_order_distance

                    if order_number == 0:
                        # За первым заказом мы ходили из начальной точки курьера
                        courier_distance += math.dist((courier_x, courier_y),
                                                         (visited_order[1], visited_order[2]))
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
        if possible_courier[0] not in couriers_plan:
            couriers_plan[possible_courier[0]] = []
        couriers_plan[possible_courier[0]].append(order)
    return couriers_plan


def get_full_plan_path(plan, couriers):
    full_path = 0
    for courier in couriers:
        name = courier[0]
        courier_x = courier[1]
        courier_y = courier[2]
        if name not in plan:
            continue
        for number, order in enumerate(plan[name]):
            # Добавляем в пройденный путь то, как мы шли с заказом
            full_path += math.dist((order[1], order[2]), (0, 0))

            if number == 0:
                # За первым заказом мы ходили из начальной точки курьера
                full_path += math.dist((courier_x, courier_y),
                                                    (order[1], order[2]))
            else:
                # За остальными заказами мы ходили из точки (0;0
                full_path += math.dist((order[1], order[2]), (0, 0))

    return full_path


def main():
    couriers = load_couriers()
    orders = load_orders()
    show_plot(orders, couriers)

    # Ключ - имя курьера, значение - его заказы
    couriers_plan = calculate_plan(couriers, orders)

    print(f'{couriers_plan=}')
    plan_distance = get_full_plan_path(couriers_plan, couriers)
    print(f'{plan_distance=}')

    expected_plan = {'Курьер 1': [('A', 1, 1), ('B', 3, 3)], 'Курьер 2': [('C', 8, 5), ('D', 6, 6)]}
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
    best_plan = {'Курьер 1': [('A', 1, 1), ('D', 6, 6)], 'Курьер 3': [('B', 3, 3)], 'Курьер 2': [('C', 8, 5)]}
    print(f'{couriers_plan_using_full_path_couriers_orders=}')
    print(expected_plan == couriers_plan_using_full_path_couriers_orders)
    print(best_plan == couriers_plan_using_full_path_order_couriers)
    best_plan_distance_couriers_orders = get_full_plan_path(couriers_plan_using_full_path_couriers_orders, couriers)
    print(f'{best_plan_distance_couriers_orders=}')
    print(f'{best_plan_distance_order_couriers=}')
    print(f'{plan_distance=}')

    possible_best_plan = {
        'Курьер 1': [('B', 3, 3), ('A', 1, 1)],
        'Курьер 2': [('C', 8, 5)],
        'Курьер 3': [('D', 6, 6)],
    }
    possible_best_plan_distance = get_full_plan_path(possible_best_plan, couriers)
    print(f'{possible_best_plan_distance=}')


if __name__ == '__main__':
    main()


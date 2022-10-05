import math

import plotly.graph_objects as go
import streamlit as st


def load_couriers():
    _couriers = \
        [
            ("Курьер 1", 2, 2),
            ("Курьер 2", 13, 7),
            ("Курьер 3", 20, 20),
            ("Курьер 4", 21, 21),
        ]
    return _couriers


def load_orders():
    _orders = \
        [
            ("A", 1, 1),
            ("B", 3, 1),
            ("C", 8, 5),
            ("D", 6, 0),
        ]
    return _orders


def show_plot(orders, couriers):
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


if __name__ == '__main__':

    couriers = load_couriers()
    orders = load_orders()
    show_plot(orders, couriers)

    # Ключ - имя курьера, значение - его заказы
    couriers_plan = {}

    # Количество заказов, которое может быть на одном курьере - столько раз мы будем пытаться улучшить расписание
    max_iteration_count = len(orders)
    for i in range(1):
        print(f'Запустили итерацию {i}')
        for order in orders:
            print(f'Ищем курьера для заказа {order}')
            order_name = order[0]
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
                print(f'Расстояние до заказа составляет {courier_distance}')

                fill_distance = courier_distance + order_distance
                print(f'Полное расстояние для заказа составляет {fill_distance}')
                if min_full_distance == 0 or min_full_distance > fill_distance:
                    possible_courier = courier
                    min_full_distance = fill_distance
            print(f'Для заказа {order} лучший курьер - {possible_courier}')
            if possible_courier[0] not in couriers_plan:
                couriers_plan[possible_courier[0]] = []
            couriers_plan[possible_courier[0]].append(order)
    print(couriers_plan)

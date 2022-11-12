# coding: utf-8
# license: GPLv3

import numpy as np

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.

    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5
        r = max(r, body.R) # FIXME: обработка аномалий при прохождении одного тела сквозь другое
        F = (gravitational_constant * body.m * obj.m)/(r**2)
        if body.x > obj.x and body.y > obj.y: # 1 четверть
            alpha = np.arctan((body.x - obj.x)/(body.y - obj.y))
            body.Fx+=(-F)*np.sin(alpha)
            body.Fy+=(-F)*np.cos(alpha)
        if body.x < obj.x and body.y > obj.y: # 2 четверть
            alpha = np.arctan((obj.x - body.x)/(body.y - obj.y))
            body.Fx+=F*np.sin(alpha)
            body.Fy+=(-F)*np.cos(alpha)
        if body.x < obj.x and body.y < obj.y: # 3 четверть
            alpha = np.arctan((obj.x - body.x)/(obj.y - body.y))
            body.Fx+=F*np.sin(alpha)
            body.Fy+=F*np.cos(alpha)
        if body.x > obj.x and body.y < obj.y: # 4 четверть
            alpha = np.arctan((body.x - obj.x)/(obj.y - body.y))
            body.Fx+=(-F)*np.sin(alpha)
            body.Fy+=F*np.cos(alpha)
        if body.x == obj.x:
            if body.y > obj.y:
                body.Fy+=(-F)
            else:
                body.Fy+=F
        if body.y == obj.y:
            if body.x > obj.x:
                body.Fx+=(-F)
            else:
                body.Fx+=F
    
def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """

    ax = body.Fx/body.m
    body.Vx += ax * dt
    body.x += body.Vx * dt
    ay = body.Fy/body.m
    body.Vy += ay * dt
    body.y += body.Vy * dt
    
def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")

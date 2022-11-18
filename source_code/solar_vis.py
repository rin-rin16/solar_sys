# coding: utf-8
# license: GPLv3

import pygame as pg

"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие гaрафические объекты и перемещающие их на экране, принимают физические координаты
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

window_width = 900
"""Ширина окна"""

window_height = 1200   # там было 12, но с 1200 оно вроде работает лучше
"""Высота окна"""

class ScFac:
    """Класс для "глобальной" числовой переменной, использующейся в solar_vis"""
    def __init__(self):
        self.fac = 1

    def setting(self, arg):
        self.fac = arg

    def read(self):
        return self.fac


scale_factor = ScFac()          # Масштабирование экранных координат по отношению к физическим. Тип: float. Мера: количество пикселей на один метр.


def calculate_scale_factor(max_distance):
    """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине"""
    scale_factor.setting(0.5*min(window_height, window_width)/max_distance)
    print('Scale factor:', scale_factor.read())


def scale_x(x):
    """Возвращает экранную **x** координату по **x** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **x** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.

    Параметры:

    **x** — x-координата модели.
    """

    return int(x*scale_factor.read()) + window_width//2 + 37


def scale_y(y):
    """Возвращает экранную **y** координату по **y** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **y** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.
    Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

    Параметры:

    **y** — y-координата модели.
    """
    return -int(y*scale_factor.read()) + window_height//2 - 150



if __name__ == "__main__":
    print("This module is not for direct call!")


class Drawer:
    def __init__(self, screen):
        self.screen = screen


    def update(self, figures, ui):
        self.screen.fill((0, 0, 0))
        for figure in figures:
            figure.draw(self.screen)
        
        ui.blit()
        ui.update()
        pg.display.update()


class DrawableObject:
    def __init__(self, obj):
        self.obj = obj

    def draw(self, surface):
        """Рисует выбранный объект"""
        pg.draw.circle(surface, self.obj.color, (scale_x(self.obj.x), scale_y(self.obj.y)), self.obj.R)

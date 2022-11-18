# coding: utf-8
# license: GPLv3


class Star:
    """Тип данных, описывающий звезду.
    Принимает на вход массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """
    type = "Star"

    def __init__(self, R, color, m, x, y, Vx, Vy):
        self.R = int(R)
        self.color = color
        self.m = float(m)
        self.x = float(x)
        self.y = float(y)
        self.Vx = float(Vx)
        self.Vy = float(Vy)


class Planet:
    """Тип данных, описывающий планету.
    Принимает на вход массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет
    """
    type = "Planet"

    def __init__(self, R, color, m, x, y, Vx, Vy):
        self.R = int(R)
        self.color = color
        self.m = float(m)
        self.x = float(x)
        self.y = float(y)
        self.Vx = float(Vx)
        self.Vy = float(Vy)
       
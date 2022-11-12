# coding: utf-8
# license: GPLv3


class Star:
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """

    type = "star"
    """Признак объекта звезды"""

    m = 1
    """Масса звезды"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 5
    """Радиус звезды"""

    color = "red"
    """Цвет звезды"""
    
    def __init__(self, R, color, m, x, y, Vx, Vy):
        self.R = int(R)
        self.color = color
        self.m = float(m)
        self.x = float(x)
        self.y = float(y)
        self.Vx = float(Vx)
        self.Vy = float(Vy)

    def ret_kwargs(self):
        """Returns kwargs of stars"""
        return {self.R : self.R, self.color : self.color, self.m : self.m, self.x : self.x,
                self.y : self.y, self.Vx : self.Vx, self.Vy : self.Vy}

class Planet:
    """Тип данных, описывающий планету.
    Содержит массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет
    """

    type = "planet"
    """Признак объекта планеты"""

    m = 1
    """Масса планеты"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 5
    """Радиус планеты"""

    color = "green"
    """Цвет планеты"""

    def __init__(self, R, color, m, x, y, Vx, Vy):
        self.R = int(R)
        self.color = color
        self.m = float(m)
        self.x = float(x)
        self.y = float(y)
        self.Vx = float(Vx)
        self.Vy = float(Vy)

    def ret_kwargs(self):
        """Returns kwargs of planets"""
        return {self.R : self.R, self.color : self.color, self.m : self.m, self.x : self.x,
                self.y : self.y, self.Vx : self.Vx, self.Vy : self.Vy}
# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet
from solar_vis import DrawableObject
from solar_main import space_objects

def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем

            object_type = line.split()[0].lower()
            if object_type == "star":
                star = parse_star_parameters(line)
                objects.append(star)
            elif object_type == "planet":
                planet = parse_planet_parameters(line)
                objects.append(planet)
            else:
                print("Unknown space object")

    return [DrawableObject(obj) for obj in objects]


def parse_star_parameters(line):
    """Считывает данные о звезде из строки.

    Входная строка должна иметь слеюущий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.

    Пример строки:

    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.

    **star** — объект звезды.
    """
    
    sp_line = line.split()
    qwargs = {'R':sp_line[1], 'color':sp_line[2], 'm':sp_line[3], 'x':sp_line[4], 'y':sp_line[5], 'Vx':sp_line[6], 'Vy':sp_line[7]}
    star = Star(**qwargs)
    return (star)


def parse_planet_parameters(line):
    """Считывает данные о планете из строки.
    Входная строка должна иметь слеюущий формат:

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.

    Пример строки:

    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.

    **planet** — объект планеты.
    """
    
    sp_line = line.split()
    qwargs = {'R':sp_line[1], 'color':sp_line[2], 'm':sp_line[3], 'x':sp_line[4], 'y':sp_line[5], 'Vx':sp_line[6], 'Vy':sp_line[7]}
    planet = Planet(**qwargs)
    return (planet)

def write_space_objects_data_to_file(space_objects):
    """Сохраняет данные о космических объектах в файл.

    Строки должны иметь следующий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла

    **space_objects** — список объектов планет и звёзд
    """
    with open('output.txt', 'w') as out_file:
        print(space_objects)



if __name__ == "__main__":
    print("This module is not for direct call!")

def te():
    print('HI!')

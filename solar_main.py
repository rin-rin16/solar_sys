# coding: utf-8
# license: GPLv3

import pygame as pg
from solar_vis import *
from solar_model import *
from solar_input import *
from solar_objects import *
from solar_stats import *
import thorpy
import time

class NumVariables:
    """Класс, в котором хранятся "глобальные" числовые переменные, использующиеся в main_py"""
    def __init__(self):
        self.count = 0

    def adding(self, arg):
        self.count += arg

    def setting(self, arg):
        self.count = arg

    def read(self):
       return self.count


class BullVariables:
    """Класс, в котором хранятся "глобальные" булевы переменные, использующиеся в main_py"""
    def __init__(self):
        self.bull = True

    def bullTrue(self):
        self.bull = True

    def bullFalse(self):
        self.bull = False

    def read(self):
        return self.bull


class ListVariables:
    """Класс, в котором хранятся "глобальные" переменные типа список, использующиеся в main_py"""

    def __init__(self):
        self.list = []

    def transform(self, thelist):
        self.list = thelist

    def appending(self, el):
        self.list.append(el)

    def read(self):
        return self.list


perform_execution = BullVariables()     # Флаг цикличности выполнения расчёта             # Объявляю "глобальные" переменные
alive = BullVariables()                 # Отвечает за выход из симуляции

time_scale = NumVariables()             # Шаг по времени при моделировании. Тип: float
time_scale.setting(1000)
model_time = NumVariables()             # Физическое время от начала расчёта. Тип: float

space_objects = ListVariables()         # Список космических объектов
t_list = ListVariables()                # Переменные для сохранения статистики данных
xs_list = ListVariables()
ys_list = ListVariables()
Vxs_list = ListVariables()
Vys_list = ListVariables()
xp_list = ListVariables()
yp_list = ListVariables()
Vxp_list = ListVariables()
Vyp_list = ListVariables()

def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    recalculate_space_objects_positions([dr.obj for dr in space_objects.read()], delta)
    model_time.adding(delta)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    perform_execution.bullTrue()

def pause_execution():
    """Обработчик события нажатия на кнопку Pause.
    Приостанавливает циклическое исполнение функции execution.
    """
    perform_execution.bullFalse()

def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    alive.bullFalse()

def open_file():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    model_time.setting(0)
    in_filename = "one_satellite.txt"
    space_objects.transform(read_space_objects_data_from_file(in_filename))
    max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in space_objects.read()])
    calculate_scale_factor(max_distance)

def write_file():
    """Применяет функцию, выводящую координаты, с выбранными параметрами"""
    write_space_objects_data_to_file('output.txt', space_objects.read())

def out_stat():
    """Применяет функцию, выводящую статистику, с выбранными параметрами"""
    output_statistics(t_list, xs_list, ys_list, Vxs_list, Vys_list, xp_list, yp_list, Vxp_list, Vyp_list)

def handle_events(events, menu):
    for event in events:
        menu.react(event)
        if event.type == pg.QUIT:
            alive.bullFalse()

def slider_to_real(val):
    return np.exp(5 + val)

def slider_reaction(event):
    time_scale.setting(slider_to_real(event.el.get_value()))

def init_ui(screen):
    slider = thorpy.SliderX(100, (-10, 10), "Simulation speed")
    slider.user_func = slider_reaction
    button_stop = thorpy.make_button("Quit", func=stop_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    button_play = thorpy.make_button("Play", func=start_execution)
    timer = thorpy.OneLineText("Seconds passed")

    button_load = thorpy.make_button(text="Load a file", func=open_file)
    button_write = thorpy.make_button(text="Output file", func=write_file)
    button_statistics = thorpy.make_button(text="Statistics", func=out_stat)

    box = thorpy.Box(elements=[
        slider,
        button_pause, 
        button_stop, 
        button_play, 
        button_load,
        button_write,
        button_statistics,
        timer])
    reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=slider_reaction,
                                event_args={"id":thorpy.constants.EVENT_SLIDE},
                                params={},
                                reac_name="slider reaction")
    box.add_reaction(reaction1)
    
    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((0,0))
    box.blit()
    box.update()
    return menu, box, timer

def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """

    print('Modelling started!')

    pg.init()
    
    width = 1000
    height = 900
    screen = pg.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = Drawer(screen)
    menu, box, timer = init_ui(screen)
    perform_execution.bullTrue()

    while alive.read():
        handle_events(pg.event.get(), menu)
        cur_time = time.perf_counter()
        if perform_execution.read():
            execution((cur_time - last_time) * time_scale.read())
            text = "%d seconds passed" % (int(model_time.read()))
            timer.set_text(text)
            save_statistics(model_time.read(), t_list, xs_list, ys_list, Vxs_list, Vys_list,
                            xp_list, yp_list, Vxp_list, Vyp_list, space_objects)

        last_time = cur_time
        drawer.update(space_objects.read(), box)
        time.sleep(1.0 / 60)

    dist_t_plot(t_list, xs_list, ys_list, xp_list, yp_list)
    print('Modelling finished!')

if __name__ == "__main__":
    main()
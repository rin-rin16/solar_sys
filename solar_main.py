# coding: utf-8
# license: GPLv3

import source_code.solar_vis as vis
import source_code.solar_model as model
import source_code.solar_input as input
import source_code.solar_stats as stats
import numpy as np
import thorpy as thorpy
import time

class NumVariables:
    """Класс, в котором хранятся "глобальные" числовые переменные, использующиеся в main_py"""
    def __init__(self):
        self.count = 0

    def adder(self, arg):
        self.count += arg

    def setter(self, arg):
        self.count = arg

    def getter(self):
       return self.count


class BullVariables:
    """Класс, в котором хранятся "глобальные" булевы переменные, использующиеся в main_py"""
    def __init__(self):
        self.bull = True

    def bullTrue(self):
        self.bull = True

    def bullFalse(self):
        self.bull = False

    def getter(self):
        return self.bull


class ListVariables:
    """Класс, в котором хранятся "глобальные" переменные типа list, использующиеся в main_py"""

    def __init__(self):
        self.list = []

    def transform(self, thelist):
        self.list = thelist

    def appender(self, el):
        self.list.append(el)

    def getter(self):
        return self.list

class StringVariables():
    """Класс, в котором хранятся "глобальные" переменные типа string, использующиеся в main_py"""
    def __init__(self):
        self.str = ""

    def setter(self, arg):
        self.str = str(arg)

    def getter(self):
        return self.str


perform_execution = BullVariables()     # Флаг цикличности выполнения расчёта             # Объявляю "глобальные" переменные
alive = BullVariables()                 # Отвечает за выход из симуляции

time_scale = NumVariables()             # Шаг по времени при моделировании. Тип: float
time_scale.setter(1000)
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

File_Name = StringVariables()           # Имя файла, который будет моделироваться

def sol_sys_init():
    """Запускает файл солнеченой системы"""
    File_Name.setter("systems/solar_system.txt")
    perform_execution.bullFalse()

def double_star_init():
    """Запускает файл двойной звезды"""
    File_Name.setter("systems/double_star.txt")
    perform_execution.bullFalse()

def one_sat_init():
    """Запускает файл одного спутника"""
    File_Name.setter("systems/one_satellite.txt")
    perform_execution.bullFalse()

def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    model.recalculate_space_objects_positions([dr.obj for dr in space_objects.getter()], delta)
    model_time.adder(delta)


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

def open_file(File_Name):
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    model_time.setter(0)
    in_filename = File_Name.getter()
    space_objects.transform(input.read_space_objects_data_from_file(in_filename))
    max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in space_objects.getter()])
    vis.calculate_scale_factor(max_distance)

def write_file():
    """Применяет функцию, выводящую координаты, с выбранными параметрами"""
    input.write_space_objects_data_to_file('output/output.txt', space_objects.getter())

def out_stat():
    """Применяет функцию, выводящую статистику, с выбранными параметрами"""
    stats.output_statistics(t_list, xs_list, ys_list, Vxs_list, Vys_list, xp_list, yp_list, Vxp_list, Vyp_list)

def handle_events(events, menu):
    for event in events:
        menu.react(event)
        if event.type == vis.pg.QUIT:
            alive.bullFalse()

def Time_Factor(File_Name):
    """Возвращает числа в зависимости от того, какой файл запущен. Используется для уменьшения максимальной скорости
    симуляции системы двойной звезды

    Аргументы:

    Имя файла"""
    if File_Name.getter() == "systems/double_star.txt":
        return 15
    else:
        return 1

def slider_to_real(val):
    return np.exp(5 + val)

def slider_reaction(event):
    time_scale.setter(slider_to_real(event.el.get_value()))

def start_ui(screen):
    button_solar_sys = thorpy.make_button("Solar system", func=sol_sys_init)
    button_double_star = thorpy.make_button("Double star", func=double_star_init)
    button_one_sattelite = thorpy.make_button("One satellite", func=one_sat_init)

    box = thorpy.Box(elements=[
        button_solar_sys,
        button_double_star,
        button_one_sattelite])

    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((vis.window_width//2 - 25, vis.window_height//2 - 225))
    box.blit()
    box.update()
    return menu, box

def init_ui(screen):
    slider = thorpy.SliderX(100, (-10, 10), "Simulation speed")
    slider.user_func = slider_reaction
    button_stop = thorpy.make_button("Quit", func=stop_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    button_play = thorpy.make_button("Play", func=start_execution)
    timer = thorpy.OneLineText("Seconds passed")

    button_load = thorpy.make_button(text="Load a file", func=open_file, params={"File_Name": File_Name})
    button_write = thorpy.make_button(text="Output file", func=write_file)
    button_statistics = thorpy.make_button(text="Statistics", func=out_stat)

    if File_Name.getter() == "systems/one_satellite.txt":
        box = thorpy.Box(elements=[
            slider,
            button_pause,
            button_stop,
            button_play,
            button_load,
            button_write,
            button_statistics,
            timer])
    else:                               # Убирает из меню не работающую кнопку для систем, не являющихся одиночным спутником
        box = thorpy.Box(elements=[
            slider,
            button_pause,
            button_stop,
            button_play,
            button_load,
            button_write,
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

    vis.pg.init()
    
    width = 1000
    height = 900
    screen = vis.pg.display.set_mode((width, height))

    perform_execution.bullTrue()
    drawer = vis.Drawer(screen)
    menu, box = start_ui(screen)

    while perform_execution.getter():
        handle_events(vis.pg.event.get(), menu)
        drawer.update(space_objects.getter(), box)

    last_time = time.perf_counter()
    drawer = vis.Drawer(screen)
    menu, box, timer = init_ui(screen)
    perform_execution.bullTrue()

    while alive.getter():
        handle_events(vis.pg.event.get(), menu)
        cur_time = time.perf_counter()
        if perform_execution.getter():
            execution((cur_time - last_time) * time_scale.getter() / Time_Factor(File_Name))    # Уменьшаем максимальную скорость симуляции для
            text = "%d seconds passed" % (int(model_time.getter()))                             # двойной звезды
            timer.set_text(text)
            if File_Name.getter() == "systems/one_satellite.txt":       # Собираем статистику только для одиночного спутника
                stats.save_statistics(model_time.getter(), t_list, xs_list, ys_list, Vxs_list, Vys_list,
                                      xp_list, yp_list, Vxp_list, Vyp_list, space_objects)

        last_time = cur_time
        drawer.update(space_objects.getter(), box)
        time.sleep(1.0 / 60)

    if File_Name.getter() == "systems/one_satellite.txt":  # Выводим графики только для одиночного спутника
        stats.V_t_plot(t_list, Vxp_list, Vyp_list)
        stats.dist_t_plot(t_list, xs_list, ys_list, xp_list, yp_list)
        stats.V_dist_plot(xs_list, ys_list, xp_list, yp_list, Vxp_list, Vyp_list)

    print('Modelling finished!')

if __name__ == "__main__":
    main()
import numpy as np
import matplotlib.pyplot as plt

def save_statistics(time, t_list, xs_list, ys_list, Vxs_list,
                    Vys_list, xp_list, yp_list, Vxp_list, Vyp_list, space_objects):
    """Сохраняет статистику данных о космических объектах в виде списков.

    Параметры:

    Все списки, куда будут сохраняться данные, и список всех космических объектов
    """
    for obj in space_objects.read():
        if obj.obj.type == "Star":
            t_list.appending(time)
            xs_list.appending(obj.obj.x)
            ys_list.appending(obj.obj.y)
            Vxs_list.appending(obj.obj.Vx)
            Vys_list.appending(obj.obj.Vy)
        if obj.obj.type == "Planet":
            xp_list.appending(obj.obj.x)
            yp_list.appending(obj.obj.y)
            Vxp_list.appending(obj.obj.Vx)
            Vyp_list.appending(obj.obj.Vy)

def output_statistics(t_list, xs_list, ys_list, Vxs_list, Vys_list, xp_list, yp_list, Vxp_list, Vyp_list):
    """Выводит сохранённую статистику о спутнике и звезде

    Параметры:

    Все списки, содержащие статистику
    """
    with open("stats.txt", "w") as stat_file:
        print("Время: ", t_list.read(), "\n\n\n"                                 
              "Звезда: \n\n",
              "X: ", xs_list.read(), "\n\n",
              "Y: ", ys_list.read(), "\n\n",
              "Vx: ", Vxs_list.read(), "\n\n",
              "Vy: ", Vys_list.read(), "\n\n\n"
              "Планета: \n\n",
              "X: ", xp_list.read(), "\n\n",
              "Y: ", yp_list.read(), "\n\n",
              "Vx: ", Vxp_list.read(), "\n\n",
              "Vy: ", Vyp_list.read(),
              file=stat_file)

def dist_t_plot(t_list, xs_list, ys_list, xp_list, yp_list):
    dist_list = []
    for i in range(len(t_list.read())):
        dist_list.append(np.sqrt((xp_list.read()[i] - xs_list.read()[i])**2 +
                                 (yp_list.read()[i] - ys_list.read()[i])**2))
    plt.plot(t_list.read(), dist_list)
    plt.xlabel("t, s")
    plt.ylabel("Distance, m")
    plt.title("Distance vs Time")
    plt.show()

def V_dist_plot(xs_list, ys_list, xp_list, yp_list, Vxp_list, Vyp_list):
    dist_list = []
    V_list = []
    for i in range(len(xp_list.read())):
        dist_list.append(np.sqrt((xp_list.read()[i] - xs_list.read()[i])**2 +
                                 (yp_list.read()[i] - ys_list.read()[i])**2))
        V_list.append(np.sqrt(Vxp_list.read()[i]**2 +Vyp_list.read()[i]**2))
    plt.plot(dist_list, V_list)
    plt.xlabel("Distance, m")
    plt.ylabel("Speed, m/s")
    plt.title("Speed vs Distance")
    plt.show()
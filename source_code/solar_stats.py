import numpy as np
import matplotlib.pyplot as plt

def save_statistics(time, t_list, xs_list, ys_list, Vxs_list,
                    Vys_list, xp_list, yp_list, Vxp_list, Vyp_list, space_objects):
    """Сохраняет статистику данных о космических объектах в виде списков.

    Параметры:

    Все списки, куда будут сохраняться данные, и список всех космических объектов
    """
    for obj in space_objects.getter():
        if obj.obj.type == "Star":
            t_list.appender(time)
            xs_list.appender(obj.obj.x)
            ys_list.appender(obj.obj.y)
            Vxs_list.appender(obj.obj.Vx)
            Vys_list.appender(obj.obj.Vy)
        if obj.obj.type == "Planet":
            xp_list.appender(obj.obj.x)
            yp_list.appender(obj.obj.y)
            Vxp_list.appender(obj.obj.Vx)
            Vyp_list.appender(obj.obj.Vy)

def output_statistics(t_list, xs_list, ys_list, Vxs_list, Vys_list, xp_list, yp_list, Vxp_list, Vyp_list):
    """Выводит сохранённую статистику о спутнике и звезде

    Параметры:

    Все списки, содержащие статистику
    """
    with open("output/stats.txt", "w") as stat_file:
        print("Время: ", t_list.getter(), "\n\n\n"                                 
              "Звезда: \n\n",
              "X: ", xs_list.getter(), "\n\n",
              "Y: ", ys_list.getter(), "\n\n",
              "Vx: ", Vxs_list.getter(), "\n\n",
              "Vy: ", Vys_list.getter(), "\n\n\n"
              "Планета: \n\n",
              "X: ", xp_list.getter(), "\n\n",
              "Y: ", yp_list.getter(), "\n\n",
              "Vx: ", Vxp_list.getter(), "\n\n",
              "Vy: ", Vyp_list.getter(),
              file=stat_file)

def V_t_plot(t_list, Vxp_list, Vyp_list):
    V_list = []
    for i in range(len(t_list.getter())):
        V_list.append(np.sqrt(Vxp_list.getter()[i]**2 +Vyp_list.getter()[i]**2))
    plt.plot(t_list.getter(), V_list)
    plt.xlabel("t, s")
    plt.ylabel("Speed, m/s")
    plt.title("Speed vs Time")
    plt.show()

def dist_t_plot(t_list, xs_list, ys_list, xp_list, yp_list):
    dist_list = []
    for i in range(len(t_list.getter())):
        dist_list.append(np.sqrt((xp_list.getter()[i] - xs_list.getter()[i])**2 +
                                 (yp_list.getter()[i] - ys_list.getter()[i])**2))
    plt.plot(t_list.getter(), dist_list)
    plt.xlabel("t, s")
    plt.ylabel("Distance, m")
    plt.title("Distance vs Time")
    plt.show()

def V_dist_plot(xs_list, ys_list, xp_list, yp_list, Vxp_list, Vyp_list):
    dist_list = []
    V_list = []
    for i in range(len(xp_list.getter())):
        dist_list.append(np.sqrt((xp_list.getter()[i] - xs_list.getter()[i])**2 +
                                 (yp_list.getter()[i] - ys_list.getter()[i])**2))
        V_list.append(np.sqrt(Vxp_list.getter()[i]**2 +Vyp_list.getter()[i]**2))
    plt.plot(dist_list, V_list)
    plt.xlabel("Distance, m")
    plt.ylabel("Speed, m/s")
    plt.title("Speed vs Distance")
    plt.show()

if __name__ == "__main__":
    print("This module is not for direct call!")
from matplotlib import pylab as plt, animation as animation

from orbits import get_current_adalia_day, position_at_adalia_day, full_position

plt.style.use('dark_background')


def animate_single_orbit(rock, pos, frame_count):
    """
    Animates a single asteroid orbit around Adalia
    :param rock: asteroid as dict
    :param pos: list of xyz positions
    :param frame_count: amount of frames in animation
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.plot(pos[::, 1], pos[::, 0], 'c-')

    rock_name = rock['customName'] if rock['customName'] else rock['baseName']
    red_dot, = plt.plot(pos[0][1], pos[0][0], 'ro', label=rock_name)

    def animate(i):
        red_dot.set_data(pos[i][1], pos[i][0])
        return red_dot,

    # create animation using the animate() function
    my_animation = animation.FuncAnimation(fig, animate, frames=frame_count, interval=0.01, blit=True, repeat=True)
    plt.plot(0, 0, 'bo', markersize=9, label="Adalia")

    # Misc styling
    plt.title('Orbital Simulation')
    plt.axis('off')
    plt.legend(loc="upper right")
    plt.show()


def plot_asteroid_paths(*rocks):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    colors = ['r*', 'g*', 'b*', 'k*']

    ax.plot3D([0], [0], [0], 'bo', markersize=15, label="Adalia")
    curr_aday = get_current_adalia_day()

    for i, rock in enumerate(rocks):
        color = colors[i % len(colors)]
        rock_name = rock['customName'] if rock['customName'] else rock['baseName']
        cur_pos = position_at_adalia_day(rock, curr_aday)
        pos = full_position(rock)
        ax.plot3D([cur_pos[1]], [cur_pos[0]], [cur_pos[2]], color, markersize=10, label=rock_name)
        ax.plot3D(pos[::, 1], pos[::, 0], pos[::, 2], 'w-', alpha=0.5)

    # Misc styling
    ax.axis('off')
    plt.title('Orbital Simulation')
    plt.legend(loc="lower right")
    plt.show()

import matplotlib.animation as animation
import matplotlib.pylab as plt
from PyAstronomy import pyasl

plt.style.use('dark_background')


def setup_ellipse(rock):
    """
    Set up a PyAstronomy ellipse
    a: Semi-major axis
    e: Eccentricity
    i: Inclination
    o: Longitude of ascending node
    w: Argument of periapsis
    m: Mean anomoly at epoch
    T: orbital period (days)
    :param rock: asteroid as dict
    :return: KeplerEllipse object
    """
    ke = pyasl.KeplerEllipse(rock['orbital.a'],
                             rock['orbital.T'],
                             e=rock['orbital.e'],
                             Omega=rock['orbital.o'],
                             i=rock['orbital.i'],
                             w=rock['orbital.w'])
    return ke


def animate_single_orbit(rock, pos, frame_count):
    """
    Animates a single asteroid orbit around Adalia
    :param rock: asteroid as dict
    :param pos: list of xyz positions
    :param frame_count: amount of frames in animation
    """

    def animate(i, pos, asteroid_point):
        asteroid_point.set_data([pos[i][1], pos[i][0]])
        asteroid_point.set_3d_properties(pos[i][2])
        return asteroid_point,

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    rock_name = rock['customName'] if rock['customName'] else rock['baseName']
    asteroid_point, = ax.plot(pos[::, 1], pos[::, 0], pos[::, 2], 'ro', label=rock_name)

    # Set Adalia and orbit
    ax.plot([0], [0], [0], 'bo', markersize=9, label="Adalia")
    ax.plot(pos[::, 1], pos[::, 0], pos[::, 2], 'w-', label="Asteroid Trajectory")

    # create animation using the animate() function
    ani = animation.FuncAnimation(fig, animate, frame_count, fargs=(pos, asteroid_point), interval=0.01, blit=False)

    # Plot styling
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    plt.legend(loc="upper right")
    plt.show()

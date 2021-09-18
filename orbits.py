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
    plt.style.use('default')
    plt.title('Orbital Simulation')
    plt.axis('off')
    plt.legend(loc="upper right")
    plt.show()

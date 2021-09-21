import numpy as np
import plotly.graph_objects as go
from matplotlib import pylab as plt, animation as animation

from orbits import get_current_adalia_day, position_at_adalia_day, full_position

AU_multiplier = 150.18  # Astronomical Unit. 150.18 million kilometer.


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


def spheres(size, clr, dist=0):
    # Set up 100 points. First, do angles
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 100)

    # Set up coordinates for points on the sphere
    x0 = dist + size * np.outer(np.cos(theta), np.sin(phi))
    y0 = size * np.outer(np.sin(theta), np.sin(phi))
    z0 = size * np.outer(np.ones(100), np.cos(phi))

    # Set up trace
    trace = go.Surface(x=x0, y=y0, z=z0, colorscale=[[0, clr], [1, clr]])
    trace.update(showscale=False)

    return trace


def orbits(coordinates, clr='white', wdth=2):
    xcrd = coordinates[::, 0] * AU_multiplier
    ycrd = coordinates[::, 1] * AU_multiplier
    zcrd = coordinates[::, 2] * AU_multiplier

    trace = go.Scatter3d(x=xcrd, y=ycrd, z=zcrd, marker=dict(size=0.1), line=dict(color=clr, width=wdth))
    return trace


def annot(xcrd, zcrd, txt, xancr='center'):
    strng = dict(showarrow=False, x=xcrd, y=0, z=zcrd, text=txt, xanchor=xancr, font=dict(color='white', size=12))
    return strng


def plot_roids(rock):
    # Rock data
    curr_aday = get_current_adalia_day()
    cur_pos = position_at_adalia_day(rock, curr_aday)
    pos = full_position(rock)
    semi_major_axis = rock['orbital.a']

    # Setup
    print(rock['orbital.a'], semi_major_axis * AU_multiplier)
    distance_from_sun = [0, semi_major_axis * AU_multiplier]

    # Create spheres for the Sun and planets
    trace_adalia_sphere = spheres(20, '#ffffff', distance_from_sun[0])
    trace_rock_sphere = spheres(5, '#325bff', distance_from_sun[1])

    # Set up orbit traces
    trace_rock_orbit = orbits(pos)

    layout = go.Layout(title='Adalia System', showlegend=False, margin=dict(l=0, r=0, t=0, b=0),
                       scene=dict(xaxis=dict(title='Distance from Sun', titlefont_color='black',
                                             range=[-7000, 7000], backgroundcolor='black', color='black',
                                             gridcolor='black'),
                                  yaxis=dict(title='Distance from Sun', titlefont_color='black',
                                             range=[-7000, 7000], backgroundcolor='black', color='black',
                                             gridcolor='black'),
                                  zaxis=dict(title='', range=[-7000, 7000], backgroundcolor='black', color='white',
                                             gridcolor='black'),
                                  annotations=[annot(distance_from_sun[0], 40, 'Adalia', xancr='left')]
                                  ))

    fig = go.Figure(data=[trace_adalia_sphere, trace_rock_sphere, trace_rock_orbit], layout=layout)

    fig.show()

import numpy as np
import plotly.graph_objects as go
from matplotlib import pylab as plt, animation as animation

from orbits import get_current_adalia_day, position_at_adalia_day, full_position

AU_MULTIPLIER = 150.18  # Astronomical Unit. 150.18 million kilometer.

plt.style.use('dark_background')


def spheres(size, pos, clr, dist=0):
    # xyz position of asteroid
    x, y, z = pos[0] * AU_MULTIPLIER, pos[1] * AU_MULTIPLIER, pos[2] * AU_MULTIPLIER

    # Set up 100 points. First, do angles
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 100)

    # Set up coordinates for points on the sphere
    x0 = x + size * np.outer(np.cos(theta), np.sin(phi))
    y0 = y + size * np.outer(np.sin(theta), np.sin(phi))
    z0 = z + size * np.outer(np.ones(100), np.cos(phi))

    # Set up trace
    trace = go.Surface(x=x0, y=y0, z=z0, colorscale=[[0, clr], [1, clr]])
    trace.update(showscale=False)

    return trace


def orbits(coordinates, clr='white', wdth=2):
    """
    Returns a trace for the orbit of an asteroid
    :param coordinates: list of xyz coordinates
    :param clr: color in hex
    :param wdth: width of trace
    :return: plotly trace
    """
    xcrd = coordinates[::, 0] * AU_MULTIPLIER
    ycrd = coordinates[::, 1] * AU_MULTIPLIER
    zcrd = coordinates[::, 2] * AU_MULTIPLIER
    trace = go.Scatter3d(x=xcrd, y=ycrd, z=zcrd, marker=dict(size=0.1), line=dict(color=clr, width=wdth))
    return trace


def annot(xcrd, zcrd, txt, xancr='center'):
    strng = dict(showarrow=False, x=xcrd, y=0, z=zcrd, text=txt, xanchor=xancr, font=dict(color='white', size=12))
    return strng


def plot_asteroids(*rocks):
    """
    Plot asteroids in 3d space around Adalia
    :param rocks: indefinite amount of asteroids (as dict)
    """
    # Init
    asteroid_spheres = []
    asteroid_orbits = []
    curr_aday = get_current_adalia_day()

    # Set up Adalia sphere
    trace_adalia_sphere = spheres(25, [0, 0, 0], '#bfbfbf', 0)

    # Set up asteroid orbits/spheres
    for rock in rocks:
        # Rock data
        cur_pos = position_at_adalia_day(rock, curr_aday)
        coordinates = full_position(rock)

        # Set up orbit traces
        trace_rock_orbit = orbits(coordinates)
        asteroid_orbits.append(trace_rock_orbit)

        # Create asteroid spheres
        dist = rock['orbital.a'] * AU_MULTIPLIER
        trace_rock_sphere = spheres(10, cur_pos, '#FFFF00', dist)
        asteroid_spheres.append(trace_rock_sphere)

    layout = go.Layout(title='Adalia System', showlegend=False, margin=dict(l=0, r=0, t=0, b=0),
                       scene=dict(xaxis=dict(title='Distance from Sun', titlefont_color='black',
                                             range=[-1000, 1000], backgroundcolor='black', color='black',
                                             gridcolor='black'),
                                  yaxis=dict(title='Distance from Sun', titlefont_color='black',
                                             range=[-1000, 1000], backgroundcolor='black', color='black',
                                             gridcolor='black'),
                                  zaxis=dict(title='', range=[-1000, 1000], backgroundcolor='black', color='white',
                                             gridcolor='black'),
                                  annotations=[annot(0, 40, 'Adalia', xancr='left')]
                                  )
                       )

    fig = go.Figure(data=[trace_adalia_sphere, *asteroid_orbits, *asteroid_spheres], layout=layout)
    fig.show()

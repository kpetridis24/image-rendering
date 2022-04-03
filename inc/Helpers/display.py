import matplotlib.pyplot as plt
import imageio
import numpy as np


def display_npy(img, save=False, filename='out'):
    """Displays a numpy matrix as a PNG image

    Parameters
    ----------
    img : MxNx3 image with RGB colors
    save : indicates whether to save the image
    filename : the name to store the image, without the extension
    """
    plt.imshow(img, interpolation='nearest')
    plt.show()
    if save:
        imageio.imsave(filename + '.png', img)
        # imageio.imsave(filename + '.png', (img * 255).astype(np.uint8))


def show_vscan(y, active_edges, active_nodes, vertices_of_edge):
    """Shows the state of the vertical scanning on the specified triangle

    Parameters
    ----------
    y : horizontal line, scanning vertically. In each step, y is increased by 1, until the whole triangle is scanned
    active_edges : the edges, intersected by line y, in the current state. only these are displayed
    active_nodes : the points that the y line, intersects the active edges
    vertices_of_edge : the coordinates from the vertices of each edge of the triangle
    """
    for i, edge in enumerate(active_edges):
        if edge:
            X = list(vertices_of_edge[i, :, 0])
            Y = list(vertices_of_edge[i, :, 1])
            plt.plot(X, Y)
    for v in active_nodes[active_edges]:
        plt.plot([v[0]], [v[1]], marker='o', markersize=5, color="black")
        plt.axhline(y, color='r', linestyle='-')
    plt.show()


def show_triangle(vertices_of_edge):
    """Displays the specified triangle

    Parameters
    ----------
    vertices_of_edge : the coordinates from the vertices of each edge of the triangle
    """
    for i in range(3):
        X = list(vertices_of_edge[i, :, 0])
        Y = list(vertices_of_edge[i, :, 1])
        plt.plot(X, Y)
    plt.show()
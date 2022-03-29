"""
Image displaying functions
"""
import matplotlib.pyplot as plt
from PIL import Image


"""
Given a numpy matrix, displays it as a PNG image

@param img: MxNx3 image with RGB colors
@param save: indicates whether to save the image 
@param filename: the name to store the image, without the .png extension
"""
def display_npy(img, save=False, filename='out'):
    plt.imshow(img, interpolation='nearest')
    plt.show()
    if save:
        fig = Image.fromarray(img, 'RGB')
        fig.save(filename + '.png')


def display_scan_state(y, active_edges, active_nodes, x_edge_limits, y_edge_limits):
    for i, e in enumerate(active_edges):
        if e:
            X = list(x_edge_limits[i])
            Y = list(y_edge_limits[i])
            plt.plot(X, Y)
    for e, point in enumerate(active_nodes):
        if active_edges[e]:
            plt.plot([point[0]], [point[1]], marker='o', markersize=4, color="red")
    plt.axhline(y, color='r', linestyle='-')
    plt.show()
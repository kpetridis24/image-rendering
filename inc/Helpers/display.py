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


def show_vscan(y, active_edges, active_nodes, vertices_of_edge):
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
    for i in range(3):
        X = list(vertices_of_edge[i, :, 0])
        Y = list(vertices_of_edge[i, :, 1])
        plt.plot(X, Y)
    plt.show()
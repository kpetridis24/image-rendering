"""
Linear interpolation of the colors of two triangle vertices
"""
import numpy as np


"""
Computes the RGB color of a point, via the linear interpolation of colors from two triangle vertices.
@note: 
At this point we assume that the choice of whether to use the x or y of the two vertices has already been done. This 
means that whether the two vertices belong to the same x or y has already been checked before calling this function, 
and the appropriate arguments (x or y) have been passed.
 
@param x1: x or y of the first triangle vertex
@param x2: x or y of the second triangle vertex
@param x: position to calculate the interpolation
@param c1: RGB color of the first vertex
@param c2: RGB color of the second vertex
@return: RGB color of the specified position
"""
def interpolate_color(x1, x2, x, c1, c2):
    sigma = (x2 - x) / (x2 - x1)
    color_value = np.array([sigma * c1 + (1 - sigma) * c2])
    return color_value


def color_horizontal(edge_idx, y, x_limits_of_edge, color, img, node_combination_on_edge, vcolors):
    x_min, x_max = int(np.amin(x_limits_of_edge)), int(np.amax(x_limits_of_edge))
    if color is None:
        node_pair = node_combination_on_edge[edge_idx]
        c1, c2 = vcolors[node_pair[0]], vcolors[node_pair[1]]
        for x in range(x_min, x_max + 1):
            color = interpolate_color(x_min, x_max, x, c1, c2)
            img[int(np.around(x)), int(np.around(y))] = color
    else:
        for x in range(x_min, x_max + 1):
            img[int(np.around(x)), int(np.around(y))] = color
    return img


def color_vertex(y_max, edge_idx, sigma_of_edge, vertices_of_edge, verts2d, vcolors, img):
    random_edge = edge_idx % 2 + 1
    if sigma_of_edge[edge_idx] > 0 or sigma_of_edge[random_edge] == float('inf'):
        x_to_paint = np.max(vertices_of_edge[random_edge, :, 0])
    else:
        x_to_paint = np.min(vertices_of_edge[random_edge, :, 0])
    for t, p in enumerate(verts2d):
        if np.array_equal(p, [x_to_paint, y_max]):
            img[int(x_to_paint), int(y_max)] = vcolors[t]
            break

    return img
import numpy as np


def interpolate_color(x1, x2, x, c1, c2):
    """Computes the RGB color of a point, via the linear interpolation of colors from two triangle vertices

    At this point we assume that the choice of whether to use the x or y of the two vertices has already been done. This
    means that whether the two vertices belong to the same x or y has already been checked before calling this function,
    and the appropriate arguments (x or y) have been passed. If the vertices belong to a horizontal line, then x should
    be passed, in all other cases (including a vertical line), y is passed.

    Parameters
    ----------
    x1 : x or y of the first triangle vertex
    x2 : x or y of the second triangle vertex
    x : position to calculate the interpolation
    c1 : RGB color of the first vertex
    c2 : RGB color of the second vertex

    Returns
    -------
    color_value : 1x3 vector, containing the RGB color of the specified position
    """
    sigma = (x2 - x) / (x2 - x1)
    color_value = np.array([sigma * c1 + (1 - sigma) * c2])
    return color_value


def color_horizontal(edge_idx, y, x_limits_of_edge, color, img, node_combination_on_edge, vcolors):
    """Flat/smooth coloring of a horizontal line

    Parameters
    ----------
    edge_idx : the index of the edge, as stored in my current implementation
    y : horizontal line to fill
    x_limits_of_edge : the min(x) and max(x) of the edge
    color : if not None, the color to shade flat. Otherwise, shades gouraud
    img : MxNx3 image matrix
    node_combination_on_edge : maps the vertices of an edge, to their index as stored in this implementation
    vcolors : the RGB colors of the three vertices, of this triangle

    Returns
    -------
    img : the updated MxNx3 image matrix, after the coloring of the horizontal edge
    """
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
    """Colors a single vertex

    This function is used when all three vertices of a triangle are located in the same pixel. This happens because
    initially, the 3D scene is divided into triangles and then the triangles are projected to the 2D space. So there
    are both cases of line-trianlges (third vertex towards axis z, which is not visible in 2D space) and single-point
    triangles, which is basically a line triangle turned in such a way that all tree vertices fall to the same pixel.

    Parameters
    ----------
    y_max : The y of the vertices
    edge_idx : the index of the current edge whose slope is 'nan' i.e. turned towards z axis
    sigma_of_edge : the slopes for every edge of the triangle
    vertices_of_edge : the vertices incident to every edge
    verts2d : the coordinates of all the vertices of the triangle
    vcolors : the RGB colors of the three vertices, of this triangle
    img : MxNx3 image matrix

    Returns
    -------
    img : the updated MxNx3 image matrix, after the coloring of the horizontal edge
    """
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
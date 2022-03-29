"""
Triangle filling functions
"""
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
import inc.Helpers.tools as tls
from inc.interpolate_color import interpolate_color
from inc.Helpers.display import display_scan_state
from inc.Helpers.display import display_npy


def draw_pixel_flat(x, y, vcolors, img):
    rgb_value = np.array(np.sum(vcolors, axis=0) / 3)
    img[x, y, :] = rgb_value
    return img


def shade_flat(y, x_min, x_max, active_nodes, active_edges, vcolors, img):
    occurence_count = 0
    for x in range(x_min, x_max + 1):
        occurence_count += np.count_nonzero(x == np.around(active_nodes[active_edges, 0]))
        if occurence_count % 2 != 0:
            img = draw_pixel_flat(x, y, vcolors, img)
    return img


def shade_smooth(y, x_min, x_max, x_edge_limits, y_edge_limits, active_nodes, active_edges, vcolors, img):
    active_nodes_color = np.zeros((3, 3))
    node_combination_on_edge = {0: [0, 1],
                                1: [0, 2],
                                2: [1, 2]
                                }
    for i, point in enumerate(active_nodes):
        if active_edges[i]:
            # The edge coordinates of every active node. This is the edge i.
            x_edge = np.array(x_edge_limits[i])
            y_edge = np.array(y_edge_limits[i])
            node_pair = node_combination_on_edge[i]
            c1, c2 = vcolors[node_pair[0]], vcolors[node_pair[1]]
            # case of horizontal edge
            if y_edge[0] == y_edge[1] and x_edge[0] != x_edge[1]:
                active_nodes_color[i] = interpolate_color(x_edge[0], x_edge[1], y, c1, c2)
            elif x_edge[0] == x_edge[1] and y_edge[0] != y_edge[1]:
                # case of vertical line
                active_nodes_color[i] = interpolate_color(y_edge[0], y_edge[1], y, c1, c2)
                img[int(active_nodes[i, 0]), int(active_nodes[i, 1])] = active_nodes_color[i]
            elif y_edge[0] != y_edge[1]:
                # all normal cases
                active_nodes_color[i] = interpolate_color(y_edge[0], y_edge[1], y, c1, c2)
                img[int(active_nodes[i, 0]), int(active_nodes[i, 1])] = active_nodes_color[i]

    x_left, idx_left = np.min(active_nodes[active_edges, 0]), np.argmin(active_nodes[active_edges, 0])
    x_right, idx_right = np.max(active_nodes[active_edges, 0]), np.argmax(active_nodes[active_edges, 0])
    c1, c2 = active_nodes_color[active_edges][idx_left], active_nodes_color[active_edges][idx_right]

    occurence_count = 0
    for x in range(x_min, x_max + 1):
        occurence_count += np.count_nonzero(x == np.around(active_nodes[active_edges, 0]))
        if occurence_count % 2 != 0 and int(np.around(x_left)) != int(np.around(x_right)):
            img[x, y] = interpolate_color(int(np.around(x_left)), int(np.around(x_right)), x, c1, c2)


# def draw_pixel_smooth()


"""
Fills the specified triangle with color

@param verts2d: 3x2 matrix containing the coordinates of all 3 vertices of the triangle
@param vcolors: 3x3 matrix containing the RGB color values of all 3 vertices of the triangle
@param shade_t: coloring strategy, with 'flat' and 'gouraud' indicating that the triangle should be filled with a 
single color and have a gradual color changing effect respectively
@return: MxNx3 image, with updated RGB values on the specified triangle
"""
def shade_triangle(img, verts2d, vcolors, shade_t):
    x_min, x_max = int(np.amin(verts2d[:, 0])), int(np.amax(verts2d[:, 0]))
    y_min, y_max = int(np.amin(verts2d[:, 1])), int(np.amax(verts2d[:, 1]))
    active_edges = np.array([False, False, False])
    active_nodes = np.zeros((3, 2))

    x_edge_limits, y_edge_limits = tls.compute_edge_limits(verts2d)
    edges_sigma = tls.compute_edge_sigma(verts2d)

    x_edge_lookup = {0: {0: 0,
                         1: 1},
                     1: {0: 0,
                         1: 2},
                     2: {0: 1,
                         1: 2}
                     }

    for y in range(y_min, y_max + 1):
        active_edges, active_nodes = tls.compute_active_elements(y, verts2d, y_edge_limits, active_edges,
                                                                 active_nodes, x_edge_lookup)
        # display_scan_state(y, active_edges, active_nodes, x_edge_limits, y_edge_limits)
        if shade_t == 'flat':
            shade_flat(y, x_min, x_max, active_nodes, active_edges, vcolors, img)
        else:
            shade_smooth(y, x_min, x_max, x_edge_limits, y_edge_limits, active_nodes, active_edges, vcolors, img)

        active_nodes = tls.update_active_nodes(edges_sigma, active_edges, active_nodes)

    return img


"""
Iterates over every triangle, from the farthest to the nearest, and calls the coloring method for each one separately.

@param verts2d: Lx2 matrix containing the coordinates of every vertex (L vertices)
@param faces: Kx3 matrix containing the vertex indices of every triangle (K triangles)
@param vcolors: Lx3 matrix containing the RGB color values of every vertex 
@param depth: Lx1 array containing the depth of every vertex in its initial, 3D scene 
@param shade_t: coloring strategy, with 'flat' and 'gouraud' indicating that every triangle should be filled with a 
single color and have a gradual color changing effect respectively
@return: MxNx3 image with colors
"""
def render(verts2d, faces, vcolors, depth, shade_t):
    assert verts2d.shape[1] == 2 and vcolors.shape[1] == 3 and shade_t in ('gouraud', 'flat')
    m = 512
    n = 512
    d = 3

    img = np.ones((m, n, d))
    triangles_depth = np.array(np.mean(depth[faces[:, 0:3]], axis=1))
    ordered_triangles = list(np.flip(np.argsort(triangles_depth)))

    for t in ordered_triangles:
        vertices_t = np.array(faces[t])
        verts2d_t = np.array(verts2d[vertices_t])
        vcolors_t = np.array(vcolors[vertices_t])
        img = shade_triangle(img, verts2d_t, vcolors_t, shade_t)

    return img

    # # todo: iterate over every triangle, starting from those with the most depth
    # triangle = 0
    # vertices_t = np.array(faces[triangle])
    # verts2d_t = np.array(verts2d[vertices_t])
    # vcolors_t = np.array(vcolors[vertices_t])
    # img = shade_triangle(img, verts2d_t, vcolors_t, shade_t)

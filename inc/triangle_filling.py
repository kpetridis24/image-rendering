from cmath import isnan
import numpy as np
import inc.Helpers.tools as tls
import inc.coloring as clr
import inc.Helpers.display as dsp


def render_smooth(verts2d, vcolors, img):
    if (verts2d == verts2d[0]).all():
        img[int(verts2d[0, 0]), int(verts2d[0, 1])] = np.mean(vcolors, axis=0)
        return img

    # compute edge limits and sigma
    vertices_of_edge, x_limits_of_edge, y_limits_of_edge, sigma_of_edge = tls.compute_edge_limits(verts2d)

    # find min/max x and y
    x_min, x_max = int(np.amin(x_limits_of_edge)), int(np.amax(x_limits_of_edge))
    y_min, y_max = int(np.amin(y_limits_of_edge)), int(np.amax(y_limits_of_edge))

    # find initial active edges for y = 0
    active_edges = np.array([False, False, False])
    active_nodes = np.zeros((3, 2))

    is_invisible = False
    node_combination_on_edge = {0: [0, 1],
                                1: [0, 2],
                                2: [1, 2]
                                }

    active_edges, active_nodes, is_invisible = tls.initial_active_elements(active_edges, active_nodes, vertices_of_edge,
                                                                           y_limits_of_edge, sigma_of_edge)
    if is_invisible:
        return img

    for y in range(y_min, y_max):
        active_edges, active_nodes, updated_nodes = tls.update_active_edges(y, vertices_of_edge, y_limits_of_edge,
                                                                            sigma_of_edge, active_edges, active_nodes)
        active_nodes = tls.update_active_nodes(sigma_of_edge, active_edges, active_nodes, updated_nodes)

        img, active_nodes_color = tls.paint_active_nodes(y, node_combination_on_edge,
                                                         x_limits_of_edge, y_limits_of_edge, sigma_of_edge,
                                                         active_edges, active_nodes, vcolors, img)

        x_left, idx_left = np.min(active_nodes[active_edges, 0]), np.argmin(active_nodes[active_edges, 0])
        x_right, idx_right = np.max(active_nodes[active_edges, 0]), np.argmax(active_nodes[active_edges, 0])
        c1, c2 = active_nodes_color[active_edges][idx_left], active_nodes_color[active_edges][idx_right]

        cross_counter = 0
        for x in range(x_min, x_max + 1):
            cross_counter += np.count_nonzero(x == np.around(active_nodes[active_edges, 0]))
            if cross_counter % 2 != 0 and int(np.around(x_left)) != int(np.around(x_right)):
                img[x, y] = clr.interpolate_color(int(np.around(x_left)), int(np.around(x_right)), x, c1, c2)

    return img


def render_flat(verts2d, vcolors, img):
    new_color = np.array(np.mean(vcolors, axis=0))
    if (verts2d == verts2d[0]).all():
        img[int(verts2d[0, 0]), int(verts2d[0, 1])] = new_color
        return img

    # compute edge limits and sigma
    vertices_of_edge, x_limits_of_edge, y_limits_of_edge, sigma_of_edge = tls.compute_edge_limits(verts2d)

    # find min/max x and y
    x_min, x_max = int(np.amin(x_limits_of_edge)), int(np.amax(x_limits_of_edge))
    y_min, y_max = int(np.amin(y_limits_of_edge)), int(np.amax(y_limits_of_edge))

    # find initial active edges for y = 0
    active_edges = np.array([False, False, False])
    active_nodes = np.zeros((3, 2))

    active_edges, active_nodes, is_invisible = tls.initial_active_elements(active_edges, active_nodes, vertices_of_edge,
                                                                           y_limits_of_edge, sigma_of_edge)
    if is_invisible:
        return img

    # dsp.show_vscan(y_min, active_edges, active_nodes, vertices_of_edge)
    for y in range(y_min, y_max + 1):
        # dsp.show_vscan(y, active_edges, active_nodes, vertices_of_edge)
        cross_counter = 0
        for x in range(x_min, x_max + 1):
            cross_counter += np.count_nonzero(x == np.around(active_nodes[active_edges][:, 0]))
            if cross_counter % 2 != 0:
                img[x, y] = new_color
            elif y == y_max and np.count_nonzero(x == np.around(active_nodes[active_edges][:, 0])) > 0:
                img[x, y] = new_color

        active_edges, active_nodes, updated_nodes = tls.update_active_edges(y, vertices_of_edge, y_limits_of_edge,
                                                                            sigma_of_edge, active_edges, active_nodes)
        active_nodes = tls.update_active_nodes(sigma_of_edge, active_edges, active_nodes, updated_nodes)
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
def render(verts2d, faces, vcolors, depth, m, n, shade_t):
    assert shade_t in ('flat', 'gouraud') and m >= 0 and n >= 0
    img = np.ones((m, n, 3))
    # depth of every triangle. depth[i] = depth of triangle i
    depth_tr = np.array(np.mean(depth[faces], axis=1))
    # order from the farthest triangle to the closest, depth-wise
    triangles_in_order = list(np.flip(np.argsort(depth_tr)))

    for t in triangles_in_order:#[4004:4005]:
        vertices_tr = faces[t]
        verts2d_tr = np.array(verts2d[vertices_tr])  # x,y of the 3 vertices of triangle t
        vcolors_tr = np.array(vcolors[vertices_tr])  # color of the 3 vertices of triangle t
        if shade_t == 'flat':
            img = render_flat(verts2d_tr, vcolors_tr, img)
        else:
            img = render_smooth(verts2d_tr, vcolors_tr, img)

    return img
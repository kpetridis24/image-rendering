"""
Calculate the necessary limits for a specified triangle
"""
from cmath import isnan

import numpy as np


def compute_edge_limits(verts2d):
    edges_verts = np.array([[verts2d[0], verts2d[1]], [verts2d[0], verts2d[2]], [verts2d[1], verts2d[2]]])

    x_limits = np.array([np.min(edges_verts[:, :, 0], axis=1),
                         np.max(edges_verts[:, :, 0], axis=1)]).T
    y_limits = np.array([np.min(edges_verts[:, :, 1], axis=1),
                         np.max(edges_verts[:, :, 1], axis=1)]).T

    diff = np.array(edges_verts[:, 1] - edges_verts[:, 0])
    # 1. positive/negative number means it's a line
    # 2. 0 means it's horizontal line
    # 3. float('inf') means it's a vertical line
    # 4. nan means it's a dot, not a line. So the triangle is a line (twisted inside z axis, not visible)
    edges_sigma = np.array(diff[:, 1] / diff[:, 0])
    return edges_verts, x_limits, y_limits, edges_sigma


def compute_active_elements(y, vertices_of_edge, y_limits_of_edge, sigma_of_edge, active_edges, active_nodes):
    is_invisible = False
    for i, y_limit in enumerate(y_limits_of_edge):
        if y_limit[0] == y:  # y-scan line meets new edge from the bottom
            if sigma_of_edge[i] == 0:  # it's a horizontal line
                is_horizontal = True
                continue
            if isnan(sigma_of_edge[i]):  # it's an invisible line
                is_invisible = True
                continue
            active_edges[i] = True  # in other cases, it's an active line
            pos = np.argmin(vertices_of_edge[i, :, 1])
            active_nodes[i] = [vertices_of_edge[i, pos, 0], y_limits_of_edge[i, 0]]
        if y_limit[1] == y - 1:
            active_edges[i] = False

    return active_edges, active_nodes, is_invisible


def update_active_nodes(sigma_of_edge, active_edges, active_nodes):
    for i, sigma in enumerate(sigma_of_edge):
        if active_edges[i] and sigma != 0:
            active_nodes[i, 0] += 1 / sigma_of_edge[i]
            active_nodes[i, 1] += 1
    return active_nodes

"""
Calculate the necessary limits for a specified triangle
"""
import numpy as np
from sympy.utilities.iterables import multiset_permutations
from itertools import combinations


def compute_edge_limits(verts2d):
    x_edge_limits = np.array([[verts2d[0, 0], verts2d[1, 0]], [verts2d[0, 0], verts2d[2, 0]],
                              [verts2d[1, 0], verts2d[2, 0]]])
    y_edge_limits = np.array([[verts2d[0, 1], verts2d[1, 1]], [verts2d[0, 1], verts2d[2, 1]],
                              [verts2d[1, 1], verts2d[2, 1]]])
    return x_edge_limits, y_edge_limits


def compute_edge_sigma(verts2d):
    x_verts, y_verts = np.array(verts2d[:, 0]), np.array(verts2d[:, 1])
    edges_sigma = np.zeros((3,))
    for i, (pair_x, pair_y) in enumerate(zip(combinations(x_verts, 2), combinations(y_verts, 2))):
        if pair_x[1] != pair_x[0]:
            edges_sigma[i] = (pair_y[1] - pair_y[0]) / (pair_x[1] - pair_x[0])
        else:
            edges_sigma[i] = float('inf')
    return edges_sigma


def compute_active_elements(y, verts2d, y_edge_limits, active_edges, active_nodes, x_edge_lookup):
    for i, y_edge in enumerate(y_edge_limits):
        pos = np.argmin(y_edge)
        if np.min(y_edge) == y:
            active_edges[i] = True
            active_nodes[i] = [verts2d[x_edge_lookup[i][int(pos)], 0], np.min(y_edge)]
        if np.max(y_edge) == y - 1:
            active_edges[i] = False

    return active_edges, active_nodes


def update_active_nodes(edges_sigma, active_edges, active_nodes):
    x_updated = np.zeros((3,))
    for cnt, s in enumerate(edges_sigma):
        if s != 0:
            x_updated[cnt] = active_nodes[cnt, 0] + 1 / edges_sigma[cnt]

    y_updated = np.ones((3,))
    active_nodes[active_edges, 0] = x_updated[active_edges]
    active_nodes[active_edges, 1] += y_updated[active_edges]
    return active_nodes

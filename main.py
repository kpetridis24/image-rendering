"""
Triangle filling demo
"""
import numpy as np
from inc.Helpers.display import display_npy
from inc.Helpers.reader import load_data_npy
from inc.triangle_filling import render, shade_triangle


verts2d, vcolors, faces, depth = load_data_npy(filename='hw1.npy')
img = render(verts2d, faces, vcolors, depth, shade_t='gouraud')
# img_ready = img/np.amax(img)
display_npy(img)

# img = np.ones((512, 512, 3))
# for t in range(140, 141):
#     v2d = np.array(verts2d[faces[t]])
#     vc = np.array(vcolors[faces[t]])
#     # v2d = np.array([[0, 0], [5, 0], [2, 4]])
#     # print(v2d)
#     img = shade_triangle(img, v2d, vc, shade_t='flat')
#
# display_npy(img)
# a = np.array([[1, 1, 1], [2, 2, 3], [1, 2, 3]])
# c = np.array(np.sum(a, axis=0) / 3)
# img[1, 1, :] = c
# print(img)

# a = np.array([[1, 3], [4, 2], [1, 6]])
# print(np.count_nonzero(a[:, 0] == 4))

# x_edge_min, x_edge_max, y_edge_min, y_edge_max = compute_limits(v2d)
# y_edges = np.array(np.c_[y_edge_min, y_edge_max])
#
# y_min, y_max = int(np.min(y_edge_min)), int(np.max(y_edge_max))
# y_edge_limits = np.array(np.c_[y_edge_min, y_edge_max])
# active_edges = np.array([False, False, False])
#
# x_verts, y_verts = np.array(v2d[:, 0]), np.array(v2d[:, 1])
# edges_sigma = np.zeros((3, ))
#
# for i, (pair_x, pair_y) in enumerate(zip(combinations(x_verts, 2), combinations(y_verts, 2))):
#     if pair_x[1] != pair_x[0]:
#         edges_sigma[i] = (pair_y[1] - pair_y[0]) / (pair_x[1] - pair_x[0])
#     else:
#         edges_sigma[i] = float('inf')




# print(y_edge_min)
# print(y_edge_max)
# print(y_edge_limits)

# X = [v2d[0, 0], v2d[1, 0], v2d[2, 0]]
# Y = [v2d[0, 1], v2d[1, 1], v2d[2, 1]]
# plt.plot(X, Y)
# plt.show()

# for y in range(y_min, y_max):
#     for i, y_edge in enumerate(y_edge_limits):
#         if y_edge[0] == y:
#             active_edges[i] = True
#         if y_edge[1] == y - 1:
#             active_edges[i] = False

# print(active_edges)
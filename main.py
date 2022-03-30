"""
Triangle filling demo via image coloring
"""
import inc.Helpers.display as dsp
import inc.Helpers.reader as rd
from inc.triangle_filling import render
import time


m = 512
n = 512
verts2d, vcolors, faces, depth = rd.load_data_npy(filename='data/hw1.npy')

start = time.time()
img = render(verts2d, faces, vcolors, depth, m, n, shade_t='flat')
end = time.time()

print('Elapsed time: ', end - start)
dsp.display_npy(img)



# img = np.ones((m, n, 3))
#
# vertex_coord_tr = verts2d[faces]  # Vertex coordinates of triangles. Triangle i has vertices with coordinates arr[i]
# depth_tr = np.array(np.mean(depth[faces], axis=1))  # depth of every triangle. depth[i] = depth of triangle i
# triangles_in_order = list(np.flip(np.argsort(depth_tr)))  # order from the farthest triangle to the closest, depth-wise
#
# start = time.time()
# # for every triangle t <- index of the triangle
# for t in triangles_in_order:
#     vertices_tr = faces[t]
#     verts2d_tr = np.array(verts2d[vertices_tr])  # x,y of the 3 vertices of triangle t
#     vcolors_tr = np.array(vcolors[vertices_tr])  # color of the 3 vertices of triangle t
#
#     new_color = np.array(np.mean(vcolors_tr, axis=0))  # for flat painting, color of triangle t
#
#     if (verts2d_tr == verts2d_tr[0]).all():
#         img[int(verts2d_tr[0, 0]), int(verts2d_tr[0, 1])] = new_color
#         continue
#
#     vertices_of_edge = np.array([[verts2d_tr[0], verts2d_tr[1]],
#                                  [verts2d_tr[0], verts2d_tr[2]],
#                                  [verts2d_tr[1], verts2d_tr[2]]])
#
#     x_limits_of_edge = np.array([np.min(vertices_of_edge[:, :, 0], axis=1),
#                                  np.max(vertices_of_edge[:, :, 0], axis=1)]).T
#     y_limits_of_edge = np.array([np.min(vertices_of_edge[:, :, 1], axis=1),
#                                  np.max(vertices_of_edge[:, :, 1], axis=1)]).T
#
#     diff = np.array(vertices_of_edge[:, 1] - vertices_of_edge[:, 0])
#     # 1. positive/negative number means it's a line
#     # 2. 0 means it's horizontal line
#     # 3. float('inf') means it's a vertical line
#     # 4. nan means it's a dot, not a line. So the triangle is a line (twisted inside z axis, not visible)
#     sigma_of_edge = np.array(diff[:, 1] / diff[:, 0])
#
#     # find min/max x and y
#     x_min, x_max = int(np.amin(x_limits_of_edge)), int(np.amax(x_limits_of_edge))
#     y_min, y_max = int(np.amin(y_limits_of_edge)), int(np.amax(y_limits_of_edge))
#
#     # find initial active edges for y = 0
#     active_edges = np.array([False, False, False])
#     active_nodes = np.zeros((3, 2))
#     is_horizontal = False
#     is_invisible = False
#
#     for i, y_limit in enumerate(y_limits_of_edge):
#         if y_limit[0] == y_min:  # y-scan line meets new edge from the bottom
#             if sigma_of_edge[i] == 0:  # it's a horizontal line
#                 is_horizontal = True
#                 continue
#             if isnan(sigma_of_edge[i]):  # it's an invisible line
#                 is_invisible = True
#                 continue
#             active_edges[i] = True  # in other cases, it's an active line
#             pos = np.argmin(vertices_of_edge[i, :, 1])
#             active_nodes[i] = [vertices_of_edge[i, pos, 0], y_limits_of_edge[i, 0]]
#         if y_limit[1] == y_min - 1:
#             active_edges[i] = False
#
#     if is_invisible:
#         continue
#
#     # y scan
#     for y in range(y_min + 1, y_max + 1):
#         cross_counter = 0
#
#         for i, sigma in enumerate(sigma_of_edge):
#             if active_edges[i] and sigma != 0:
#                 active_nodes[i, 0] += 1 / sigma_of_edge[i]
#                 active_nodes[i, 1] += 1
#
#         # dsp.show_vscan(y, active_edges, active_nodes, vertices_of_edge)
#
#         for x in range(x_min, x_max + 1):
#             cross_counter += np.count_nonzero(x == np.around(active_nodes[active_edges][:, 0]))
#             if cross_counter % 2 != 0:
#                 img[x, y] = new_color
#             elif y == y_max and np.count_nonzero(x == np.around(active_nodes[active_edges][:, 0])) > 0:
#                 img[x, y] = new_color
#
#         for i, y_limit in enumerate(y_limits_of_edge):
#             if y_limit[0] == y:  # y-scan line meets new edge from the bottom
#                 if sigma_of_edge[i] == 0:  # it's a horizontal line
#                     is_horizontal = True
#                     continue
#                 if isnan(sigma_of_edge[i]):  # it's an invisible line
#                     is_invisible = True
#                     continue
#                 active_edges[i] = True  # in other cases, it's an active line
#                 pos = np.argmin(vertices_of_edge[i, :, 1])
#                 active_nodes[i] = [vertices_of_edge[i, pos, 0], y_limits_of_edge[i, 0]]
#             if y_limit[1] == y - 1:
#                 active_edges[i] = False




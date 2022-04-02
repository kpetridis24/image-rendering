"""
Reader function to load data from .npy file
"""
import numpy as np
import scipy.io as io


"""
Loads the necessary data from a .npy file.

@param filename: the name of the file, including the .npy extension.
@return: vertex coordinates & indices, color and depth of all triangles
"""
def load_data_npy(filename):
    data = np.load(filename, allow_pickle=True).tolist()
    data = dict(data)

    verts2d = np.array(data['verts2d'])
    vcolors = np.array(data['vcolors'])
    faces = np.array(data['faces'])
    depth = np.array(data['depth'])

    return verts2d, vcolors, faces, depth


"""
Loads the necessary data from a .mat file.

@param filename: the name of the file, including the .mat extension.
@return: vertex coordinates & indices, color and depth of all triangles
"""
def load_data_mat(filename):
    data = io.loadmat(filename)
    verts2d = np.array(data['vertices_2d'] - 1)
    vcolors = np.array(data['vertex_colors'])
    faces = np.array(data['faces'] - 1)
    depth = np.array(data['depth']).T[0]

    return verts2d, vcolors, faces, depth

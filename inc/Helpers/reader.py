"""
Reader function to load data from .npy file
"""
import numpy as np


"""
Loads the necessary data from a .npy file.

@param filename: the name of the file, including the .npy extension.
@return: vertex coordinates & indices, color and depth of all triangles
"""
def load_data_npy(filename):
    data = np.load(filename, allow_pickle=True).tolist()
    data = dict(data)

    verts2d = np.array([data['verts2d']])
    vcolors = np.array([data['vcolors']])
    faces = np.array([data['faces']])
    depth = np.array([data['depth']])

    verts2d = verts2d.reshape(verts2d.shape[1], verts2d.shape[2])
    vcolors = vcolors.reshape(vcolors.shape[1], vcolors.shape[2])
    faces = faces.reshape(faces.shape[1], faces.shape[2])
    depth = depth.reshape(depth.shape[1])

    return verts2d, vcolors, faces, depth

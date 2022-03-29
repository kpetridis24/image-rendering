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

    verts2d = np.array(data['verts2d'])
    vcolors = np.array(data['vcolors'])
    faces = np.array(data['faces'])
    depth = np.array(data['depth'])

    return verts2d, vcolors, faces, depth


def load_data_npy2(filename):
    data = np.load(filename, allow_pickle=True)
    verts2d = np.array(data.item().get('verts2d'))
    vcolors = np.array(data.item().get('vcolors'))
    faces = np.array(data.item().get('faces'))
    depth = np.array(data.item().get('depth'))

    return verts2d, vcolors, faces, depth
"""
Linear interpolation of the colors of two triangle vertices
"""
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

"""
Computes the RGB color of a point, via the linear interpolation of colors from two triangle vertices.
@note: 
At this point we assume that the choice of whether to use the x or y of the two vertices has already been done. This 
means that whether the two vertices belong to the same x or y has already been checked before calling this function, 
and the appropriate arguments (x or y) have been passed.
 
@param x1: x or y of the first triangle vertex
@param x2: x or y of the second triangle vertex
@param x: position to calculate the interpolation
@param c1: RGB color of the first vertex
@param c2: RGB color of the second vertex
@return: RGB color of the specified position
"""
def interpolate_color(x1, x2, x, c1, c2):
    sigma = (x2 - x) / (x2 - x1)
    color_value = np.array([sigma * c1 + (1 - sigma) * c2])
    return color_value
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
# verts2d, vcolors, faces, depth = rd.load_data_mat(filename='data/racoon_hw1.mat')

start = time.time()
img = render(verts2d, faces, vcolors, depth, m, n, shade_t='gouraud')
end = time.time()

print('Elapsed time: ', end - start)
dsp.display_npy(img)

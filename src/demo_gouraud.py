from inc.triangle_filling import render
import inc.Helpers.display as dsp
import inc.Helpers.reader as rd
import time


m = 512
n = 512
# load the necessary data into numpy matrices
verts2d, vcolors, faces, depth = rd.load_data_npy(filename='../data/hw1.npy')

# perform the gouraud triangle filling
start = time.time()
img = render(verts2d, faces, vcolors, depth, m, n, shade_t='gouraud')
end = time.time()

# print the elapsed time and display-save the final image
print('Elapsed time: ', end - start)
dsp.display_npy(img, save=True, filename='gouraud')
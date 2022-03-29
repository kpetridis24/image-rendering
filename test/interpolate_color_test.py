from inc.interpolate_color import interpolate_color
import numpy as np

x1 = 1
x2 = 5
x = 2
c1 = np.array([1., 3., 2.])
c2 = np.array([4., 9., 6.])

new_color = interpolate_color(x1, x2, x, c1, c2)
expected = np.array([1.75, 4.5, 3]).reshape(1, 3)

assert np.array_equal(new_color, expected)

from fsnake import *
from pylab import *
from imcore import CoM

im = np.zeros((70,70))
snake = init_snake(30,(30,25),im.shape)

print snake[0]

for point in snake:
    im[point[0],point[1]] = 1
    
c = CoM(im)

print c
imshow(im)
scatter(c[1],c[0])
show()


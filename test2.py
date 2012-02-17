from fsnake import *
from pylab import *
from imcore import CoM

im = np.zeros((11,11))
snake = init_snake(2,(6,6),im.shape)

print snake[0]

for point in snake[1:]:
    im[point[0],point[1]] = 1
    
c_ = CoM(im)

print snake
print im

print c_
imshow(im)
scatter(c_[1],c_[0])
scatter(snake[0][1],snake[0][0])
show()
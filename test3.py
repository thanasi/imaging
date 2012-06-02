from pylab import *
from imsearch import *
from imcore import CoM
from fsnake import snake2im

im = flood_fill(make_ball(10)).astype(int)
start = locate_object(im)

H = contour(im,CoM(im))
r = np.nonzero(H==H.min())[0]+ 1
snake_im = np.zeros(im.shape)
snake = init_snake(r, CoM(im), im.shape)
snake_im = snake2im(snake,im.shape)

plot(H)
figure(2)
imshow(snake_im+im)
scatter(start[1],start[0])
scatter(CoM(im)[1],CoM(im)[0])
show()
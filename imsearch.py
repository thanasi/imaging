# Athanasios Athanassiadis Feb 2013
import numpy as np
from scipy.misc import imsave, imread

from imcore import pad_image, flood_fill
from ball import make_ball
from fsnake import init_snake, cost
from fourierd import *

# locate the first object in a binary image by rastering through
def locate_object(im, startrow=0):
    for i in range(startrow+2,im.shape[0]-3):
        for j in range(2,im.shape[1]-3):
            if (im[i-2:i+2,j-2:j+2]==1).all():
                return [i,j]
    print 'locate_object: No object found!'
    return [-1,-1]
    

# find the best fitting contour to an isolated object
# startpoint should be [row,col]
def contour(im, startpoint):
    H = []
    snake_im = np.zeros(im.shape)
    
    # snake should be stored as the set of Fourier Descriptors of the snake
    # it should only be transformed into real space for the purpose of checking cost
    # also, cost should be improved since it doesn't seem to be working correctly at the moment
    
    i=0
    while i < 15:
        snake = init_snake(i+1, startpoint, im.shape)
        for point in snake:
            snake_im[point[0],point[1]] = 1
        
        H.append(cost(im, snake_im))
        
        i += 1

    return np.array(H)

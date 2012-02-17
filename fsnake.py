# Athanasios Athanassiadis Feb 2012
import numpy as np
import fourierd as fd
import segmentation as seg
import imcore
from ball import make_ball

# cost heuristic for the fourier snake
def cost(im, snake, sigma = 1):
    #edge = seg.decode_chain8(chain8)
    region = imcore.flood_fill(snake).astype(np.int)

    m_in = (region * im).mean()
    m_out =((1-region) * im).mean()
    
    H = (((im - m_in)**2 + (im - m_out)**2) / (2 * sigma**2)).sum()
    
    return H
    
# initialize a snake (path)
# centered at center
# do this by defining the FD to just have first two components
def init_snake(r, center, shape):
    center = np.array(center)
    #ball = make_ball(r, bgsize=(2*r+1,2*r+1), shell=2)
    #edge,chain = seg.track_edge(ball)
    if (center-r < 0).any() or (center+r > np.array(shape)).any():
        print 'init_snake: snake initialization failed - snake would not fit on image'
        return np.array([center])
    #chain[:2] += center - r                     # center it where desired
    #snake2 = seg.path2coords(chain[:-1])         # last point is redundant
    
    Z = np.array([ center[0] + 1j * center[1], r])
    N = 7 * r
    snake = fd.fd2path(Z,N)
    
    return snake
    
def snake2im(snake, shape):
    snake_im = np.zeros(shape)
    for point in snake:
        snake_im[point[0],point[1]] = 1
        
    return snake_im
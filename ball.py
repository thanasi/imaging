# Athanasios Athanassiadis Jan 2012
import numpy as np
from dmetrics import *

# draw a ball
# shell can be specified by outer radius and thickness (default thickness 1px)
# or by two bounding radii
# uses matrix coordinates (row,col)
def make_ball(r, shell=1, r2=None, bgsize=(32,32), center=None, dmetric='euclid', ret='mask'):
    # make sure the desired distance algorithm is valid
    dmetric = str(dmetric)
    if dmetric not in distalgs:
        dmetric = 'euclid'
        print 'make_ball: invalid metric. proceeding with euclidean metric'

    dist = distalgs[dmetric]
        
    # initialize input variables to array datatype (np.array)
    # set center to middle of image if not specified
    bgsize = np.array(bgsize)
    if center==None:
        center = bgsize/2

    # init image
    img = np.zeros(bgsize)

    # compute distances to center
    for x in range(bgsize[0]):
        for y in range(bgsize[1]):
            img[x,y] = dist((x,y), center)

    # create binary mask based on distances
    if r2 == None:
        mask = (img <= r) * (img > r-shell)
    else:
        mask = (img <= max([r, r2])) * (img > min([r,r2]))

    # if desired, only return distance map, else just return mask
    if ret=='img':
        return img
    else:
        return mask
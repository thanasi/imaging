from __future__ import division
import numpy as np
cimport numpy as np

DTYPE1 = np.int32
DTYPE2 = np.bool

def dist(int p1x, int p1y, int p2x, int p2y):
    return np.sqrt((p1x-p2x)**2 + (p1y-p2y)**2)

def make_ball(int r, int sh, int bgx, int bgy, int cx, int cy):
    cdef np.ndarray ball = np.zeros([bgx, bgy], dtype=DTYPE2)
    cdef float d
    cdef int i,j
    
    for i in range(bgx):
        for j in range(bgy):
            d = dist(i,j,cx,cy)
            ball[i,j] = (d<=r) & (d>(r-sh))
    
    return ball

from __future__ import division
import numpy as np

def dist(p1x, p1y, p2x, p2y):
    return np.sqrt((p1x-p2x)**2 + (p1y-p2y)**2)

def make_ball(r, sh, bgx, bgy, cx, cy):
    ball = np.zeros([bgx,bgy], dtype=np.bool)

    for i in range(bgx):
        for j in range(bgy):
            d = dist(i,j,cx,cy)
            ball[i,j] = (d<=r) & (d>(r-sh))
    
    return ball

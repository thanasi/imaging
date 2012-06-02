# Athanasios Athanassiadis Feb 2012
import numpy as np

# define various metrics for distances
def euclid_dist(pt1, pt2=[0]):
    # convert input into useful np.array datatype
    pt1 = np.array(pt1)
    pt2 = np.array(pt2)
    # make sure the points have the same dimensionality, or that one is a constant
    if pt2.ndim==0: pt2 = np.array([pt2])
    if (pt1.ndim == pt2.ndim) or (pt2.ndim == 1):
        return np.sqrt(sum((pt1-pt2)**2))
    else:
        print 'euclid_dist: distance not computable.  please give two points with the same dimensions'
        return 0

def four_dist(pt1, pt2=[0]):
    pt1 = np.array(pt1)
    pt2 = np.array(pt2)
    if pt2.ndim==0: pt2 = np.array([pt2])
    if (pt1.ndim == pt2.ndim) or (pt2.ndim == 1):
        return sum(abs(pt1-pt2))
    else:
        print 'four_dist: distance not computable. please give two points with the same dimensions'
        return 0
    
def eight_dist(pt1, pt2=[0]):
    pt1 = np.array(pt1)
    pt2 = np.array(pt2)
    if pt2.ndim==0: pt2 = np.array([pt2])
    if (pt1.ndim == pt2.ndim) or (pt2.ndim == 1):
        return max(abs(pt1-pt2))
    else:
        print 'eight_dist: distance not computable. please give two points with the same dimensions'
        return 0

# dictionary of distance algorithms for easy user access later
distalgs = {'euclid': euclid_dist, '4': four_dist, '8': eight_dist}
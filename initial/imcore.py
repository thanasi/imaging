# Athanasios Athanassiadis Feb 2012
from __future__ import division
import numpy as np
import pylab as pl
from scipy import ndimage

import mahotas

contrast_max = mahotas.stretch

# define the 26 different image rolls for 3D
# 2D Primary
shiftU = lambda m: np.roll(m, -1, axis=0)
shiftD = lambda m: np.roll(m,  1, axis=0)
shiftL = lambda m: np.roll(m, -1, axis=1)
shiftR = lambda m: np.roll(m,  1, axis=1)
# 2D Secondary
shiftUL = lambda m: shiftU(shiftL(m))
shiftDL = lambda m: shiftD(shiftL(m))
shiftUR = lambda m: shiftU(shiftR(m))
shiftDR = lambda m: shiftD(shiftR(m))
# 3D Primary
shiftF = lambda m: np.roll(m, -1, axis=2)
shiftB = lambda m: np.roll(m,  1, axis=2)
# 3D Secondary
shiftFR = lambda m: shiftF(shiftR(m))
shiftFL = lambda m: shiftF(shiftL(m))
shiftFU = lambda m: shiftF(shiftU(m))
shiftFD = lambda m: shiftF(shiftD(m))
shiftBR = lambda m: shiftB(shiftR(m))
shiftBL = lambda m: shiftB(shiftL(m))
shiftBU = lambda m: shiftB(shiftU(m))
shiftBD = lambda m: shiftB(shiftD(m))
# 3D Ternary
shiftFUL = lambda m: shiftFU(shiftL(m))
shiftFDL = lambda m: shiftFD(shiftL(m))
shiftFUR = lambda m: shiftFU(shiftR(m))
shiftFDR = lambda m: shiftFD(shiftR(m))
shiftBUL = lambda m: shiftBU(shiftL(m))
shiftBDL = lambda m: shiftBD(shiftL(m))
shiftBUR = lambda m: shiftBU(shiftR(m))
shiftBDR = lambda m: shiftBD(shiftR(m))


def double_otsu_smaller(im):
    t = mahotas.otsu(im)
    t2 = mahotas.otsu(im[im<t])
    return t2


def double_otsu_larger(im):
    t = mahotas.otsu(im)
    t2 = mahotas.otsu(im[im>t])
    return t2


def get_largest_component(la):
    ''' return the largest component of a labeled image '''
    
    sums = ndimage.measurements.sum(la>0, la, range(la.max() + 1))
    big_value = np.argmax(sums)
    largest = im == big_value
    
    return largest


def eccentricity(im):
    ''' im should be a binary image with a single region '''
    
    c = mahotas.center_of_mass(im)
    
    m11 = mahotas.moments(im, 1, 1, c)
    m02 = mahotas.moments(im, 2, 0, c)
    m20 = mahotas.moments(im, 0, 2, c)
    
    l1 = (m20 + m02) / 2 + np.sqrt(4*m11**2 + (m20-m02)**2) / 2
    
    l2 = (m20 + m02) / 2 - np.sqrt(4*m11**2 + (m20-m02)**2) / 2
    
    e = np.sqrt(1 - l2 / l1)
    
    return e


def pad(im, n, mode='const', c=0):
    '''
        pad an image with n pixels on each side
        
    '''
    
    shape = np.array(im.shape)
    im_p = np.ones(shape + 2*n)
    if mode == 'const':
        im_p *= c
    
    slice_ = [slice(n,-n,None) for i in range(im.ndim)]
    im_p[slice_] = im
    
    if mode == 'reflect':
        # implement this at some point
        print msg('reflect mode not implemented yet')
    
    return im_p


def unpad(im, n):
    ''' unpad a padded image '''
    
    slice_ = [slice(n,-n,None) for i in range(im.ndim)]
    return im[slice_]

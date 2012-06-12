# Athanasios Athanassiadis June 2012

from __future__ import division
from mahotas import stretch
import pylab as pl

from imcore import double_otsu_smaller

def overlay_withcolor(base, overlay, \
                      overlaycm=pl.cm.jet, overlayalpha=.8):
    '''
    overlay_withcolor(base, overlay, overlaycm, overlayalpha)
        take a base grayscale image and overlay the overlay image 
        with colormap overlaycm and alpha level overlayalpha
        
    '''
    gr = pl.cm.gray(base / base.max())
    col = overlaycm(overlay / overlay.max(),alpha=overlayalpha)
    for j in range(4):
        col[:,:,j][overlay==0] = 0
    
    return gr + col * overlayalpha - gr * col * overlayalpha


def overlay_thresh(im):
    return overlay_withcolor(im, stretch(im) < double_otsu_smaller(stretch(im)))
    
#Athanasios Athanassiadis Feb 2012
import numpy as np
import fourierd as fd
import segmentation as seg

def cost(im, contour, sigma = 1):
    H = 0
    for x in
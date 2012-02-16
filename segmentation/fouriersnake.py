#Athanasios Athanassiadis Feb 2012
import numpy as np
import fourierd as fd
import segmentation as seg

#cost heuristic for the fourier snake
def cost(im, chain8, sigma = 1):
    edge = seg.decode_chain8(chain8)
    region = seg.flood_fill(edge)

    m_in = (region * im).mean()
    m_out =((1-region) * im).mean()
    
    H = ((im - m_in)**2 + (im - m_out)**2) / (2 * sigma**2)).sum()
    
    return H
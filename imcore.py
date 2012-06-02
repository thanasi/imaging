# Athanasios Athanassiadis Feb 2012
import numpy as np
import pylab as pl

# get the optimal thresholding level for an n-dim image
# from Otsu Threshold Selection Method paper
def otsu_level(im, plot=True):
    if im.std() < 10e-10:
        print 'otsu_level: Uniform Image, no optimal threshold'
        return -1
    pdf, bins = np.histogram(im,bins=256,density=True)
    bins = bins[1:]
    width = bins[1]-bins[0]
    
    mt = (pdf * bins).sum()
    st2 = ((bins - mt)**2 * pdf).sum()
    
    sb2 = []
    
    for k in range(1,len(bins)):
        w0 = pdf[:k].sum() * width
        w1 = pdf[k:].sum() * width
        m0 = (bins * pdf)[:k].sum() / w0
        m1 = (bins * pdf)[k:].sum() / w1
        
        sb2.append(w0 * w1 * (m1 - m0)**2)
    
    sb2 = np.array(sb2)
    eta = sb2 / st2
    
    kk = bins[eta==eta.max()][0]
    if plot:
        pl.plot(bins+width/2,pdf)
        pl.axvline(kk)
        pl.show()
   
    return kk
    
# fill the interior of a region (including the boundary)
# using a cue
# input should be binary edge of a region with no holes
def flood_fill(edge, i=None, j=None):
    region = edge.copy()
    if i==None or j==None:
        i,j = CoM(edge)
    
    q = [(i,j)]
    
    while len(q) != 0:
        i,j = q.pop(0)
        if region[i,j]==0:
            region[i,j] = 1
            q.append((i-1,j))
            q.append((i+1,j))
            q.append((i,j+1))
            q.append((i,j-1))
    return region    


# pad image with zeros    
def pad_image(im, pad=1):
    newim = np.zeros(np.array(im.shape) + 2*pad)
    newim[pad:-pad,pad:-pad] = im.copy()
    
    return newim

# resample an image evenly into newshape
def resample(im,newshape=(8,8)):
    samples = np.zeros(im.shape)
    sim = np.zeros(newshape)
    
    # get the sample spacing in each direction
    # and the appropriate shift to center the sampling
    spacing = np.array(im.shape,dtype=np.float)/np.array(newshape,dtype=np.float)
    shift = spacing/2

    for n in range(newshape[0]):
        for m in range(newshape[1]):
            # np.around() to round indices to nearest int
            samples[np.floor(n*spacing[0]+shift[0]),\
                    np.floor(m*spacing[1]+shift[1])] += 1
            
            sim[n,m] = im[np.floor(n*spacing[0]+shift[0]),\
                          np.floor(m*spacing[1]+shift[1])]

    return sim,samples
    
# perform 2-dimensional center of mass calculation
def CoM(im):
    center = np.zeros(2)
    shape = np.array(im.shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            center += im[i,j]*np.array([i,j])
    center /= 1.0*len(np.nonzero(im)[0])
    return np.around(center)

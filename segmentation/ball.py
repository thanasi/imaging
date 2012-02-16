#Athanasios Athanassiadis Jan 2012
import numpy as np
from scipy.misc import imsave

#define various metrics for distances
def euclid_dist(pt1, pt2=[0]):
    #convert input into useful np.array datatype
    pt1 = np.array(pt1)
    pt2 = np.array(pt2)
    #make sure the points have the same dimensionality, or that one is a constant
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

#dictionary of distance algorithms for easy user access later
distalgs = {'euclid': euclid_dist, '4': four_dist, '8': eight_dist}

#draw a ball
#shell can be specified by outer radius and thickness (default thickness 1px)
#or by two bounding radii
#uses matrix coordinates (row,col)
def make_ball(r, shell=1, r2=None, bgsize=(32,32), center=None, dmetric='euclid', ret='mask'):
    #make sure the desired distance algorithm is valid
    if dmetric not in distalgs:
        dmetric = 'euclid'
        print 'make_ball: invalid metric. proceeding with euclidean metric'

    dist = distalgs[dmetric]
        
    #initialize input variables to array datatype (np.array)
    #set center to middle of image if not specified
    bgsize = np.array(bgsize)
    if center==None:
        center = bgsize/2

    #init image
    img = np.zeros(bgsize)

    #compute distances to center
    for x in range(bgsize[0]):
        for y in range(bgsize[1]):
            img[x,y] = dist((x,y), center)

    #create binary mask based on distances
    if r2 == None:
        mask = (img <= r) * (img > r-shell)
    else:
        mask = (img <= max([r, r2])) * (img > min([r,r2]))

    #if desired, only return distance map, else just return mask
    if ret=='img':
        return img
    else:
        return mask

#resample an image evenly into newshape
def resample(im,newshape=(8,8)):
    samples = np.zeros(im.shape)
    sim = np.zeros(newshape)
    
    #get the sample spacing in each direction
    #and the appropriate shift to center the sampling
    spacing = np.array(im.shape,dtype=np.float)/np.array(newshape,dtype=np.float)
    shift = spacing/2

    for n in range(newshape[0]):
        for m in range(newshape[1]):
            #np.around() to round indeces to nearest int
            samples[np.floor(n*spacing[0]+shift[0]),\
                    np.floor(m*spacing[1]+shift[1])] += 1
            
            sim[n,m] = im[np.floor(n*spacing[0]+shift[0]),\
                          np.floor(m*spacing[1]+shift[1])]

    return sim,samples
    
#turn a binary image into run-length data
def im2rl(im):
    arr=np.array(im)
    rl = ''
    opn = 0    #keep track of whether we're in the image or in the bkg
    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            if arr[r,c]==0 and opn==1: #if black and was white
                    rl += '{}) '.format(c-1)
                    opn = 0
            if arr[r,c]==1 and opn==0: #if white and was black
                    rl += '({},{},'.format(r,c)
                    opn = 1
        if opn==1:  #if last pix in row was white
            rl += '{}) '.format(c)
            opn = 0
                    
    return rl

#decode run-length code into binary image
def rl2im(rl, fn=None, imdim=(32,32)):
    im = np.zeros(imdim)
    if not(fn==None):
        with open(fn,'r') as infile:
            rl=infile.readline()

    for code in rl.split():
        try:
            [r,c1,c2] = [int(i) for i in code[1:-1].split(',')]
            for c in range(c1,c2+1):
                im[r,c] = 1 
        except:
            print 'improper input format. skipping input: {}\n'.format(code)        
        
    return im

#convert image into quad-tree code
#encodes from top left of the quadrant at each level
def im2qt(im):
    arr = np.array(im)
    scores = []
    tmpscores = []
    qtcode = ''
    s1,s2 = arr.shape

    #uniformity metric is all black or all white.  Gray causes a daughter node to be created.
    if arr.sum()==0:
        qtcode = 'b '
    elif arr.sum()==np.prod(arr.shape):
        qtcode = 'w '
    else:
        qtcode += 'g( '
        for i1,i2 in [(0,s1/2),(s1/2,s1)]:
            for j1,j2 in [(0,s2/2),(s2/2,s2)]:
                qtcode += im2qt(arr[i1:i2,j1:j2])
        qtcode += ') '

    return qtcode

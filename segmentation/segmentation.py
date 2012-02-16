# Athanasios Athanassiadis Jan 2012
import numpy as np
from scipy.misc import imsave
import pylab as pl

# establish maps between direction and motion
# 4-connected
#   X  1  X
#   2  X  0
#   X  3  X
map4 = {0: np.array((0,1)),
        1: np.array((-1,0)),
        2: np.array((0,-1)),
        3: np.array((1,0))
        }
# 8-connected
#   3  2  1
#   4  X  0
#   5  6  7
map8 = {0: np.array((0,1)),
        1: np.array((-1,1)),
        2: np.array((-1,0)),
        3: np.array((-1,-1)),
        4: np.array((0,-1)),
        5: np.array((1,-1)),
        6: np.array((1,0)),
        7: np.array((1,1))
        }
        
# pad image with zeros    
def pad_image(im, pad=1):
    newim = np.zeros(np.array(im.shape) + 2*pad)
    newim[pad:-pad,pad:-pad] = im.copy()
    
    return newim

# track the edge of a region in an image
# im should be a binary mask
# start is an optional point to start the search
def track_edge(im,start=None):
    edge = np.zeros(im.shape)
    im2 = pad_image(im)
    chain = []
    dir = 6
    
    # if it exists, find first 'on' point in image
    # row,col point encoding
    try:
        on = np.nonzero(im2)
        i,j =on[0][0],on[1][0]
        chain = [i-1,j-1]
        p0 = (i,j)
        point = np.array(p0)
    except:
        print 'No figure found'
        return edge, np.array(chain)
    
    # unless a start point is specified, use the first 'on' point as the start
    if start!=None:
        p0 = start
        point = np.array(p0)
        
    iter = 0
    # loop until break or too many iterations reached
    while True:
        iter+=1
        if iter >= len(im2.flatten()):
            print '***track_edge: max iterations reached with no end in sight...'
            break
        # set next direction to look, 1 step counterclockwise from where we came
        checkdir = (dir+7) % 8
        i,j = point + map8[checkdir]
        
        # if we hit a pixel in the region, move there and add the direction to the list
        if im2[i,j]==1:
            dir = checkdir
            point = point+map8[checkdir]
            edge[i,j]=1
            chain.append(dir)
            
            # if we've hit the start, then end the loop
            if (i,j) == p0:
                break
           
        # otherwise, check the next dir
        else:
            dir+=1
    
    return edge,np.array(chain)

# reduce 4-connected edge to be 8-connected where possible
def reduce_chain(chain):
    # keep starting pixel info - it can't be redundant
    chain8 = [chain[i] for i in range(2)]
    i,j = 2,3
    
    while j<len(chain):
        # based on search direction, the edge is redundant if the difference of the directions gone is a positive odd number
        # also because going counter-clockwise, movement of 0 should be treated as a 4 when paired with a movement of 3, so handle that case individually
        # handle those individually
        if chain[i] == 0 and chain[j]==3:
            newdir = 7
            chain8.append(newdir)
            i+=2
            j+=2
        elif chain[i] == 3 and chain[j] ==0:
            newdir = 6
            chain8.append(newdir)
            i+=1
            j+=1
        elif (chain[i]-chain[j]>0) and ((chain[i]-chain[j]) % 2 == 1) and (chain[i]-chain[j]!=3):
            newdir = chain[i]+chain[j]                     
            chain8.append(newdir)
            i+=2 
            j+=2
        
        # need to account for the fact that numbers have changed between encodings
        else:
            chain8.append(2*chain[i])
            j+=1
            i+=1
  
    return np.array(chain8)

# decode 8-connected chain code
def decode_edge8(chain8, shape):
    edge = np.zeros(shape)
    i,j = chain8[:2]
    edge[i,j] = 1

    for dir in chain8[2:]:
        i,j = np.array([i,j])+map8[dir]
        edge[i,j] = 1

    return edge

# convert an 8-connected path to a list of coordinates
def path2coords(path):
    coords = [np.array((path[0],path[1]))]
    for dir in path[2:]:
        coords.append(coords[-1]+map8[dir])
    
    return np.array(coords)
    
# write the chain-code
def write_chain(fn, chain):
    with open(fn,'w') as of:
        for i in chain:
            of.write('{} '.format(i))
    print 'Successfully wrote: '+fn

# find and label 8-connected components
def label_components(im):
    # initially pad label image so that we can the first row without error
    l_im = pad_image(np.zeros(im.shape))
    equiv = {0:0.0}
    
    # raster through image
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i,j]==1:
                # find if any neighbors have already been labeled
                # if so, then take the smalles of all neighboring labels
                # otherwise, create a new label
                nearby = []
                for dir in [1,2,3,4]:
                    dirval = l_im[i+map8[dir][0]+1,j+map8[dir][1]+1]
                    if dirval > 0:
                        nearby.append(dirval)
                if nearby==[]:
                    newval = max(equiv)+1
                    nearby.append(newval)
                else:
                    newval = min(nearby) 
                    
                l_im[i+1,j+1] = newval
            
                # adjust equivalence table, but maintain previous corrections to the table
                for n in nearby:
                    if n in equiv:
                        equiv[n] = min(newval,equiv[n])
                    else:
                        equiv[n] = newval
    
    # adjust image according to equivalence table
    # go backwards through the keys so that chains of equivalences are handled properly
    for key in equiv.keys()[::-1]:
        l_im[l_im==key] = equiv[key]
    
    return l_im[1:-1,1:-1],equiv    # return without padding
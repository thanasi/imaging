from pylab import *
from scipy.misc import imread
from scipy.ndimage.filters import gaussian_filter

from ball import make_ball
from segmentation import track_edge, reduce_chain, decode_edge8, path2coords, pad_image
from fourierd import *

print 'making image'
#ball = pad_image(make_ball(175, shell=176, bgsize = (600,600), dmetric='euclid'))
#ball2 = pad_image(make_ball(50, shell=51, center=(200, 200), bgsize = (600,600), dmetric='8'))
#im = ball + ball2

im = imread('im.png').astype(np.int)

print 'tracking edge'
edge,chain8 = track_edge(im>0)
#print 'reducing chain'
#chain8 = reduce_chain(chain)

print 'running path2coords'
z = path2coords(chain8)

print 'makeFDfunc'
Z = makeFDfunc(z)

print 'should get output soon....'
print Z(0), Z(1)

N = len(z)
Z2 = np.array([Z(k) for k in range(N)])


path = np.around(fd2path(Z2, N))

FDedge = np.zeros(im.shape)

for point in path:
    FDedge[point[0],point[1]] = 1

gray()    
figure(1)
imshow(im)
scatter(path[:,1], path[:,0], c='r')
#axis([im.shape[0]-1,0,im.shape[1]-1,0])
figure(2)
imshow(FDedge)


print 'tracking reconstructed edge'
FDedge2,FDchain = track_edge(FDedge)
figure(3)
spectral()
imshow(FDedge2+FDedge)

print (FDedge==FDedge2).sum(), FDedge.shape[0] * FDedge.shape[1]

show()
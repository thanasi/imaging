from pylab import *
from ball import make_ball
from segmentation import track_edge, reduce_chain, decode_edge8, path2coords
from fourierd import *

print 'making ball'
ball = make_ball(100, shell=5, bgsize=(300,300), dmetric='euclid')
#ball2 = make_ball(5, shell=2, center=(5,15),dmetric='8')

print 'tracking edge'
edge,chain = track_edge(ball)
print 'reducing chain'
chain8 = reduce_chain(chain)

print 'running path2coords'
z = path2coords(chain8)

print 'makeFDfunc'
Z = makeFDfunc(z)

print 'should get output soon....'
print Z(0), Z(1)

N = len(z)
Z2 = np.array([Z(k) for k in range(N)])


path = fd2path(Z2, N)

#FDedge = np.zeros(ball.shape)

#for point in path:
#    FDedge[point[0],point[1]] = 1

gray()    
figure(1)
imshow(ball)
scatter(path[:,1], path[:,0])
#figure(2)
#imshow(FDedge)
show()
# Athanasios Athanassiadis Feb 2012

# Errors 2/15:
#   fd2path doesn't return correct results unless len(Z) == N
#   path2fd seems to return slightly incorrect Z(0) and a fairly incorrect Z(1)



import numpy as np
from segmentation import map8

pi = np.pi
sqrt = np.sqrt
exp = np.exp
atan2 = np.arctan2


# create a function based on the path that returns
# the desired fourier descriptor
def makeFDfunc(path):
    return lambda k: path2fd(path, k)

# calculate the kth fourier descriptor of a path
# path should be an Nx2 array of x,y coords
def path2fd(path, k):
    N = len(path)
    n = np.arange(N)
    # adjust order to be x,y from row,col
    [x,y] = np.array(path).T
  
    z = x + 1.0j * y
    Zk = 1.0 / N * (z*exp(-2j * pi * n * k / N)).sum()
                         
    # if the imaginary part is < 1e-10, then consider the number real
    return np.real_if_close(Zk,1e6)
    
# calculate a path of length given a set of fourier descriptors  
def fd2path(Z,N):
    N2 = len(Z)
    Z2 = np.zeros(N)
    if N>N2:
        Z2[:N2-N] = Z
    elif N<N2:
        Z2 = Z[:N-N2]
    else:
        Z2 = Z
    k = np.arange(N)
    z = np.array([(Z2 * exp(2j * pi * n * k / N)).sum() \
                  for n in range(N)])
    
    x = np.real(z)
    y = np.imag(z)
    
    # switch back to row,col from x,y
    path = np.array(zip(x,y))
    
    return path
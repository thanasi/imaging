#Athanasios Athanassiadis Feb 2012
import numpy as np

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

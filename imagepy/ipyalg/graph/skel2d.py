import numpy as np
import scipy.ndimage as ndimg
from numba import jit

from scipy.ndimage import label, generate_binary_structure
from scipy.ndimage import distance_transform_edt
strc = np.ones((3,3), dtype='bool')
    
# check whether this pixcel can be removed
def check(n):
    a = [(n>>i) & 1 for i in range(8)]
    a.insert(4, 0) # make the 3x3 unit
    # if up, down, left, right all are 1, you cannot make a hole
    if a[1] & a[3] & a[5] & a[7]:return False
    #if sum(a)==1: return False
    a = np.array(a).reshape((3,3))
    # segments
    n = label(a, strc)[1]
    # if sum is 0, it is a isolate point, you cannot remove it.
    # if number of segments > 2, you cannot split them.
    return n<2
    return a.sum()>1 and n<2
    if a.sum()==1 or n>2: return 2
    if a.sum()>1 and n<2: return 1
    return 0

lut = np.array([check(n) for n in range(256)])
lut = np.dot(lut.reshape((-1,8)), [1,2,4,8,16,32,64,128]).astype(np.uint8)
'''
lut = np.array([200, 206, 220, 204, 0, 207, 0, 204, 0, 207, 221, 51, 1, 207, 221, 51,
       0, 0, 221, 204, 0, 0, 0, 204, 1, 207, 221, 51, 1, 207, 221, 51], dtype=np.int8)
'''

fac = np.array([1,2,4,8,16,32,64,128])

@jit(nopython=True)
def medial_axis(data, idx, branch = True):
    h, w = data.shape
    data = data.ravel()
    for id in idx:
        if data[id]==0:continue
        i2=id-w;i8=id+w;i1=i2-1;i3=i2+1;
        i4=id-1;i6=id+1;i7=i8-1;i9=i8+1;

        c = (data[i1]>0)<<0|(data[i2]>0)<<1\
            |(data[i3]>0)<<2|(data[i4]>0)<<3\
            |(data[i6]>0)<<4|(data[i7]>0)<<5\
            |(data[i8]>0)<<6|(data[i9]>0)<<7
        if (lut[c//8]>> c%8) &1:data[id]=0
    return 0;

def mid_axis(img):
    dis = distance_transform_edt(img)
    dis[[0,-1],:] = 0; dis[:,[0,-1]] = 0
    idx = np.argsort(dis.flat).astype(np.int32)
    medial_axis(dis, idx, lut)
    return dis

if __name__ == '__main__':
    from time import time
    from skimage.data import horse
    #from skimage.morphology import medial_axis
    import matplotlib.pyplot as plt

    img = ~horse()*255
    mid_axis(img.copy())
    t1 = time()
    a = mid_axis(img)
    t2 = time()
    print(t2 - t1)
    plt.imshow(a)
    plt.show()
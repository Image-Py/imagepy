# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 00:26:45 2016
@author: yxl
"""
import numpy as np
from skimage.morphology import skeletonize
from skimage.morphology import medial_axis

from imagepy.core.engine import Filter

class Skeleton(Filter):
    title = 'Skeleton'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        img[:] = skeletonize(snap>0)
        img *= 255

class MedialAxis(Filter):
    title = 'Medial Axis'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'dis':False}
    view = [(bool,'distance transform', 'dis')]

    def run(self, ips, snap, img, para = None):
        rst = medial_axis(snap>0,return_distance=para['dis'])
        if not para['dis']:
            img[:] = rst
            img *= 255
        else:
            img[:] = rst[0]
            np.multiply(img, rst[1], out=img, casting='unsafe')

plgs = [Skeleton, MedialAxis]
'''
import numpy as np
import scipy.ndimage as nimg
from scipy.ndimage import label, generate_binary_structure

strc = generate_binary_structure(2, 2)

def check(n):
    a = [(n>>i) & 1 for i in range(8)]
    a.insert(4, 0) # make the 3x3 unit
    # if up, down, left, right all are 1, you cannot make a hole
    if a[1] & a[3] & a[5] & a[7]:return False
    a = np.array(a).reshape((3,3))
    # segments
    n = label(a, strc)[1]
    # if sum is 0, it is a isolate point, you cannot remove it.
    # if number of segments > 2, you cannot split them.
    return a.sum()>1 and n<2

lut = [check(n) for n in range(256)]

def skel2d(data, idx, lut):
    h, w = data.shape
    data = data.flat
    for i in idx:
        if data[i]==0 : continue
        xy = [i-w-1, i-w, i-w+1,\
              i-1  ,      i+1  ,\
              i+w-1, i+w, i+w+1]

        c = sum([(data[xy[j]]==255)<<j for j in range(8)])
        if lut[c]:data[i] = 128


def mid_axis(img):
    dis = nimg.distance_transform_edt(img)
    idx = np.argsort(dis.flat).astype(np.int32)
    skel2d(img, idx, lut)
    #api.skel2d(dis.ctypes.data, idx.ctypes.data, dis.size, dis.shape[1], dis.shape[0],lut.ctypes.data)
    return img

class MyMedialAxis(Filter):
  title = 'My Medial Axis'
  note = ['all', 'auto_msk', 'auto_snap', 'preview']
  para = {'dis':False}
  view = [(bool,'distance transform', 'dis')]

  #process
  def run(self, ips, snap, img, para = None):
    mid_axis(img)

plgs = [Skeleton, MedialAxis, MyMedialAxis]

## Description
[I use the medial_axis function, the result image has some double lines or small holes, then I count make a topology analysis!]
![demo picture] (http://data.imagepy.org/skebug.png "The medial_axis result and mine result")

I view the source code, and found the medial_axis function, sort by distance map, then use the skeletonize function's table to check if to remove the pixel. But some times the sort cannot make sure the out-inside turn in extreme condition. So we need a new table for the media_axis. This is my code：

**Build the table**
```python
from scipy.ndimage import label, generate_binary_structure

strc = generate_binary_structure(2, 2)

# check whether this pixel can be removed
def check(n):
    a = [(n>>i) & 1 for i in range(8)]
    a.insert(4, 0) 
    make the 3x3 unit
       0  1  2
       3  p  4
       5  6  7
    # if up, down, left, right all are 1, you cannot make a hole
    if a[1] & a[3] & a[5] & a[7]:return False
    a = np.array(a).reshape((3,3))
    # segments
    n = label(a, strc)[1]
    # if sum is 0, it is a isolate point, you cannot remove it.
    # if sum is 1, it is a terminal point, you cannot remove it.
    # if number of segments = 2, you cannot split the line.
    # if number of segments > 2, it is a node, you cannot remove it.
    return a.sum()>1 and n<2

lut = [check(n) for n in range(256)]
'''
'''
like this:
array([[0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1],
       [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
       [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
       [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
       [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
       [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0]])
'''
'''
```

**Remove the pixcels**
```python
def skel2d(data, idx, lut):
    h, w = data.shape
    data = data.flat
    for i in idx:
        if data[i]==0 : continue
        xy = [i-w-1, i-w, i-w+1,\
                i-1  ,            i+1  ,\
                i+w-1, i+w, i+w+1]

        c = sum([(data[xy[j]]==255)<<j for j in range(8)])
        if lut[c]:data[i] = 128

def mid_axis(img):
    dis = nimg.distance_transform_edt(img)
    idx = np.argsort(dis.flat).astype(np.int32)
    skel2d(img, idx, lut)
```
I think my code is right, but needs more test.
May I send a Pull Request after rewrite in cython?

## Way to reproduce
[If reporting a bug, please include the following important information:]
- [test image ] (http://data.imagepy.org/ske_bug.png "My Test Image")
- [Ubuntu 14.0 ] Operating system and version
- [ 2.7] Python version
- [ 0.12.3] scikit-image version (run `skimage.__version__`)
'''
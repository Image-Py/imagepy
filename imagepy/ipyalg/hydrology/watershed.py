import numpy as np
from numba import jit
from scipy.ndimage import label, generate_binary_structure
from skimage.io import imread, imsave

def neighbors(shape, conn=1):
    dim = len(shape)
    block = generate_binary_structure(dim, conn)
    block[tuple([1]*dim)] = 0
    idx = np.where(block>0)
    idx = np.array(idx, dtype=np.uint8).T
    idx = np.array(idx-[1]*dim)
    acc = np.cumprod((1,)+shape[::-1][:-1])
    return np.dot(idx, acc[::-1])

@jit
def step(img, msk, line, pts, s, level, up, nbs):
    cur = 0
    while cur<s:
        p = pts[cur]
        if msk[p] == 0xfffffffe or up and img[p]>level or not up and img[p]<level:
            cur += 1
            continue
        for dp in nbs:
            cp = p+dp
            if msk[cp]==0:
                msk[cp] = msk[p]
                if s == len(pts):
                    s, cur = clear(pts, s, cur)
                pts[s] = cp
                s+=1
                
            elif msk[cp] == msk[p]:
                continue
            elif msk[cp] == 0xffffffff:
                continue
            elif msk[cp] == 0xfffffffe:
                continue
                
            elif line : msk[cp] = 0xfffffffe
        pts[cur] = -1
        cur+=1
    return cur

@jit
def clear(pts, s, cur):
    ns = 0; nc=0;
    for c in range(s):
        if pts[c]!=-1:
            pts[ns] = pts[c]
            ns += 1
            if c<cur:nc += 1
    return ns, nc
        
@jit
def collect(img, mark, nbs, pts):
    bins = np.zeros(img.max()+1, dtype=np.uint32)
    cur = 0
    for p in range(len(mark)):
        bins[img[p]] += 1
        if mark[p]==0xffffffff: continue # edge
        if mark[p]==0: continue      # zero
        for dp in nbs:
            if mark[p+dp]!=mark[p]:
                pts[cur] = p
                cur += 1
                break
    return cur, bins

@jit
def erose(mark):
    for i in range(len(mark)):
        if mark[i]>0xfffffff0:mark[i]=0

def buffer(img, dtype):
    buf = np.zeros(tuple(np.array(img.shape)+2), dtype=dtype)
    buf[tuple([slice(1,-1)]*buf.ndim)] = img
    return buf

def watershed(img, mark, conn=1, line=False, up=True):
    maxv = img.max(); minv = img.min();
    if img.dtype != np.uint8:
        img = ((img-minv)*(255/(maxv-minv))).astype(np.uint8)
    img = buffer(img, np.uint8)
    mark = buffer(mark, np.uint32)
    ndim = img.ndim
    for n in range(ndim):
        idx = [slice(None) if i!=n else [0,-1] for i in range(ndim)]
        mark[tuple(idx)] = 0xffffffff
    
    nbs = neighbors(img.shape, conn)
    img = img.ravel()
    mark1d = mark.ravel()

    pts = np.zeros(img.size//3, dtype=np.int64)
    s, bins = collect(img, mark1d, nbs, pts)

    for level in range(len(bins))[::1 if up else -1]:
        if bins[level]==0:continue
        s, c = clear(pts, s, 0)
        s = step(img, mark1d, line, pts, s, level, up, nbs)
    if line:erose(mark1d)
    return mark[tuple([slice(1,-1)]*ndim)]
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from skimage.filters import sobel
    from skimage.data import coins
    coins = coins()
    dem = sobel(coins)
    markers = np.zeros_like(coins, dtype=np.uint32)
    markers[coins < 30] = 1
    markers[coins > 150] = 2
    plt.imshow(markers)
    plt.show()
    watershed(dem, markers)
    plt.imshow(markers)
    plt.show()
    '''
    from skimage.io import imread
    import matplotlib.pyplot as plt
    from time import time
    
    dem = imread('ice.png')
    mark = imread('mark.png')
    mark, n = label(mark>0, generate_binary_structure(2,2), output=np.uint16)
    start = time()
    #skrst = skwsh(dem, mark, watershed_line=True)
    print('skimage:', time()-start)
    watershed(dem, mark.copy())
    start = time()
    watershed(dem, mark, 1)
    print('mine:', time()-start)

    imsave('line.png', ((mark>0)*255).astype(np.uint8))
    '''

import scipy.ndimage as ndimg
import numpy as np
from numba import jit

def neighbors(shape):
    dim = len(shape)
    block = np.ones([3]*dim)
    block[tuple([1]*dim)] = 0
    idx = np.where(block>0)
    idx = np.array(idx, dtype=np.uint8).T
    idx = np.array(idx-[1]*dim)
    acc = np.cumprod((1,)+shape[::-1][:-1])
    return np.dot(idx, acc[::-1])

@jit(nopython=True) # trans index to r, c...
def idx2rc(idx, acc):
    rst = np.zeros((len(idx), len(acc)), dtype=np.int16)
    for i in range(len(idx)):
        for j in range(len(acc)):
            rst[i,j] = idx[i]//acc[j]
            idx[i] -= rst[i,j]*acc[j]
    return rst

@jit(nopython=True)  # fill a node (may be two or more points)
def fill(img, msk, p, nbs, buf):
    buf[0] = p
    back = img[p]
    cur = 0; s = 1;
    
    while cur<s:
        p = buf[cur]
        for dp in nbs:
            cp = p+dp
            if img[cp]==back and msk[cp]==1:
                msk[cp] = 3
                buf[s] = cp
                s+=1
                if s==len(buf):
                    buf[:s-cur] = buf[cur:]
                    s-=cur; cur=0;
        cur += 1

@jit(nopython=True)  # my mark
def mark(img, nbs, msk, buf, mode): # mark the array use (0, 1, 2)
    idx = np.zeros(msk.size//3, dtype=np.int64)
    img = img.ravel()
    msk = msk.ravel()
    s = 0
    for p in range(len(img)):
        if msk[p]!=1:continue
        sta = 0
        for dp in nbs:
            if img[p+dp]==img[p]:sta+=1
            if mode and img[p+dp]>img[p]:
                sta = 100
                break
            elif not mode and img[p+dp]<img[p]:
                sta = 100
                break
        if sta==100:continue
        msk[p] = 3
        if sta>0:
            fill(img, msk, p, nbs, buf)
            
        idx[s] = p
        s += 1
        if s==len(idx):break
    return idx[:s].copy()

@jit(nopython=True)  # 3 max 2 zmd b4 ptd
def filter(img, msk, nbs, acc, idx, bur, tor, mode):
    img = img.ravel()
    msk = msk.ravel()

    arg = np.argsort(img[idx])[::-1 if mode else 1]
    
    for i in arg:
        if msk[idx[i]]!=3:
            idx[i] = 0
            continue
        cur = 0; s = 1;
        bur[0] = idx[i]
        while cur<s:
            p = bur[cur]
            if msk[p] == 2:
                idx[i]=0
                break

            for dp in nbs:
                cp = p+dp
                if msk[cp]==0 or cp==idx[i] or msk[cp] == 4: continue
                if mode and img[cp] < img[idx[i]]-tor: continue
                if not mode and img[cp] > img[idx[i]]+tor: continue
                bur[s] = cp
                s += 1
                if s==msk.size//3:
                    cut = cur//2
                    msk[bur[:cut]] = 2
                    bur[:s-cut] = bur[cut:]
                    cur -= cut
                    s -= cut
    
                if msk[cp]!=2:msk[cp] = 4
            cur += 1
        msk[bur[:s]] = 2

    return idx2rc(idx[idx>0], acc)
    

def find_maximum(img, tor, mode = True):
    msk = np.zeros_like(img, dtype=np.uint8)
    msk[tuple([slice(1,-1)]*img.ndim)] = 1
    buf = np.zeros(img.size//3, dtype=np.int64)
    nbs = neighbors(img.shape)
    acc = np.cumprod((1,)+img.shape[::-1][:-1])[::-1]
    idx = mark(img, nbs, msk, buf, mode)
    idx = filter(img, msk, nbs, acc, idx, buf, tor, mode)
    return idx

if __name__ == '__main__':
    from skimage.io import imread
    from scipy.ndimage import gaussian_filter, distance_transform_edt
    from time import time
    import matplotlib.pyplot as plt
    from skimage.data import horse

    img = distance_transform_edt(~horse())
    pts = find_maximum(img, 20, True)
    start = time()
    pts = find_maximum(img, 10, True)
    print(time()-start)
    plt.imshow(img, cmap='gray')
    plt.plot(pts[:,1], pts[:,0], 'y.')
    plt.show()

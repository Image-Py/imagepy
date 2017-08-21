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

@jit # trans index to r, c...
def idx2rc(idx, acc):
    rst = np.zeros((len(idx), len(acc)), dtype=np.int16)
    for i in range(len(idx)):
        for j in range(len(acc)):
            rst[i,j] = idx[i]//acc[j]
            idx[i] -= rst[i,j]*acc[j]
    return rst


@jit # fill a node (may be two or more points)
def fill(img, msk, p, nbs, buf):
    msk[p] = 2
    buf[0] = p
    back = img[p]
    cur = 0; s = 1;
    
    while cur<s:
        p = buf[cur]
        for dp in nbs:
            cp = p+dp
            if img[cp]==back and msk[cp]==1:
                msk[cp] = 2
                buf[s] = cp
                s+=1
                if s==len(buf):
                    print('abced')
                    print(cur, s)
                    buf[:s-cur] = buf[cur:]
                    s-=cur; cur=0;
                    print(cur, s)
        cur += 1
    msk[p] = 3

@jit # my mark
def mark(img, msk, buf, mode): # mark the array use (0, 1, 2)
    nbs = neighbors(img.shape)
    idx = np.zeros(1024*128, dtype=np.int64)
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
        if sta==len(nbs):
            fill(img, msk, p, nbs, buf)
        else:
            msk[p] = 3
        idx[s] = p
        s += 1
        if s==len(idx):
            print('break!!!')
            break
    return idx[:s].copy()

@jit # 3 最大值标记 2 殖民地标记 4 普通殖民地
def filter(img, msk, idx, bur, tor, mode):
    nbs = neighbors(img.shape)
    acc = np.cumprod((1,)+img.shape[::-1][:-1])[::-1]
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
            if msk[p] == 2: #已经被更高的占领
                idx[i]=0
                break
            msk[p] = 2
            for dp in nbs:
                cp = p+dp
                if msk[cp]==0 or msk[cp]==4 or msk[cp]==2: continue #边缘和自己不要
                if mode and img[cp] < img[bur[0]]-tor: continue
                if not mode and img[cp] > img[bur[0]]+tor: continue
                #if img[cp] < img[bur[0]]-tor: continue
                bur[s] = cp
                msk[cp] = 4
                s += 1
                if s==1024*128:
                    bur[:s-cur] = bur[cur:]
                    s = s-cur; cur=0;
                    
                 
                #if msk[cp] != 2: msk[cp] = 4
            cur += 1

        #msk[bur[:s]] = 2
    return idx2rc(idx[idx>0], acc)
    

def find_maximum(img, tor, mode = True):
    msk = np.zeros_like(img, dtype=np.uint8)
    msk[tuple([slice(1,-1)]*img.ndim)] = 1
    buf = np.zeros(1024*128, dtype=np.int64)
    idx = mark(img, msk, buf, mode)
    idx = filter(img, msk, idx, buf, tor, mode)
    return idx

if __name__ == '__main__':
    from scipy.misc import imread
    from scipy.ndimage import gaussian_filter
    import matplotlib.pyplot as plt
    img = gaussian_filter(imread('test.png'), 2)
    pts = find_maximum(img, 5, False)
    plt.imshow(img, cmap='gray')
    plt.plot(pts[:,1], pts[:,0], 'y.')
    plt.show()
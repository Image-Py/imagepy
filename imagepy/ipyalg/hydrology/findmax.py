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

@jit # my mark
def mark(img, buf, mode): # mark the array use (0, 1, 2)
    nbs = neighbors(img.shape)
    idx = np.zeros(1024*128, dtype=np.int64)
    img = img.ravel()
    bur = buf.ravel()
    s = 0
    for p in range(len(img)):
        if bur[p]==0:continue
        sta = False
        for dp in nbs:
            if mode and img[p+dp]>img[p]:
                sta = True
                break
            elif not mode and img[p+dp]<img[p]:
                sta = True
                break
        if sta:continue
        bur[p] = 3
        idx[s] = p
        s += 1
        if s==len(idx):break
    return idx[:s].copy()

@jit
def filter(img, buf, idx, tor, mode):
    nbs = neighbors(img.shape)
    acc = np.cumprod((1,)+img.shape[::-1][:-1])[::-1]
    img = img.ravel()
    buf1 = buf.ravel()
    arg = np.argsort(img[idx])[::-1 if mode else 1]
    bur = np.zeros(1024*128, dtype=np.int64)
    for i in arg:
        if buf1[idx[i]]!=3:
            idx[i] = 0
            continue
        cur = 0; s = 1;
        bur[0] = idx[i]
        while True:
            p = bur[cur]
            if buf1[p] == 2:
                idx[i]=0
                break
            for dp in nbs:
                cp = p+dp
                if buf1[cp]==0 or cp==bur[0]: continue
                if buf1[cp] == 4: continue
                if mode and img[cp] < img[bur[0]]-tor: continue
                if not mode and img[cp] > img[idx[i]]+tor: continue
                if img[cp] < img[bur[0]]-tor: continue
                bur[s] = cp
                s += 1
                if s==1024*128:
                    cut = cur//2
                    buf1[bur[:cut]] = 2
                    bur[:s-cut] = bur[cut:]
                    cur -= cut
                    s -= cut
                 
                if buf1[cp] != 2: buf1[cp] = 4
            cur += 1
            if cur==s:break
        buf1[bur[:s]] = 2
    return idx2rc(idx[idx>0], acc)
    

def find_maximum(img, tor, mode = True):
    buf = np.zeros_like(img, dtype=np.uint8)
    buf[tuple([slice(1,-1)]*img.ndim)] = 1
    idx = mark(img, buf, mode)
    idx = filter(img, buf, idx, tor, mode)
    return idx
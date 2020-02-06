import numpy as np
from numba import jit
import random
from scipy.ndimage import generate_binary_structure

def neighbors(shape, conn=1):
    dim = len(shape)
    block = generate_binary_structure(dim, conn)
    block[tuple([1]*dim)] = 0
    idx = np.where(block>0)
    idx = np.array(idx, dtype=np.uint8).T
    idx = np.array(idx-[1]*dim)
    acc = np.cumprod((1,)+shape[::-1][:-1])
    return np.dot(idx, acc[::-1])

@jit(nopython=True)
def unique(idx):
    msk = idx[:,0]<idx[:,1]
    key = idx[:,0]<<16
    key += idx[:,1]
    sort = np.argsort(key)
    idx[:] = idx[sort]
    s = i = 1
    while s<len(idx):
        if key[sort[s]]!=key[sort[s-1]]:
            idx[i,0] = idx[s,0]
            idx[i,1] = idx[s,1]
            i += 1
        s += 1
    return i
    
@jit(nopython=True)
def search(img, nbs, back):
    s, line = 0, img.ravel()
    rst = np.zeros((len(line)//2, 2), img.dtype)
    for i in range(len(line)):
        if line[i]==0:continue
        for d in nbs:
            if not back and line[i+d]==0: continue
            if line[i]==line[i+d]: continue
            rst[s,0] = line[i]
            rst[s,1] = line[i+d]
            s += 1
            
            if s==len(rst):
                s = unique(rst)
    return rst[:s]
                            
def connect_graph(img, conn=1, back=False):
    buf = np.pad(img, 1, 'constant')
    nbs = neighbors(buf.shape, conn)
    rst = search(buf, nbs, back)
    if len(rst)<2: return rst
    rst.sort(axis=1)
    return rst[:unique(rst)].copy()

def mapidx(idx):
    dic = {}
    for i in np.unique(idx): dic[i] = []
    for i,j in idx:
        dic[i].append(j)
        dic[j].append(i)
    return dic

if __name__ == '__main__':
    img = np.array([[1,1,1,1,1],
                    [1,1,2,2,1],
                    [1,3,0,0,1],
                    [1,3,1,1,4]])
    rst = connect_graph(img, 2, True)
    print(rst)
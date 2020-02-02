import numpy as np
from numba import jit
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
def search(img, nbs):
    s, line = 0, img.ravel()
    rst = np.zeros((len(line),2), img.dtype)
    for i in range(len(line)):
        if line[i]==0:continue
        for d in nbs:
            if line[i+d]==0: continue
            if line[i]==line[i+d]: continue
            rst[s,0] = line[i]
            rst[s,1] = line[i+d]
            s += 1
    return rst[:s]

def connect(img, conn=1):
    buf = np.pad(img, 1, 'constant')
    nbs = neighbors(buf.shape, conn)
    rst = search(buf, nbs)
    if len(rst)==0: return rst
    rst.sort()
    return np.unique(rst, axis=0)

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
    rst = connect(img, 2)
    print(rst)
import numpy as np
from numba import jit

from scipy.ndimage import label, generate_binary_structure

strc = np.ones((3,3), dtype=np.bool)

def count(n):
    a = [(n>>i) & 1 for i in range(8)]
    if sum(a)<=1:return False
    if a[1] & a[3] & a[5] & a[7]:return False
    a = np.array([[a[0],a[1],a[2]],
                  [a[7],  0 ,a[3]],
                  [a[6],a[5],a[4]]])
    n = label(a, strc)[1]
    return n<2
'''
lut = np.array([count(n) for n in range(256)])
lut = np.dot(lut.reshape((-1,8)), [1,2,4,8,16,32,64,128]).astype(np.uint8)
print(lut)
'''
@jit
def core(n):
    a = np.zeros(8, dtype=np.uint8)
    for i in range(8):
        a[i] = (n>>i*2)&3
    if a[1]==1 and a[0]==0: a[0]=1
    if a[1]==1 and a[2]==0: a[0]=1
    if a[3]==1 and a[2]==0: a[2]=1
    if a[3]==1 and a[4]==0: a[4]=1
    if a[5]==1 and a[4]==0: a[4]=1
    if a[5]==1 and a[6]==0: a[6]=1
    if a[7]==1 and a[6]==0: a[6]=1
    if a[7]==1 and a[0]==0: a[0]=1
    for i in range(8):
        if a[i]==0 or a[i]==2:a[i]=0
        if a[i]==1 or a[i]==3:a[i]=1
    s = 0
    for i in range(8):
        s |= a[i]<<i
    return s

index = np.array([core(i) for i in range(65536)], dtype=np.uint8)



lut = np.array([223, 221, 1, 221, 1, 221, 1, 221, 1, 0, 0, 0, 1, 221, 1, 221, 207, 204,
                0, 204, 207,  51, 207, 1, 207, 204, 0, 204, 207, 51, 207, 51], dtype=np.uint8)


def nbs8(h, w):
    return np.array([-w-1,-w,-w+1,+1,+w+1,+w,+w-1,-1], dtype=np.int32)

def nbs4(h, w):
    return np.array([-1,-w,1,w], dtype=np.int32)

@jit
def fill(img, msk, p, level, up, pts, s, c, nbs, buf):
    n = 0; cur = 0; buf[0] = p; msk[p]=2; bs = 1;
    while cur<bs:
        p = buf[cur]
        for dp in nbs:
            cp = p+dp
            if msk[cp]!=0:continue
            if up and img[cp]<level or not up and img[cp]>level:
                buf[bs] = cp
                msk[cp] = 2
                bs+=1
                if bs==len(buf):
                    buf[:bs-cur] = buf[cur:bs]
                    bs -= cur
                    cur = 0
            else:
                if s == len(pts):
                    s, c = clear(msk, pts, s, c)
                pts[s] = cp
                msk[cp] = 1
                s += 1
        cur+=1
    return s, c


@jit
def check(msk, p, nbs, lut):
    c = 0; s = 0;
    for i in range(8):
        v = msk[p+nbs[i]]
        #if v==0: c|=(0<<i*2)
        if v==1: c|=(1<<i*2)
        if v==2: c|=(2<<i*2)
        if v==3: c|=(3<<i*2)
    v = index[c]
    if lut[v//8]>>v%8 & 1:msk[p]=2
    else: msk[p]=3


@jit
def step(img, msk, pts, s, level, up, nbs, nbs8):
    ddd=0
    cur = 0
    buf = np.zeros(10240, dtype=np.int64)
    while cur<s:
        p = pts[cur]

        if up and img[p]>level or not up and img[p]<level:
            cur += 1
            continue

        filled = False
        for dp in nbs:
            cp = p+dp
            if msk[cp]==4:msk[p] = 2
            if msk[cp]==0:
                if up and img[cp]>=level or not up and img[cp]<=level:
                    msk[cp] = 1
                    if s == len(pts):
                        s, cur = clear(msk, pts, s, cur)
                    pts[s] = cp
                    s+=1
                    
                else:
                    n1,n2 = fill(img, msk, p, level, up, pts, s, cur, nbs, buf)
                    s = n1; cur = n2-1; filled = True
        
        if filled:
            cur +=1; continue;
        elif msk[p]==1:
            check(msk, p, nbs8, lut)

        cur+=1
    return cur

@jit
def clear(msk, pts, s, cur):
    ns = 0; nc=0
    for c in range(s):
        if msk[pts[c]]==1:
            pts[ns] = pts[c]
            ns += 1
            if c<cur:nc += 1
    return ns, nc
        
@jit
def collect(img, mark, nbs, pts):
    bins = np.zeros(img.max()+1, dtype=np.uint32)
    cur = 0
    
    for p in range(len(mark)):
        if mark[p]!=0:continue
        for dp in nbs:
            if mark[p+dp]==1:
                mark[p]=2

    for p in range(len(mark)):
        if mark[p]==1:mark[p]=2

    for p in range(len(mark)):
        if mark[p]!=0:continue
        s=0
        for dp in nbs:
            if mark[p+dp]==2:
                s+=0
                mark[p] = 1
                pts[cur] = p
                cur += 1
                break
        if s==0:bins[img[p]]+=1
    return cur, bins

@jit
def ridge(img, mark, up=True):
    oimg, omark = img, mark
    ndim = img.ndim
    mark[[0,-1],:] = 4
    mark[:,[0,-1]] = 4
    
    nb4 = nbs4(*img.shape)
    nb8 = nbs8(*img.shape)
    acc = np.cumprod((1,)+img.shape[::-1][:-1])[::-1]
    img = img.ravel()
    mark = mark.ravel()

    pts = np.zeros(131072, dtype=np.int64)
    s, bins = collect(img, mark, nb4, pts)
    
    #print(bins)
    aaa=0
    for level in range(len(bins))[::1 if up else -1]:
        
        if bins[level]==0:continue
        aaa+=1
        s, c = clear(mark, pts, s, 0)
        s = step(img, mark, pts, s, level, up, nb4, nb8)
        '''
        if level>250:
            plt.imshow(omark, cmap='gray')
            plt.show()
        '''
    for i in range(len(mark)):
        if mark[i] == 3:mark[i] = 255
        else: mark[i] = 0

if __name__ == '__main__':
    from skimage.io import imread
    import scipy.ndimage as ndimg
    import matplotlib.pyplot as plt
    from time import time
    
    dem = imread('dem.png')
    dem = ndimg.gaussian_filter(dem, 1)
    mark = (dem==0).astype(np.uint8)
    plt.imshow(mark)
    plt.show()
    ridge(dem, mark.copy())
    start = time()
    ridge(dem, mark)
    print(time()-start)
    dem//=2
    dem[mark==3] = 255
    plt.imshow(mark, cmap='gray')
    plt.show()

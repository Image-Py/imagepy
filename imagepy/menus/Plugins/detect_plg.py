import numpy as np
from numba import jit

def neighbors(shape):                            # 邻居坐标转索引内存
    dim = len(shape)
    block = np.ones([3]*dim)
    block[tuple([1]*dim)] = 0
    idx = np.where(block>0)
    idx = np.array(idx, dtype=np.uint8).T
    idx = np.array(idx-[1]*dim)
    acc = np.cumprod((1,)+shape[::-1][:-1])
    return np.dot(idx, acc[::-1])

@jit # trans index to r, c...
def idx2rc(idx, acc):                             # 索引转坐标
    rst = np.zeros((len(idx), len(acc)), dtype=np.int16)
    for i in range(len(idx)):
        for j in range(len(acc)):
            rst[i,j] = idx[i]//acc[j]
            idx[i] -= rst[i,j]*acc[j]
    return rst

@jit # fill a node (may be two or more points)
def fill(img, msk, p, nbs, buf):
    buf[0] = p
    back = img[p]
    cur = 0; s = 1;
    
    while cur<s:
        p = buf[cur]
        for dp in nbs:
            cp = p+dp
            if img[cp]==back and msk[cp]==1:  # 如果邻居颜色一样，并且未标记
                msk[cp] = 3                   # 标记成3，压栈
                buf[s] = cp
                s+=1
                if s==len(buf):               # 如果装满了，清理没用的
                    buf[:s-cur] = buf[cur:]
                    s-=cur; cur=0;
        cur += 1

@jit # my mark
def mark(img, msk, buf, thr, mode): # mark the array use (0：边界, 1：普通, 2:占领， 3：极值标记)
    nbs = neighbors(img.shape)
    idx = np.zeros(msk.size//3, dtype=np.int64)    # 极值数组
    img = img.ravel()
    msk = msk.ravel()
    s = 0
    for p in range(len(img)):
        if msk[p]!=1:continue    # 靠近边缘，不继续
        if img[p]>thr:continue   # 大于阈值，不继续
        sta = 0
        for dp in nbs: # 获取邻居像素索引
            if img[p+dp]==img[p]:sta+=1    # 如果周围的有一样大的，标记+1
            if mode and img[p+dp]>img[p]:  # 如果周围的有更大的，标记为100
                sta = 100
                break
            elif not mode and img[p+dp]<img[p]: # 最小值模式
                sta = 100
                break
        if sta==100:continue               # 不是极值，跳过
        msk[p] = 3                         # 标记为 3
        if sta>0:
            fill(img, msk, p, nbs, buf)    # 如果有若干一样大的，将一样大的区域填充（对于大块平坦区域，可以有效提升性能）
        idx[s] = p                         # 装入极值点
        s += 1
        if s==len(idx):break               # 装满退出（异常情况）
    return idx[:s].copy()                  # 截断拷贝

@jit # 3 max 2 zmd b4 ptd
def filter(img, msk, idx, bur, tor, area, mode):
    nbs = neighbors(img.shape)
    img = img.ravel()
    msk = msk.ravel()

    arg = np.argsort(img[idx])[::-1 if mode else 1]         # 将极值点排序

    for i in arg:                                           # 从最小的点开始遍历
        if msk[idx[i]]!=3:                                  # 如果标记位置已经不是3，则跳过
            idx[i] = 0
            continue
        cur = 0; s = 1;
        bur[0] = idx[i]
        while cur<s:
            p = bur[cur]
            if msk[p] == 2:                                 # 已经被占领
                idx[i]=0                                    # 从极值序列中擦除
                break
            if s > area:                                     # 面积超出，不符合，擦除退出
                idx[i]=0
                break
            for dp in nbs:                                   # 邻居压栈
                cp = p+dp
                if msk[cp]==0 or cp==idx[i] or msk[cp] == 4: continue    # 边缘不加，自己不加，已经标记不加
                if mode and img[cp] < img[idx[i]]-tor: continue          # 超过水位高度不加
                if not mode and img[cp] > img[idx[i]]+tor: continue      # 极小值情况
                bur[s] = cp
                s += 1
                if s==msk.size//3: # 装满清空
                    cut = cur//2
                    msk[bur[:cut]] = 2                 # 被填充的点设定为2 (占领)
                    bur[:s-cut] = bur[cut:]
                    cur -= cut
                    s -= cut
    
                if msk[cp]!=2:msk[cp] = 4              # 本次标记
            cur += 1
        msk[bur[:s]] = 2                               # 将领地标记为2
    return idx                                         # 返回有效极值坐标
    
def find_maximum(img, tor, thr, area, mode = True, mar=1):
    msk = np.zeros_like(img, dtype=np.uint8) # 复制掩膜数组
    msk[tuple([slice(mar,-mar)]*img.ndim)] = 1   # 中间部分设定为1，边缘是0
    buf = np.zeros(img.size//2, dtype=np.int64) # 缓冲数组
    idx = mark(img, msk, buf, thr, mode)        # 图像预标记
    acc = np.cumprod((1,)+img.shape[::-1][:-1])[::-1]
    idx = filter(img, msk, idx, buf, tor, area, mode)
    #idx2 = filter(img, msk.copy(), idx.copy(), buf, tor2, area, mode)
    pts = idx2rc(idx[idx>0], acc)
    #pts2 = idx2rc(idx2[idx2>0], acc)
    return pts

from imagepy.core.engine import Simple
from imagepy.core.mark import GeometryMark

class Plugin(Simple):
    title = 'Desys'
    note = ['8-bit', 'auto_snap', 'preview']
    para = {'tol':60, 'thr':180, 'area':256, 'mode':False}
    view = [(int, 'tol', (0,100), 0,  'tolerance', 'no wrong'),
            # (int, 'tol2', (0,100), 0, 'tolerance2', 'no left'),
            (int, 'thr', (1,255), 0, 'threshold', ''),
            (int, 'area', (0,10240), 0, 'area', 'max'),
            (bool, 'mode', 'white')]

    def preview(self, ips, para):
        pts = find_maximum(ips.img, para['tol'], para['thr'], para['area'], para['mode'])
        sure = {'type':'circles', 'color':(255,0,0), 'body':[list(i[::-1])+[20] for i in pts], 'lw':2}
        ips.mark = GeometryMark(sure)

    def run(self, ips, imgs, para = None):
        marks = {'type':'layers', 'body':{}}
        for i in range(len(imgs)):
            pts = find_maximum(imgs[i], para['tol'], para['thr'], para['area'], para['mode'])
            sure = {'type':'circles', 'color':(255,0,0), 'body':[list(i[::-1])+[20] for i in pts], 'lw':2}
            marks['body'][i] = sure
        ips.mark = GeometryMark(marks)

if __name__ == '__main__':
    from skimage.io import imread
    from scipy.ndimage import gaussian_filter
    from time import time
    import matplotlib.pyplot as plt
    img = gaussian_filter(imread('test.png'), 0)
    pts = find_maximum(img, 20, True)
    start = time()
    pts = find_maximum(img, 10, True)
    print(time()-start)
    plt.imshow(img, cmap='gray')
    plt.plot(pts[:,1], pts[:,0], 'y.')
    plt.show()

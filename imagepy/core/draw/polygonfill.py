# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 17:40:41 2016
@author: yxl
"""
from __future__ import absolute_import
import numpy as np

def f(p1,p2,y):
    if abs(p1[1]-y) > abs(p2[1]-y):p1,p2 = p2,p1
    k =1.0* (p1[1]-y)/(y-p2[1])
    return round((p1[0]+k*p2[0])/(1+k),4)

def scan(polys, idx, ys, st, y, cur, buf):
    while cur<len(idx) and ys[st[cur]]<=y:
        c = idx[st[cur]]
        poly = polys[c[0]]
        for i in (c[0], (c[1]-1)%len(poly)), tuple(c):
            if i in buf:buf.remove(i)
            else: buf.append(i)
        cur += 1
    return cur

def roots(polys, buf, y):
    rs = []
    for i in buf:
        poly = polys[i[0]]
        i1,i2 = i, (i[0],(i[1]+1)%len(poly))
        rs.append(f(poly[i1[1]], poly[i2[1]],y))
    return np.sort(rs)

def fill(plgs, img, color = 1, o=(0,0)):
    polys = [np.array(plg[:-1])-0.5 for plg in plgs]
    shape = img.shape[:2]
    ys = []
    for i in range(len(polys)):
        for j in range(len(polys[i])):
            ys.append((i,j,polys[i][j][1]))
    ys = np.array(ys)
    st = np.argsort(ys[:,2])
    buf, rst, cur = [], [], 0
    bot,top = np.clip([int(ys[:,2].min()-1),int(ys[:,2].max()+2)], 0, shape[0])
    idx = ys[:,:2].astype(np.int16)
    for y in range(bot, top):
        cur = scan(polys, idx, ys[:,2], st, y, cur, buf)

        rs = roots(polys, buf, y)
        for i in zip(rs[::2],rs[1::2]):
            x1, x2 = int(np.ceil(i[0])), int(np.floor(i[1])+2)
            x1, x2 = max(x1,0), min(x2, shape[1])
            if x1 >= shape[1] or x2 < 0: continue
            #rst.extend([(x,y) for x in range(max(x1,o[0]), min(x2, shape[2]))])
            img[y,x1:x2] = color

    return np.array(rst).T

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from time import time
    # pg.shape = (1,4,2)
    pg = np.array([[(-300,-100),(1100,100),(400,1300),(100,100)]])
    # img.shape = (1000, 500)
    img = np.zeros((1000, 500))
    a = time()
    rc= fill(pg, img)
    print(time() - a)
    plt.imshow(img, interpolation='nearest',cmap='gray')
    plt.show()
    print("Done!")

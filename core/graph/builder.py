# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 22:05:43 2016

@author: yxl
"""
import numpy as np

loc = np.array([(1,0),(1,1),(0,1),(-1,1),
        (-1,0),(-1,-1),(0,-1),(1,-1),(1,0)])

def trace(img, p, p1):
    rst = [p, p1]
    while True:
        if img[rst[-1]]==2:break
        ep, bp = rst[-1], None
        img[ep] = 0
        for lo in loc[:-1]:
            cp = tuple(ep+lo)
            if img[cp]==0:continue
            if ep==p1:
                dp = (p1[0]-p[0], p1[1]-p[1])
                s = dp[0]*lo[0] + dp[1]*lo[1]
                if s<0:continue
            bp, v = cp, img[cp]
            if v>1:break
        if bp==None:return None
        rst.append(bp)
    return rst
    
def build_one(img, p):
    arcs, nodes, buf, num = [], {}, [p], 10
    while len(buf)!=0:
        p = buf.pop(0)
        if img[p]>=10:continue
        for lo in loc[:-1]:
            ii = tuple(lo+p)
            if img[ii]==0 or img[ii]>9:
                continue
            arc = trace(img, p, ii)
            if arc!=None:
                arcs.append(arc)
                buf.append(arc[-1])
        nodes[num-10] = p
        img[p], num = num, num+1
    for i in range(len(arcs)):
        se = img[arcs[i][0]], img[arcs[i][-1]]
        arcs[i] = (sorted((se[0]-10, se[1]-10)), arcs[i])
    return nodes, arcs

def build(img):
    pts = np.array(np.where(img==2)).T
    rst = []
    for p in pts:
        p = tuple(p)
        if img[p]==2:
            rst.append(build_one(img, p))
    return rst
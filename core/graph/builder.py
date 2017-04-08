# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 22:05:43 2016

@author: yxl
"""
import numpy as np
from scipy.ndimage.filters import convolve
'''
nodes = {id:obj...}
arcs = {id:(s,e,obj)}
graph = {'n1':[(a1, 2, lid),(a2, 5 ,lid)]}
'''

lut = np.array([1, 2, 2, 0, 2, 1, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 0, 1, 0,
       0, 1, 1, 0, 0, 1, 1, 0, 0, 2, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 1, 1,
       0, 0, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 2, 1, 1, 1, 1,
       2, 1, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2,
       0, 0, 2, 2, 0, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 0,
       0, 0, 2, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1,
       2, 1, 2, 2, 2, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1,
       2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1,
       1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 2, 2, 0,
       0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 0, 1, 1, 1, 1, 2,
       1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 2, 0,
       0, 2, 2], dtype=np.uint8)

loc = np.array([(1,0),(1,1),(0,1),(-1,1),
        (-1,0),(-1,-1),(0,-1),(1,-1),(1,0)])

def mark(img):
    lo = np.array([[-1,-1,-1,0,0,1,1,1],
        [-1,0,1,-1,1,-1,0,1]])
    core = np.array([[1,1,1],[1,0,1],[1,1,1]])
    msk = img>0
    convolve(msk, core, output=img)
    img *= msk
    np.clip(img, 0, 3, out=img)
    pts = np.array(np.where(img==3)).T

    for p in pts:
        idx = (lo.T+p).T
        v = img[idx[0], idx[1]]>0
        fac = np.array([1,2,4,8,16,32,64,128])
        c = lut[np.dot(v, fac)]
        if c==0: img[tuple(p)] = 0
    pts = np.array(np.where(img==3)).T
    for p in pts:
        if img[tuple(p)]==0:continue
        idx = (lo.T+p).T
        v = img[idx[0], idx[1]]>0
        fac = np.array([1,2,4,8,16,32,64,128])
        c = lut[np.dot(v, fac)]
        if c==1: img[tuple(p)] = 2
    img[:] = np.array([0,255,128,255], dtype=np.uint8)[img] 

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
    arcs, nodes, buf, num = [], [], [p], 0
    mark = {}
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
        nodes.append(p)
        mark[p] = num
        img[p], num = 10, num+1
        
    for i in range(len(arcs)):
        se = mark[arcs[i][0]], mark[arcs[i][-1]]
        line = np.array(arcs[i])
        s = np.linalg.norm(line[1:] - line[:-1], axis=1).sum()
        arcs[i] = (se[0], se[1], s, line)
    return nodes, arcs  

def build_graph(img):
    pts = np.array(np.where(img==2)).T
    rst = []
    for p in pts:
        p = tuple(p)
        if img[p]==2:
            rst.append(build_one(img, p))
    return rst
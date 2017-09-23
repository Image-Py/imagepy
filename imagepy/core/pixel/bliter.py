# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 22:58:58 2016
@author: yxl
"""
import numpy as np

def count_box(s1, s2, c, r):
    box1c = slice(max(0, c), min(s1[1], c+s2[1])) 
    box1r = slice(max(0, r), min(s1[0], r+s2[0]))
    box2c = slice(max(-c, 0), min(s2[1], s1[1]-c))
    box2r = slice(max(-r, 0), min(s2[0], s1[0]-r))
    return (box1r, box1c), (box2r, box2c)
  
def blit_copy(img1, img2):
    img1[:] = img2
    
def blit_max(img1, img2):
    msk = img2>img1
    img1[msk] = img2[msk]
    
def blit_min(img1, img2):
    msk = img2<img1
    img1[msk] = img2[msk]
    
def blit_diff(img1, img2):
    msk = img2>img1
    umsk = True ^ msk
    img1[msk] = img2[msk] - img1[msk]
    img1[umsk] = img1[umsk] - img2[umsk]
    
def blit_add(img1, img2):
    if img1.dtype == np.uint8:
        msk = img2 > 255-img1
        img1 += img2
        img1[msk] = 255
    else: img1 += img2
    
def blit_substract(img1, img2):
    if img1.dtype == np.uint8:
        msk = img1<img2
        img1 -= img2
        img1[msk] = 0
    else: img1 -= img2
        
funcs = {'max':blit_max, 'min':blit_min, 'diff':blit_diff, 
         'add':blit_add, 'substract':blit_substract, 'copy':blit_copy}

def blit(img1, img2, c=0, r=0, mode='copy'):
    shp1 = img1.shape
    shp2 = img2.shape
    bx1, bx2 = count_box(shp1, shp2, c, r)
    if img1.ndim==2 and img2.ndim==2:
        funcs[mode](img1[bx1], img2[bx2])
    if img1.ndim==3 and img2.ndim==3:
        print(bx1, bx2)
        funcs[mode](img1[bx1], img2[bx2])
    if img1.ndim==2 and img2.ndim==3:
        funcs[mode](img1[bx1], img2[bx2].mean(axis=2))
    if img1.ndim==3 and img2.ndim==2:
        for i in range(shp1[2]):
            funcs[mode](img1[:,:,i][bx1], img2[bx2])
        
        
        
    

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 01:57:23 2016
@author: yxl
"""

def affine(body, m, o):
    if isinstance(body, list):
        return [affine(i, m, o) for i in body]
    if isinstance(body, tuple):
        return tuple(m.dot(body)+o)
        

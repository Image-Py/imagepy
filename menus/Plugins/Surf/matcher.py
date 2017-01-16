# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 03:48:49 2017

@author: yxl
"""

import cv2
import numpy as np
from numpy.linalg import norm

class Matcher:
    def __init__(self, dim , std):
        self.dim, self.std = dim, std
        self.V = np.mat(np.zeros((self.dim,1)))
        self.Dk = np.mat(np.diag(np.ones(self.dim)*1e6))
        
    def match(self, desc1, desc2):
        matcher = cv2.BFMatcher(cv2.NORM_L2)
        pair = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 1)
        lt = [(i[0].distance, i[0].queryIdx, i[0].trainIdx) for i in pair]
        return np.array(sorted(lt))[:,1:].astype(np.int16)

    def getT(self, v1, v2):
        (x1, y1), (x2, y2) = v1, v2
        if self.dim==6:
            return np.mat([[v1[0],v1[1],1,0,0,0],
                       [0,0,0,v1[0],v1[1],1]])
        if self.dim==8:
            return np.mat([[x1, y1, 1, 0, 0, 0, -x1*x2, -y1*x2],
                           [0, 0, 0, x1, y1, 1, -x1*y2, -y1*y2]])

    def test(self, v1, v2):
        T = self.getT(v1.A1,v2.A1)
        goal = T * self.V
        o = goal.reshape((1,2))
        d = norm(v2 - o)
        dv = (v2 - o)/d
        D = T * self.Dk * T.T
        s = np.sqrt(dv * D * dv.T + self.std ** 2)
        return 3 * s > d

    def accept(self, v1, v2):
        L = v2
        Dl = np.mat(np.diag(np.ones(2)))*self.std**2
        T = self.getT(v1.A1,v2.A1)
        CX = (self.Dk.I + T.T * Dl.I * T).I
        CL = CX * T .T* Dl.I
        CV = np.mat(np.diag(np.ones(self.dim))) - CX * T.T * Dl.I * T
        self.V = CL * L + CV * self.V
        self.Dk = CV * self.Dk * CV.T + CL * Dl * CL.T
        
    def normalrize(self, pts):
        o = pts.mean(axis=0)
        l = norm(pts-o, axis=1).mean()
        pts[:] = (pts-o)/l
        
    def filter(self, kpt1, feat1, kpt2, feat2):
        kpt1 = np.array([(k.pt[0],k.pt[1]) for k in kpt1])
        kpt2 = np.array([(k.pt[0],k.pt[1]) for k in kpt2])
        self.normalrize(kpt1), self.normalrize(kpt2)
        idx = self.match(feat1, feat2)
        if self.dim == 0: 
            return idx, np.ones(len(idx), dtype=np.bool), 1
        mask = []
        for i1, i2 in idx:
            v1 = np.mat(kpt1[i1])
            v2 = np.mat(kpt2[i2])
            if self.test(v1, v2):
                self.accept(v1.T,v2.T)
                mask.append(True)
            else: mask.append(False)
        mask = np.array(mask)
        #print mask
        return idx, mask, self.V

    def getTrans(self):
        result = np.eye(3)
        result[:2] = self.V.reshape((2,3))
        return result

    def checkV(self):
        trans = self.getTrans()[:2,:2]
        axis = norm(trans,axis=0)
        return norm(axis-1)< 0.5
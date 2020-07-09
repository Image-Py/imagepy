import scipy.ndimage as ndimg
import numpy as np
from sciapp.action import Filter, Simple
import pandas as pd

def colorselect(img, pts, k, usecov=True):
    pts = img[pts].T
    mean = pts.mean(axis=-1)
    cov = np.cov(pts)
    dif = img-mean
    dis2 = (dif**2).sum(axis=2)
    if not usecov:
        return dis2<k*k
    dif2 = np.dot(dif, cov)*dif
    dif2 = dif2.sum(axis=2)
    return dis2/(dif2/dis2)<k*k

def grayselect(img, pts, k, usecov=True):
    pts = img[pts]
    mean = pts.mean()
    var = np.var(pts)
    dis2 = (img-mean)**2
    if not usecov:
        return dis2<k*k
    return dis2/var<k*k

def within(msk, pts):
    lab, n = ndimg.label(msk)
    hist = np.zeros(n+1, dtype=np.bool)
    hist[lab[pts]] = 1
    hist[0] = 0
    return hist[lab]

class ColorCluster(Filter):
    title = 'Color Cluster'
    note = ['rgb', 'auto_snap', 'not_channel', 'not_slice', 'req_roi', 'preview']
    
    para = {'sigma':3, 'cov':True, 'new':True, 'msk':'nothing', 'within':False, 'msk':'nothing'}
    view = [(float, 'sigma', (0,255), 1, 'torlerance', ''),
            (bool, 'cov', 'use cov instead of distance'),
            (bool, 'within', 'only points within'),
            (bool, 'new', 'result as new mask'),
            (list, 'msk', ['red', 'dark out', 'nothing'], str, 'mask', '')]
    
    def preview(self, ips, para):
        snap, img = ips.snap, ips.img
        pts = np.where(ips.mask())
        img[:] = snap
        msk = colorselect(img, pts, para['sigma'], para['cov'])
        if para['within']:msk = within(msk, pts)
        img[msk] = (255,0,0)

    def run(self, ips, snap, img, para = None):
        img[:] = snap
        pts = np.where(ips.mask())
        msk = colorselect(snap, pts, para['sigma'], para['cov'])
        if para['within']:msk = within(msk, pts)
        if para['msk'] == 'red':img[msk]=(255,0,0)
        if para['msk'] == 'dark out':img[~msk]//=3
        if para['new']:
            msk = np.multiply(msk,255,dtype=np.uint8)
            self.app.show_img([msk], ips.title+'-colormsk')

class ColorCluster3D(Simple):
    title = 'Color Cluster 3D'
    note = ['8-bit', '16-bit', 'int', 'float', 'req_roi', 'stack3d', 'preview']
    modal = False

    def run(self, ips, imgs, para = None):
        pass

class GrayCluster(Filter):
    title = 'Gray Cluster'
    note = ['8-bit', '16-bit', 'int', 'float', 'auto_snap', 'not_channel', 'not_slice', 'req_roi', 'preview']
    
    para = {'sigma':3, 'cov':True, 'new':True, 'within':False, 'msk':'nothing','msk':'nothing'}
    view = [(float, 'sigma', (0,255), 1, 'torlerance', ''),
            (bool, 'cov', 'use cov instead of distance'),
            (bool, 'within', 'only points within'),
            (bool, 'new', 'result as new mask'),
            (list, 'msk', ['clear out', 'nothing'], str, 'mask', '')]
    
    def load(self, ips):
        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True

    def preview(self, ips, para):
        snap, img = ips.snap, ips.img
        pts = np.where(ips.mask())
        pts = img[pts].T
        mean = pts.mean()
        std = np.std(pts)
        k = para['sigma']
        if para['cov']: k*=std
        v1, v2 = mean-k, mean+k
        lim1, lim2 = ips.range
        l1 = max(0, int((v1-lim1)*255/(lim2-lim1)))
        l2 = min(255, int((v2-lim1)*255/(lim2-lim1)))
        ips.lut[:] = self.buflut
        ips.lut[l1:l2] = (255,0,0)
        ips.update()

    def cancel(self, ips):
        ips.lut = self.buflut
        ips.update()

    def run(self, ips, snap, img, para = None):
        ips.lut = self.buflut
        pts = np.where(ips.mask())
        msk = grayselect(snap, pts, para['sigma'], para['cov'])
        if para['within']:msk = within(msk, pts)
        if para['msk'] == 'clear out':img[~msk]=ips.range[0]
        if para['new']:
            msk = np.multiply(msk,255,dtype=np.uint8)
            self.app.show_img([msk], ips.title+'-graymsk')

class GrayCluster3D(Simple):
    title = 'Gray Cluster 3D'
    note = ['8-bit', '16-bit', 'int', 'float', 'req_roi', 'stack3d', 'preview']
    modal = False
    para = {'sigma':3, 'cov':True, 'new':True, 'within':False, 'msk':'nothing','msk':'nothing'}
    view = [(float, 'sigma', (0,255), 1, 'torlerance', ''),
            (bool, 'cov', 'use cov instead of distance'),
            (bool, 'within', 'only points within'),
            (bool, 'new', 'result as new mask'),
            (list, 'msk', ['clear out', 'nothing'], str, 'mask', '')]
    
    def load(self, ips):
        if ips.roi is None or ips.roi.roitype != 'point':
            self.app.alert('need a point roi')
            return False
        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True

    def preview(self, ips, para):
        idx = np.array(ips.roi.body).astype(np.uint16).T
        pts = ips.imgs[idx[2], idx[1], idx[0]]
        mean = pts.mean()
        std = np.std(pts)
        k = para['sigma']
        if para['cov']: k*=std
        v1, v2 = mean-k, mean+k
        lim1, lim2 = ips.range
        l1 = max(0, int((v1-lim1)*255/(lim2-lim1)))
        l2 = min(255, int((v2-lim1)*255/(lim2-lim1)))
        ips.lut[:] = self.buflut
        ips.lut[l1:l2] = (255,0,0)
        ips.update()

    def cancel(self, ips):
        ips.lut = self.buflut
        ips.update()

    def run(self, ips, imgs, para = None):
        ips.lut = self.buflut
        idx = np.array(ips.roi.body).astype(np.uint16).T
        pts = (idx[2], idx[1], idx[0])
        msk = grayselect(imgs, pts, para['sigma'], para['cov'])
        if para['within']:msk = within(msk, pts)
        if para['msk'] == 'clear out':imgs[~msk]=ips.range[0]
        if para['new']:
            msk = np.multiply(msk,255,dtype=np.uint8)
            IPy.show_img(msk, ips.title+'-graymsk')

plgs = [GrayCluster, ColorCluster, '-', GrayCluster3D, ColorCluster3D]
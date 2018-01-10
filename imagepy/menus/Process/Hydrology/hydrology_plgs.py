import scipy.ndimage as ndimg
import numpy as np
from numba import jit
from imagepy.core.engine import Filter
from imagepy.ipyalg import find_maximum, ridge, stair, isoline, watershed
from imagepy.core.roi import PointRoi
#from skimage.morphology import watershed, disk
from skimage.filters import rank
from skimage.filters import sobel
from imagepy import IPy

class IsoLine(Filter):
    title = 'Find IsoLine'
    note = ['8-bit', 'not_slice', 'auto_snap', 'not_channel', 'preview']
    
    para = {'low':0, 'high':255, 'step':20, 'type':'stair'}
    view = [(int, (0,255), 0, 'low', 'low', 'value'),
            (int, (0,255), 0, 'high', 'high', 'value'),
            (int, (0, 50), 0, 'step', 'step', ''),
            (list, ['stair', 'white line', 'gray line', 'white line on ori'], str, 'output', 'type', '')]

    #process
    def run(self, ips, snap, img, para = None):
        img[:] = snap
        stair(img, para['low'], para['high'], para['step'])
        if para['type']=='stair':
            stair(img, para['low'], para['high'], para['step'])
        else: mark = isoline(img, para['low'], para['high'], para['step'])
        if para['type'] == 'stair':return
        elif para['type'] == 'white line':
            img[:] = mark
        elif para['type'] == 'gray line':
            np.minimum(snap, mark, out=img)
        if para['type'] == 'white line on ori':
            np.maximum(snap, mark, out=img)

class FindMax(Filter):
    title = 'Find Maximum'
    note = ['8-bit', 'not_slice', 'auto_snap', 'not_channel', 'preview']
    
    para = {'tol':2, 'mode':False, 'wsd':False}
    view = [(int, (0,100), 0,  'tolerance', 'tol', 'value')]

    def run(self, ips, snap, img, para = None):
        pts = find_maximum(self.ips.img, para['tol'])
        self.ips.roi = PointRoi([tuple(i) for i in pts[:,::-1]])
        self.ips.update = True

class FindMin(Filter):
    title = 'Find Minimum'
    note = ['8-bit', 'not_slice', 'auto_snap', 'not_channel', 'preview']
    
    para = {'tol':2, 'mode':False, 'wsd':False}
    view = [(int, (0,100), 0,  'tolerance', 'tol', 'value')]

    def run(self, ips, snap, img, para = None):
        pts = find_maximum(self.ips.img, para['tol'], False)
        self.ips.roi = PointRoi([tuple(i) for i in pts[:,::-1]])
        self.ips.update = True

class UPRidge(Filter):
    title = 'Find Riedge'
    note = ['8-bit', 'not_slice', 'auto_snap', 'not_channel', 'preview']
    
    para = {'sigma':1.0, 'thr':0, 'ud':True, 'type':'white line'}
    view = [(float, (0,5), 1, 'sigma', 'sigma', 'pix'),
            ('slide', (0,255), 'Low', 'thr', ''),
            (bool, 'ascend', 'ud'),
            (list, ['white line', 'gray line', 'white line on ori'], str, 'output', 'type', '')]

    def load(self, ips):
        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True
    
    def preview(self, ips, para):
        ips.lut[:] = self.buflut
        if para['ud']:
            ips.lut[:para['thr']] = [0,255,0]
        else:
            ips.lut[para['thr']:] = [255,0,0]
        ips.update = 'pix'

    #process
    def run(self, ips, snap, img, para = None):
        self.ips.lut[:] = self.buflut
        ndimg.gaussian_filter(snap, para['sigma'], output=img)
        mark = img<para['thr'] if para['ud'] else img>para['thr']
        mark = mark.astype(np.uint8)

        ridge(img, mark, para['ud'])
        if para['type'] == 'white line':
            img[:] = mark
        if para['type'] == 'gray line':
            np.minimum(snap, mark, out=img)
        if para['type'] == 'white line on ori':
            #img //=2
            np.maximum(snap, mark, out=img)

class ARidge(Filter):
    title = 'Active Ridge'
    note = ['8-bit', 'not_slice', 'auto_snap', 'not_channel']
    
    para = {'sigma':1.0, 'ud':True, 'type':'white line'}
    view = [(float, (0,5), 1, 'sigma', 'sigma', 'pix'),
    (list, ['white line', 'gray line', 'white line on ori'], str, 'output', 'type', ''),
            (bool, 'ascend', 'ud')]
    
    def run(self, ips, snap, img, para = None):
        mark = np.zeros_like(img, dtype=np.uint8)
        ips.roi.sketch(mark, color=1)
        ridge(img, mark, para['ud'])
        if para['type'] == 'white line':
            img[:] = mark
        if para['type'] == 'gray line':
            np.minimum(snap, mark, out=img)
        if para['type'] == 'white line on ori':
            #img //=2
            np.maximum(snap, mark, out=img)

class Watershed(Filter):
    title = 'Find Watershed'
    note = ['8-bit', 'auto_snap', 'not_channel', 'preview']
    
    para = {'sigma':1.0, 'thr':0, 'con':False, 'ud':True, 'type':'white line'}
    view = [(float, (0,5), 1, 'sigma', 'sigma', 'pix'),
            ('slide', (0,255), 'Low', 'thr', ''),
            (bool, 'full connectivity', 'con'),
            (bool, 'ascend', 'ud'),
            (list, ['white line', 'gray line', 'white line on ori'], str, 'output', 'type', '')]

    def load(self, ips):
        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True
    
    def preview(self, ips, para):
        ips.lut[:] = self.buflut
        if para['ud']:
            ips.lut[:para['thr']] = [0,255,0]
        else:
            ips.lut[para['thr']:] = [255,0,0]
        ips.update = 'pix'

    #process
    def run(self, ips, snap, img, para = None):
        self.ips.lut[:] = self.buflut
        ndimg.gaussian_filter(snap, para['sigma'], output=img)
        mark = img<para['thr'] if para['ud'] else img>para['thr']

        markers, n = ndimg.label(mark, np.ones((3,3)), output=np.uint16)
        if not para['ud']:img[:] = 255-img
        mark = watershed(img, markers, line=True, conn=para['con']+1)
        mark = np.multiply((mark==0), 255, dtype=np.uint8)
        if para['type'] == 'white line':
            img[:] = mark
        if para['type'] == 'gray line':
            np.minimum(snap, mark, out=img)
        if para['type'] == 'white line on ori':
            #img //=2
            np.maximum(snap, mark, out=img)

class UPWatershed(Filter):
    title = 'Up And Down Watershed'
    note = ['8-bit', 'auto_msk', 'auto_snap', 'preview']
    
    para = {'thr1':0, 'thr2':255, 'type':'line'}
    view = [('slide', (0,255), 'Low', 'thr1', ''),
            ('slide', (0,255), 'High', 'thr2', ''),
            (list, ['line', 'up area', 'down area'], str, 'output', 'type', '')]

    def load(self, ips):
        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True
    
    def preview(self, ips, para):
        ips.lut[:] = self.buflut
        ips.lut[:para['thr1']] = [0,255,0]
        ips.lut[para['thr2']:] = [255,0,0]
        ips.update = 'pix'

    def cancel(self, ips):
        ips.lut = self.buflut
        ips.update = 'pix'

    #process
    def run(self, ips, snap, img, para = None):
        edge = sobel(snap)
        img[:] = 0
        img[snap>para['thr2']] = 2
        img[snap<para['thr1']] = 1
        ips.lut = self.buflut
        mark = watershed(edge, img, line=True)
        img[:] = ips.range[0]
        if para['type'] == 'line': 
            img[mark==0] = ips.range[1]
        elif para['type'] == 'up area':
            img[mark!=1] = ips.range[1]
        elif para['type'] == 'down area':
            img[mark!=2] = ips.range[1]

class ROIWatershed(Filter):
    title = 'Watershed With ROI'
    note = ['8-bit', 'auto_snap', 'not_channel']
    
    para = {'sigma':0, 'type':'white line', 'con':False, 'ud':True}
    view = [#(int, (0,10), 0,  'sigma', 'sigma', 'pix'),
            #(int, (0, 10), 0,  'gradient', 'gdt', ''),
            (bool, 'full connectivity', 'con'),
            (bool, 'ascend', 'ud'),
            (list, ['white line', 'gray line', 'white line on ori'], str, 'output', 'type', '')]
    
    def run(self, ips, snap, img, para = None):
        #denoised = rank.median(img, disk(para['sigma']))
        #gradient = rank.gradient(denoised, disk(para['gdt']))
        ndimg.gaussian_filter(snap, para['sigma'], output=img)

        markers, n = ndimg.label(ips.get_msk(), np.ones((3,3)), output=np.uint32)
        if not para['ud']:img[:] = 255-img
        mark = watershed(img, markers, line=True, conn=para['con']+1)
        mark = np.multiply((mark==0), 255, dtype=np.uint8)

        if para['type'] == 'white line':
            img[:] = mark
        if para['type'] == 'gray line':
            np.minimum(snap, mark, out=img)
        if para['type'] == 'white line on ori':
            np.maximum(snap, mark, out=img)

plgs = [FindMax, FindMin, IsoLine, '-', UPRidge, ARidge, '-', Watershed, UPWatershed, ROIWatershed]
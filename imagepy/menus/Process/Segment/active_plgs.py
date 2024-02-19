import numpy as np
from scipy.ndimage import binary_dilation
from sciapp.action import Filter
from skimage import img_as_float
from skimage.segmentation import chan_vese, morphological_chan_vese, \
    morphological_geodesic_active_contour, inverse_gaussian_gradient, \
    clear_border, random_walker

class ChanVese(Filter):
    title = 'Evolving Level Set'
    note = ['all', 'not_slice', 'auto_snap', 'preview']
    
    para = {'mu':0.25, 'lambda1':1.0, 'lambda2':1.0, 'tol':0.001, 'max_iter':500, 
        'dt':0.5, 'init_level_set':'checkerboard', 'extended_output':False, 'out':'mask'}

    view = [(float, 'mu', (0,1), 2, 'mu', ''),
            (float, 'lambda1', (0,10), 2, 'lambda1', ''),
            (float, 'lambda2', (0,10), 2, 'lambda2', ''),
            (float, 'tol', (0,1), 3, 'tol', ''),
            (int, 'max_iter', (0,512), 0, 'max_iter', 'times'),
            (float, 'dt', (0,10), 2, 'dt', ''),
            (list, 'init_level_set', ['checkerboard', 'disk', 'small disk'], str, 'init', ''),
            (list, 'out', ['mask', 'line on ori'], str, 'output', '')]

    def run(self, ips, snap, img, para = None):
        msk = chan_vese(snap, mu=para['mu'], lambda1=para['lambda1'], lambda2=para['lambda2'], 
            tol=para['tol'], max_iter=para['max_iter'], dt=para['dt'], init_level_set=para['init_level_set'])
        (c1, c2), img[:] = ips.range, snap
        if para['out'] == 'mask': img[~msk], img[msk] = c1, c2
        else: img[binary_dilation(msk) ^ msk] = c2

class MorphChanVese(Filter):
    title = 'Morphological Snake Fit'
    note = ['all', 'not_slice', 'auto_snap', 'preview']
    
    para = {'iter':10, 'init':'checkerboard', 'smooth':1, 'lambda1':1.0, 
        'lambda2':1.0, 'out':'mask', 'sub':False}

    view = [(int, 'iter', (0,64), 0, 'iterations', 'time'),
            (list, 'init', ['checkerboard', 'circle'], str, 'init set', ''),
            (int, 'smooth', (1, 10), 0, 'smoothing', ''),
            (float, 'lambda1', (0,10), 2, 'lambda1', ''),
            (float, 'lambda2', (0,10), 2, 'lambda2', ''),
            (list, 'out', ['mask', 'line on ori'], str, 'output', ''),
            (bool, 'sub', 'show sub stack')]

    def preview(self, ips, para):
        snap, img = ips.snap, ips.img
        msk = morphological_chan_vese(snap, para['iter'], init_level_set=para['init'], 
            smoothing=para['smooth'], lambda1=para['lambda1'], lambda2=para['lambda2']) > 0
        (c1, c2), img[:] = ips.range, snap
        if para['out'] == 'mask': img[~msk], img[msk] = c1, c2
        else: img[binary_dilation(msk) ^ msk] = c2
        ips.update()

    def run(self, ips, snap, img, para = None):
        stackimg = []
        callback = lambda x: stackimg.append((x*255).astype(np.uint8)) if para['sub'] else 0
        msk = morphological_chan_vese(snap, para['iter'], init_level_set=para['init'], 
            smoothing=para['smooth'], lambda1=para['lambda1'], lambda2=para['lambda2'],
            iter_callback=callback) > 0
        (c1, c2), img[:] = ips.range, snap
        if para['out'] == 'mask': img[~msk], img[msk] = c1, c2
        else: img[binary_dilation(msk) ^ msk] = c2
        if para['sub']: self.app.show_img(stackimg, ips.title+'-sub')

class MorphGeoChanVese(Filter):
    title = 'Bound Snake Fit'
    note = ['all', 'not_slice', 'auto_snap', 'preview']
    
    para = {'iter':10, 'smooth':1, 'thr':128, 'auto':True, 'balloon':-1, 'out':'mask', 'sub':False}

    view = [(int, 'iter', (0, 1024), 0, 'iterations', 'time'),
            (int, 'smooth', (1, 10), 0, 'smoothing', ''),
            (float, 'thr', (0,1e5), 2, 'threshold', ''),
            (bool, 'auto', 'auto threshold'),
            (float, 'balloon', (-5, 5), 1, 'balloon', ''),
            (list, 'out', ['mask', 'line on ori'], str, 'output', ''),
            (bool, 'sub', 'show sub stack')]

    def preview(self, ips, para):
        snap, img = ips.snap, ips.img
        gimage = inverse_gaussian_gradient(img_as_float(snap))
        init = np.ones(img.shape, dtype='bool')
        msk = morphological_geodesic_active_contour(gimage, para['iter'], 
            init_level_set=init, smoothing=para['smooth'], 
            threshold='auto' if para['auto'] else para['thr'], balloon=para['balloon']) > 0
        (c1, c2), img[:] = ips.range, snap
        if para['out'] == 'mask': img[~msk], img[msk] = c1, c2
        else: img[binary_dilation(msk) ^ msk] = c2
        ips.update()

    def run(self, ips, snap, img, para = None):
        stackimg = []
        callback = lambda x: stackimg.append((x*255).astype(np.uint8)) if para['sub'] else 0
        gimage = inverse_gaussian_gradient(img_as_float(snap))
        init = np.ones(img.shape, dtype='bool')
        msk = morphological_geodesic_active_contour(gimage, para['iter'], 
            init_level_set=init, smoothing=para['smooth'], 
            threshold='auto' if para['auto'] else para['thr'], 
            balloon=para['balloon'], iter_callback=callback) > 0
        (c1, c2), img[:] = ips.range, snap
        if para['out'] == 'mask': img[~msk], img[msk] = c1, c2
        else: img[binary_dilation(msk) ^ msk] = c2
        if para['sub']: self.app.show_img(stackimg, ips.title+'-sub')

class MorphGeoRoi(Filter):
    title = 'ROI Snake Fit'
    note = ['all', 'not_slice', 'auto_snap', 'req_roi', 'preview']
    
    para = {'iter':10, 'smooth':1, 'thr':128, 'auto':True, 'balloon':-1, 'out':'mask', 'sub':False}

    view = [(int, 'iter', (0, 1024), 0, 'iterations', 'time'),
            (int, 'smooth', (1, 10), 0, 'smoothing', ''),
            (float, 'thr', (0,1e5), 2, 'threshold', ''),
            (bool, 'auto', 'auto threshold'),
            (float, 'balloon', (-5, 5), 1, 'balloon', ''),
            (list, 'out', ['mask', 'line on ori'], str, 'output', ''),
            (bool, 'sub', 'show sub stack')]

    def preview(self, ips, para):
        snap, img = ips.snap, ips.img
        gimage = inverse_gaussian_gradient(img_as_float(snap))
        init = ips.mask('out')
        msk = morphological_geodesic_active_contour(gimage, para['iter'], 
            init_level_set=init, smoothing=para['smooth'], 
            threshold='auto' if para['auto'] else para['thr'], balloon=para['balloon']) > 0
        (c1, c2), img[:] = ips.range, snap
        if para['out'] == 'mask': img[~msk], img[msk] = c1, c2
        else: img[binary_dilation(msk) ^ msk] = c2
        ips.update()

    def run(self, ips, snap, img, para = None):
        stackimg = []
        callback = lambda x: stackimg.append((x*255).astype(np.uint8)) if para['sub'] else 0
        gimage = inverse_gaussian_gradient(img_as_float(snap))
        init = ips.mask('out')
        msk = morphological_geodesic_active_contour(gimage, para['iter'], 
            init_level_set=init, smoothing=para['smooth'], 
            threshold='auto' if para['auto'] else para['thr'], 
            balloon=para['balloon'], iter_callback=callback) > 0
        (c1, c2), img[:] = ips.range, snap
        if para['out'] == 'mask': img[~msk], img[msk] = c1, c2
        else: img[binary_dilation(msk) ^ msk] = c2
        if para['sub']: self.app.show_img(stackimg, ips.title+'-sub')

class RandomWalker(Filter):
    title = 'Random Walker'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    modal = False

    def load(self, ips):
        minv, maxv = ips.range
        self.para = {'beta':130, 'mode':'bf', 'tol':0.001, 'thr1':minv, 'thr2':maxv, 'out':'mask'}
        self.view = [('slide', 'thr1', (minv, maxv), 4, 'Low'),
                     ('slide', 'thr2', (minv,maxv), 4, 'High'),
                     (int, 'beta', (10,256), 0, 'beta', ''),
                     (list, 'mode', ['cg_mg', 'cg', 'bf'], str, 'mode', ''),
                     (float, 'tol', (0,1), 3, 'tolerance', ''),
                     (list, 'out', ['mask', 'line on ori'], str, 'output', '')]

        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True

    def cancel(self, ips):
        ips.lut = self.buflut
        ips.update()

    def preview(self, ips, para):
        ips.lut[:] = self.buflut
        minv, maxv = ips.range
        lim1 = (para['thr1']-minv)*255/(maxv-minv)
        lim2 = (para['thr2']-minv)*255/(maxv-minv)
        ips.lut[:int(lim1)] = [0,255,0]
        ips.lut[int(lim2):] = [255,0,0]
        ips.update()

    #process
    def run(self, ips, snap, img, para = None):
        msk = np.zeros_like(img)
        msk[img>para['thr2']] = 1
        msk[img<para['thr1']] = 2
        msk = random_walker(snap, msk, beta=para['beta'], mode=para['mode'], tol=para['tol'])==1
        ips.lut = self.buflut
        if para['out'] == 'mask': img[~msk], img[msk] = ips.range
        else: img[binary_dilation(msk) ^ msk] = ips.range[1]

plgs = [ChanVese, MorphChanVese, '-', MorphGeoChanVese, MorphGeoRoi, '-', RandomWalker]
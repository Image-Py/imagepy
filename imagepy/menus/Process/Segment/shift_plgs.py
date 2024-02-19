from sciapp.action import Filter, Simple
from skimage import data, io, segmentation, color

class SLIC(Filter):
    title = 'SLIC Superpixel'
    note = ['all', 'not_slice', 'auto_snap', 'auto_msk', 'not_channel', 'preview']
    
    para = {'n_segments':100, 'compactness':10.0, 'max_iter':10, 'sigma':0}
    view = [(int, 'n_segments', (1, 1e8), 0, 'segments', 'n'),
            (float, 'compactness', (0.01, 100), 2, 'campactness', 'color-space'),
            (int, 'max_iter', (3, 50), 0, 'max_iter', 'n'),
            (float, 'sigma', (0, 30), 1, 'sigma', 'smooth')]

    def run(self, ips, snap, img, para = None):
        lab = segmentation.slic(snap, para['n_segments'], 
            para['compactness'], para['max_iter'], para['sigma'])
        return color.label2rgb(lab, snap, kind='avg')

class Quickshift(Filter):
    title = 'Quick Shift'
    note = ['all', 'not_slice', 'auto_snap', 'auto_msk', 'not_channel', 'preview']
    
    para = {'ratio':1.0, 'kernel_size':5, 'max_dist':10, 'sigma':0}
    view = [(float, 'ratio', (0, 1), 2, 'ratio', 'color-space'),
            (float, 'kernel_size', (0, 30), 2, 'kernel_size', ''),
            (float, 'max_dist', (1, 1024), 2, 'distance', 'cut off'),
            (float, 'sigma', (0, 30), 1, 'sigma', 'smooth')]

    def run(self, ips, snap, img, para = None):
        lab = segmentation.quickshift(snap, para['ratio'], para['kernel_size'],
            para['max_dist'], para['sigma'])
        return color.label2rgb(lab, snap, kind='avg')

class Felzenszwalb(Filter):
    title = 'Felzenszwalb'
    note = ['all', 'not_slice', 'auto_snap', 'auto_msk', 'not_channel', 'preview']
    
    para = {'scale':1.0, 'sigma':0.8, 'min_size':20}
    view = [(float, 'scale', (0.01, 1024), 2, 'scale', ''),
            (float, 'sigma', (0, 30), 2, 'sigma', ''),
            (int, 'min_size', (1, 1024), 0, 'min_size', '')]

    def run(self, ips, snap, img, para = None):
        lab = segmentation.felzenszwalb(snap, para['scale'], para['sigma'], para['min_size'])
        return color.label2rgb(lab, snap, kind='avg')

class SLICLab(Simple):
    title = 'SLIC Superpixel Label'
    note = ['all', 'preview']
    
    para = {'n_segments':100, 'compactness':10.0, 'max_iter':10, 'sigma':0, 'stack':False}
    view = [(int, 'n_segments', (1, 1e8), 0, 'segments', 'n'),
            (float, 'compactness', (0.01, 1024), 2, 'campactness', 'color-space'),
            (int, 'max_iter', (3, 50), 0, 'max_iter', 'n'),
            (float, 'sigma', (0, 30), 1, 'sigma', 'smooth'),
            (bool, 'stack', 'stack')]

    def load(self, ips): return ips.snapshot()==None
    def cancel(self, ips): ips.swap()

    def preview(self, ips, para): 
        lab = segmentation.slic(ips.snap, para['n_segments'], 
            para['compactness'], para['max_iter'], para['sigma'])
        ips.img[:] = color.label2rgb(lab, ips.snap, kind='avg')

    def run(self, ips, imgs, para = None):
        if not para['stack']: imgs = [ips.img]
        ips.swap()
        rst = []
        for i in range(len(imgs)):
            rst.append(segmentation.slic(imgs[i], para['n_segments'], 
                para['compactness'], para['max_iter'], para['sigma']).astype('int32'))
            rst[-1] += 1
            self.progress(i, len(imgs))
        self.app.show_img(rst, ips.title+'-sliclab')

class QuickshiftLab(Simple):
    title = 'Quickshift Label'
    note = ['all', 'preview']
    
    para = {'ratio':1.0, 'kernel_size':5, 'max_dist':10, 'sigma':0, 'stack':False}
    view = [(float, 'ratio', (0, 1), 2, 'ratio', 'color-space'),
            (float, 'kernel_size', (0, 30), 2, 'kernel_size', ''),
            (float, 'max_dist', (1, 1024), 2, 'distance', 'cut off'),
            (float, 'sigma', (0, 30), 1, 'sigma', 'smooth'),
            (bool, 'stack', 'stack')]

    def load(self, ips): return ips.snapshot()==None
    def cancel(self, ips): ips.swap()

    def preview(self, ips, para): 
        lab = segmentation.quickshift(ips.snap, para['ratio'], para['kernel_size'],
            para['max_dist'], para['sigma'])
        ips.img[:] = color.label2rgb(lab, ips.snap, kind='avg')

    def run(self, ips, imgs, para = None):
        if not para['stack']: imgs = [ips.img]
        ips.swap()
        rst = []
        for i in range(len(imgs)):
            rst.append(segmentation.quickshift(imgs[i], para['ratio'], para['kernel_size'],
                para['max_dist'], para['sigma']).astype('int32'))
            rst[-1] += 1
            self.progress(i, len(imgs))
        self.app.show_img(rst, ips.title+'-quickshiftlab')

class FelzenszwalbLab(Simple):
    title = 'Felzenszwalb Label'
    note = ['all', 'preview']
    
    para = {'scale':1.0, 'sigma':0.8, 'min_size':20, 'stack':False}
    view = [(float, 'scale', (0.01, 10), 2, 'scale', ''),
            (float, 'sigma', (0, 30), 2, 'sigma', ''),
            (int, 'min_size', (1, 1024), 0, 'min_size', ''),
            (bool, 'stack', 'stack')]

    def load(self, ips): return ips.snapshot()==None
    def cancel(self, ips): ips.swap()

    def preview(self, ips, para): 
        lab = segmentation.felzenszwalb(ips.snap, para['scale'], para['sigma'], para['min_size'])
        ips.img[:] = color.label2rgb(lab, ips.snap, kind='avg')

    def run(self, ips, imgs, para = None):
        if not para['stack']: imgs = [ips.img]
        ips.swap()
        rst = []
        for i in range(len(imgs)):
            rst.append(segmentation.felzenszwalb(imgs[i], para['scale'], 
                para['sigma'], para['min_size']).astype('int32'))
            rst[-1] += 1
            self.progress(i, len(imgs))
        self.app.show_img(rst, ips.title+'-felzenszwalblab')
        
plgs = [SLIC, Quickshift, Felzenszwalb, '-', SLICLab, QuickshiftLab, FelzenszwalbLab]
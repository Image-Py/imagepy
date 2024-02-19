import numpy as np
from sciapp.action import Filter
from imagepy.ipyalg.transform import transform
from numpy.fft import fft2, ifft2, fftshift, ifftshift

class Plugin(Filter):
    title = 'Depress Cyclic Wave'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    para = {'gap':0.01, 'lim':0.01}
    view = [(float, 'lim', (0.001, 0.1), 3, 'limit', 'width'),
            (float, 'gap', (0.001, 0.1), 3, 'gap', 'width')]

    def run(self, ips, snap, img, para = None):
        lim, gap = para['lim'], para['gap']
        poimg = transform.linear_polar(snap)
        h, w = poimg.shape[:2]
        lim = max(1, int(w*lim))
        gap = max(1, int(gap*h))
        fftpoimg = fftshift(fft2(poimg))
        fftpoimg[:h//2-gap,w//2-lim:w//2+lim] = 0
        fftpoimg[h//2+gap:,w//2-lim:w//2+lim] = 0
        poimg = ifft2(ifftshift(fftpoimg))
        poimg = np.clip(poimg.real, snap.min(), snap.max())
        poimg = poimg.astype(snap.dtype)
        transform.polar_linear(poimg, output=img[:,:,None])
from ..advanced import Filter
from scipy.ndimage import gaussian_filter

class Gaussian(Filter):
    title = 'Gaussian'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    para = {'sigma':2}
    view = [(float, 'sigma', (0,30), 1,  'sigma', 'pix')]
    
    def run(self, ips, snap, img, para = None):
        gaussian_filter(snap, para['sigma'], output=img)
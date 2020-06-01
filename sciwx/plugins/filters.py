from sciapp.action import ImgAction
from scipy.ndimage import gaussian_filter

class Gaussian(ImgAction):
    name = 'Gaussian'
    note = ['auto_snap', 'preview']
    para = {'sigma':2}
    view = [(float, 'sigma', (0, 30), 1, 'sigma', 'pix')]

    def run(self, ips, img, snap, para):
        gaussian_filter(snap, para['sigma'], output=img)

class Undo(ImgAction):
    name = 'Undo'
    def run(self, ips, img, snap, para): ips.swap()
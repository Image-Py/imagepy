import numpy as np
from sciapp.action import Filter
#from imagepy.ui.widgets import CurvePanel
from scipy import interpolate

#widgets['curve'] = CurvePanel

class Plugin(Filter):
    title = 'Curve Adjust'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'curve': [(0,0), (255, 255)]}

    def load(self, ips):
        hist = ips.histogram(chans='all', step=512)
        self.view = [('curve', 'curve', hist)]
        return True

    #process
    def run(self, ips, snap, img, para = None):
        x, y = np.array(para['curve']).T
        kind = 'linear' if len(para['curve'])==2 else 'quadratic'
        f = interpolate.interp1d(x, y, kind=kind)
        if img.dtype == np.uint8:
            img[:] = np.clip(f(np.arange(256)),0,255).astype(np.uint8)[snap]
        else:
            np.clip(snap, ips.range[0], ips.range[1], out=img)
            img[:] -= ips.range[0]
            np.multiply(img, 255.0/(ips.range[1]-ips.range[0]), out=img, casting='unsafe')
            np.clip(f(img), 0, 255, out=img)
            np.multiply(img, (ips.range[1]-ips.range[0])/255.0, out=img, casting='unsafe')
            img[:] += ips.range[0]
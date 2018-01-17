from imagepy import IPy
import numpy as np
from imagepy.core.engine import Filter
from imagepy.ui.panelconfig import ParaDialog
from imagepy.ui.widgets import CurvePanel
from scipy import interpolate

class ThresholdDialog(ParaDialog):
    def init_view(self, items, para, hist):
        self.curvep = CurvePanel(self)
        self.curvep.set_hist(hist)
        self.add_ctrl('curve', self.curvep)
        ParaDialog.init_view(self, items, para, True)

class Plugin(Filter):
    title = 'Curve Adjust'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'curve': [(0,0), (255, 255)]}
    view = []

    def show(self):
        self.dialog = ThresholdDialog(IPy.get_window(), self.title)
        hist = np.histogram(self.ips.lookup(),list(range(257)))[0]
        self.dialog.init_view(self.view, self.para, hist)
        self.dialog.set_handle(lambda x:self.preview(self.ips, self.para))
        return self.dialog.ShowModal()

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
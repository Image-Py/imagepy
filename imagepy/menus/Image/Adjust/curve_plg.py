from imagepy import IPy
import numpy as np
from imagepy.core.engine import Filter
from imagepy.ui.panelconfig import ParaDialog
from imagepy.ui.widgets import CurvePanel

class ThresholdDialog(ParaDialog):
    def init_view(self, items, para, hist):
        self.curvep = CurvePanel(self)
        self.curvep.set_hist(hist)
        self.add_ctrl(self.curvep, 'curve')
        ParaDialog.init_view(self, items, para, True)
    
        
class Plugin(Filter):
    title = 'Curve Adjust'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    para = {'curve': 1}
    view = []

    def show(self):
        self.dialog = ThresholdDialog(IPy.get_window(), self.title)
        hist = np.histogram(self.ips.lookup(),list(range(257)))[0]
        self.dialog.init_view(self.view, self.para, hist)
        self.dialog.set_handle(lambda x:self.preview(self.para))
        return self.dialog.ShowModal()

    #process
    def run(self, ips, snap, img, para = None):
        print('hhh')
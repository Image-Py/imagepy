import sys, wx
sys.path.append('../../')
from scipy.ndimage import gaussian_filter
from sciwx.app.canvasapp import CanvasApp
from sciapp.action import ImgAction

class Gaussian(ImgAction):
    title = 'Gaussian'
    note = ['auto_snap', 'preview']
    para = {'sigma':2}
    view = [(float, 'sigma', (0, 30), 1, 'sigma', 'pix')]

    def run(self, ips, img, snap, para):
        gaussian_filter(snap, para['sigma'], output=img)

class Undo(ImgAction):
    title = 'Undo'
    def run(self, ips, img, snap, para):
        print(ips.img.mean(), ips.snap.mean())
        ips.swap()

if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread

    app = wx.App()
    ca = CanvasApp(None, autofit=False)
    ca.set_img(camera())
    bar = ca.add_menubar()
    bar.load(('menu',[('Filter',[('Gaussian', Gaussian),
                                 ('Unto', Undo)]),
                      ]))
    ca.Show()
    app.MainLoop()

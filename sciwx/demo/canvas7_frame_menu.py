import sys, wx
sys.path.append('../../')
from scipy.ndimage import gaussian_filter
from sciwx.canvas import CanvasFrame
from sciwx.event import ImgEvent

class Gaussian(ImgEvent):
    title = 'Gaussian'
    note = ['auto_snap', 'preview']
    para = {'sigma':2}
    view = [(float, 'sigma', (0, 30), 1, 'sigma', 'pix')]

    def run(self, ips, img, snap, para):
        gaussian_filter(snap, para['sigma'], output=img)

class Undo(ImgEvent):
    title = 'Undo'
    def run(self, ips, img, snap, para):
        print(ips.img.mean(), ips.snap.mean())
        ips.swap()

if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread

    app = wx.App()
    cf = CanvasFrame(None, autofit=False)
    cf.set_imgs([camera(), 255-camera()])
    cf.set_cn(0)
    bar = cf.add_menubar()
    bar.load(('menu',[('Filter',[('Gaussian', Gaussian),
                                 ('Unto', Undo)]),
                      ]))
    cf.Show()
    app.MainLoop()

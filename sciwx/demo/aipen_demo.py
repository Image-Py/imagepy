import sys, wx
sys.path.append('../../')
from skimage.draw import line
from sciwx.canvas import CanvasFrame
from sciapp.action import Tool, DefaultTool

from skimage.morphology import flood_fill, flood
from skimage.draw import line, circle
from skimage.segmentation import felzenszwalb
import numpy as np

class AIPen(Tool):
    title = 'AI Pen'
    para = {'win':48, 'ms':30}
    view = [(int, 'win', (28, 64), 0, 'window', 'size'),
            (float, 'ms', (10, 50), 0, 'stickiness', 'pix')]
    
    def __init__(self): self.status = None
        
    def mouse_down(self, ips, x, y, btn, **key):
        self.status = 'down'
        self.oldp = (y, x)
        ips.snapshot()
    
    def mouse_up(self, ips, x, y, btn, **key): self.status = None

    def mouse_move(self, ips, x, y, btn, **key):
        if self.status == None: return
        img, color = ips.img, (255,255,0)
        rs, cs = line(*[int(round(i)) for i in self.oldp + (y, x)])
        np.clip(rs, 0, img.shape[0]-1, out=rs)
        np.clip(cs, 0, img.shape[1]-1, out=cs)
        color = (np.mean(color), color)[img.ndim==3]
        w = self.para['win']

        for r,c in zip(rs, cs):
            sr = (max(0,r-w), min(img.shape[0], r+w))
            sc = (max(0,c-w), min(img.shape[1], c+w))
            r, c = min(r, w), min(c, w)
            clip = img[slice(*sr), slice(*sc)]
            if (clip[r,c] - color).sum()==0: continue
            lab = felzenszwalb(clip, 1, 0, self.para['ms'])
            clip[flood(lab, (r, c), connectivity=2)] = color

        self.oldp = (y, x)
        ips.update()

if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread

    app = wx.App()
    cf = CanvasFrame(None, autofit=False)
    cf.set_imgs([astronaut(), 255-astronaut()])
    cf.set_cn((0,1,2))
    bar = cf.add_toolbar()
    bar.add_tool(DefaultTool, 'M')
    bar.add_tool(AIPen, 'A')
    cf.Show()
    app.MainLoop()

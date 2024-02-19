import sys, wx
sys.path.append('../../')
from skimage.draw import line
from sciwx.app.canvasapp import CanvasApp
from sciapp.action import Tool, ImageTool

class Pencil(ImageTool):
    title = 'Pencil'
    para = {'pc':(255,0,0)}
    view = [('color', 'pc','pen', 'color')]
        
    def __init__(self):
        self.status = False
        self.oldp = (0,0)
        
    def mouse_down(self, ips, x, y, btn, **key):
        self.status = True
        self.oldp = (y, x)
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.status = False
    
    def mouse_move(self, ips, x, y, btn, **key):
        if not self.status:return
        se = self.oldp + (y,x)
        rs,cs = line(*[int(i) for i in se])
        rs.clip(0, ips.shape[1], out=rs)
        cs.clip(0, ips.shape[0], out=cs)
        ips.img[rs,cs] = self.para['pc']
        self.oldp = (y, x)
        key['canvas'].update()
        
    def mouse_wheel(self, ips, x, y, d, **key):pass

if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread

    app = wx.App()
    cf = CanvasApp(None, autofit=False)
    cf.set_img(astronaut())
    bar = cf.add_toolbar()
    bar.add_tool('M', ImageTool)
    bar.add_tool('P', Pencil)
    cf.Show()
    app.MainLoop()

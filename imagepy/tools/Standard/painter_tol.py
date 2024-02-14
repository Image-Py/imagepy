from sciapp.action import ImageTool
from skimage.draw import line, disk

def drawline(img, oldp, newp, w, value):
    if img.ndim == 2 and hasattr(value, '__iter__'): value = sum(value)/3
    oy, ox = line(*[int(round(i)) for i in oldp+newp])
    cy, cx = disk((0, 0), w/2+1e-6)
    ys = (oy.reshape((-1,1))+cy).clip(0, img.shape[0]-1)
    xs = (ox.reshape((-1,1))+cx).clip(0, img.shape[1]-1)
    img[ys.ravel(), xs.ravel()] = value

class Plugin(ImageTool):
    title = 'Pencil'
    
    para = {'width':1}
    view = [(int, 'width', (0,30), 0,  'width', 'pix')]
    
    def __init__(self):
        self.status = False
        self.oldp = (0,0)
        
    def mouse_down(self, ips, x, y, btn, **key):
        self.status = True
        self.oldp = (y, x)
        ips.snapshot()
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.status = False
    
    def mouse_move(self, ips, x, y, btn, **key):
        if not self.status:return
        w = self.para['width']
        value = self.app.manager('color').get('front')
        drawline(ips.img, self.oldp, (y, x), w, value)
        self.oldp = (y, x)
        ips.update()
        
    def mouse_wheel(self, ips, x, y, d, **key):pass
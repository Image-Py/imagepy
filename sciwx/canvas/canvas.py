import wx, numpy as np
from sciapp.util.imgutil import mix_img, cross, multiply, merge, lay, mat, like
from .mark import drawmark
from sciapp.object import Image, Shape, mark2shp, Layer, json2shp
from sciapp.action import ImageTool, ShapeTool
from time import time

class Canvas (wx.Panel):
    scales = [0.03125, 0.0625, 0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 8, 10, 15, 20, 30, 50]
    
    def __init__(self, parent, autofit=False, ingrade=False, up=False):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY,
            pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL )

        self.winbox = None
        self.conbox = [0,0,1,1]
        self.oribox = [0,0,1,1]
        
        self.outbak = None
        self.outimg = None
        self.outrgb = None
        self.outbmp = None
        self.outint = None
        self.buffer = None

        self.first = True

        self.images = []
        self.marks = {}
        self.tool = None
        
        self.scaidx = 6
        self.autofit = autofit
        self.ingrade = ingrade
        self.up = up
        self.scrbox = wx.DisplaySize()
        self.bindEvents()

    def get_obj_tol(self): return self, Tool.default
    
    def bindEvents(self):
        for event, handler in [ \
                (wx.EVT_SIZE, self.on_size),
                (wx.EVT_MOUSE_EVENTS, self.on_mouse),
                (wx.EVT_IDLE, self.on_idle),
                (wx.EVT_PAINT, self.on_paint)]:
            self.Bind(event, handler)

    def on_mouse(self, me):
        px, py = me.GetX(), me.GetY()
        x, y = self.to_data_coor(px, py)
        obj, tol = self.get_obj_tol()
        btn, tool = me.GetButton(), self.tool or tol
        ld, rd, md = me.LeftIsDown(), me.RightIsDown(), me.MiddleIsDown()
        sta = [me.AltDown(), me.ControlDown(), me.ShiftDown()]
        others = {'alt':sta[0], 'ctrl':sta[1],
            'shift':sta[2], 'px':px, 'py':py, 'canvas':self}
        if me.Moving() and not (ld or md or rd): 
            for i in (ImageTool, ShapeTool):
                if isinstance(tool, i): i.mouse_move(tool, obj, x, y, btn, **others)
        if me.ButtonDown():
            self.SetFocus()
            tool.mouse_down(obj, x, y, btn, **others)
        if me.ButtonUp():
            tool.mouse_up(obj, x, y, btn, **others)
        if me.Moving():
            tool.mouse_move(obj, x, y, None, **others)
        btn = [ld, md, rd,True]
        btn  = (btn.index(True) +1) %4
        wheel = np.sign(me.GetWheelRotation())
        if me.Dragging():
            tool.mouse_move(obj, x, y, btn, **others)
        if wheel!=0:
            tool.mouse_wheel(obj, x, y, wheel, **others)
        ckey = {'arrow':1,'cross':5,'hand':6}
        cursor = ckey[tool.cursor] if tool.cursor in ckey else 1
        self.SetCursor(wx.Cursor(cursor))
            
    def initBuffer(self):
        box = self.GetClientSize()
        self.buffer = wx.Bitmap(*box)
        self.winbox = [0, 0, *box]
        lay(self.winbox, self.conbox)

    def fit(self):
        self.update_box()
        oriw = self.oribox[2]-self.oribox[0]
        orih = self.oribox[3]-self.oribox[1]
        if not self.autofit: a,b,c,d = self.winbox
        else: 
            (a,b),(c,d) = (0,0), self.scrbox
            c, d = c*0.9, d*0.9
        if not self.ingrade:
            for i in self.scales[6::-1]:
                if oriw*i<c-a and orih*i<d-b: break
            self.scaidx = self.scales.index(i)
        else: i = min((c-a)*0.9/oriw, (d-b)*0.9/orih)
        self.zoom(i, 0, 0)
        lay(self.winbox, self.conbox)
        self.update()

    def update_box(self):
        box = [1e10, 1e10, -1e10, -1e10]
        for i in self.images: box = merge(box, i.box)
        shapes = [i for i in self.marks.values() if isinstance(i, Shape)]
        shapes = [i for i in shapes if not i.box is None]
        for i in shapes: box = merge(box, i.box)
        if box[2]<=box[0]: box[0], box[2] = box[0]-1e-3, box[2]+1e-3
        if box[1]<=box[3]: box[1], box[3] = box[1]-1e-3, box[3]+1e-3
        if self.winbox and self.oribox == box: return
        self.conbox = self.oribox = box

    def draw_image(self, dc, img, back, mode):
        out, bak, rgb = self.outimg, self.outbak, self.outrgb
        ori, cont = self.oribox, self.conbox
        cellbox = like(ori, cont, img.box)
        csbox = cross(self.winbox, cellbox)
        
        if min(csbox[2]-csbox[0], csbox[3]-csbox[1])<5: return
        shp = csbox[3]-csbox[1], csbox[2]-csbox[0]
        o, m = mat(self.oribox, self.conbox, cellbox, csbox)
        shp = tuple(np.array(shp).round().astype(np.int))
        if out is None or (out.shape, out.dtype) != (shp, img.dtype):
            self.outimg = np.zeros(shp, dtype=img.dtype)
        if not back is None and not back.img is None and (
            bak is None or (bak.shape, bak.dtype) != (shp, back.dtype)):
            self.outbak = np.zeros(shp, dtype=back.dtype)
        if rgb is None or rgb.shape[:2] != shp:
            self.outrgb = np.zeros(shp+(3,), dtype=np.uint8)
            self.outint = np.zeros(shp, dtype=np.uint8)
            buf = memoryview(self.outrgb)
            self.outbmp = wx.Bitmap.FromBuffer(*shp[::-1], buf)
        if not back is None:
            mix_img(back.imgs[img.cur], m, o, shp, self.outbak, 
                self.outrgb, self.outint, back.rg, back.lut,
                back.log, cns=back.cn, mode='set')
        mix_img(img.img, m, o, shp, self.outimg,
            self.outrgb, self.outint, img.rg, img.lut,
            img.log, cns=img.cn, mode=img.mode)
        
        self.outbmp.CopyFromBuffer(memoryview(self.outrgb))
        dc.DrawBitmap(self.outbmp, *csbox[:2])
        
    def update(self, counter = [0,0]):
        #self.update_box()
        if None in [self.winbox, self.conbox]: return
        if self.first:
            self.first = False
            return self.fit()
        counter[0] += 1
        start = time()
        # lay(self.winbox, self.conbox)
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        #dc.SetBackground(wx.Brush((255,255,255)))
        dc.Clear()
        for i in self.images: self.draw_image(dc, i, i.back, 0)
        
        for i in self.marks.values():
            if i is None: continue
            if callable(i):
                i(dc, self.to_panel_coor, k=self.scale, cur=0,
                    winbox=self.winbox, oribox=self.oribox, conbox=self.conbox)
            else:
                drawmark(dc, self.to_panel_coor, i, k=self.scale, cur=0,
                    winbox=self.winbox, oribox=self.oribox, conbox=self.conbox)
        dc.UnMask()

        counter[1] += time()-start
        if counter[0] == 50:
            print('frame rate:',int(50/max(0.001,counter[1])))
            counter[0] = counter[1] = 0

    def set_tool(self, tool): self.tool = tool

    @property
    def scale(self):
        conw = self.conbox[2]-self.conbox[0]
        oriw = self.oribox[2]-self.oribox[0]
        conh = self.conbox[3]-self.conbox[1]
        orih = self.oribox[3]-self.oribox[1]
        l1, l2 = conw**2+conh**2, oriw**2+orih**2
        return l1**0.5 / l2**0.5

    def move(self, dx, dy, coord='win'):
        if coord=='data':
            dx,dy = dx*self.scale, dy*self.scale
        arr = np.array(self.conbox)
        arr = arr.reshape((2,2))+(dx, dy)
        self.conbox = arr.ravel().tolist()
        self.update()

    def on_size(self, event):
        if max(self.GetClientSize())>20 and self.images[0].img is not None:
            self.initBuffer()
        if len(self.images)+len(self.marks)==0: return
        if self.conbox[2] - self.conbox[0] > 1: self.update()

    def on_idle(self, event):
        need = sum([i.dirty for i in self.images])
        shapes = [i for i in self.marks.values() if isinstance(i, Shape)]
        need += sum([i.dirty for i in shapes])
        if need==0: return
        else:
            for i in self.images: i.dirty = False
            for i in shapes: i.dirty = False
            return self.update()

    def on_paint(self, event):
        if self.buffer is None: return
        wx.BufferedPaintDC(self, self.buffer)
        
    def center(self, x, y, coord='win'):
        if coord=='data':
            x,y = self.to_panel_coor(x, y)
        dx = (self.winbox[2]-self.winbox[0])/2 - x
        dy = (self.winbox[3]-self.winbox[1])/2 - y
        for i,j in zip((0,1,2,3),(dx,dy,dx,dy)):
            self.conbox[i] += j
        lay(self.winbox, self.conbox)
        
    def zoom(self, k, x, y, coord='win'):
        if coord=='data':
            x,y = self.to_panel_coor(x, y)
            if self.up: y = (self.winbox[3]-self.winbox[1]) - y
        box = np.array(self.conbox).reshape((2,2))
        box = (box - (x,y)) / self.scale * k + (x, y)
        self.conbox = box.ravel().tolist()
        if not self.autofit: return
        a,b,c,d = self.conbox
        if c-a<self.scrbox[0]*0.9 and d-b<self.scrbox[1]*0.9:
            self.SetInitialSize((c-a+4, d-b+4))
        lay(self.winbox, self.conbox)
        self.GetParent().Fit()
        
    def zoomout(self, x, y, coord='win', grade=True):
        if not self.ingrade:
            self.scaidx = min(self.scaidx + 1, len(self.scales)-1)
            i = self.scales[self.scaidx]
        else: i = self.scale * 1.5
        self.zoom(i, x, y, coord)
        self.update()

    def zoomin(self, x, y, coord='win'):
        if not self.ingrade:
            self.scaidx = max(self.scaidx - 1, 0)
            i = self.scales[self.scaidx]
        else: i = self.scale / 1.5
        self.zoom(i, x, y, coord)
        self.update()

    def to_data_coor(self, x, y):
        if self.up: y = (self.winbox[3]-self.winbox[1]) - y
        x, y = x / self.scale, y / self.scale
        x += -self.conbox[0]/self.scale+self.oribox[0]
        y += -self.conbox[1]/self.scale+self.oribox[1]
        return x-0.5, y-0.5

    def to_panel_coor(self, x, y):
        x, y = (x+0.5) * self.scale, (y+0.5) * self.scale
        x += -self.oribox[0] * self.scale + self.conbox[0]
        y += -self.oribox[1] * self.scale + self.conbox[1]
        if self.up: y = (self.winbox[3]-self.winbox[1]) - y
        return x, y

    def save_buffer(self, path):
        dcSource = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        # based largely on code posted to wxpython-users by Andrea Gavana 2006-11-08
        size = dcSource.Size

        # Create a Bitmap that will later on hold the screenshot image
        # Note that the Bitmap must have a size big enough to hold the screenshot
        # -1 means using the current default colour depth
        bmp = wx.Bitmap(size.width, size.height)

        # Create a memory DC that will be used for actually taking the screenshot
        memDC = wx.MemoryDC()

        # Tell the memory DC to use our Bitmap
        # all drawing action on the memory DC will go to the Bitmap now
        memDC.SelectObject(bmp)

        # Blit (in this case copy) the actual screen on the memory DC
        # and thus the Bitmap
        memDC.Blit( 0, # Copy to this X coordinate
            0, # Copy to this Y coordinate
            size.width, # Copy this width
            size.height, # Copy this height
            dcSource, # From where do we copy?
            0, # What's the X offset in the original DC?
            0  # What's the Y offset in the original DC?
            )

        # Select the Bitmap out of the memory DC by selecting a new
        # uninitialized Bitmap
        memDC.SelectObject(wx.NullBitmap)

        img = bmp.ConvertToImage()
        img.SaveFile(path, wx.BITMAP_TYPE_PNG)

    def __del__(self):
        # self.img = self.back = None
        print('========== canvas del')

if __name__=='__main__':
    from skimage.data import astronaut, camera
    import matplotlib.pyplot as plt

    app = wx.App()
    frame = wx.Frame(None, title='Canvas')
    canvas = Canvas(frame, autofit=False, ingrade=True, up=True)
    
    line = mark2shp({'type':'polygon', 'color':(255,0,0), 'lstyle':'o', 'fill':True,
                     'body':[[(0,0),(1000,1000),(2000,0), (0,0)],
                             [(0,0),(100,100),(200,0),(0,0)],
                             [(100,400),(300,100),(300,600),(100,400)]]})
    layer = Layer()
    layer.color = (0,0,0)
    layer.lw = 1

    import json
    import geonumpy.io as gio
    shp = gio.read_shp('C:/Users/54631/Documents/projects/huangqu/demo/shape/province.shp')
    feats = json.loads(shp.to_json())['features']
    for i in feats:
        shp = json2shp(i['geometry'])
        layer.body.append(shp)
    canvas.marks.append(layer)
    
    '''
    image = Image()
    image.img = camera()
    image.pos = (0,0)
    canvas.images.append(image)
    '''
    '''
    image = Image()
    image.img = astronaut()
    image.pos = (100,200)
    image.cn = (0,1,2)
    canvas.images.append(image)
    '''
    
    frame.Show(True)
    app.MainLoop()

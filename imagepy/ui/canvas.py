"""
Created on Wed Oct 12 14:15:01 2016

@author: yxl
"""
import wx, sys
import numpy as np
from math import ceil
from ..core.manager import ToolsManager
from scipy.ndimage import affine_transform
from imagepy import IPy
from time import time
from numba import jit

#import sys
#get_npbuffer = np.getbuffer if sys.version[0]=="2" else memoryview
if sys.version_info[0]==2:memoryview=np.getbuffer

def cross(r1, r2):
    x,y = max(r1[0], r2[0]),max(r1[1], r2[1])
    w = min(r1[0]+r1[2], r2[0]+r2[2])-x
    h = min(r1[1]+r1[3], r2[1]+r2[3])-y
    return [x, y, w, h]

def multiply(r, kx, ky):
    r = [r[0]*kx, r[1]*ky, r[2]*kx, r[3]*ky]
    return [ceil(i) for i in r]

def lay(r1, r2):
    if r2[2]<=r1[2]:r2[0]=(r1[2]-r2[2])//2+r1[0]
    elif r2[0]>r1[0]:r2[0]=r1[0]
    elif r2[0]+r2[2]<r1[0]+r1[2]:
        r2[0]=r1[0]+r1[2]-r2[2]

    if r2[3]<=r1[3]:r2[1]=(r1[3]-r2[3])//2+r1[1]
    elif r2[1]>r1[1]:r2[1]=r1[1]
    elif r2[1]+r2[3]<r1[1]+r1[3]:
        r2[1]=r1[1]+r1[3]-r2[3]

def trans(r1, r2):
    return [r2[0]-r1[0], r2[1]-r1[1], r2[2], r2[3]]

@jit
def my_transform(img, m, offset=(0,0), output=None, k=0.5, clip=False):
    kr=m[0]; kc=m[1]; ofr=offset[0]; ofc=offset[1];
    for r in range(output.shape[0]):
        for c in range(output.shape[1]):
            rr = int(r*kr+ofr)
            cc = int(c*kc+ofc)
            if output[r,c]==0 or not clip:
                output[r,c] = output[r,c]*(1-k)+img[rr,cc]*k

class Canvas (wx.Panel):
    scales = [0.03125, 0.0625, 0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 8, 10]
    def __init__(self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(300,300), style = wx.TAB_TRAVERSAL )
        self.initBuffer()
        self.bindEvents()
        self.scaleidx = 4
        self.oldscale = 1
        self.o = (0, 0)
        self.reInitBuffer = True
        self.resized = True
        self.ips = None
        self.scrsize = wx.DisplaySize()
        self.s = 0
        self.handle = None
        self.imgbox = [0,0,0,0]
        self.imgsize = (0,0)

    def set_handler(self, handle=None):
        self.handle = handle

    def on_mouseevent(self, me):
        tool = self.ips.tool
        if tool == None : tool = ToolsManager.curtool
        x,y = self.to_data_coor(me.GetX(), me.GetY())
        if me.Moving() and not me.LeftIsDown() and not me.RightIsDown() and not me.MiddleIsDown():
            xx,yy = int(round(x)), int(round(y))
            k, unit = self.ips.unit
            if xx>=0 and xx<self.ips.img.shape[1] and yy>=0 and yy<self.ips.img.shape[0]:
                IPy.set_info('Location:%.1f %.1f  Value:%s'%(x*k, y*k, self.ips.img[yy,xx]))
        if tool==None:return
        
        sta = [me.AltDown(), me.ControlDown(), me.ShiftDown()]
        if me.ButtonDown():tool.mouse_down(self.ips, x, y, me.GetButton(), alt=sta[0], ctrl=sta[1], shift=sta[2], canvas=self)
        if me.ButtonUp():tool.mouse_up(self.ips, x, y, me.GetButton(), alt=sta[0], ctrl=sta[1], shift=sta[2], canvas=self)
        if me.Moving():tool.mouse_move(self.ips, x, y, None, alt=sta[0], ctrl=sta[1], shift=sta[2], canvas=self)
        btn = [me.LeftIsDown(), me.MiddleIsDown(), me.RightIsDown(),True].index(True)
        if me.Dragging():tool.mouse_move(self.ips, x, y, 0 if btn==3 else btn+1, alt=sta[0], ctrl=sta[1], shift=sta[2], canvas=self)
        wheel = np.sign(me.GetWheelRotation())
        if wheel!=0:tool.mouse_wheel(self.ips, x, y, wheel, alt=sta[0], ctrl=sta[1], shift=sta[2], canvas=self)
        if hasattr(tool, 'cursor'):
            self.SetCursor(wx.Cursor(tool.cursor))
        else : self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

    def bindEvents(self):
        for event, handler in [ \
                (wx.EVT_SIZE, self.on_size),
                (wx.EVT_MOUSE_EVENTS, self.on_mouseevent),      # Draw
                (wx.EVT_IDLE, self.on_idle),
                (wx.EVT_PAINT, self.on_paint)]: # Start drawing]:
            self.Bind(event, handler)

    def initBuffer(self):
        box = self.GetClientSize()
        #print(self.GetChientSize())
        self.buffer = wx.Bitmap(box.width, box.height)
        self.box = [0,0,box[0],box[1]]

    def self_fit(self):
        #print('self_fit')
        for i in self.scales[6::-1]:
            if self.ips.size[1]*i<=self.scrsize[0]*0.9 and\
            self.ips.size[0]*i<=self.scrsize[1]*0.9:
                break
        self.scaleidx = self.scales.index(i)
        self.zoom(self.scales[self.scaleidx], 0, 0)

    def set_ips(self, ips):
        samesize = tuple(ips.img.shape[:2]) == self.imgsize
        if ips==self.ips and samesize:return
        self.imgsize = tuple(ips.img.shape[:2])
        self.ips = ips
        self.imgbox = [0,0,ips.size[1],ips.size[0]]
        self.self_fit()

    def zoom(self, k, x, y):
        # print 'scale', k
        k1 = self.oldscale * 1.0
        self.oldscale = k2 = k
        self.imgbox[0] = int(self.imgbox[0] + (k1-k2)*x+0.5)
        self.imgbox[1] = int(self.imgbox[1] + (k1-k2)*y+0.5)
        self.imgbox[2] = int(self.ips.size[1] * k2+0.5)
        self.imgbox[3] = int(self.ips.size[0] * k2+0.5)
        lay(self.box, self.imgbox)
        if self.imgbox[2]<=self.scrsize[0]*0.9 and\
        self.imgbox[3]<=self.scrsize[1]*0.9 and not IPy.aui:
            self.SetInitialSize((self.imgbox[2], self.imgbox[3]))
            if not self.handle is None: self.handle(self.ips, True)

    def move(self, dx, dy):
        if self.imgbox[2]<=self.box[2] and self.imgbox[3]<=self.box[3]:return
        self.imgbox[0] += int(dx+0.5)
        self.imgbox[1] += int(dy+0.5)
        self.update(True)

    def center(self, x, y):
        k = self.scales[self.scaleidx]
        self.imgbox[0] = self.box[2]/2 - x*k
        self.imgbox[1] = self.box[3]/2 - y*k
        lay(self.box, self.imgbox)

    def on_size(self, event):
        self.reInitBuffer = True

    def on_idle(self, event):
        if not self.IsShown() or self.ips==None:return
        if self.reInitBuffer:
            self.initBuffer()
            #print 'resized update'
            self.update(True)
            self.reInitBuffer = False
            self.ips.update = False
            print('resize')
        if self.ips.scrchanged:
            self.set_ips(self.ips)
            self.ips.scrchanged = False
            print('scr changed')
        if self.ips.update != False:
            #print 'normal update'
            self.update(self.ips.update == 'pix')
            self.ips.update = False
            print('update')

    def on_paint(self, event):
        wx.BufferedPaintDC(self, self.buffer)
        '''
        cdc = wx.ClientDC(self)
        #cdc.BeginDrawing()
        if self.ips.roi != None:
            self.ips.roi.draw(cdc, self.to_panel_coor)
        if self.ips.mark != None:
            self.ips.mark.draw(cdc, self.to_panel_coor, cur=self.ips.cur, k = self.get_scale())
        if self.ips.unit!=(1,'pix'):
            self.draw_ruler(cdc)
        #cdc.EndDrawing()
        '''
    def merge(self, img, back, M, O, mode, shape, win, lookup):
        if img.ndim == 2:
            rstarr = np.zeros(shape, dtype=img.dtype)
            my_transform(img, M, offset=O, output=rstarr, k=1, clip=False)
            rstarr = lookup(rstarr)
        
        if img.ndim == 3:
            rstarr = np.zeros((win[3], win[2], 3), dtype=img.dtype)
            for i in range(3):
                my_transform(img[:,:,i], M, offset=O, 
                    output=rstarr[:,:,i], k=1, clip=False)
        
        if not back is None:
            for i in range(3):
                my_transform(back[:,:,i] if back.ndim==3 else back, M, offset=O, 
                    output=rstarr[:,:,i], k=mode[0], clip = mode[1]=='Clip')
        
        return rstarr

    def draw_image(self, dc, ndarr, back, mode, rect, scale, dirty):
        #print(rect, self.box)
        win = cross(self.box, rect)
        win2 = trans(rect, win)
        sx = sy = 1.0/scale
        box = multiply(win2, sx, sy)

        M = np.array([sx, sy])
        O = (win2[1]*sx, win2[0]*sy)
        shape = (win2[3], win2[2])

        if dirty:
            start = time()
            rst = self.merge(ndarr, back, M, O, mode, shape, win2, self.ips.lookup)
            self.bmp = wx.Bitmap.FromBuffer(win2[2], win2[3], memoryview(rst))
            print(time()-start)
        dc.DrawBitmap(self.bmp, win[0], win[1])
        
    def save_buffer(self, path):
        self.buffer.SaveFile(path, wx.BITMAP_TYPE_PNG)

    def draw_ruler(self, dc):
        dc.SetPen(wx.Pen((255,255,255), width=2, style=wx.SOLID))
        x1 = max(self.imgbox[0], self.box[0])+5
        x2 = min(self.imgbox[2], self.box[2])+x1-10
        pixs = (x2-x1+10)*self.ips.size[1]/10.0/self.imgbox[2]
        h = min(self.imgbox[1]+self.imgbox[3],self.box[3])-5
        dc.DrawLineList([(x1,h,x2,h)])
        dc.DrawLineList([(i,h,i,h-8) for i in np.linspace(x1, x2, 3)])
        dc.DrawLineList([(i,h,i,h-5) for i in np.linspace(x1, x2, 11)])

        dc.SetTextForeground((255,255,255))
        k, unit = self.ips.unit
        text = 'Unit = %.1f %s'%(k*pixs, unit)
        dw,dh = dc.GetTextExtent(text)
        dc.DrawText(text, (x2-dw, h-10-dh))

    def update(self, pix):
        if self.ips == None: return
        lay(self.box, self.imgbox)
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        #dc.BeginDrawing()
        dc.Clear()
        self.draw_image(dc, self.ips.img, self.ips.backimg, self.ips.backmode, 
            self.imgbox, self.scales[self.scaleidx], pix)

        #dc.EndDrawing()
        
        #cdc = wx.ClientDC(self)
        #cdc.BeginDrawing()
        if self.ips.roi != None:
            self.ips.roi.draw(dc, self.to_panel_coor)
        if self.ips.mark != None:
            self.ips.mark.draw(dc, self.to_panel_coor, cur=self.ips.cur, k = self.get_scale())
        #cdc.EndDrawing()
        if self.ips.unit!=(1,'pix'):
            self.draw_ruler(dc)
        if self.handle != None: self.handle(self.ips)
        dc.UnMask()

    def zoomout(self, x, y):
        if self.scaleidx == len(self.scales)-1:return
        #x,y = self.to_data_coor(x, y)
        self.scaleidx += 1
        self.zoom(self.scales[self.scaleidx],x,y)
        self.ips.update = 'pix'

    def zoomin(self, x, y):
        if self.scaleidx == 0:return
        #x,y = self.to_data_coor(x, y)
        self.scaleidx -= 1
        self.zoom(self.scales[self.scaleidx], x,y)
        self.ips.update = 'pix'

    def get_scale(self):
        return self.scales[self.scaleidx]

    def to_data_coor(self, x, y):
        x = (x - self.box[0] - self.imgbox[0])
        y = (y - self.box[1] - self.imgbox[1])
        return (x/self.get_scale(), y/self.get_scale())

    def to_panel_coor(self, x, y):
        x = x * self.get_scale() + self.imgbox[0] + self.box[0]
        y = y * self.get_scale() + self.imgbox[1] + self.box[1]
        return x,y

    def on_update(self):
        pass

    def __del__(self):
        print('========== canvas')

if __name__=='__main__':
    import sys
    sys.path.append('../')
    import numpy as np
    from imageplus import ImagePlus
    from scipy.misc import imread
    img = imread('../imgs/flower.jpg')
    app = wx.PySimpleApp()
    frame = wx.Frame(None)
    canvas = Canvas(frame)
    ips = ImagePlus(img)
    canvas.set_ips(ips)
    canvas.fit = frame
    canvas.set_handler(TestTool())
    frame.Fit()
    frame.Show(True)
    app.MainLoop()


    #r1 = [0,0,20,10]
    #r2 = [1,2,10,10]

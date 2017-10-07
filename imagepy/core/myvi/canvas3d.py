import sys
import ModernGL
import numpy as np
import wx, math
import wx.glcanvas as glcanvas
from .manager import *
from .util import build_surf2d, build_surf3d, build_ball, build_balls

#----------------------------------------------------------------------
from wx.glcanvas import WX_GL_DEPTH_SIZE 
attribs=[WX_GL_DEPTH_SIZE,32,0,0]; 

class Canvas3D(glcanvas.GLCanvas):
    def __init__(self, parent):
        attribList = attribs = (glcanvas.WX_GL_RGBA, glcanvas.WX_GL_DOUBLEBUFFER, glcanvas.WX_GL_DEPTH_SIZE, 24)
        glcanvas.GLCanvas.__init__(self, parent, -1, attribList=attribList)
        self.init = False
        self.context = glcanvas.GLContext(self)
        self.manager = None
        self.size = None

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.lastx, self.lasty = None, None
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.update = True

    def InitGL(self):
        manager = self.manager = Manager()
        
        #img = imread('C:/Users/Administrator/Desktop/dem.png')
        #print(img.shape, img.dtype)
        #vts, fs, ns, cs = build_surf2d(img)
        #manager.add_obj('dem', vts, fs, ns, cs)
        '''
        fs = glob('C:/Users/Administrator/Desktop/ipygl/imgs/*.png')
        imgs = np.array([imread(i, True) for i in fs])
        imgs = nimg.gaussian_filter(imgs, 1)
        vts, fs, ns, vs = build_surf3d(imgs, 128, step=1)
        ns = (ns+1)/2
        manager.add_obj('xg', vts, fs, ns, (1,0,0))
        '''
        '''
        vts, fs, ns, cs = build_ball((100,100,100), 50, (0,1,0))
        manager.add_surface(vts, fs, ns, cs)
        vts, fs, ns, cs = build_ball((200,200,200), 30, (1,1,0))
        manager.add_surface(vts, fs, ns, cs)
        '''
        #vts, fs, ns, cs = build_balls([(200,200,200),(100,100,100)], [30, 50],[(1,1,0),(0,0,1)])
        #manager.add_obj('balls', vts, fs, ns, cs)
        
        #manager.get_obj('balls').set_style(blend=0.4)
        #self.manager.count_box()
        self.manager.reset(60, 0, 0)
        
    def OnDraw(self):
        self.manager.set_viewport(0, 0, self.Size.width, self.Size.height)
        #self.manager.count_mvp()
        self.manager.draw()
        self.SwapBuffers()

    def on_idle(self, event):
        if self.update:
            self.Refresh(False)
            self.update = False

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        if not self.manager is None:
            self.manager.set_viewport(0, 0, self.Size.width, self.Size.height)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.lastx, self.lasty = evt.GetPosition()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        self.SetFocus()
        if evt.Dragging() and evt.LeftIsDown():
            x, y = evt.GetPosition()
            dx, dy = x-self.lastx, y-self.lasty
            self.lastx, self.lasty = x, y
            #self.manager.h -= dx/200
            angx = self.manager.angx - dx/200
            angy = self.manager.angy + dy/200
            #print('ang', angx, angy)
            self.manager.set_pers(angx=angx, angy=angy)
            self.Refresh(False)

    def save_bitmap(self, path):
        context = wx.ClientDC( self )
        memory = wx.MemoryDC( )
        x, y = self.ClientSize
        bitmap = wx.Bitmap( x, y, -1 )
        memory.SelectObject( bitmap )
        memory.Blit( 0, 0, x, y, context, 0, 0)
        memory.SelectObject( wx.NullBitmap)
        bitmap.SaveFile( path, wx.BITMAP_TYPE_PNG )

    def OnMouseWheel(self, evt):
        k = 0.9 if evt.GetWheelRotation()>0 else 1/0.9
        self.manager.set_pers(l=self.manager.l*k)
        self.Refresh(False)
        #self.update = True

    def view_x(self): 
        self.manager.reset(angx=0)
        self.Refresh(False)

    def view_y(self): 
        self.manager.reset(angx=pi/2)
        self.Refresh(False)

    def view_z(self): 
        self.manager.reset(angy=pi/2-1e-4)
        self.Refresh(False)

    def view_pers(self, b):
        self.manager.set_pers(pers=b)
        self.Refresh(False)

    def set_background(self, rgb):
        self.manager.set_background(rgb)
        
#----------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App(False)
    frm = wx.Frame(None, title='GLCanvas Sample')
    canvas = Canvas3D(frm)

    frm.Show()


    app.MainLoop()



#----------------------------------------------------------------------


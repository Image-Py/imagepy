# -*- coding: utf-8 -*-
# Some widgets(HistCanvas/NumCtrl/ColorCtrl) defination 
"""
Created on Sat Nov 26 15:30:47 2016

@author: yxl
"""
import wx
import numpy as np

class HistCanvas(wx.Panel):
    """ HistCanvas: diverid from wx.core.Panel """
    def __init__(self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, 
                            pos = wx.DefaultPosition, size = wx.Size(256,81), 
                            style = wx.TAB_TRAVERSAL )
        self.init_buf()
        self.his = None
        self.update = False
        self.x1, self.x2 = 0, 255
        self.Bind(wx.EVT_SIZE, self.on_size)  
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def init_buf(self):
        box = self.GetClientSize()
        self.buffer = wx.Bitmap(box.width, box.height)
        
    def on_size(self, event):
        self.init_buf()
        self.update = True
        
    def on_idle(self, event):
        if self.update == True:
            self.draw()
            self.update = False
            
    def on_paint(self, event):
        wx.BufferedPaintDC(self, self.buffer)
        
    def set_hist(self, hist):
        self.hist = (hist*80/hist.max()).astype(np.uint8)
        self.update = True
        
    def set_lim(self, x1, x2):
        self.x1, self.x2 = x1, x2
        self.update = True
        
    def draw(self):
        if self.hist is None:
            return
        
        # get client device context buffer
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.Clear()
        # w, h = self.GetClientSize()
    
        # the main draw process 
        print("drawing histogram")
        dc.SetPen(wx.Pen((100,100,100), width=1, style=wx.SOLID))        
        for i in range(256):
            dc.DrawLine(i,80,i,80-self.hist[i])            
        dc.SetPen(wx.Pen((0,0,0), width=1, style=wx.SOLID))
        dc.DrawLine(self.x1, 80, self.x2, 0)
        dc.DrawLines([(0,0),(255,0),(255,80),(0,80),(0,0)])
        
class NumCtrl(wx.TextCtrl):
    """NumCtrl: diverid from wx.core.TextCtrl """
    def __init__(self, parent, rang, accury):
        wx.TextCtrl.__init__(self, parent, wx.TE_RIGHT)
        self.min, self.max = rang
        self.accury = accury
        wx.TextCtrl.Bind(self, wx.EVT_KEY_UP, self.ontext)
        
    #! TODO: what is this?
    def Bind(self, z, f):
        self.f = f
        
    def ontext(self, event):
        self.f(event)
        if self.GetValue()==None:
            self.SetBackgroundColour((255,255,0))
        else:
            self.SetBackgroundColour((255,255,255))
        
    def SetValue(self, n):
        wx.TextCtrl.SetValue(self, str(round(n,self.accury) if self.accury>0 else int(n)))
        
    def GetValue(self):
        sval = wx.TextCtrl.GetValue(self)
        try:
            num = float(sval) if self.accury>0 else int(sval)
        except ValueError:
            return None
        if num<self.min or num>self.max:
            return None
        if abs(round(num, self.accury) - num) > 1E-5:
            return None
        return num
        
class ColorCtrl(wx.TextCtrl):
    """ColorCtrl: deverid fron wx.coreTextCtrl"""
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, wx.TE_RIGHT)
        wx.TextCtrl.Bind(self, wx.EVT_KEY_UP, self.ontext)
        wx.TextCtrl.Bind(self, wx.EVT_LEFT_DOWN, self.oncolor)
        
    def Bind(self, z, f):
        self.f = f
        
    def ontext(self, event):
        print('ColorCtrl')
        
    def oncolor(self, event):
        rst = None
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            rst = dlg.GetColourData().GetColour()
            self.SetBackgroundColour(rst)
            self.SetValue(rst.GetAsString(wx.C2S_HTML_SYNTAX))
            self.f(event)
        dlg.Destroy()
    
    def SetValue(self, color):
        wx.TextCtrl.SetBackgroundColour(self, color)
        des = self.GetBackgroundColour().GetAsString(wx.C2S_HTML_SYNTAX)
        wx.TextCtrl.SetValue(self, des)
        
    def GetValue(self):
        return self.GetBackgroundColour().Get(False)
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None)
    hist = Histogram(frame)
    frame.Fit()
    frame.Show(True)
    hist.set_hist(np.arange(256))
    app.MainLoop() 
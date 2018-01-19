import wx
import numpy as np

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
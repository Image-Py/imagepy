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
        
class FloatSlider(wx.Panel):
    
    def __init__( self, parent, rang, accury):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.slider = wx.Slider( self, wx.ID_ANY, 128, 0, 255, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_SELRANGE )
        sizer.Add( self.slider, 1, wx.ALIGN_CENTER|wx.ALL, 0 )
        self.text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
        sizer.Add( self.text, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        self.spin = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.Size(25, 25), 0 )
        sizer.Add( self.spin, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        self.SetSizer( sizer )
        self.Layout()
        
        # Connect Events
        self.slider.Bind( wx.EVT_SCROLL, self.on_scroll )
        self.text.Bind( wx.EVT_KEY_UP, self.on_text )
        self.spin.Bind( wx.EVT_SPIN_DOWN, self.on_down )
        self.spin.Bind( wx.EVT_SPIN_UP, self.on_up )
        self.set_para(rang, accury)

    def Bind(self, z, f):
        self.f = f

    def set_para(self, rang, accury):
        self.min = round(rang[0], accury)
        self.max = round(rang[1], accury)
        self.accury = accury

    def on_scroll(self, event):
        n = self.slider.GetValue()/255.0*(self.max-self.min)+self.min
        print(n, round(n, self.accury))
        self.text.SetValue(str(round(n,self.accury) if self.accury>0 else int(n)))
        self.text.SetBackgroundColour((255,255,255))
        self.f(event)

    def on_up(self, event):
        self.slider.SetValue(self.slider.GetValue()+1)
        self.on_scroll(event)

    def on_down(self, event):
        self.slider.SetValue(self.slider.GetValue()-1)
        self.on_scroll(event)

    def on_text(self, event):
        self.f(event)
        if self.GetValue()==None:
            self.text.SetBackgroundColour((255,255,0))
        else:
            self.text.SetBackgroundColour((255,255,255))

    def SetValue(self, n):
        if not self.text.HasFocus():
            self.text.SetValue(str(round(n,self.accury) if self.accury>0 else int(n)))
        self.slider.SetValue(int(round((n-self.min)/(self.max-self.min)*255)))
        
    def GetValue(self):
        sval = self.text.GetValue()
        try:
            num = float(sval) if self.accury>0 else int(sval)
        except ValueError:
            return None
        if num<self.min-1e-20 or num>self.max+1e-20:
            print(num, self.min, self.max)
            return None
        if abs(round(num, self.accury) - num) > 1E-5:
            print('fffffffffff')
            return None
        return num

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None)
    hist = Histogram(frame)
    frame.Fit()
    frame.Show(True)
    hist.set_hist(np.arange(256))
    app.MainLoop() 
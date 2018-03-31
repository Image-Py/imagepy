import wx, platform
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
        self.linux = platform.system() == 'Linux'
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(-1,-1), style = wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.slider = wx.Slider( self, wx.ID_ANY, 128, 0, 255, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL)
        sizer.Add( self.slider, 0, wx.ALL|wx.EXPAND, 0 )
        subsizer = wx.BoxSizer( wx.HORIZONTAL )
        self.lab_min = wx.StaticText( self, wx.ID_ANY, '0', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lab_min.Wrap( -1 )
        subsizer.Add( self.lab_min, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        subsizer.AddStretchSpacer(prop=1)
        self.text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50,-1), 0 )
        subsizer.Add( self.text, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        self.spin = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.Size([20,-1][self.linux],-1),  [0, wx.SP_HORIZONTAL][self.linux])
        self.spin.SetRange(0, 255)
        self.spin.SetValue(128)
        subsizer.Add( self.spin, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 0 )
        subsizer.AddStretchSpacer(prop=1)
        self.lab_max = wx.StaticText( self, wx.ID_ANY, '0', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lab_max.Wrap( -1 )
        subsizer.Add( self.lab_max, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        sizer.Add( subsizer, 1, wx.EXPAND, 5 )


        self.SetSizer( sizer )
        self.Layout()
        
        # Connect Events
        self.slider.Bind( wx.EVT_SCROLL, self.on_scroll )
        self.text.Bind( wx.EVT_KEY_UP, self.on_text )
        #if not self.linux:
        self.spin.Bind( wx.EVT_SPIN, self.on_spin )
        self.set_para(rang, accury)

    def Bind(self, z, f):
        self.f = f

    def set_para(self, rang, accury):
        self.min = round(rang[0], accury)
        self.max = round(rang[1], accury)
        self.lab_min.SetLabel(str(round(rang[0],accury)))
        self.lab_max.SetLabel(str(round(rang[1],accury)))
        self.accury = accury

    def on_scroll(self, event):
        value = self.slider.GetValue()#self.slider.GetThumbPosition() if self.linux else 
        self.spin.SetValue(value)
        n = value/255.0*(self.max-self.min)+self.min
        self.text.SetValue(str(round(n,self.accury) if self.accury>0 else int(n)))
        self.text.SetBackgroundColour((255,255,255))
        self.f(event)

    def on_spin(self, event):
        self.slider.SetValue(self.spin.GetValue())
        self.on_scroll(event)

    def on_text(self, event):
        self.f(event)
        if self.GetValue()==None:
            self.text.SetBackgroundColour((255,255,0))
        else:
            self.text.SetBackgroundColour((255,255,255))
            self.SetValue(self.GetValue())

    def SetValue(self, n):
        if not self.text.HasFocus():
            self.text.SetValue(str(round(n,self.accury) if self.accury>0 else int(n)))
        pos = int(round((n-self.min)/(self.max-self.min)*255))
        #if self.linux:self.slider.SetScrollbar(pos, 0, 255, 0)
        #if not self.linux:
        self.slider.SetValue(pos)
        self.spin.SetValue(pos)
        
    def GetValue(self):
        sval = self.text.GetValue()
        try:
            num = float(sval) if self.accury>0 else int(sval)
        except ValueError:
            return None
        if num<self.min-1e-20 or num>self.max+1e-20:
            return None
        if abs(round(num, self.accury) - num) > 1E-5:
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
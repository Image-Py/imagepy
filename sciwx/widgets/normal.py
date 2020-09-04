import wx, platform
import numpy as np

class NumCtrl(wx.Panel):
    """NumCtrl: diverid from wx.core.TextCtrl """
    def __init__(self, parent, rang, accury, title, unit, app=None):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.prefix = lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                  wx.DefaultPosition, wx.DefaultSize)

        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.ctrl = wx.TextCtrl(self, wx.TE_RIGHT)
        self.ctrl.Bind(wx.EVT_KEY_UP, lambda x : self.para_changed(key))
        sizer.Add( self.ctrl, 2, wx.ALL, 5 )

        self.postfix = lab_unit = wx.StaticText( self, wx.ID_ANY, unit,
                                wx.DefaultPosition, wx.DefaultSize)

        lab_unit.Wrap( -1 )
        sizer.Add( lab_unit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.SetSizer(sizer)

        self.min, self.max = rang
        self.accury = accury
        self.ctrl.Bind(wx.EVT_KEY_UP, self.ontext)
        
    #! TODO: what is this?
    def Bind(self, z, f):self.f = f
        
    def ontext(self, event):
        self.f(self)
        if self.GetValue()==None:
            self.ctrl.SetBackgroundColour((255,255,0))
        else:
            self.ctrl.SetBackgroundColour((255,255,255))
        self.Refresh()
        
    def SetValue(self, n):
        self.ctrl.SetValue(str(round(n,self.accury) if self.accury>0 else int(n)))
        
    def GetValue(self):
        sval = self.ctrl.GetValue()
        try:
            num = float(sval) if self.accury>0 else int(sval)
        except ValueError:
            return None
        if num<self.min or num>self.max:
            return None
        if abs(round(num, self.accury) - num) > 1E-5:
            return None
        return num
        
class TextCtrl(wx.Panel):
    def __init__(self, parent, title, unit, app=None):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.prefix = lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                  wx.DefaultPosition, wx.DefaultSize)

        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.ctrl = wx.TextCtrl(self, wx.TE_RIGHT)
        sizer.Add( self.ctrl, 2, wx.ALL, 5 )

        self.postfix = lab_unit = wx.StaticText( self, wx.ID_ANY, unit,
                                  wx.DefaultPosition, wx.DefaultSize)

        lab_unit.Wrap( -1 )
        sizer.Add( lab_unit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.SetSizer(sizer)

        self.ctrl.Bind(wx.EVT_KEY_UP, self.ontext)
        
    #! TODO: what is this?
    def Bind(self, z, f):self.f = f
        
    def ontext(self, event):
        self.f(self)
        
    def SetValue(self, n):
        self.ctrl.SetValue(n)
        
    def GetValue(self):
        return self.ctrl.GetValue()

class ColorCtrl(wx.Panel):
    def __init__(self, parent, title, unit, app=None):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.prefix = lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize)
        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.ctrl = wx.TextCtrl(self, wx.TE_RIGHT)
        sizer.Add( self.ctrl, 2, wx.ALL, 5 )
        self.postfix = lab_unit = wx.StaticText( self, wx.ID_ANY, unit,
                                  wx.DefaultPosition, wx.DefaultSize)
        lab_unit.Wrap( -1 )
        sizer.Add( lab_unit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.SetSizer(sizer)
        
        self.ctrl.Bind(wx.EVT_KEY_UP, self.ontext)
        self.ctrl.Bind( wx.EVT_LEFT_DCLICK, self.oncolor)
        
    def Bind(self, z, f):
        self.f = f
        
    def ontext(self, event):
        self.f(self)
        if self.GetValue()==None:
            self.ctrl.SetBackgroundColour((255,255,255))
        else:
            self.ctrl.SetBackgroundColour(self.GetValue())
        self.Refresh()
        
    def oncolor(self, event):
        rst = None
        dialog = wx.ColourDialog(self)
        dialog.GetColourData().SetChooseFull(True)
        if dialog.ShowModal() == wx.ID_OK:
            rst = dialog.GetColourData().GetColour()
            self.ctrl.SetBackgroundColour(rst)
            self.ctrl.SetValue(rst.GetAsString(wx.C2S_HTML_SYNTAX))
            self.f(self)
        dialog.Destroy()
    
    def SetValue(self, color):
        self.ctrl.SetBackgroundColour(color)
        des = self.ctrl.GetBackgroundColour().GetAsString(wx.C2S_HTML_SYNTAX)
        self.ctrl.SetValue(des)
        
    def GetValue(self):
        rgb = self.ctrl.GetValue()
        if len(rgb)!=7 or rgb[0]!='#': return None
        try: rgb = int(rgb[1:], 16)
        except: return None
        return wx.Colour(rgb).Get(False)[::-1]

class PathCtrl(wx.Panel):
    def __init__(self, parent, filt, io, title, app=None):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.prefix = lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize)
        self.filt, self.io = filt, io
        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.ctrl = wx.TextCtrl(self, wx.TE_RIGHT)
        sizer.Add( self.ctrl, 2, wx.ALL, 5 )
        self.SetSizer(sizer)
        
        self.ctrl.Bind(wx.EVT_KEY_UP, self.ontext)
        self.ctrl.Bind( wx.EVT_LEFT_DCLICK, self.onselect)
        
    def Bind(self, z, f): self.f = f
        
    def ontext(self, event): 
        self.f(self)
        
    def onselect(self, event):
        if isinstance(self.filt, str): self.filt = self.filt.split(',')
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in self.filt])
        dic = {'open':wx.FD_OPEN, 'save':wx.FD_SAVE}
        if self.io=='folder':
            dialog = wx.DirDialog(self, 'Path Select', '.', wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST | wx.FD_CHANGE_DIR)
        else: dialog = wx.FileDialog(self, 'Path Select', '', '.', filt, dic[self.io] | wx.FD_CHANGE_DIR)
        rst = dialog.ShowModal()
        if rst == wx.ID_OK:
            path = dialog.GetPath()
            self.ctrl.SetValue(path)
            self.f(self)
        dialog.Destroy()
        
    def SetValue(self, value):
        self.ctrl.SetValue(value)
        
    def GetValue(self):
        return self.ctrl.GetValue()

class Choice(wx.Panel):
    def __init__(self, parent, choices, tp, title, unit, app=None):
        wx.Panel.__init__(self, parent)
        self.tp, self.choices = tp, choices
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.prefix = lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize)

        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.ctrl = wx.Choice( self, wx.ID_ANY,
                          wx.DefaultPosition, wx.DefaultSize,
                          [str(choice) for choice in choices], 0 )

        self.ctrl.SetSelection(0)
        sizer.Add( self.ctrl, 2, wx.ALL, 5 )
        self.postfix = lab_unit = wx.StaticText( self, wx.ID_ANY, unit,
                                  wx.DefaultPosition, wx.DefaultSize)
        lab_unit.Wrap( -1 )
        sizer.Add( lab_unit, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.SetSizer(sizer)
        self.ctrl.Bind( wx.EVT_CHOICE, self.on_choice)
        
    def Bind(self, z, f):
        self.f = f
        
    def on_choice(self, event):
        self.f(self)

    def SetValue(self, x):
        n = self.choices.index(x) if x in self.choices else 0
        self.ctrl.SetSelection(n)
        
    def GetValue(self):
        return self.tp(self.choices[self.ctrl.GetSelection()])

class AnyType( wx.Panel ):
    def __init__( self, parent, title, app=None):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(-1, -1), style = wx.TAB_TRAVERSAL )
        
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.prefix = lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize)
        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.txt_value = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer.Add( self.txt_value, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        com_typeChoices = ['Int', 'Float', 'Str']
        self.postfix = self.com_type = wx.ComboBox( self, wx.ID_ANY, 'Float', wx.DefaultPosition, wx.DefaultSize, com_typeChoices, 0 )
        sizer.Add( self.com_type, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        
        self.SetSizer( sizer )
        self.Layout()
        
        # Connect Events
        self.txt_value.Bind( wx.EVT_KEY_UP, self.on_text )
        self.com_type.Bind( wx.EVT_COMBOBOX, self.on_type )
    
    def Bind(self, z, f):
        self.f = f
    
    def SetValue(self, v):
        self.txt_value.SetValue(str(v))
        if isinstance(v, int):
            self.com_type.Select(0)
        if isinstance(v, float):
            self.com_type.Select(1)
        else: self.com_type.Select(2)


    def GetValue(self):
        tp = self.com_type.GetValue()
        sval = wx.TextCtrl.GetValue(self.txt_value)
        if tp == 'Float':
            try: num = float(sval)
            except ValueError: return None
        if tp == 'Int':
            try: num = int(sval)
            except ValueError: return None
        if tp == 'Str':
            try: num = str(sval)
            except ValueError: return None
        return num
    
    # Virtual event handlers, overide them in your derived class
    def on_text( self, event ):
        self.f(self)
        if self.GetValue()==None:
            self.txt_value.SetBackgroundColour((255,255,0))
        else: self.txt_value.SetBackgroundColour((255,255,255))
        self.Refresh()
    
    def on_type( self, event ):
        if self.GetValue()==None:
            self.txt_value.SetBackgroundColour((255,255,0))
        else: self.txt_value.SetBackgroundColour((255,255,255))
        self.Refresh()

class Choices(wx.Panel):
    def __init__( self, parent, choices, title, app=None):
        self.choices = list(choices)
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize)
        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALL, 5 )
        self.ctrl = wx.CheckListBox(self, -1, (80, 50), wx.DefaultSize, [str(i) for i in choices])
        sizer.Add( self.ctrl, 1, wx.ALL|wx.EXPAND, 0 )
        self.ctrl.SetMaxSize( wx.Size( -1,100 ) )
        self.SetSizer(sizer)
        self.ctrl.Bind(wx.EVT_CHECKLISTBOX, self.on_check)

    def Bind(self, z, f):
        self.f = f

    def on_check(self, event):
        self.f(self)

    def GetValue(self):
        return [self.choices[i] for i in self.ctrl.GetCheckedItems()]
        
    def SetValue(self, value):
        print('set value', value)
        self.ctrl.SetCheckedItems([
            self.choices.index(i) for i in value if i in self.choices])

class FloatSlider(wx.Panel):
    def __init__( self, parent, rang, accury, title, unit='', app=None):
        self.linux = platform.system() == 'Linux'
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(-1,-1), style = wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.slider = wx.Slider( self, wx.ID_ANY, 128, 0, 255, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL)
        sizer.Add( self.slider, 0, wx.TOP|wx.EXPAND, 5 )
        subsizer = wx.BoxSizer( wx.HORIZONTAL )
        self.lab_min = wx.StaticText( self, wx.ID_ANY, '0', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lab_min.Wrap( -1 )
        subsizer.Add( self.lab_min, 1, wx.BOTTOM|wx.LEFT|wx.ALIGN_CENTER, 5 )
        #subsizer.AddStretchSpacer(prop=1)
        self.lab_title = wx.StaticText( self, wx.ID_ANY, title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lab_title.Wrap( -1 )
        subsizer.Add( self.lab_title, 0, wx.ALIGN_CENTER|wx.BOTTOM|wx.RIGHT, 5 )
        self.text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50,-1), 0 )
        subsizer.Add( self.text, 0, wx.BOTTOM|wx.ALIGN_CENTER, 5 )
        self.spin = wx.SpinButton( self, wx.ID_ANY, wx.DefaultPosition, wx.Size([20,-1][self.linux],-1),  [0, wx.SP_HORIZONTAL][self.linux])
        self.spin.SetRange(0, 255)
        self.spin.SetValue(128)
        subsizer.Add( self.spin, 0, wx.BOTTOM|wx.EXPAND, 5 )
        self.lab_unit = wx.StaticText( self, wx.ID_ANY, unit, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lab_unit.Wrap( -1 )
        subsizer.Add( self.lab_unit, 0, wx.ALIGN_CENTER|wx.BOTTOM|wx.LEFT, 5 )
        #subsizer.AddStretchSpacer(prop=1)
        self.lab_max = wx.StaticText( self, wx.ID_ANY, '0', wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.lab_max.Wrap( -1 )
        subsizer.Add( self.lab_max, 1, wx.ALIGN_CENTER|wx.BOTTOM|wx.RIGHT, 5 )
        sizer.Add( subsizer, 0, wx.EXPAND, 0 )


        self.SetSizer( sizer )
        self.Layout()
        
        # Connect Events
        self.slider.Bind( wx.EVT_SCROLL, self.on_scroll )
        self.text.Bind( wx.EVT_KEY_UP, self.on_text )
        #if not self.linux:
        self.spin.Bind( wx.EVT_SPIN, self.on_spin)
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
        self.f(self)

    def on_spin(self, event):
        self.slider.SetValue(self.spin.GetValue())
        self.on_scroll(event)

    def on_text(self, event):
        self.f(self)
        if self.GetValue()==None:
            self.text.SetBackgroundColour((255,255,0))
        else:
            self.text.SetBackgroundColour((255,255,255))
            self.SetValue(self.GetValue())
        self.Refresh()

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

class Label(wx.Panel):
    def __init__(self, parent, title, app=None):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALL, 5 )
        self.SetSizer(sizer)

    def Bind(self, z, f): pass
    def SetValue(self, v): pass
    def GetValue(self, v): pass

class Check(wx.Panel):
    def __init__(self, parent, title, app=None):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        check = wx.CheckBox(self, -1, title)
        sizer.Add( check, 0, wx.ALL, 5 )
        self.SetSizer(sizer)

        self.SetValue = check.SetValue
        self.GetValue = check.GetValue
        check.Bind(wx.EVT_CHECKBOX, self.on_check)

    def on_check(self, event):self.f(self)
    def Bind(self, z, f): self.f = f

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    frame.Show()
    app.MainLoop() 

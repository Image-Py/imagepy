# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 01:24:41 2016

@author: yxl
"""
import wx, os
import wx.lib.agw.aui as aui
from .canvas import Canvas
from ..core.manager import ImageManager, WindowsManager, ToolsManager
from ..core.manager import ShotcutManager
from .. import IPy, root_dir
import numpy as np
import weakref

class CanvasPanel(wx.Panel):
    """CanvasFrame: derived from the wx.core.Frame"""
    ## TODO: Main frame ???
    def __init__(self, parent=None):
        wx.Frame.__init__ ( self, parent)

        #self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        
        self.SetSizeHints( wx.Size( 560,-1 ), wx.DefaultSize )
        WindowsManager.add(self)
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        sizer = wx.BoxSizer( wx.VERTICAL )
        self.txt_info = wx.StaticText( self, wx.ID_ANY,
                                       '500*500 pixels 173k',
                                       wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_info.Wrap( -1 )
        sizer.Add( self.txt_info, 0, wx.ALL, 0 )
        
        self.canvas = Canvas(self, autofit = IPy.uimode()=='ij')
        self.canvas.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)
        self.Bind(wx.EVT_IDLE, self.on_idle)
        #self.canvas.set_handler(self.set_info)
        self.handle = None
        sizer.Add( self.canvas, 1, wx.EXPAND |wx.ALL, 0 )

        self.chan = wx.Slider( self, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, 
            wx.SL_HORIZONTAL| wx.SL_SELRANGE| wx.SL_TOP)
        sizer.Add( self.chan, 0, wx.ALL|wx.EXPAND, 0 )
        self.chan.SetMaxSize( wx.Size( -1,18 ) )
        self.chan.Hide()

        self.page = wx.ScrollBar( self, wx.ID_ANY,
                                  wx.DefaultPosition, wx.DefaultSize, wx.SB_HORIZONTAL)
        self.page.SetScrollbar(0,0,0,0, refresh=True)
        sizer.Add( self.page, 0, wx.ALL|wx.EXPAND, 0 )
        self.page.Hide()

        self.SetSizer(sizer)
        self.Layout()
        self.page.Bind(wx.EVT_SCROLL, self.on_scroll)
        self.chan.Bind(wx.EVT_SCROLL, self.on_scroll)
        # panel.Bind(wx.EVT_CHAR, self.OnKeyDown)
        self.opage = self.ochan = 0
        self.chantype = None
        self.ips = self.back = None
        self.olddia = 0
        #self.Fit()

        #self.SetAcceleratorTable(IPy.curapp.shortcut)
        
    '''
    def SetTitle(self, title):
        parent = self.GetParent()
        if not IPy.aui: parent.SetTitle(title)
        else: parent.SetPageText(parent.GetPageIndex(self), title)
        #print(dir(parent)) #parent.DeletePage(parent.GetPageIndex(self))
    '''
    
    def on_mouse(self, me):
        tool = self.ips.tool
        if tool == None : tool = ToolsManager.curtool
        x,y = self.canvas.to_data_coor(me.GetX(), me.GetY())
        if me.Moving() and not me.LeftIsDown() and not me.RightIsDown() and not me.MiddleIsDown():
            xx,yy = int(round(x)), int(round(y))
            k, unit = self.ips.unit
            if xx>=0 and xx<self.ips.img.shape[1] and yy>=0 and yy<self.ips.img.shape[0]:
                IPy.set_info('Location:%.1f %.1f  Value:%s'%(x*k, y*k, self.ips.img[yy,xx]))
        if tool==None:return
        
        sta = [me.AltDown(), me.ControlDown(), me.ShiftDown()]
        if me.ButtonDown():tool.mouse_down(self.ips, x, y, me.GetButton(), 
            alt=sta[0], ctrl=sta[1], shift=sta[2], canvas=self.canvas)
        if me.ButtonUp():tool.mouse_up(self.ips, x, y, me.GetButton(), 
            alt=sta[0], ctrl=sta[1], shift=sta[2], canvas=self.canvas)
        if me.Moving():tool.mouse_move(self.ips, x, y, None, 
            alt=sta[0], ctrl=sta[1], shift=sta[2], canvas=self.canvas)
        btn = [me.LeftIsDown(), me.MiddleIsDown(), me.RightIsDown(),True].index(True)
        if me.Dragging():tool.mouse_move(self.ips, x, y, 0 if btn==3 else btn+1, 
            alt=sta[0], ctrl=sta[1], shift=sta[2], canvas=self.canvas)
        wheel = np.sign(me.GetWheelRotation())
        if wheel!=0:tool.mouse_wheel(self.ips, x, y, wheel, 
            alt=sta[0], ctrl=sta[1], shift=sta[2], canvas=self.canvas)
        if hasattr(tool, 'cursor'):
            self.canvas.SetCursor(wx.Cursor(tool.cursor))
        else : self.canvas.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

    def on_idle(self, event):
        if not self.IsShown() or self.ips==None:return
        if self.ips.scrchanged:
            self.set_ips(self.ips)
            self.ips.scrchanged = False
            self.set_info(self.ips)
            self.canvas.fit()
            self.set_fit(self.ips)
            print('scr changed =====')
        
        if self.ips.dirty != False:
            self.set_info(self.ips)
            if self.ips.roi is None: self.canvas.marks['roi'] = None
            else: 
                draw = lambda dc, f, **key: self.ips.roi.draw(dc, f, cur=self.ips.cur, **key)
                self.canvas.marks['roi'] = draw
            if self.ips.mark is None: self.canvas.marks['mark'] = None
            else:
                if self.ips.mark is None: draw = None
                else: draw = lambda dc, f, **key: self.ips.mark.draw(dc, f, cur=self.ips.cur, **key)
                self.canvas.marks['mark'] = draw
            if self.ips.unit == (1, 'pix'): self.canvas.marks['unit'] = None
            else:
                self.canvas.marks['unit'] = lambda dc, f, **key:self.draw_ruler(dc)

            self.canvas.set_img(self.ips.imgs[self.ips.cur])
            self.canvas.set_cn(self.ips.chan)
            self.canvas.set_rg(self.ips.chan_range)
            self.canvas.set_log(self.ips.log)

            if self.ips.back != None:
                self.ips.back.cur = self.ips.cur
                self.canvas.set_back(self.ips.back.img)
                self.canvas.set_cn(self.ips.back.chan, True)
                self.canvas.set_log(self.ips.back.log, True)
                self.canvas.set_rg(self.ips.back.chan_range, True)
                self.canvas.set_lut(self.ips.back.lut, True)
                self.canvas.set_mode(self.ips.chan_mode)
            else: 
                self.canvas.set_back(None)
                self.canvas.set_mode('set')

            self.canvas.lut = self.ips.lut
            #self.canvas.marks['roi'] = self.ips.roi
            # self.canvas.marks['mark'] = self.ips.mark.body[ips.cursor]
            self.set_fit(self.ips)
            self.canvas.update()
            self.ips.dirty = False
        if not self.handle is None: self.handle(self.ips)
    
    def draw_ruler(self, dc):
        dc.SetPen(wx.Pen((255,255,255), width=2, style=wx.SOLID))
        conbox, winbox = self.canvas.conbox, self.canvas.winbox
        x1 = max(conbox[0], winbox[0])+5
        x2 = min(conbox[2], winbox[2])+x1-10
        pixs = (x2-x1+10)*self.ips.size[1]/10.0/conbox[2]
        h = min(conbox[1]+conbox[3],winbox[3])-5
        dc.DrawLineList([(x1,h,x2,h)])
        dc.DrawLineList([(i,h,i,h-8) for i in np.linspace(x1, x2, 3)])
        dc.DrawLineList([(i,h,i,h-5) for i in np.linspace(x1, x2, 11)])

        dc.SetTextForeground((255,255,255))
        k, unit = self.ips.unit
        text = 'Unit = %.1f %s'%(k*pixs, unit)
        dw,dh = dc.GetTextExtent(text)
        dc.DrawText(text, (x2-dw, h-10-dh))

    def set_handler(self, handle=None):
        self.handle = handle

    def set_info(self, ips):
        stk = 'stack' if ips.is3d else 'list'
        label='S:{}/{};  C:{}/{}; {}  {}x{} pixels; {}; {} M'.format(ips.cur+1, ips.get_nslices(),
            ips.chan+1 if isinstance(ips.chan, int) else tuple(ips.chan), ips.get_nchannels(), 
            stk if ips.get_nslices()>1 else '', ips.size[0], ips.size[1], ips.imgtype, round(ips.get_nbytes()/1024.0/1024.0, 2))
        if label != self.txt_info.GetLabel(): self.txt_info.SetLabel(label)

    def set_fit(self, ips):
        resize = False
        if ips.get_nslices() != self.opage:
            self.opage = ips.get_nslices()
            if ips.get_nslices()==1 and self.page.Shown:
                self.page.Hide()
                resize = True
            if ips.get_nslices()>1 and not self.page.Shown:
                self.page.Show()
                print('Show ......')
                resize = True
            self.page.SetScrollbar(0, 0, ips.get_nslices()-1, 0, refresh=True)
        if ips.get_nchannels() != self.ochan or type(ips.chan) != self.chantype:
            self.ochan = ips.get_nchannels()
            self.chantype = type(ips.chan)
            isrgb = not isinstance(ips.chan, int)
            if not isinstance(ips.chan, int) and self.chan.Shown:
                self.chan.Hide()
                resize = True
            if isinstance(ips.chan, int) and ips.get_nchannels()>1 and not self.chan.Shown:
                self.chan.Show()
                resize = True
            self.chan.SetMax(ips.get_nchannels()-1)
        a,b,c,d = self.canvas.conbox
        l = ((c-a)**2+(d-b)**2)**0.5
        if resize or abs(self.olddia-l)>1: 
            self.olddia = l
            if IPy.uimode()!='ipy': 
                w = self.canvas.scrbox[0]*0.9
                h = self.canvas.scrbox[1]*0.9
                if c-a<w and d-b<h:
                    self.Fit()
                    self.GetParent().Fit()
                    self.Layout()
            else: self.Layout()

                #self.GetSizer().Layout()

        #if not self.handle is None: self.handle(ips, resize)
        
        #print('CanvasFrame:set_info')
        #self.page.Show()

    def set_ips(self, ips):
        self.ips = ips
        self.canvas.set_img(ips.img)
        self.canvas.set_cn(ips.chan)
        self.canvas.set_rg(ips.chan_range)
        self.canvas.set_lut(ips.lut)

    '''
    def set_back(self, ips):
        self.back = ips
        if ips is None:
            return self.canvas.set_back(None)
        self.canvas.set_back(ips.img)
        self.canvas.set_cn(ips.chan, True)
        self.canvas.set_rg(ips.chan_range, True)
        self.canvas.set_lut(ips.lut, True)
    '''
    def on_scroll(self, event):
        self.ips.cur = self.page.GetThumbPosition()
        if isinstance(self.ips.chan, int):
            self.ips.chan = self.chan.GetValue()
        self.ips.update()
        self.on_idle(None)

    def close(self):
        parent = self.GetParent()
        if IPy.uimode()=='ij':
            parent.Close()
        if IPy.uimode()=='ipy':
            idx = parent.GetPageIndex(self)
            parent.DeletePage(idx)
            self.set_handler()
            self.canvas.set_handler()
            WindowsManager.remove(self)
    
    def __del__(self):
        print('canvas panel del')

class CanvasFrame(wx.Frame):
    """CanvasFrame: derived from the wx.core.Frame"""
    ## TODO: Main frame ???
    def __init__(self, parent=None):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                            title = wx.EmptyString,
                            pos = wx.DefaultPosition,
                            size = wx.Size( -1,-1 ),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.canvaspanel = CanvasPanel(self)
        logopath = os.path.join(root_dir, 'data/logo.ico')
        self.SetIcon(wx.Icon(logopath, wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_ACTIVATE, self.on_valid)
        self.SetAcceleratorTable(IPy.curapp.shortcut)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.canvaspanel.set_handler(self.set_title)
    
    def set_ips(self, ips):
        self.canvaspanel.set_ips(ips)

    def set_title(self, ips):
        title = ips.title + '' if ips.tool==None else ' [%s]'%ips.tool.title
        self.SetTitle(ips.title)

    def on_valid(self, event):
        if event.GetActive():
            ImageManager.add(self.canvaspanel.ips)
            WindowsManager.add(self.canvaspanel)

    def on_close(self, event):
        #self.canvaspanel.set_handler()
        #self.canvaspanel.canvas.set_handler()
        WindowsManager.remove(self.canvaspanel)
        ImageManager.remove(self.canvaspanel.ips)
        self.canvaspanel.ips = None
        self.canvaspanel.back = None
        event.Skip()


class ImgArtProvider(aui.AuiDefaultDockArt):
    def __init__(self, img):
        aui.AuiDefaultDockArt.__init__(self)
        self.bitmap = wx.Bitmap(img, wx.BITMAP_TYPE_PNG)

    def DrawBackground(self, dc, window, orient, rect):
        aui.AuiDefaultDockArt.DrawBackground(self, dc, window, orient, rect)
        
        
        memDC = wx.MemoryDC()
        memDC.SelectObject(self.bitmap)
        w, h = self.bitmap.GetWidth(), self.bitmap.GetHeight()
        dc.Blit((rect[2]-w)//2, (rect[3]-h)//2, w, h, memDC, 0, 0, wx.COPY, True)
        
        #dc.DrawBitmap(self.bitmap, 0, 0)
        #dc.DrawRectangle(rect)

class CanvasNoteBook(wx.lib.agw.aui.AuiNotebook):
    def __init__(self, parent):
        wx.lib.agw.aui.AuiNotebook.__init__( self, parent, wx.ID_ANY, 
            wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.aui.AUI_NB_DEFAULT_STYLE )
        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_pagevalid) 
        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        self.SetArtProvider(aui.AuiSimpleTabArt())
        
    def set_background(self, img):
        self.GetAuiManager().SetArtProvider(ImgArtProvider(img))

    def add_page(self, panel, ips):
        self.AddPage(panel, ips.title, True, wx.NullBitmap )
        panel.set_handler(lambda ips, pan=panel: self.set_title(ips, pan))
        self.Refresh()

    def set_title(self, ips, panel):
        title = ips.title + '' if ips.tool==None else ' [%s]'%ips.tool.title
        self.SetPageText(self.GetPageIndex(panel), title)

    def on_pagevalid(self, event):
        ImageManager.add(event.GetEventObject().GetPage(event.GetSelection()).ips)
        WindowsManager.add(event.GetEventObject().GetPage(event.GetSelection()))

    def on_close(self, event):
        WindowsManager.remove(event.GetEventObject().GetPage(event.GetSelection()))
        ImageManager.remove(event.GetEventObject().GetPage(event.GetSelection()).ips)
        event.GetEventObject().GetPage(event.GetSelection()).ips = None
        event.GetEventObject().GetPage(event.GetSelection()).back = None

class VirturlCanvas:
    instance = []
    class Canvas:
        def __init__(self, ips):
            self.ips = ips
        def __del__(self):
            print('virturl canvas deleted!')

    def __init__(self, ips):
        self.ips = ips
        self.canvas = VirturlCanvas.Canvas(ips)
        VirturlCanvas.instance.append(self)
        ImageManager.add(self)

    def close(self): VirturlCanvas.instance.remove(self)


if __name__=='__main__':
    app = wx.PySimpleApp()
    CanvasFrame().Show(True)
    app.MainLoop()

import wx.lib.agw.ribbon as rb
import wx
import numpy as np

def make_logo(path, w=40):
    if isinstance(path, str):
        img = wx.Bitmap(path).ConvertToImage()
    else: img = wx.Image(1, 1, np.array(path, dtype=np.uint8).tobytes())
    return img.Rescale(w, w).ConvertToBitmap()

def make_logo(obj, w=40):
    bmp = None
    if isinstance(obj, str) and '.' in obj:
        bmp = wx.Bitmap(obj).ConvertToImage()
    if isinstance(obj, str) and not '.' in obj:
        bmp = wx.Bitmap(w, w)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush((255,255,255)))
        dc.Clear()
        dc.SetTextForeground((100,0,128))
        font = dc.GetFont()
        font.SetPointSize(22)
        dc.SetFont(font)
        ww, hh = dc.GetTextExtent(obj)
        dc.DrawText(obj, (w-ww)//2, (w-hh)//2)
        rgb = bytes(w * w * 3)
        dc.SelectObject(wx.NullBitmap)
        bmp.CopyToBuffer(rgb)
        a = memoryview(rgb[::3]).tolist()
        a = bytes([255-i for i in a])
        bmp = wx.Bitmap.FromBufferAndAlpha(w, w, rgb, a)
        bmp = bmp.ConvertToImage()
    if isinstance(obj, tuple): 
        bmp = wx.Image(1, 1, np.array(obj, dtype=np.uint8).tobytes())

    return bmp.Rescale(w, w).ConvertToBitmap()

def hot_key(txt):
    sep = txt.split('-')
    acc, code = wx.ACCEL_NORMAL, -1
    if 'Ctrl' in sep: acc|= wx.ACCEL_CTRL
    if 'Alt' in sep: acc|= wx.ACCEL_ALT
    if 'Shift' in sep: acc|= wx.ACCEL_SHIFT
    fs = ['F%d'%i for i in range(1,13)]
    if sep[-1] in fs:
        code = 340+fs.index(sep[-1])
    elif len(sep[-1])==1: code = ord(sep[-1])
    return acc, code

class RibbonBar(rb.RibbonBar):
    def __init__(self, app):
        rb.RibbonBar.__init__(self, app, wx.ID_ANY, wx.DefaultPosition, (-1, 140), rb.RIBBON_BAR_DEFAULT_STYLE|rb.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS )
        self.app = app.GetTopLevelParent()

    def parse(self, ks, vs, pt):
        if isinstance(vs, list):
            menu = wx.Menu()
            for kv in vs:
                if kv == '-': menu.AppendSeparator()
                else: self.parse(*kv, menu)
            pt.Append(1, ks, menu)
        else:
            item = wx.MenuItem(pt, -1, ks)
            f = lambda e, p=vs: p().start(self.app)
            self.Bind(wx.EVT_MENU, f, item)
            pt.Append(item)

    def parse(self, ks, vs, pt, short, rst):
        page = rb.RibbonPage( self, wx.ID_ANY, ks , wx.NullBitmap , 0 )
        panel = toolbar = None

        for kv1 in vs:
            if len(kv1) == 2:
                kv1 = (kv1[0], None, kv1[1])
            if kv1 == '-': continue
            pname = kv1[0] if isinstance(kv1[2], list) else '--'
            if panel is None and not isinstance(kv1[2], list):
                panel = rb.RibbonPanel( page, wx.ID_ANY, pname , make_logo(kv1[1] or kv1[0][0]), wx.DefaultPosition, wx.DefaultSize, rb.RIBBON_PANEL_DEFAULT_STYLE )
                toolbar = rb.RibbonButtonBar( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
            if not isinstance(kv1[2], list):
                btn = toolbar.AddSimpleButton( wx.NewId(), kv1[0], make_logo(kv1[1] or kv1[0][0]), wx.EmptyString)
                toolbar.Bind(rb.EVT_RIBBONBUTTONBAR_CLICKED, lambda e, p=kv1[2]:p().start(self.app), id=btn.id)
                self.GetParent().Bind(wx.EVT_MENU, lambda e, p=kv1[2]:p().start(self.app), id=btn.id)
                if kv1[0] in short: rst.append((short[kv1[0]], btn.id))

            else:
                panel = rb.RibbonPanel( page, wx.ID_ANY, pname , make_logo(kv1[1] or kv1[0][0]) , wx.DefaultPosition, wx.DefaultSize, rb.RIBBON_PANEL_DEFAULT_STYLE )
                toolbar = rb.RibbonButtonBar( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
                for kv2 in kv1[2]:
                    if len(kv2) == 2:
                        kv2 = (kv2[0], None, kv2[1])
                    if kv2 == '-': continue
                    btn = toolbar.AddSimpleButton( wx.NewId(), kv2[0], make_logo(kv2[1] or kv2[0][0]), wx.EmptyString)
                    toolbar.Bind(rb.EVT_RIBBONBUTTONBAR_CLICKED, lambda e, p=kv2[2]:p().start(self.app), id=btn.id)
                    self.GetParent().Bind(wx.EVT_MENU, lambda e, p=kv2[2]:p().start(self.app), id=btn.id)
                    if kv2[0] in short: rst.append((short[kv2[0]], btn.id))
                panel = toolbar = None
        self.Realize()

    def Append(self, id, item, menu):
        wx.MenuBar.Append(self, menu, item)
        
    def load(self, data, shortcut={}):
        rst = []
        for klv in data[1]:
            if len(klv) == 2:
                self.parse(klv[0], klv[1], self, shortcut, rst)
            else:
                self.parse(klv[0], klv[2], self, shortcut, rst)

        rst = [(*hot_key(i[0]), i[1]) for i in rst]
        return wx.AcceleratorTable(rst)

    def on_menu(self, event): 
        print('here')

    def clear(self):
        self._pages.clear()
        self._current_page = -1
        self.DestroyChildren()
        self.Realize()

if __name__ == '__main__':
    class P:
        def __init__(self, name):
            self.name = name

        def start(self, app):
            print(self.name)

        def __call__(self):
            return self
        
    data = ('menu', [
                ('File', None, [
                    ('Open CV', (255,0,0), P('O')),
                    '-',
                      ('Close', None, P('C'))]),
            ('Edit', None, [('Copy', None, P('C')),
                      ('A', None, [('B', None, P('B')),
                             ('C', None, P('C'))]),
                      ('Paste', P('P'))])])
    app = wx.App()
    frame = wx.Frame(None)
    menubar = RibbonBar(frame)
    acc = menubar.load(data, {'Open CV':'Ctrl-O'})
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add( menubar, 0, wx.ALL | wx.EXPAND, 0 )
    frame.SetSizer(sizer)
    frame.Show()
    app.MainLoop()

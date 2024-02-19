import wx, os
from sciapp.action import Free
from imagepy import root_dir
from imagepy.app import ShortcutManager

class VirtualListCtrl(wx.ListCtrl):
    def __init__(self, parent, title, data=[]):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL)
        self.title, self.data = title, data
        #self.Bind(wx.EVT_LIST_CACHE_HINT, self.DoCacheItems)
        for col, text in enumerate(title):
            self.InsertColumn(col, text)
        self.set_data(data)
        
    def OnGetItemText(self, row, col):
        return self.data[row][col]
        
    def OnGetItemAttr(self, item):  return None
        
    def OnGetItemImage(self, item): return -1
        
    def set_data(self, data):
        self.data = data
        self.SetItemCount(len(data))
        
    def refresh(self):
        self.SetItemCount(len(self.data))
        
class Plugin( wx.Panel ):
    title = 'Shortcut Editor'
    single = None

    def __init__( self, parent, app=None):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                            pos = wx.DefaultPosition, size = wx.Size( 500,300 ), 
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.app = app
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, "Search:", 
                                            wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer2.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.txt_search = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, 
                                       wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.txt_search, 1, wx.ALL, 5 )
        bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
        self.lst_plgs = VirtualListCtrl( self, ['Name', 'Shortcut'])
        self.lst_plgs.SetColumnWidth(0,200)
        self.lst_plgs.SetColumnWidth(1,200)
        bSizer1.Add( self.lst_plgs, 1, wx.ALL|wx.EXPAND, 5 )
        self.SetSizer( bSizer1 )
        self.Layout()
        self.Centre( wx.BOTH )
        # Connect Events
        self.txt_search.Bind( wx.EVT_TEXT, self.on_search )
        self.lst_plgs.Bind(wx.EVT_LIST_KEY_DOWN, self.on_run)
        self.lst_plgs.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.on_active)
        self.lst_plgs.Bind( wx.EVT_LIST_ITEM_SELECTED, self.on_select)
        
        self.load()
        self.active = -1
    
    #def list_plg(self, lst, items
    def load(self):
        lst = self.app.plugin_names()
        self.plgs = [[i, ShortcutManager.get(i)] for i in lst]
        for i in self.plgs:
            if i[1]==None:i[1]=''
        self.plgs.sort()
        self.buf = self.plgs
        self.lst_plgs.set_data(self.plgs)
    
    # Virtual event handlers, overide them in your derived class
    def on_search( self, event ):
        wd = self.txt_search.GetValue()
        self.buf = [i for i in self.plgs if wd.lower() in i[0].lower()]
        self.lst_plgs.set_data(self.buf)
        self.Refresh()

    def ist(self, cont, txt):
        sep = cont.split('-')
        if txt in sep: sep.remove(txt)
        else:sep.append(txt)
        cas = [i for i in ('Ctrl','Alt','Shift') if i in sep]
        sep = [i for i in sep if not i in cas]
        if len(sep)>0:cas.append(sep[-1])
        return '-'.join(cas)

    def on_active(self, event):
        self.active = event.GetIndex()

    def on_select(self, event):
        self.active = -1
        
    def on_run(self, event):
        if self.active != event.GetIndex():
            return self.app.alert('please double click to activate an item')
        code = event.GetKeyCode()
        title = self.buf[event.GetIndex()][0]
        txt = self.buf[event.GetIndex()][1]
        if code == wx.WXK_DELETE: txt = ''
        elif code == wx.WXK_CONTROL: 
            txt = self.ist(txt, 'Ctrl')
        elif code == wx.WXK_ALT: 
            txt = self.ist(txt, 'Alt')
        elif code == wx.WXK_SHIFT: 
            txt = self.ist(txt, 'Shift')
        elif code in range(340,352):
            fs = ['F'+str(i) for i in range(1,13)]
            txt = self.ist(txt, fs[code-340])
        elif code<100: 
            txt = self.ist(txt, chr(event.GetKeyCode()))
        if len(txt)>0 and txt[-1]=='-':txt=txt[:-1]
        self.buf[event.GetIndex()][1] = txt
        self.lst_plgs.RefreshItem(event.GetIndex())
        if txt!='': ShortcutManager.add(title, txt)
        #PluginsManager.plgs[self.buf[event.GetIndex()][0]]().start()
        
    def close(self):
        ShortcutManager.write(os.path.join(root_dir,'data/shortcut.json'))

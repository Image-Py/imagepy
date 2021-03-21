# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:01:14 2017

@author: yxl
"""
import wx, os, glob, shutil, random
from imagepy import root_dir
from sciwx.text import MDPad
from sciapp.action import Macros
#from imagepy.ui.mkdownwindow import HtmlPanel, md2html

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
        
def parse(path):
    f = open(path, encoding='utf-8')
    body = {'file':path}
    try:
        line = f.readline()
        if line[0] == '#':body['name'] = line.split('#')[-1].strip()
        while line:
            line = f.readline()
            if line.startswith('**Path:'): body['path'] = line.split('**')[-1].strip()
            if line.startswith('**Version:'): body['version'] = line.split('**')[-1].strip()
            if line.startswith('**Author:'): body['author'] = line.split('**')[-1].strip()
            if line.startswith('**Email:'): body['email'] = line.split('**')[-1].strip()
            if line.startswith('**Keyword:'): body['keyword'] = line.split('**')[-1].strip()
            if line.startswith('**Description'): body['Description'] = line.split('**')[-1].strip()
        f.close()
    except: body = [0]
    finally: f.close()
    return None if len(body)!=8 else body

class Plugin( wx.Panel ):
    title = 'Plugins Manager'
    single = None
    def __init__( self, parent, app=None):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, 
                            pos = wx.DefaultPosition, size = wx.Size( 600,300 ), 
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer( wx.HORIZONTAL)
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, "Search:", 
                                            wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.EXPAND, 5 )
        self.txt_search = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, 
                                       wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.txt_search, 1, wx.ALL, 5 )
        self.btn_update = wx.Button( self, wx.ID_ANY, 'Refresh List Online', wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
        bSizer2.Add( self.btn_update, 0, wx.ALL, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
        self.btn_install = wx.Button( self, wx.ID_ANY, 'Install/Update', wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
        self.btn_uninstall = wx.Button( self, wx.ID_ANY, 'Remove', wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
        self.chk_has = wx.CheckBox( self, wx.ID_ANY, 'only installed', wx.DefaultPosition, wx.DefaultSize, 0 )

        bSizer3.Add(self.chk_has, 0, wx.ALL|wx.EXPAND, 5)
        bSizer3.AddStretchSpacer(1)
        bSizer3.Add( self.btn_install, 0, wx.ALL, 5)
        bSizer3.Add( self.btn_uninstall, 0, wx.ALL, 5)
        bSizer1.Add( bSizer2, 0, wx.EXPAND, 5)
        self.lst_plgs = VirtualListCtrl( self, ['Name', 'Author', 'Version', 'Status'])
        self.lst_plgs.SetColumnWidth(0,100)
        self.lst_plgs.SetColumnWidth(1,100)
        self.lst_plgs.SetColumnWidth(2,60)
        self.lst_plgs.SetColumnWidth(3,60)
        self.htmlpanel = MDPad(self)
        bSizer1.Add( self.lst_plgs, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 5 )
        bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )
        sizer.Add(bSizer1, 0, wx.ALL|wx.EXPAND, 0)
        sizer.Add(self.htmlpanel, 1, wx.ALL|wx.EXPAND, 5 )

        self.SetSizer( sizer )
        self.Layout()
        self.Centre( wx.BOTH )
        # Connect Events
        self.txt_search.Bind( wx.EVT_TEXT, self.on_search)
        self.lst_plgs.Bind( wx.EVT_LIST_ITEM_SELECTED, self.on_run)
        self.btn_update.Bind(wx.EVT_BUTTON, self.on_update)
        self.btn_install.Bind(wx.EVT_BUTTON, self.on_install)
        self.btn_uninstall.Bind(wx.EVT_BUTTON, self.on_remove)
        self.chk_has.Bind( wx.EVT_CHECKBOX, self.on_check)
        self.app = app
        self.load()
    
    #def list_plg(self, lst, items
    def load(self):
        here = os.path.abspath(os.path.dirname(__file__))
        has = glob.glob(os.path.join(root_dir,'plugins/*/*.md'))
        fs = glob.glob(here+'/Contributions/*.md')
        prjs = [p for p in [parse(i) for i in fs] if not p is None]
        has = [p for p in [parse(i) for i in has] if not p is None]
        keys = set([i['path'] for i in prjs])
        for i in has:
            if not i['path'] in keys: prjs.append(i)
        prjs = sorted([(i['name']+str(random.random()), i) for i in prjs])
        self.prjs = [i[1] for i in prjs]

        for i in self.prjs:
            for j in has:
                if i['path'] == j['path']:
                    i['old'] = j['version']
                    i['folder'] = os.path.split(j['file'])[0]
        self.on_search(None)
    
    # Virtual event handlers, overide them in your derived class
    def on_search( self, event ):
        wd = self.txt_search.GetValue()
        f = lambda x:  '' if not 'old' in x else ['update', 'installed'][x['old']==x['version']]
        self.buf = [[i['name'], i['author'], i['version'], f(i), i]
            for i in self.prjs if wd.lower() in str(i).lower()]
        if self.chk_has.GetValue(): self.buf = [i for i in self.buf if i[3]!='']
        self.lst_plgs.set_data(self.buf)
        self.lst_plgs.Refresh()
        
    def on_update(self, event):
        Macros('', ['Update Plugins List>None']).start(self.app, callafter=self.load)

    def on_run(self, event):
        f = open(self.buf[event.GetIndex()][-1]['file'], encoding='utf-8')
        cont = f.read()
        f.close()
        cont = '\n'.join([i.strip() for i in cont.split('\n')])
        self.htmlpanel.set_cont(cont)

    def on_install(self, event):
        i = self.lst_plgs.GetFirstSelected()
        if i==-1: return
        path = self.buf[i][-1]['path']
        self.app.plugin_manager.get('Install Plugins').para['repo'] = path
        self.app.plugin_manager.get('Install Plugins')().start(
            self.app, None, self.load)

    def on_remove(self, event):
        i = self.lst_plgs.GetFirstSelected()
        if i==-1: return
        shutil.rmtree(self.buf[i][-1]['folder'])
        self.app.load_all()
        self.load()

    def on_check(self, event): self.load()

if __name__ == '__main__':
    from glob import glob
    fs = glob('Contributions/*.md')
    for i in fs: print(parse(i))
# -*- coding: utf-8 -*-
# ConfigPanel used for parameters setting
import wx, platform
from ..core.manager import ImageManager, WindowsManager, TableManager
from .widgets import *

widgets = { 'ctrl':None, 'slide':FloatSlider, int:NumCtrl,
            float:NumCtrl, 'lab':Label, bool:Check, str:TextCtrl, 
            list:Choice, 'img':ImageList, 'color':ColorCtrl, 
            'any':AnyType, 'chos':Choices, 'fields':TableFields,
            'hist':HistCanvas}

class ParaDialog (wx.Dialog):
    def __init__( self, parent, title):
        wx.Dialog.__init__ (self, parent, -1, title, style = wx.DEFAULT_DIALOG_STYLE)
        self.lst = wx.BoxSizer( wx.VERTICAL )
        self.tus = []

        self.on_ok, self.on_cancel = None, None
        self.ctrl_dic = {}
        boxBack = wx.BoxSizer()
        boxBack.Add(self.lst, 0, wx.ALL, 10)
        self.SetSizer( boxBack )
        self.Layout()
        self.handle = self.handle_

    def commit(self, state):
        self.Destroy()
        if state=='ok' and self.on_ok:self.on_ok()
        if state=='cancel' and self.on_cancel:self.on_cancel()

    def add_confirm(self, modal=True):
        self.lst.AddStretchSpacer(1)
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.btn_OK = wx.Button( self, wx.ID_OK, 'OK')
        sizer.Add( self.btn_OK, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.btn_cancel = wx.Button( self, wx.ID_CANCEL, 'Cancel')
        sizer.Add( self.btn_cancel, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
        self.lst.Add(sizer, 0, wx.ALIGN_RIGHT, 5 )
        if not modal:
            self.btn_OK.Bind( wx.EVT_BUTTON, lambda e:self.commit('ok'))
            self.btn_cancel.Bind( wx.EVT_BUTTON, lambda e:self.commit('cancel'))

    def init_view(self, items, para, preview=False, modal = True):
        self.para = para
        for item in items:
            self.add_ctrl_(widgets[item[0]], item[1], item[2:])
        if preview:self.add_ctrl_(Check, 'preview', ('preview',))
        self.reset(para)
        self.add_confirm(modal)
        self.pack()

    def parse(self, para) :
        self.add_ctrl_(widgets[para[0]], *para[1:])
        #self.funcs[para[0]](*para[1:])
    '''
    def add_ctrl(self, key, ctrl):
        self.lst.Add( ctrl, 0, wx.EXPAND, 5 )
        if not key is None:
            self.ctrl_dic[key] = ctrl
            if hasattr(ctrl, 'set_handle'):
                ctrl.set_handle(lambda x=None : self.para_changed(key))
    '''

    def add_ctrl_(self, Ctrl, key, p):
        ctrl = Ctrl(self, *p)
        if not p[0] is None: self.ctrl_dic[key] = ctrl
        if hasattr(ctrl, 'Bind'):
            ctrl.Bind(None, lambda x : self.para_changed(key))
        pre = ctrl.prefix if hasattr(ctrl, 'prefix') else None
        post = ctrl.postfix if hasattr(ctrl, 'postfix') else None
        self.tus.append((pre, post))
        self.lst.Add( ctrl, 0, wx.EXPAND, 0 )

    def pack(self):
        self.Layout()
        mint, minu = [], []
        for t,u in self.tus:
            if not t is None: mint.append(t.GetSize()[0])
            if not u is None:minu.append(u.GetSize()[0])
        for t,u in self.tus:
            if not t is None:t.SetInitialSize((max(mint),-1))
            if not u is None:u.SetInitialSize((max(minu),-1))
        self.Fit()

    def para_check(self, para, key):pass

    def para_changed(self, key):

        para = self.para
        for p in list(para.keys()):
            if p in self.ctrl_dic:
                para[p] = self.ctrl_dic[p].GetValue()
        
        sta = sum([i is None for i in list(para.values())])==0
        self.btn_OK.Enable(sta)
        if not sta: return
        self.para_check(para, key)
        if 'preview' not in self.ctrl_dic:return
        if not self.ctrl_dic['preview'].GetValue():return
        self.handle(para)

    def reset(self, para=None):
        if para!=None:self.para = para
        #print(para, '====')
        for p in list(self.para.keys()):
            if p in self.ctrl_dic:
                self.ctrl_dic[p].SetValue(self.para[p])

    def get_para(self):
        return self.para

    def set_handle(self, handle):
        self.handle = handle
        if handle==None: self.handle = self.handle_

    def handle_(self, para):
        print(para)

    def __del__( self ):
        pass

if __name__ == '__main__':
    view = [(float, 'r', (0,20), 1, '半径', 'mm'),
            ('slide', 'mm', (-20,20), '亮度', 'slide'),
            ('color', 'color', '颜色', 'rgb'),
            (bool, 'preview', 'preview')]
    data = {'r':1.2, 'slide':0,  'preview':True, 'color':(0,255,0)}

    app = wx.PySimpleApp()
    pd = ParaDialog(None, 'Test')
    pd.init_view(view, para)
    pd.pack()
    pd.ShowModal()
    app.MainLoop()
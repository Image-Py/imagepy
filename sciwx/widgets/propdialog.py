#!/usr/bin/env python

import sys, time, math, os.path

import wx, wx.adv
import wx.propgrid as wxpg

from six import exec_
_ = wx.GetTranslation

class GridDialog( wx.Dialog ):

    def __init__( self, parent, title):
        wx.Dialog.__init__ (self, parent, -1, title, style = wx.DEFAULT_DIALOG_STYLE, size = wx.Size((300, 480)))
        # wx.Panel.__init__(self, parent, wx.ID_ANY)

    def commit(self, state):
        self.Destroy()
        if state=='ok' and self.on_ok:self.on_ok()
        if state=='cancel' and self.on_cancel:self.on_cancel()

    def add_confirm(self, modal):
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(self, wx.ID_OK, "OK")
        rowsizer.Add(but,1)
        #but.Bind( wx.EVT_BUTTON, self.OnGetPropertyValues )
        but = wx.Button(self, wx.ID_CANCEL,"Cancel")
        rowsizer.Add(but,1)
        if not modal:
            self.btn_ok.Bind( wx.EVT_BUTTON, lambda e:self.commit('ok'))
            self.btn_cancel.Bind( wx.EVT_BUTTON, lambda e:self.commit('cancel'))
        self.GetSizer().Add(rowsizer,0,wx.EXPAND)

    def init_view(self, items, para, preview=False, modal=True, app=None):
        self.para, self.modal = para, modal
        self.pg = pg = wxpg.PropertyGridManager(self, style=wxpg.PG_SPLITTER_AUTO_CENTER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # Show help as tooltips
        pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)
        pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        pg.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )

        pg.AddPage('')
        for i in items:
            if i[0] == 'lab': pg.Append(wxpg.PropertyCategory(i[2]))
            if i[0] == int: pg.Append( wxpg.IntProperty(i[1], value=int(para[i[1]]) or 0))
            if i[0] == float: pg.Append( wxpg.FloatProperty(i[1], value=float(para[i[1]]) or 0))
            if i[0] == str: pg.Append( wxpg.StringProperty(i[1], value=para[i[1]] or ''))
            if i[0] == 'txt': pg.Append( wxpg.LongStringProperty(i[1], value=para[i[1]] or ''))
            if i[0] == bool: pg.Append( wxpg.BoolProperty(i[1]))
            if i[0] == 'date': pg.Append( wxpg.DateProperty(i[1], value=wx.DateTime.Now()))
            #if i[0] == 'list': pg.Append( wxpg.EnumProperty(i[1], i[1], [i.strip() for i in i[2][1:-1].split(',')]))
            #if i[0] == 'img': pg.Append( wxpg.EnumProperty(v[1], v[1], ['a','b','c']))
            #if i[0] == 'tab': pg.Append( wxpg.EnumProperty(v[1], v[1], ['a','b','c']))

        #if preview:self.add_ctrl_(Check, 'preview', ('preview',), app=app)
        #self.reset(para)
        sizer.Add(pg, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.add_confirm(modal)
        self.Layout()
        self.Fit()
        wx.Dialog.Bind(self, wx.EVT_WINDOW_DESTROY, self.OnDestroy)
        #wx.Dialog.Bind(self, wx.EVT_IDLE, lambda e: self.reset())
        print('bind close')

    def OnDestroy( self, event ):
        self.handle = print
        self.on_cancel = self.on_ok = self.on_help = None
        del self.ctrl_dic

    def GetValue(self):
        return self.pg.GetPropertyValues(as_strings=True)

    def OnGetPropertyValues(self,event):
        para = self.pg.GetPropertyValues(inc_attributes=True)

    def OnPropGridChange(self, event):
        p = event.GetProperty()
        if p: print('%s changed to "%s"\n' % (p.GetName(),p.GetValueAsString()))

    def OnPropGridSelect(self, event):
        p = event.GetProperty()
        if p: self.txt_info.SetValue('%s: %s'%(p.GetName(), self.key[p.GetName()][3]))

if __name__ == '__main__':
    app = wx.App(False)

    para = {'sid':'001', 'name':'yxl', 'Date':None, 'age':5}
    view = [('lab', None, 'Label1'),
            (str, 'sid', 'Sample_ID'),
            (str, 'name', 'Operator_Name'),
            ('lab', None, 'Label2'),
            (int, 'age', 'Your Age')]

    frame = GridDialog(None, 'Property Grid')
    frame.init_view(view, para)
    rst = frame.ShowModal() == wx.ID_OK
    app.MainLoop()
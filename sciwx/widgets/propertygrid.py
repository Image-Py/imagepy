#!/usr/bin/env python

import sys, time, math, os.path

import wx, wx.adv
import wx.propgrid as wxpg

from six import exec_
_ = wx.GetTranslation

data = [('Sheet1', [((4, 5), ['str', 'Sample_ID', '5', "image's name"]), ((4, 17), ['str', 'Operator_Name', None, 'your name']), ((4, 30), ['date', 'Date', None, 'today']), ((10, 1), ['img', 'Original_Image', '[8.16,5.76,0.9,0]', 'the original image']), ((10, 20), ['img', 'Mask_Image', '[8.16,5.76,0.9,0]', '']), ((28, 1), ['tab', 'Record', '[1,3,0,0]', 'records'])]), ('Sheet2', [((0,0), ['list', 'a', '[1,2,345]', 'nothing'])]), ('Sheet3', [])]
key = {'Sample_ID': ['str', 'Sample_ID', '5', "image's name"], 'Operator_Name': ['str', 'Operator_Name', None, 'your name'], 'Date': ['date', 'Date', None, 'today'], 'Original_Image': ['img', 'Original_Image', '[8.16,5.76,0.9,0]', 'the original image'], 'Mask_Image': ['img', 'Mask_Image', '[8.16,5.76,0.9,0]', ''], 'Record': ['tab', 'Record', '[1,3,0,0]', 'records']}

class GridDialog( wx.Dialog ):

    def __init__( self, parent, title, tree, key):
        wx.Dialog.__init__ (self, parent, -1, title, style = wx.DEFAULT_DIALOG_STYLE, size = wx.Size((300, 480)))
        # wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.app = parent

        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)

        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = pg = wxpg.PropertyGridManager(panel,
                        style=wxpg.PG_SPLITTER_AUTO_CENTER)

        # Show help as tooltips
        pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

        pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        pg.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )

        pg.AddPage('Page 1')
        self.key = key
        for page in tree:
            pg.Append(wxpg.PropertyCategory(page[0]))
            for item in page[1]:
                v = item[1]
                if v[0] == 'int': pg.Append( wxpg.IntProperty(v[1], value=int(v[2]) or 0))
                if v[0] == 'float': pg.Append( wxpg.FloatProperty(v[1], value=float(v[2]) or 0))
                if v[0] == 'str': pg.Append( wxpg.StringProperty(v[1], value=v[2] or ''))
                if v[0] == 'txt': pg.Append( wxpg.LongStringProperty(v[1], value=v[2] or ''))
                if v[0] == 'bool': pg.Append( wxpg.BoolProperty(v[1]))
                if v[0] == 'date': pg.Append( wxpg.DateProperty(v[1], value=wx.DateTime.Now()))
                if v[0] == 'list': pg.Append( wxpg.EnumProperty(v[1], v[1], [i.strip() for i in v[2][1:-1].split(',')]))
                if v[0] == 'img': pg.Append( wxpg.EnumProperty(v[1], v[1], self.app.img_names()))
                if v[0] == 'tab': pg.Append( wxpg.EnumProperty(v[1], v[1], self.app.table_names()))

        topsizer.Add(pg, 1, wx.EXPAND)
        self.txt_info = wx.TextCtrl( self, wx.ID_ANY, 'information', wx.DefaultPosition, wx.Size(80, 80), wx.TE_MULTILINE|wx.TRANSPARENT_WINDOW )
        topsizer.Add(self.txt_info, 0, wx.EXPAND|wx.ALL, 0)
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(panel, wx.ID_OK, "OK")
        rowsizer.Add(but,1)
        #but.Bind( wx.EVT_BUTTON, self.OnGetPropertyValues )
        but = wx.Button(panel, wx.ID_CANCEL,"Cancel")
        rowsizer.Add(but,1)
        topsizer.Add(rowsizer,0,wx.EXPAND)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

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
    frame = GridDialog(None, 'Property Grid', data, key)
    rst = frame.ShowModal() == wx.ID_OK
    app.MainLoop()
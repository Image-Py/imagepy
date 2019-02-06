#!/usr/bin/env python

import sys, time, math, os.path

import wx, wx.adv
import wx.propgrid as wxpg

from six import exec_
_ = wx.GetTranslation

from imagepy.core.manager import ImageManager, TableManager

data = [('Sheet1', [((2, 2), ['img', 'me']), ((2, 7), ['str', 'name']), ((3, 7), 
        ['int', 'age']), ((4, 7), ['float', 'weight']), ((5, 7), ['bool', 'married']), ((6, 7), 
        ['date', 'birth']), ((7, 7), ['list', 'sex', 'male,female']), ((8, 7), ['txt', 'info']), ((11, 2), 
        ['tab', 'score'])]), ('Sheet2', [((2, 2), ['txt', 'xyz'])]), ('Sheet3', [])]

class GridDialog( wx.Dialog ):

    def __init__( self, parent, title, data):
        wx.Dialog.__init__ (self, parent, -1, title, style = wx.DEFAULT_DIALOG_STYLE, size = wx.Size((300, 480)))
        # wx.Panel.__init__(self, parent, wx.ID_ANY)

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
        for page in data:
            pg.Append(wxpg.PropertyCategory(page[0]))
            for item in page[1]:
                v = item[1]
                if v[0] == 'int': pg.Append( wxpg.IntProperty(v[1]))
                if v[0] == 'float': pg.Append( wxpg.FloatProperty(v[1]))
                if v[0] == 'str': pg.Append( wxpg.StringProperty(v[1]))
                if v[0] == 'txt': pg.Append( wxpg.LongStringProperty(v[1]))
                if v[0] == 'bool': pg.Append( wxpg.BoolProperty(v[1]))
                if v[0] == 'date': pg.Append( wxpg.DateProperty(v[1], value=wx.DateTime.Now()))
                if v[0] == 'list': pg.Append( wxpg.EnumProperty(v[1], v[1], v[2].split(',')))
                if v[0] == 'img': pg.Append( wxpg.EnumProperty(v[1], v[1], ImageManager.get_titles()))
                if v[0] == 'tab': pg.Append( wxpg.EnumProperty(v[1], v[1], TableManager.get_titles()))

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
        if p: self.txt_info.SetValue('%s selected\n' % (p.GetName()))

if __name__ == '__main__':
    app = wx.App(False)
    frame = GridDialog(None, 'Property Grid', data)
    rst = frame.ShowModal() == wx.ID_OK
    print(rst)
    app.MainLoop()
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 00:28:59 2016

@author: yxl
"""

import wx, os
import wx.grid
from ..core.manager import TableLogManager
from .. import IPy, root_dir

class GenericTable(wx.grid.GridTableBase):
    """GenericTable: derived from wx.grid.GridTableBase"""
    def __init__(self, data, colLabels=None, rowLabels=None):
        wx.grid.GridTableBase.__init__(self)
        self.data = data # data is stored as a list of list 
        self.rowLabels = rowLabels
        self.colLabels = colLabels
        
    def GetNumberRows(self):
        return len(self.data)
        
    def GetNumberCols(self):
        return len(self.data[0])
        
    def GetColLabelValue(self, col):
        return self.colLabels[col] if self.colLabels else chr(65+col)
    
    def GetRowLabelValue(self, row):
        return  str(self.rowLabels[row]) if self.rowLabels else str(row+1)
            
    def IsEmptyCell(self, row, col):
        return row < len(self.data) and col < len(self.data[0])
            
    def GetValue(self, row, col):
        return str(self.data[row][col])
        
    def SetValue(self, row, col, value):
        # self.data[row][col] = value
        pass      
        
class TableLog(wx.Frame): 
    """TableLog: derived from wx.core.Frame"""
    @classmethod
    def table(cls, title, data, cols=None, rows=None):
        cls(IPy.curapp, TableLogManager.name(title), data, cols, rows).Show()
        
    def __init__(self, parent, title, data, cols=None, rows=None):
        wx.Frame.__init__(self, parent, -1, title)
        logopath = os.path.join(root_dir, 'data/logo.ico')
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        self.SetIcon(wx.Icon(logopath, wx.BITMAP_TYPE_ICO))
        TableLogManager.add(title, self)
        self.data, self.cols, self.rows = data, cols, rows
        tableBase = GenericTable(data, cols, rows)
        self.grid = wx.grid.Grid(self)
        
        ## create tablegrid and set tablegrid value 
        #self.grid.SetTable(tableBase)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.grid.CreateGrid(len(data), len(data[0]))
        if cols!=None:
            for i in range(len(cols)):
                self.grid.SetColLabelValue(i, cols[i])
        if rows!=None:
            for i in range(len(rows)):
                self.grid.SetColLabelValue(i, rows[i])
        for i in range(len(data)):
            for j in range(len(data[0])):
                self.grid.SetCellValue(i, j,str(data[i][j]))
        self.grid.AutoSize()
        
        ## create menus
        menus = [('File(&F)',
                  [('Save as tab', self.OnSaveTab),
                   ('Save as csv', self.OnSaveCsv),
                   ('-'),
                   ('Exit', self.OnClose)
                   ]
                  ),                 
                 ('Help(&H)', 
                  [('About', self.OnAbout)]
                  )
                 ]
        
        ## bind the menus with the correspond events 
        menuBar=wx.MenuBar()
        for menu in menus:
            m = wx.Menu()
            for item in menu[1]:
                if item[0]=='-':
                    m.AppendSeparator()
                else:
                    i = m.Append(-1, item[0])
                    if item[1]!=None:
                        self.Bind(wx.EVT_MENU,item[1], i)
            menuBar.Append(m,menu[0])
        self.SetMenuBar(menuBar) 
        self.Fit()
        
    def save_tab(self, tablepath, sep):
        with open(tablepath,"w") as f:
            f.write(sep.join([str(col) for col in self.cols])+'\n')
            for line in self.data:
                f.write(sep.join([str(item) for item in line])+'\n')

    def _OnSave(self,typename="Csv",sep=","):
        dialog=wx.FileDialog(self,typename,style=wx.FD_SAVE)
        if dialog.ShowModal()==wx.ID_OK:
            self.file=dialog.GetPath()
            self.save_tab(self.file, sep)
        dialog.Destroy()
        
    def OnSaveTab(self,event):
        self._OnSave(typename="Tab", sep="\t")
        
    def OnSaveCsv(self,event):
        self._OnSave(typename="Csv", sep=",")
        
    def OnClose(self,event):
        TableLogManager.close(self.GetTitle())
        self.Destroy()
        
    def OnAbout(self,event):
        wx.MessageBox('Table Log Window!','About',wx.OK)
        
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    TableLog.table('abc',[(1,2),(3,4)],('a','b'))
    TableLog.table('abc',[(1,2),(3,4)],('a','b'))
    app.MainLoop()

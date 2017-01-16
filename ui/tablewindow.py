# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 00:28:59 2016

@author: yxl
"""

import wx
import wx.grid
from core.managers import TableLogManager
import IPy

class GenericTable(wx.grid.PyGridTableBase):
    def __init__(self, data, colLabels=None, rowLabels=None):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.rowLabels = rowLabels
        self.colLabels = colLabels
        
    def GetNumberRows(self):
        return len(self.data)
        
    def GetNumberCols(self):
        return len(self.data[0])
        
    def GetColLabelValue(self, col):
        if self.colLabels:
            return self.colLabels[col]
        else: return chr(65+col)
        
    def GetRowLabelValue(self, row):
        if self.rowLabels:
            return self.rowLabels[row]
        else: return row + 1
            
    def IsEmptyCell(self, row, col):
            return False
            
    def GetValue(self, row, col):
        return self.data[row][col]
        
    def SetValue(self, row, col, value):
        pass      
        
class TableLog(wx.Frame): 
    @classmethod
    def table(cls, title, data, cols=None, rows=None):
        cls(IPy.curapp, TableLogManager.name(title), data, cols, rows).Show()
        
    def __init__(self, parent, title, data, cols=None, rows=None):
        wx.Frame.__init__(self, parent, -1, title)
        TableLogManager.add(title, self)
        self.data, self.cols, self.rows = data, cols, rows
        tableBase = GenericTable(data, cols, rows)
        self.grid = wx.grid.Grid(self)
        self.grid.SetTable(tableBase)
        self.grid.AutoSize()
        
        menus = [('File(&F)',[
            ('Save as tab', self.OnSaveTab),
            ('Save as csv', self.OnSaveCsv),
            ('-'),
            ('Exit', self.OnClose)]),
            ('Help(&H)', [
            ('About', self.OnAbout)])]
        
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
        
    def save_tab(self, path, sep):
        f = open(path, 'w')
        f.write(sep.join([str(i) for i in self.cols])+'\r\n')
        for line in self.data:
            f.write(sep.join([str(i) for i in line])+'\r\n')
        f.close()
        
    def OnSaveTab(self,event):
        dialog=wx.FileDialog(self,'Tab',style=wx.SAVE)
        if dialog.ShowModal()==wx.ID_OK:
            self.file=dialog.GetPath()
            self.save_tab(self.file, '\t')
        dialog.Destroy()

    def OnSaveCsv(self,event):
        dialog=wx.FileDialog(self,'Csv',style=wx.SAVE)
        if dialog.ShowModal()==wx.ID_OK:
            self.file=dialog.GetPath()
            self.save_tab(self.file, '\r/n')
        dialog.Destroy()
        
    def OnClose(self,event):
        self.Destroy()
        
    def OnAbout(self,event):
        wx.MessageBox('Table Log Window!','ImagePy',wx.OK)
        
    def OnClosing(self, event):
        TableLogManager.close(self.title)
        event.Skip()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    TableLog.table('abc',[(1,2),(3,4)],('a','b'))
    TableLog.table('abc',[(1,2),(3,4)],('a','b'))
    app.MainLoop()
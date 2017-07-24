# -*- coding: utf-8 -*-
import wx, os
from .. import IPy, root_dir
from ..core.manager import TextLogManager

class TextLog(wx.Frame):
    """TexLog:derived from wx.core.Frame"""
    @classmethod
    def write(cls, cont, title='ImagePy TexLog'):
        if title not in TextLogManager.windows:
            win = cls(title)
            win.Show()
        TextLogManager.windows[title].append(cont)
    
    def __init__(self, title='ImagePy TexLog'):
        wx.Frame.__init__(self, IPy.curapp,title=title,size=(500,300))
        logopath = os.path.join(root_dir, 'data/logo.ico')
        self.SetIcon(wx.Icon(logopath, wx.BITMAP_TYPE_ICO))
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        self.title = title
        TextLogManager.add(title, self)
        self.file=''
        
        ### Create menus (name:event) k-v pairs 
        menus = [
                ## File 
                ('File(&F)',[('Open', self.OnOpen),
                             ('Save', self.OnSave),
                             ('Save as', self.OnSaveAs),
                             ('-'),
                             ('Exit', self.OnClose)
                             ]),
                ## Edit 
                ('Edit(&E)', [ ('Undo', self.OnUndo),
                             ('Redo', self.OnRedo),
                             ('-'),
                             ('Cut', self.OnCut),
                             ('Copy', self.OnCopy),
                             ('Paste', self.OnPaste),
                             ('-'),
                             ('All', self.OnSelectAll)
                             ]),               
                ## Help 
                ('Help(&H)', [('About', self.OnAbout)])
        ]
        
        ### Bind menus with the corresponding events 
        self.menuBar=wx.MenuBar()
        for menu in menus:
            m = wx.Menu()
            for item in menu[1]:
                if item[0]=='-':
                    m.AppendSeparator()
                else:
                    i = m.Append(-1, item[0])
                    self.Bind(wx.EVT_MENU,item[1], i)
            self.menuBar.Append(m,menu[0])
        self.SetMenuBar(self.menuBar) 
        self.Bind(wx.EVT_CLOSE, self.OnClosing)
        
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.text= wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, 
                                wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        sizer.Add( self.text, 1, wx.ALL|wx.EXPAND, 1 )
        self.SetSizer( sizer )
        
        self.Bind(wx.EVT_RIGHT_DOWN,self.OnRClick)

    def OnOpen(self,event):
        dialog=wx.FileDialog(None,'wxpython Notebook(o)',style=wx.FD_OPEN)
        if dialog.ShowModal()==wx.ID_OK:
            self.file=dialog.GetPath()
            file=open(self.file)
            self.text.write(file.read())
            file.close()
        dialog.Destroy()

    def OnSave(self,event):
        if self.file=='':
            dialog=wx.FileDialog(None,'wxpython Notebook(s)',style=wx.FD_SAVE)
            if dialog.ShowModal()==wx.ID_OK:
                self.file=dialog.GetPath()
                self.text.SaveFile(self.file)
            dialog.Destroy()
        else:
            self.text.SaveFile(self.file)

    def OnSaveAs(self,event):
        dialog=wx.FileDialog(None,'wxpython notebook',style=wx.FD_SAVE)
        if dialog.ShowModal()==wx.ID_OK:
            self.file=dialog.GetPath()
            self.text.SaveFile(self.file)
        dialog.Destroy()

    def OnClose(self,event):
        self.Destroy()
        
    def OnClosing(self, event):
        TextLogManager.close(self.title)
        event.Skip()

    def OnAbout(self,event):
        wx.MessageBox('Text Log Window!','ImagePy',wx.OK)

    def OnRClick(self,event):
        pos=(event.GetX(),event.GetY())
        self.panel.PopupMenu(self.menu.edit,pos)

    def OnUndo(self,event): self.text.Undo()

    def OnRedo(self,event): self.text.Redo()

    def OnCut(self,event): self.text.Cut()

    def OnCopy(self,event): self.text.Copy()

    def OnPaste(self,event): self.text.Paste()

    def OnSelectAll(self,event): self.text.SelectAll()
        
    def append(self, cont):
        self.text.AppendText(cont+'\r\n')
        
if __name__ == '__main__':
    app=wx.App(False)
    win = TextLog()
    win.Show()
    win.append('abc')
    app.MainLoop()
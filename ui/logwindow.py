# -*- coding: utf-8 -*-
import wx     
import IPy   
from core.manager import TextLogManager

class TextLog(wx.Frame):
    @classmethod
    def write(cls, cont, title='ImagePy'):
        if title not in TextLogManager.windows:
            win = cls(title)
            win.Show()
        TextLogManager.windows[title].append(cont)
    
    def __init__(self, title='ImagePy Log'):
        wx.Frame.__init__(self, IPy.curapp,title=title,size=(500,300))
        self.title = title
        TextLogManager.add(title, self)
        self.file=''
        
        menus = [('File(&F)',[
            ('Open', self.OnOpen),
            ('Save', self.OnSave),
            ('Save as', self.OnSaveAs),
            ('-'),
            ('Exit', self.OnClose)]),
                ('Edite(&E)', [
            ('Undo', self.OnUndo),
            ('Redo', self.OnRedo),
            ('-'),
            ('Cut', self.OnCut),
            ('Copy', self.OnCopy),
            ('Paste', self.OnPaste),
            ('-'),
            ('All', self.OnSelectAll)]),
                ('Help(&H)', [
            ('About', self.OnAbout)])]
        
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
        self.text= wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        sizer.Add( self.text, 1, wx.ALL|wx.EXPAND, 1 )
        self.SetSizer( sizer )
        
        self.Bind(wx.EVT_RIGHT_DOWN,self.OnRClick)

    def OnOpen(self,event):
        dialog=wx.FileDialog(None,'wxpython Notebook',style=wx.FD_OPEN)
        if dialog.ShowModal()==wx.ID_OK:
            self.file=dialog.GetPath()
            file=open(self.file)
            self.text.write(file.read())
            file.close()
        dialog.Destroy()

    def OnSave(self,event):
        if self.file=='':
            dialog=wx.FileDialog(None,'wxpython Notebook',style=wx.FD_SAVE)
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
import wx, wx.lib.agw.aui as aui

class TextPad(wx.Panel):
    def __init__(self, parent, cont='', title='no name'):
        wx.Panel.__init__(self, parent, size=(500,300))
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        self.title = title
        
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.text= wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, 
                                wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        self.text.SetValue(cont)
        sizer.Add( self.text, 1, wx.ALL|wx.EXPAND, 1 )
        self.SetSizer( sizer )
        self.Bind(wx.EVT_RIGHT_DOWN,self.OnRClick)
        self.set_cont = self.text.SetValue

    def OnOpen(self,event):
        dialog=wx.FileDialog(self,'wxpython Notebook(o)',style=wx.FD_OPEN)
        if dialog.ShowModal()==wx.ID_OK:
            self.title=dialog.GetPath()
            title=open(self.title)
            self.text.write(title.read())
            title.close()
        dialog.Destroy()

    def OnSave(self,event):
        if self.title=='':
            dialog=wx.FileDialog(self,'wxpython Notebook(s)',style=wx.FD_SAVE)
            if dialog.ShowModal()==wx.ID_OK:
                self.filtitlee=dialog.GetPath()
                self.text.SaveFile(self.title)
            dialog.Destroy()
        else:
            self.text.SaveFile(self.fititlele)

    def OnSaveAs(self,event):
        dialog=wx.FileDialog(self,'wxpython notebook',style=wx.FD_SAVE)
        if dialog.ShowModal()==wx.ID_OK:
            self.title=dialog.GetPath()
            self.text.SaveFile(self.title)
        dialog.Destroy()

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

class TextFrame(wx.Frame):    
    def __init__(self, parent, title='no name', cont=''):
        wx.Frame.__init__(self, parent, title=title, size=(500,300))
        self.title = title
        self.textpad = TextPad(self, cont, title)
        self.append = self.textpad.append
        ### Create menus (name:event) k-v pairs 
        menus = [
                ## File 
                ('File(&F)',[('Open', self.textpad.OnOpen),
                             ('Save', self.textpad.OnSave),
                             ('Save as', self.textpad.OnSaveAs),
                             ('-'),
                             ('Exit', self.OnClose)
                             ]),
                ## Edit 
                ('Edit(&E)', [ ('Undo', self.textpad.OnUndo),
                             ('Redo', self.textpad.OnRedo),
                             ('-'),
                             ('Cut', self.textpad.OnCut),
                             ('Copy', self.textpad.OnCopy),
                             ('Paste', self.textpad.OnPaste),
                             ('-'),
                             ('All', self.textpad.OnSelectAll)
                             ]),               
                ## Help 
                ('Help(&H)', [('About', self.textpad.OnAbout)])
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

    def OnClose(self,event):
        self.Destroy()
        
    def OnClosing(self, event):
        event.Skip()
        
class TextNoteBook(wx.lib.agw.aui.AuiNotebook):
    def __init__(self, parent):
        wx.lib.agw.aui.AuiNotebook.__init__( self, parent, wx.ID_ANY, 
            wx.DefaultPosition, wx.DefaultSize, wx.lib.agw.aui.AUI_NB_DEFAULT_STYLE )
        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_valid) 
        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        self.Bind( wx.EVT_IDLE, self.on_idle)
        self.SetArtProvider(aui.AuiSimpleTabArt())
        
    def on_idle(self, event):
        for i in range(self.GetPageCount()):
            title = self.GetPage(i).title
            if self.GetPageText(i) != title:
                self.SetPageText(i, title)

    def textpad(self, i=None):
        if not i is None: return self.GetPage(i)
        else: return self.GetCurrentPage()
        
    def set_background(self, img):
        self.GetAuiManager().SetArtProvider(ImgArtProvider(img))

    def add_page(self, textpad=None):
        if textpad is None: textpad = TextPad(self)
        self.AddPage(textpad, 'Text', True, wx.NullBitmap )
        return textpad

    def set_title(self, panel, title):
        self.SetPageText(self.GetPageIndex(panel), title)

    def on_valid(self, event): pass

    def on_close(self, event): pass

class TextNoteFrame(wx.Frame):
    def __init__(self, parent, title='TextPadBookFrame'):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                            title = title,
                            pos = wx.DefaultPosition,
                            size = wx.Size( 500, 500 ),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = TextNoteBook(self)
        self.textpad = self.notebook.textpad
        sizer.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 0 )
        self.SetSizer(sizer)
        self.add_notepad = self.notebook.add_notepad
        self.Layout()

        ### Create menus (name:event) k-v pairs 
        menus = [
                ## File 
                ('File(&F)',[('Open', lambda e: self.textpad().OnOpen(e)),
                             ('Save', lambda e: self.textpad().OnSave(e)),
                             ('Save as', lambda e: self.textpad().OnSaveAs(e)),
                             ('-'),
                             ('Exit', self.OnClose)
                             ]),
                ## Edit 
                ('Edit(&E)', [ ('Undo', lambda e: self.textpad().OnUndo(e)),
                             ('Redo', lambda e: self.textpad().OnRedo(e)),
                             ('-'),
                             ('Cut', lambda e: self.textpad().OnCut(e)),
                             ('Copy', lambda e: self.textpad().OnCopy(e)),
                             ('Paste', lambda e: self.textpad().OnPaste(e)),
                             ('-'),
                             ('All', lambda e: self.textpad().OnSelectAll(e))
                             ]),               
                ## Help 
                ('Help(&H)', [('About', lambda e: self.textpad().OnAbout(e))])
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

    def OnClose(self,event):
        self.Destroy()
        
    def OnClosing(self, event):
        event.Skip()
    
if __name__ == '__main__':
    app = wx.App()
    npbf = TextNoteFrame(None)
    note1 = npbf.add_notepad()
    note1.append('abc')
    note1 = npbf.add_notepad()
    note1.append('def')
    npbf.Show()
    app.MainLoop()
    

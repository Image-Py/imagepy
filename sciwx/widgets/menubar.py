import wx

class MenuBar(wx.MenuBar):
    def __init__(self, app):
        wx.MenuBar.__init__(self)
        self.app = app
        app.SetMenuBar(self)

    def parse(self, ks, vs, pt):
        if isinstance(vs, list):
            menu = wx.Menu()
            for kv in vs:
                if kv == '-': menu.AppendSeparator()
                else: self.parse(*kv, menu)
            pt.Append(1, ks, menu)
        else:
            item = wx.MenuItem(pt, -1, ks)
            f = lambda e, p=vs: p().start(self.app)
            self.Bind(wx.EVT_MENU, f, item)
            pt.Append(item)

    def Append(self, id, item, menu):
        wx.MenuBar.Append(self, menu, item)
        
    def load(self, data):
        for k,v in data[1]: self.parse(k, v, self)

    def on_menu(self, event):
        print('here')
        

if __name__ == '__main__':
    class P:
        def __init__(self, name):
            self.name = name

        def start(self):
            print(self.name)

        def __call__(self):
            return self
        
    data = ('menu', [
            ('File', [('Open', P('O')),
                      '-',
                      ('Close', P('C'))]),
            ('Edit', [('Copy', P('C')),
                      ('A', [('B', P('B')),
                             ('C', P('C'))]),
                      ('Paste', P('P'))])])
    
    app = wx.App()
    frame = wx.Frame(None)
    menubar = MenuBar()
    menubar.load(data)
    frame.SetMenuBar(menubar)
    frame.Show()
    app.MainLoop()


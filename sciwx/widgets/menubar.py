import wx

def hot_key(txt):
    sep = txt.split('-')
    acc, code = wx.ACCEL_NORMAL, -1
    if 'Ctrl' in sep: acc|= wx.ACCEL_CTRL
    if 'Alt' in sep: acc|= wx.ACCEL_ALT
    if 'Shift' in sep: acc|= wx.ACCEL_SHIFT
    fs = ['F%d'%i for i in range(1,13)]
    if sep[-1] in fs:
        code = 340+fs.index(sep[-1])
    elif len(sep[-1])==1: code = ord(sep[-1])
    return acc, code

class MenuBar(wx.MenuBar):
    def __init__(self, app):
        wx.MenuBar.__init__(self)
        self.app = app
        app.SetMenuBar(self)

    def parse(self, ks, vs, pt, short, rst):
        if isinstance(vs, list):
            menu = wx.Menu()
            for kv in vs:
                if kv == '-': menu.AppendSeparator()
                else: self.parse(*kv, menu, short, rst)
            pt.Append(1, ks, menu)
        else:
            item = wx.MenuItem(pt, -1, ks)
            if ks in short:
                rst.append((short[ks], item.GetId()))
            f = lambda e, p=vs: p().start(self.app)
            self.Bind(wx.EVT_MENU, f, item)
            pt.Append(item)

    def Append(self, id, item, menu):
        wx.MenuBar.Append(self, menu, item)
        
    def load(self, data, shortcut={}):
        rst = []
        for k,v in data[1]: 
            self.parse(k, v, self, shortcut, rst)
        rst = [(*hot_key(i[0]), i[1]) for i in rst]
        return wx.AcceleratorTable(rst)

    def on_menu(self, event): print('here')

    def clear(self):
        while self.GetMenuCount()>0: self.Remove(0)
        

if __name__ == '__main__':
    class P:
        def __init__(self, name):
            self.name = name

        def start(self, app):
            print(self.name)

        def __call__(self):
            return self
        
    data = ('menu', [
                ('File', [
                    ('Open', P('O')),
                    '-',
                    ('Close', P('C'))]),
                ('Edit', [
                    ('Copy', P('C')),
                    ('A', [
                        ('B', P('B')),
                        ('C', P('C'))]),
                    ('Paste', P('P'))])])
    
    app = wx.App()
    frame = wx.Frame(None)
    menubar = MenuBar(frame)
    acc = menubar.load(data, {'Open':'Ctrl-O'})
    frame.SetMenuBar(menubar)
    menubar.SetAcceleratorTable(acc)
    frame.Show()
    app.MainLoop()


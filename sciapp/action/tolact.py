from .action import SciAction

class Tool(SciAction):
    title = 'Base Tool'
    default = None
    cursor = 'arrow'
    def mouse_down(self, canvas, x, y, btn, **key): pass
    def mouse_up(self, canvas, x, y, btn, **key): pass
    def mouse_move(self, canvas, x, y, btn, **key): pass
    def mouse_wheel(self, canvas, x, y, d, **key): pass
    def start(self, app): 
        self.app, self.default = app, self
        if not app is None: app.tool = self

class DefaultTool(Tool):
    title = 'Move And Scale'
    def __init__(self): 
        self.oldxy = None
        
    def mouse_down(self, obj, x, y, btn, **key):
        if btn==1: self.oldxy = key['px'], key['py']
        if btn==3: key['canvas'].fit()
        
    def mouse_up(self, obj, x, y, btn, **key):
        self.oldxy = None
    
    def mouse_move(self, obj, x, y, btn, **key):
        if self.oldxy is None: return
        ox, oy = self.oldxy
        up = (1,-1)[key['canvas'].up]
        key['canvas'].move(key['px']-ox, (key['py']-oy)*up)
        self.oldxy = key['px'], key['py']
    
    def mouse_wheel(self, obj, x, y, d, **key):
        if d>0: key['canvas'].zoomout(x, y, coord='data')
        if d<0: key['canvas'].zoomin(x, y, coord='data')

    def start(self, app): 
        self.app = app
        Tool.default = self
        if not app is None: app.tool = self

class ImageTool(DefaultTool):
    default = None
    title = 'Image Tool'

    def start(self, app): 
        self.app = app
        ImageTool.default = self
        if not app is None: app.tool = self

class ShapeTool(DefaultTool):
    default = None
    title = 'Image Tool'

    def start(self, app): 
        self.app = app
        ShapeTool.default = self
        if not app is None: app.tool = self

class TableTool(DefaultTool):
    default = None
    title = 'Table Tool'

    def start(self, app): 
        self.app = app
        TableTool.default = self
        if not app is None: app.tool = self

DefaultTool().start(None)
ImageTool().start(None)
ShapeTool().start(None)
TableTool().start(None)
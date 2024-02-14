from .action import SciAction

class Tool(SciAction):
    title = 'Base Tool'
    default = None
    cursor = 'arrow'
    view = None
    para = None

    def config(self): pass
    def mouse_down(self, canvas, x, y, btn, **key): pass
    def mouse_up(self, canvas, x, y, btn, **key): pass
    def mouse_move(self, canvas, x, y, btn, **key): pass
    def mouse_wheel(self, canvas, x, y, d, **key): pass
    def start(self, app, para=None, callafter=None): 
        self.app, self.default = app, self
        if para == 'local': return self
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
        if not hasattr(self, 'oldxy') or self.oldxy is None: return
        ox, oy = self.oldxy
        up = (1,-1)[key['canvas'].up]
        key['canvas'].move(key['px']-ox, (key['py']-oy)*up)
        self.oldxy = key['px'], key['py']
    
    def mouse_wheel(self, obj, x, y, d, **key):
        if d>0: key['canvas'].zoomout(x, y, coord='data')
        if d<0: key['canvas'].zoomin(x, y, coord='data')

    def start(self, app, para=None): 
        self.app = app
        if para == 'local': return self
        Tool.default = self
        #if not app is None: app.tool = self

class ImageTool(DefaultTool):
    default = None
    title = 'Image Tool'

    def mouse_move(self, img, x, y, btn, **key):
        if img.img is None: return
        DefaultTool.mouse_move(self, img, x, y, btn, **key)
        if self.app is None: return
        r, c = int(y), int(x)
        if (r>0) & (c>0) & (r<img.shape[0]) & (c<img.shape[1]):
            s = 'x:%d y:%d  value:%s'%(x, y, img.img[r,c])
            self.app.info(s)

    def start(self, app, para=None, callafter=None): 
        self.app = app
        if para == 'local': return self
        ImageTool.default = self
        #if not app is None: app.tool = self

class ShapeTool(DefaultTool):
    default = None
    title = 'Shape Tool'

    def mouse_move(self, shp, x, y, btn, **key):
        DefaultTool.mouse_move(self, shp, x, y, btn, **key)
        if self.app is None: return
        r, c = int(y), int(x)
        if self.app: self.app.info('%d, %d'%(x, y))

    def start(self, app, para=None, callafter=None): 
        self.app = app
        if para == 'local': return self
        ShapeTool.default = self
        # if not app is None: app.tool = self

class TableTool(DefaultTool):
    default = None
    title = 'Table Tool'

    def mouse_down(self, data, x, y, btn, **others):
        print('you click on cell', x, y)

    def start(self, app, para=None, callafter=None): 
        self.app = app
        if para == 'local': return self
        TableTool.default = self
        # if not app is None: app.tool = self

class MeshTool(DefaultTool):
    default = None
    title = 'Shape Tool'

    def start(self, app, para=None, callafter=None): 
        self.app = app
        if para == 'local': return self
        MeshTool.default = self
        # if not app is None: app.tool = self

    def mouse_move(self, obj, x, y, btn, **key):
        if not self.oldxy is None:
            dx = x - self.oldxy[0]
            dy = y - self.oldxy[1]
            camera = key['canvas'].camera
            camera.orbit(-dx/2, dy/2)
            self.oldxy = x, y

    def mouse_wheel(self, obj, x, y, d, **key):
        s = 1.1 ** - d
        camera = key['canvas'].camera
        if camera._distance is not None:
            camera._distance *= s
        camera.scale_factor *= s

DefaultTool().start(None)
ImageTool().start(None)
ShapeTool().start(None)
TableTool().start(None)
MeshTool().start(None)
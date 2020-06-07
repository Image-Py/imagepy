from sciapp.action import ImageTool

class Plugin(ImageTool):
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
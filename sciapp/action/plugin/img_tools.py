from sciapp.action import ImageTool

class MoveTool(ImageTool):
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

class ScaleTool(ImageTool):
    title = 'Scope'
    def __init__(self):
        self.ox, self.oy = 0, 0
            
    def mouse_down(self, ips, x, y, btn, **key):
        if btn==2:
            self.ox, self.oy = key['canvas'].to_panel_coor(x,y)
            print(self.ox, self.oy)
        #print 'down', self.ox, self.oy
        if btn==1: key['canvas'].zoomout(x, y, 'data')
        if btn==3: key['canvas'].zoomin(x, y, 'data')
        ips.update()
    
    def mouse_up(self, ips, x, y, btn, **key):
        pass
    
    def mouse_move(self, ips, x, y, btn, **key):
        if btn==2:
            x,y = key['canvas'].to_panel_coor(x,y)
            #print 'x,y',x,y
            #print 'dx,dy:', x-self.ox, y-self.oy
            key['canvas'].move(x-self.ox, y-self.oy)
            ips.update()
        self.ox, self.oy = x,y
        
    def mouse_wheel(self, ips, x, y, d, **key):
        if d>0:key['canvas'].zoomout(x, y, 'data')
        if d<0:key['canvas'].zoomin(x, y, 'data')
        ips.update()
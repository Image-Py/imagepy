from sciapp.action import ImageTool

class Plugin(ImageTool):
    """ColorPicker class plugin with events callbacks"""
    title = 'Color Picker'
    para = {'front':(255,255,255), 'back':(0,0,0)}
    view = [('color', 'front', 'front', 'color'),
            ('color', 'back', 'back', 'color')]
        
    def config(self):
        self.app.manager('color').add('front', self.para['front'])
        self.app.manager('color').add('back', self.para['back'])
        
    def mouse_down(self, ips, x, y, btn, **key):
        manager = self.app.manager('color')
        if btn == 1: manager.add('front', ips.img[int(y), int(x)])
        if btn == 3: manager.add('back', ips.img[int(y), int(x)])
    
    def mouse_up(self, ips, x, y, btn, **key):
        pass
    
    def mouse_move(self, ips, x, y, btn, **key):
        pass
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass
    
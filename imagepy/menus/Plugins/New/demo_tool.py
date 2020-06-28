# -*- coding: utf-8 -*-
from imagepy.draw import paint
from sciapp.action import Tool

# this is a simple tool implements a pencial
class Plugin(Tool):
    # the title on the menu
    title = 'pencil'
    
    # config parameter
    cfgv = [(int, 'width', (0,30), 0,  'width', 'pix')]
    cfgp = {'width':1}
    
    def __init__(self):
        self.sta = 0
        self.paint = paint.Paint()
        self.paint.color = 255
        self.cursor = 'cross'
        
    # do it when mouse_down
    def mouse_down(self, ips, x, y, btn, **key):
        if btn==3:
            self.paint.color = ips.img[y,x]
            return
        self.sta = 1
        self.paint.set_curpt(x,y)
        ips.snapshot()
    
    # do it when mouse_up
    def mouse_up(self, ips, x, y, btn, **key):
        self.sta = 0
    
    # do it when mouse_move
    def mouse_move(self, ips, x, y, btn, **key):
        if self.sta==1:
            self.paint.lineto(ips.img,x,y, self.cfgp['width'])
            ips.update()
        
    # do it when mouse wheel
    def mouse_wheel(self, ips, x, y, d, **key):
        pass

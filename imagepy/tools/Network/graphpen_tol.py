from sciapp.action import ImageTool
from sciapp.object import mark2shp
import numpy as np

def draw(img, lines):
    if len(lines)<2:return
    lines = np.array(lines).round()
    ox,oy = lines[0]
    xys, mark = [], []
    for i in lines[1:]:
        cx, cy = i
        dx, dy = cx-ox, cy-oy
        n = max(abs(dx), abs(dy)) + 1
        xs = np.linspace(ox, cx, n).round().astype(np.int16)
        ys = np.linspace(oy, cy, n).round().astype(np.int16)
        for x,y in zip(xs, ys):
            if x<0 or x>img.shape[1]: continue
            if y<0 or y>img.shape[0]: continue
            xys.append((y,x))
        ox, oy = i
    cur = 0
    neibs = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
    for y,x in xys:
        for dx, dy in neibs:
            if img[y+dy, x+dx]>0: 
                mark.append(cur)
                img[y+dy, x+dx] = 255
        cur += 1
    if len(mark)<4:return
    for y,x in xys[mark[0]+1:mark[-1]-1]: img[y,x] = 128
    for cur in mark: img[tuple(xys[cur])] = 255

class Plugin(ImageTool):
    title = 'Graph Cut'
    def __init__(self):
        self.status = 0
        self.line = {'type':'line', 'body':[]}
            
    def mouse_down(self, ips, x, y, btn, **key):
        if btn==1:
            ips.snapshot()
            self.status = 1
            self.line['body'] = [(x, y)]
            ips.mark = mark2shp(self.line)
            ips.update()
    
    def mouse_up(self, ips, x, y, btn, **key):
        ips.mark = None
        self.status = 0
        draw(ips.img, self.line['body'])
        ips.update()
    
    def mouse_move(self, ips, x, y, btn, **key):
        if self.status==1:
            self.line['body'].append((x, y))
            ips.mark = mark2shp(self.line)
            ips.update()
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass
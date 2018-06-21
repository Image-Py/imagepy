from imagepy.core.engine import Tool
# 用于绘制特征集
class FeatMark:
    def __init__(self, feats):
        self.feats = feats

    def draw(self, dc, f, **key):
        for i in self.feats:
            dc.DrawCircle(f(*i), 3)

# 用于双图特征集交互
class Pick(Tool):
    title = 'Key Point Pick Tool'
    def __init__(self, pts1, pts2, pair, msk, ips1, ips2, host, style):
        self.pts1, self.pts2 = pts1, pts2
        self.ips1, self.ips2 = ips1, ips2
        self.pair, self.msk = pair, msk
        self.cur, self.host = -1, host
        self.pts = self.pts1 if host else self.pts2
        self.style = style

    def nearest(self, x, y):
        mind, mini = 1000, -1
        for i1, i2 in self.pair:
            i = i1 if self.host else i2
            d = np.sqrt((x-self.pts[i,0])**2+(y-self.pts[i,1])**2)
            if d<mind: mind, mini = d, (i1, i2)
        return mini if mind<5 else None

    def mouse_down(self, ips, x, y, btn, **key):
        cur = self.nearest(x, y)
        if cur==None:return
        self.ips1.tool.cur, self.ips2.tool.cur = cur
        self.ips1.update, self.ips2.update = True, True

    def mouse_up(self, ips, x, y, btn, **key):
        pass

    def mouse_move(self, ips, x, y, btn, **key):
        pass

    def mouse_wheel(self, ips, x, y, d, **key):
        pass

    def draw(self, dc, f, **key):
        #dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush((0,0,255)))
        if self.style:
            for i in self.pts:dc.DrawCircle(f(*i), 3)
        tidx = self.pair[:,1-self.host][self.msk]
        dc.SetBrush(wx.Brush((255,255,0)))
        for i in tidx:
            dc.DrawCircle(f(*self.pts[i]), 3)
        if self.cur!=-1:
            dc.SetBrush(wx.Brush((255,0,0)))
            dc.DrawCircle(f(*self.pts[self.cur]), 3)
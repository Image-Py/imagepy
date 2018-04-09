from imagepy import IPy, wx
import numpy as np
from imagepy.core.engine import Simple
from numpy.linalg import norm

# 计算角度
def angleX(v):
    a = np.arccos(v[:,0] / norm(v[:,:2], axis=1))
    return np.where(v[:,1]>=0,a ,np.pi * 2 - a)

# 精确定位, 根据圆心和采样点，组建法方程，进行最小二乘估计
def exactly(O, r, pts):
    n = len(pts)
    B = np.zeros((n*2, n+3))
    L = np.zeros(n*2)
    appro = np.zeros(n+3)
    appro[:n] = angleX(pts-O)
    appro[n:] = [O[0], O[1], r]
    for i in range(1): # 两次迭代，确保达到稳定
        L[::2] = appro[n]+appro[-1]*np.cos(appro[:n])-pts[:,0]
        L[1::2] = appro[n+1]+appro[-1]*np.sin(appro[:n])-pts[:,1]
        B[range(0,n*2,2),range(n)] = -appro[-1]*np.sin(appro[:n])
        B[range(1,n*2,2),range(n)] = appro[-1]*np.cos(appro[:n])
        B[::2,n],B[1::2,n+1] = 1, 1
        B[::2,-1] = np.cos(appro[:n])
        B[1::2,-1] = np.sin(appro[:n])
        NN = np.linalg.inv(np.dot(B.T,B))
        x = np.dot(NN, np.dot(B.T,L))
        v = np.dot(B,x)-L
        appro -= x
    return appro[[-3,-2]], appro[-1]

def select(o, r, pts, lim):
    msk = np.ones(len(pts), dtype=np.bool)
    while True:
        if len(pts)<10:return None
        o, r = exactly(o, r, pts)
        ls = norm(pts - o, axis=1)
        msk = np.abs(ls-r)>ls.std()*lim+0.5
        if msk.sum()==0: return o, r, pts
        pts = pts[~msk]

class Mark:
    def __init__(self, o, r, pts):
        self.o, self.r, self.pts = o, r, pts

    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((255,255,0), width=1, style=wx.SOLID))
        dc.SetTextForeground((255,255,0))
        font = wx.Font(8, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        dc.SetFont(font)
        pos = f(*self.o[::-1])
        dc.SetBrush(wx.Brush((0,0,0), wx.BRUSHSTYLE_TRANSPARENT))
        dc.DrawCircle(pos[0], pos[1], self.r * key['k'])

        ls = norm(self.pts - self.o, axis=1)
        msk1 = ls-self.r<-(ls.std()*2+0.5)
        msk2 = ls-self.r>(ls.std()*2+0.5)
        redps = [f(*i[::-1]) for i in self.pts[msk1]]
        blueps = [f(*i[::-1]) for i in self.pts[msk2]]
        dc.SetPen(wx.Pen((0,0,255), width=3))
        for i in blueps: dc.DrawCircle(i[0], i[1], 1)
        dc.SetPen(wx.Pen((255,0,0), width=3))
        for i in redps: dc.DrawCircle(i[0], i[1], 1)
        dc.DrawText('STD=%.3f'%ls.std(), pos[0], pos[1])

class Plugin(Simple):
    title = 'Circle Check'
    note = ['8-bit']
    para = {'lim':3.0}
    view = [(float, (1,5), 1, 'lim', 'lim', 'pix')]
    #process
    def run(self, ips, imgs, para = None):
        print(para)
        x, y = np.where(ips.img==255)
        pts = np.array([x, y]).T
        r = len(pts)//1000
        o, r, npts = select(pts.mean(axis=0), 10, pts[::r+1], para['lim'])
        ips.mark = Mark(o, r, npts)
        print(o, r)
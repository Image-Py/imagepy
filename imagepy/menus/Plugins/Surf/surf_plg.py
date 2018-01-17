import cv2, wx
from imagepy.core.engine import Filter, Simple, Tool
from imagepy.core.manager import WindowsManager
from .matcher import Matcher
import numpy as np
from imagepy import IPy

CVSURF = cv2.xfeatures2d.SURF_create if cv2.__version__[0] =="3" else cv2.SURF

class FeatMark:
    def __init__(self, feats):
        self.feats = feats

    def draw(self, dc, f, **key):
        for i in self.feats:
            dc.DrawCircle(f(i.pt), 3)

class Surf(Filter):
    title = 'Surf Detect'
    note = ['all', 'not-slice']

    para = {'upright':False, 'oct':3, 'int':4, 'thr':1000, 'ext':False}
    view = [(int, (0,5), 0, 'octaves', 'oct', ''),
            (int, (0,5), 0, 'intervals', 'int',''),
            (int, (500,2000), 0, 'threshold', 'thr','1-100'),
            (bool, 'extended', 'ext'),
            (bool, 'upright', 'upright')]

    def run(self, ips, snap, img, para):
        detector = CVSURF(hessianThreshold=para['thr'], nOctaves=para['oct'],
            nOctaveLayers=para['int'], upright=para['upright'],extended=para['ext'])
        kps = detector.detect(img)
        ips.surf_keypoint = kps
        ips.mark = FeatMark(kps)
        IPy.write("Detect completed, {} points found!".format(len(kps)), 'Surf')

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
            d = np.sqrt((x-self.pts[i].pt[0])**2+(y-self.pts[i].pt[1])**2)
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
            for i in self.pts:dc.DrawCircle(f(*i.pt), 3)
        tidx = self.pair[:,1-self.host][self.msk]
        dc.SetBrush(wx.Brush((255,255,0)))
        for i in tidx:
            dc.DrawCircle(f(*self.pts[i].pt), 3)
        if self.cur!=-1:
            dc.SetBrush(wx.Brush((255,0,0)))
            dc.DrawCircle(f(*self.pts[self.cur].pt), 3)

class Match(Simple):
    title = 'Surf Matcher'
    note = ['all']

    #parameter
    para = {'img1':'','img2':'','upright':False,  'log':False,
            'oct':3, 'int':4, 'thr':1000, 'ext':False,
            'trans':'None', 'std':1, 'style':'Blue/Yellow'}

    def load(self, ips):
        titles = WindowsManager.get_titles()
        self.para['img1'] = titles[0]
        self.para['img2'] = titles[0]
        Match.view = [('lab','=========  two image in 8-bit  ========='),
                      (list, titles, str, 'image1', 'img1', ''),
                      (list, titles, str, 'image2', 'img2', ''),
                      ('lab',''),
                      ('lab','======  parameter about the surf  ======'),
                      (int, (0,5), 0, 'octaves', 'oct', ''),
                      (int, (0,5), 0, 'intervals', 'int',''),
                      (int, (500,2000), 0, 'threshold', 'thr','1-100'),
                      (bool, 'extended', 'ext'),
                      (bool, 'upright', 'upright'),
                      ('lab',''),
                      ('lab','======  how to match and display  ======'),
                      (list, ['None', 'Affine', 'Homo'], str, 'transform', 'trans',''),
                      (int, (1, 5), 0, 'Std', 'std', 'torlerance'),
                      (list, ['Blue/Yellow', 'Hide'], str, 'Aspect', 'style', 'color'),
                      (bool, 'Show log', 'log')]
        return True

    def filter_matches(self, kp1, kp2, matches, ratio = 0.75):
        mkp1, mkp2 = [], []
        for m in matches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                m = m[0]
                mkp1.append( kp1[m.queryIdx] )
                mkp2.append( kp2[m.trainIdx] )
        p1 = np.float32([kp.pt for kp in mkp1])
        p2 = np.float32([kp.pt for kp in mkp2])
        kp_pairs = list(zip(mkp1, mkp2))
        return p1, p2, kp_pairs

    #process
    def run(self, ips, imgs, para = None):
        ips1 = WindowsManager.get(para['img1']).ips
        ips2 = WindowsManager.get(para['img2']).ips

        detector = CVSURF(hessianThreshold=para['thr'], nOctaves=para['oct'],
            nOctaveLayers=para['int'], upright=para['upright'],extended=para['ext'])
        kps1, feats1 = detector.detectAndCompute(ips1.img, None)
        kps2, feats2 = detector.detectAndCompute(ips2.img, None)
        dim, std = {'None':0, 'Affine':6, 'Homo':8}[para['trans']], para['std']/100.0
        style = para['style']=='Blue/Yellow'
        idx, msk, m = Matcher(dim, std).filter(kps1,feats1,kps2,feats2)
        picker1 = Pick(kps1, kps2, idx, msk, ips1, ips2, True, style)
        picker2 = Pick(kps1, kps2, idx, msk, ips1, ips2, False, style)
        ips1.tool, ips1.mark = picker1, picker1
        ips2.tool, ips2.mark = picker2, picker2
        if para['log']:self.log(kps1, kps2, msk, m, dim)
        ips1.update, ips2.update = True, True

    def log(self, pts1, pts2, msk, v, dim):
        sb = []
        sb.append('Image1:{} points detected!'.format(len(pts1)))
        sb.append('Image2:{} points detected!\r\n'.format(len(pts2)))
        sb.append('Matched Point:{0}/{1}\r\n'.format(msk.sum(),len(msk)))
        if dim == 0: return
        sb.append('Transformation:')
        sb.append('%15.4f%15.4f%15.4f'%tuple(v.A1[:3]))
        sb.append('%15.4f%15.4f%15.4f'%tuple(v.A1[3:6]))
        row = [0,0,1] if dim==6 else list(v[-2:])+[1]
        sb.append('%15.4f%15.4f%15.4f'%tuple(row))
        
        cont = '\n'.join(sb)
        IPy.write(cont, 'Surf')

plgs = [Surf, Match]

if __name__ == '__main__':
    from .matcher import Matcher

    detector = CVSURF(1000, nOctaves=3, nOctaveLayers=4, upright=False,extended=False)
    #img1 = cv2.imread('/home/yxl/opencv-2.4/samples/c/box.png', 0)
    img1 = cv2.imread('/home/auss/Pictures/faces1.png',0)
    pts, des = detector.detectAndCompute(img1, None)

    matcher = cv2.BFMatcher(cv2.NORM_L2)
    raw_matches = matcher.knnMatch(des, trainDescriptors = des, k = 1)
    m = raw_matches[0][0]
    lt = [(i[0].distance, i[0].queryIdx, i[0].trainIdx) for i in raw_matches]
    lt = np.array(sorted(lt))

    matcher = Matcher(8, 3)
    idx, msk, m = matcher.filter(pts,des,pts,des)
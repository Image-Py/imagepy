# 仿照surf_plgs.py

import cv2, wx
from imagepy.core.engine import Filter, Simple, Tool
from imagepy.core.manager import ImageManager
import numpy as np
from imagepy import IPy
from .matcher import Matcher

from skimage.color import rgb2gray,gray2rgb

import pandas as pd

# CVSURF = cv2.xfeatures2d.SURF_create if cv2.__version__[0] =="3" else cv2.SURF

class FeatMark:
    def __init__(self, feats):
        self.feats = feats

    def draw(self, dc, f, **key):
        for i in self.feats:
            # print('i.pt:{},{}'.format(type(f(i.pt))，i.pt))
            dc.DrawCircle(f(i[0], i[1]), 3)

class SIFT(Filter):
    title = 'SIFT Detect'
    note = ['all', 'not-slice']

    para = {'dsample':1}
    view = [(int, 'dsample', (1,30), 0, 'down sample', '1-30')]

    def run(self, ips, snap, img, para):

        if para['dsample']>1:img = img[::para['dsample'], ::para['dsample']]

        detector = cv2.xfeatures2d.SIFT_create() if cv2.__version__[0] =="3" else cv2.SIFT()

        kps = detector.detect(img, None)
        ips.sift_keypoint = kps
        skps = np.array([i.pt for i in kps])*para['dsample']
        ips.mark = FeatMark(skps)
        IPy.write("Detect completed, {} points found!".format(len(kps)), 'SIFT')

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

class SIFTMatch(Simple):
    title = 'SIFT Matcher'
    note = ['all']

    #parameter
    para = {'img1':'','img2':'',   'knn_trees':3, 'knn_val':2,'checks':50,'trans':'None', 'std':1, 'style':'Blue/Yellow'}

    view = [    ('lab', None, '=========  two image in 8-bit  ========='),
                ('img', 'img1', 'first image', ''),
                ('img', 'img2', 'second image', ''),
                  ('lab', None, ''),
                  ('lab', None, '======  parameter about the Orb  ======'),
                  (int, 'knn_trees', (0,10), 3, 'knn trees', ''),
                  (int, 'knn_val', (0,5), 2, 'Knn cluster value', ''),
                  (int, 'checks', (10,100), 50, 'FLANN Search Para', ''),
                  ('lab', None, ''),
                  ('lab', None, '======  how to match and display  ======'),
                  (list, 'trans', ['None', 'Affine', 'Homo'], str, 'transform', ''),
                  (int, 'std', (1, 5), 0, 'Std', 'torlerance'),
                  (list, 'style', ['Blue/Yellow', 'Hide'], str, 'Aspect', 'color')

                      ]

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

    def compute_matches(self,features0,features1, matcher, knn=5, lowe=0.7):
        keypoints0, descriptors0 = features0
        keypoints1, descriptors1 = features1

        matches = matcher.knnMatch(descriptors0, descriptors1, k=knn)

        positive = []
        for match0, match1 in matches:
            if match0.distance < lowe * match1.distance:
                positive.append(match0)

        src_pts = np.array([keypoints0[good_match.queryIdx].pt for good_match in positive], dtype=np.float32)
        src_pts = src_pts.reshape((-1, 1, 2))
        dst_pts = np.array([keypoints1[good_match.trainIdx].pt for good_match in positive], dtype=np.float32)
        dst_pts = dst_pts.reshape((-1, 1, 2))

        return src_pts, dst_pts, len(positive)

    #process
    def run(self, ips, imgs, para = None):

        ips1 = ImageManager.get(para['img1'])
        ips2 = ImageManager.get(para['img2'])

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = para['knn_trees'])
        search_params = dict(checks = para['checks'])

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        detector = cv2.xfeatures2d.SIFT_create() if cv2.__version__[0] =="3" else cv2.SIFT()

        print('ips1.img:{}'.format(ips1.img.shape))
        kps1,feats1 = detector.detectAndCompute(ips1.img, None)
        kps2,feats2  = detector.detectAndCompute(ips2.img, None)

        dim, std = {'None':0, 'Affine':6, 'Homo':8}[para['trans']], para['std']/100.0
        style = para['style']=='Blue/Yellow'

        # matches_src, matches_dst, n_matches = self.compute_matches(features0,features1, flann, 2, 0.5)
        idx, msk, m = Matcher(dim, std).filter(kps1,feats1,kps2,feats2)
        picker1 = Pick(kps1, kps2, idx, msk, ips1, ips2, True, style)
        picker2 = Pick(kps1, kps2, idx, msk, ips1, ips2, False, style)

        ips1.tool, ips1.mark = picker1, picker1
        ips2.tool, ips2.mark = picker2, picker2

        tempPnt1 = np.float32([kps1[i1].pt for i1,_ in idx])
        tempPnt2 = np.float32([kps2[i2].pt for _,i2 in idx]) # tidx = self.pair[:,1-self.host][self.msk]

        newPnt1=[ np.float32(tempPnt1[i]) for i in range(len(msk)) if msk[i]!=0 ]
        newPnt2=[ np.float32(tempPnt2[i]) for i in range(len(msk)) if msk[i]!=0 ]


        H, mask = cv2.findHomography(np.array(newPnt1), np.array(newPnt2), cv2.RANSAC, 5.0)
        result = self.combine_images(ips2.img, ips1.img, H)

        title = 'SIFT Stitched image'
        IPy.show_img([result.astype(np.uint8)], title)

        # if para['com']:
        titles=['x','y','z']
        IPy.show_table(pd.DataFrame(H, columns=titles), ips.title+'-region')

    def combine_images(self,img0,img1,h_matrix):
        print('combining images... ')

        points0 = np.array(
            [[0, 0], [0, img0.shape[0]], [img0.shape[1], img0.shape[0]], [img0.shape[1], 0]], dtype=np.float32)
        points0 = points0.reshape((-1, 1, 2))

        points1 = np.array(
            [[0, 0], [0, img1.shape[0]], [img1.shape[1], img0.shape[0]], [img1.shape[1], 0]], dtype=np.float32)
        points1 = points1.reshape((-1, 1, 2))

        points2 = cv2.perspectiveTransform(points1, h_matrix)

        points = np.concatenate((points0, points2), axis=0)
        [x_min, y_min] = np.int32(points.min(axis=0).ravel() - 0.5)
        [x_max, y_max] = np.int32(points.max(axis=0).ravel() + 0.5)
        H_translation = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]])
        # logger.debug('warping previous image...')
        output_img = cv2.warpPerspective(img1, H_translation.dot(h_matrix), (x_max - x_min, y_max - y_min))
        output_img[-y_min:img0.shape[0] - y_min, -x_min:img0.shape[1] - x_min] = img0
        return output_img
        # cv2.imwrite('orb.jpg',test)
    # print surf result to the Name 'Surf' Console
    def log(self, pts1, pts2, msk, v, dim):
        sb = []
        sb.append('Image1:{} points detected!'.format(len(pts1)))
        sb.append('Image2:{} points detected!\r\n'.format(len(pts2)))
        sb.append('Matched Point:{0}/{1}\r\n'.format(len(msk),len(pts2)))
        if dim == 0: return
        sb.append('Transformation:')
        sb.append('%15.4f%15.4f%15.4f'%tuple(v[:3]))
        sb.append('%15.4f%15.4f%15.4f'%tuple(v[3:6]))
        sb.append('%15.4f%15.4f%15.4f'%tuple(v[6:9]))

        # row = [0,0,1] if dim==6 else list(v[-2:])+[1]
        # sb.append('%15.4f%15.4f%15.4f'%tuple(row))

        cont = '\n'.join(sb)
        IPy.write(cont, 'Surf')


plgs = [SIFT, SIFTMatch]

if __name__ == '__main__':
    from .matcher import Matcher

    detector = CVSURF(1000, nOctaves=3, nOctaveLayers=4, upright=False,extended=False)
    #img1 = cv2.imread('/home/yxl/opencv-2.4/samples/c/box.png', 0)
    img1 = cv2.imread('/Users/cooperjack/Desktop/0001_o.jpg',0)
    pts, des = detector.detectAndCompute(img1, None)

    matcher = cv2.BFMatcher(cv2.NORM_L2)
    raw_matches = matcher.knnMatch(des, trainDescriptors = des, k = 1)
    m = raw_matches[0][0]
    lt = [(i[0].distance, i[0].queryIdx, i[0].trainIdx) for i in raw_matches]
    lt = np.array(sorted(lt))

    matcher = Matcher(8, 3)
    idx, msk, m = matcher.filter(pts,des,pts,des)

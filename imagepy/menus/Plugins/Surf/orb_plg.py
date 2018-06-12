import cv2, wx
from imagepy.core.engine import Filter, Simple, Tool
from imagepy.core.manager import ImageManager
from .matcher import Matcher
import numpy as np
from imagepy import IPy

from skimage.color import rgb2gray,gray2rgb
from skimage.feature import ( match_descriptors, corner_harris, corner_peaks, ORB, plot_matches)
from skimage.measure import ransac
from skimage.transform import warp
from skimage.transform import SimilarityTransform
from skimage.transform import FundamentalMatrixTransform
from skimage.transform import ProjectiveTransform

import pandas as pd

CVSURF = cv2.xfeatures2d.SURF_create if cv2.__version__[0] =="3" else cv2.SURF

class OrbFeatMark:
    def __init__(self, feats):
        self.feats = feats

    def draw(self, dc, f, **key):
        for i in self.feats:
            # print('i.pt:{},{}'.format(type(f(i.pt))，i.pt))
            dc.DrawCircle(f(i[1], i[0]), 3)

class Orb(Filter):
    title = 'ORB Detect'
    note = ['all', 'not-slice']

    para = {'Num':1000}
    view = [
            (int, 'Num', (500,2000), 0, 'orb descriptor num', '1-1000')]

    def run(self, ips, snap, img, para):
        descriptor_extractor = ORB(n_keypoints=para['Num'])

        grayImg = rgb2gray(img)
        descriptor_extractor.detect_and_extract(grayImg)
        keypoints1 = descriptor_extractor.keypoints
        descriptors1 = descriptor_extractor.descriptors

        ips.orb_keypoint = keypoints1
        ips.orb_descriptors = descriptors1
        ips.mark = OrbFeatMark(keypoints1)

        IPy.write("Detect completed, {} ORB points found!".format(len(keypoints1)), 'Orb')

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

class OrbMatch(Simple):
    title = 'Orb Matcher'
    note = ['all']

    #parameter
    para = {'img1':'','img2':'',  'log':False, 'int':4, 'num':200}

    def load(self, ips):
        titles = ImageManager.get_titles()
        self.para['img1'] = titles[0]
        self.para['img2'] = titles[0]
        OrbMatch.view = [    ('lab', None, '=========  two image in 8-bit  ========='),
                          (list, 'img1', titles, str, 'image1', ''),
                          (list, 'img2', titles, str, 'image2', ''),
                          ('lab', None, ''),
                          ('lab', None, '======  parameter about the Orb  ======'),
                          (int, 'int', (0,5), 3, 'order', ''),
                          (int, 'num', (50,1000), 200, 'Descriptor_Num', '')
                          ]
        return True

    # def filter_matches(self, kp1, kp2, matches, ratio = 0.75):
    #     mkp1, mkp2 = [], []
    #     for m in matches:
    #         if len(m) == 2 and m[0].distance < m[1].distance * ratio:
    #             m = m[0]
    #             mkp1.append( kp1[m.queryIdx] )
    #             mkp2.append( kp2[m.trainIdx] )
    #     p1 = np.float32([kp.pt for kp in mkp1])
    #     p2 = np.float32([kp.pt for kp in mkp2])
    #     kp_pairs = list(zip(mkp1, mkp2))
    #     return p1, p2, kp_pairs

    #process
    def run(self, ips, imgs, para = None):

        ips1 = ImageManager.get(para['img1'])
        ips2 = ImageManager.get(para['img2'])

        grayImg1 = rgb2gray(ips1.img)
        grayImg2 = rgb2gray(ips2.img)

        print('desciptor num:{}'.format(para['num']))
        descriptor_extractor = ORB(n_keypoints=int(para['num']))

        descriptor_extractor.detect_and_extract(grayImg1)
        keypoints1 = descriptor_extractor.keypoints
        descriptors1 = descriptor_extractor.descriptors

        descriptor_extractor.detect_and_extract(grayImg2)
        keypoints2 = descriptor_extractor.keypoints
        descriptors2 = descriptor_extractor.descriptors

        matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)

        src = keypoints2[matches12[:, 1]][:, ::-1]
        dst = keypoints1[matches12[:, 0]][:, ::-1]


        model, inliers = ransac((src, dst),
                                ProjectiveTransform, min_samples=8,
                                residual_threshold=0.5, max_trials=5000)

        r, c = grayImg1.shape[:2]

        # Note that transformations take coordinates in
        # (x, y) format, not (row, column), in order to be
        # consistent with most literature.
        corners = np.array([[0, 0],
                            [0, r],
                            [c, 0],
                            [c, r]])

        # Warp the image corners to their new positions.
        warped_corners = model(corners)

        # Find the extents of both the reference image and
        # the warped target image.
        all_corners = np.vstack((warped_corners, corners))

        corner_min = np.min(all_corners, axis=0)
        corner_max = np.max(all_corners, axis=0)

        output_shape = (corner_max - corner_min)
        output_shape = np.ceil(output_shape[::-1])

        offset = SimilarityTransform(translation=-corner_min)

        # Warp pano0 to pano1 using 3rd order interpolation
        img1_ = warp(ips1.img, offset.inverse, order = int(para['int']),
                       output_shape=output_shape, cval=0)

        img1_mask = (img1_ != 0)
        img1_[~img1_mask] = 0

        img2_ = warp(ips2.img, (model + offset).inverse, order = int(para['int']),
                       output_shape=output_shape, cval=0)

        img2_[img1_mask] = 0
        test = (img1_+img2_)

        print('model:{}'.format(model._inv_matrix))
        print('(model + offset):{}'.format((model + offset)._inv_matrix))

        dim = 3
        self.log(keypoints1, keypoints2, matches12, (model + offset)._inv_matrix.flatten(), dim)
        # print('offset:{}'.format(offset))

        test *= 255
        img1_ *= 255
        img2_ *= 255
        # ips1.img = test
        # cv2.imwrite('img2_.jpg',img2_)
        # cv2.imwrite('img1_.jpg',img1_)

        title = 'Orb Stitched image'
        IPy.show_img([test.astype(np.uint8)], title)

        titles=['x','y','z']
        IPy.show_table(pd.DataFrame((model + offset)._inv_matrix, columns=titles), ips.title+'-region')

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


plgs = [Orb, OrbMatch]

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

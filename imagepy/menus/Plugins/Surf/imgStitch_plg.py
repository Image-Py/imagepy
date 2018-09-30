#-*- coding：utf-8 -*-
import cv2, wx
from imagepy.core.engine import Filter, Simple, Tool
from imagepy.core.manager import ImageManager
from .matcher import Matcher
import numpy as np
from imagepy import IPy
from skimage.color import rgb2gray
from skimage.feature import ( match_descriptors, corner_harris, corner_peaks, ORB, plot_matches)

CVSURF = cv2.xfeatures2d.SURF_create if cv2.__version__[0] =="3" else cv2.SURF

class FeatMark:
    def __init__(self, feats):
        self.feats = feats

    def draw(self, dc, f, **key):
        for i in self.feats:
            # print('i.pt:{},{}'.format(type(f(i.pt))，i.pt))
            dc.DrawCircle(f(i.pt[0], i.pt[1]), 3)

class Surf(Filter):
    title = 'Surf Detect'
    note = ['all', 'not-slice']

    para = {'upright':False, 'oct':3, 'int':4, 'thr':1000, 'ext':False}
    view = [    (int, 'oct', (0,5), 0, 'octaves',  ''),
                (int, 'int', (0,5), 0, 'intervals', ''),
                (int, 'thr', (500,2000), 0, 'threshold', '1-100'),
                (bool, 'ext', 'extended'),
                (bool, 'upright', 'upright') ]

    def run(self, ips, snap, img, para):
        detector = CVSURF(hessianThreshold=para['thr'], nOctaves=para['oct'],
            nOctaveLayers=para['int'], upright=para['upright'],extended=para['ext'])
        kps = detector.detect(img)
        ips.surf_keypoint = kps
        ips.mark = FeatMark(kps)
        IPy.write("Detect completed, {} points found!".format(len(kps)), 'Surf')


class ImgsStitch(Simple):
    title = 'ImgsStitch'
    note = ['all']

    #parameter
    para = {'imgList':'','img2':'','upright':False,  'log':False,
            'oct':3, 'int':4, 'thr':1000, 'ext':False,
            'trans':'None', 'std':1, 'style':'Blue/Yellow'}

    def myInitialize(self):
        self.images = []
        self.count = -1
        self.left_list, self.right_list, self.center_im = [], [],None
		# self.matcher_obj = matchers()

    def load(self, ips):
        titles = ImageManager.get_titles()
        self.para['imgList'] = titles[0]
        self.para['img2'] = titles[0]
        ImgsStitch.view = [  ('lab', None, '=========  two image in 8-bit  ========='),
                          (list, 'imgList', titles, str, 'image list', ''),
                          (list, 'img2', titles, str, 'image2', ''),
                          ('lab', None, ''),
                          ('lab', None, '======  parameter about the surf  ======'),
                          (int, 'oct', (0,5), 0, 'octaves', ''),
                          (int, 'int', (0,5), 0, 'intervals', ''),
                          (int, 'thr', (500,2000), 0, 'threshold', '1-100'),
                          (bool, 'ext', 'extended'),
                          (bool, 'upright', 'upright'),
                          ('lab', None, ''),
                          ('lab', None, '======  how to match and display  ======'),
                          (list, 'trans', ['None', 'Affine', 'Homo'], str, 'transform', ''),
                          (int, 'std', (1, 5), 0, 'Std', 'torlerance'),
                          (list, 'style', ['Blue/Yellow', 'Hide'], str, 'Aspect', 'color'),
                          (bool, 'log', 'show log') ]
        return True

    def prepare_lists(self):
        print( "Number of images : %d".format(self.count))
        self.centerIdx = self.count/2
        print(  "Center index image : %d".format(self.centerIdx))

        self.center_im = self.images[int(self.centerIdx)]
        for i in range(self.count):
        	if(i<=self.centerIdx):
        		self.left_list.append(self.images[i])
        	else:
        		self.right_list.append(self.images[i])
        print(  "Image lists prepared")

    def generateImgList(self,imglistpath):
        fp = open(imglistpath, 'r')
        filenames = [each.rstrip('\r\n') for each in  fp.readlines()]
        print(filenames)
        self.images = [cv2.resize(cv2.imread(each),(480,320)) for each in filenames]
        self.count = len(self.images)
        self.left_list, self.right_list, self.center_im = [], [],None
        # self.matcher_obj = matchers()
        self.prepare_lists()

    def stitchAllImgs(self,para):
        # print('current img list:{}'.format(para['imgList']))
        # curImgList = ImageManager.get(para['imgList'])
        curImgList = '/Users/cooperjack/Documents/gao-imagepy/stitchImgs.txt'
        print('curImgList:{}'.format(curImgList))

        self.generateImgList(curImgList)

        # 对左方图像进行匹配
        a = self.left_list[0]
        temp = a
        for b in self.left_list[1:]:
        # H = self.matcher_obj.match(a, b, 'left')
        #### 内存处理应该怎样进行
            temp = self.stitchTwoImg(temp, b, para)

        IPy.show_img([temp], 'left')

        # 对右方图像进行匹配
        for each in self.right_list:
            temp = self.stitchTwoImg(each,temp, para)

        # 输出最终的图像；
        title = 'Stitched images'
        IPy.show_img([temp], title)

    # 左图：ips1, 右图：ips2
    def stitchTwoImg(self,ips1, ips2,para):

        detector = CVSURF(hessianThreshold=para['thr'], nOctaves=para['oct'],
            nOctaveLayers=para['int'], upright=para['upright'],extended=para['ext'])

        kps1, feats1 = detector.detectAndCompute(ips1, None)
        kps2, feats2 = detector.detectAndCompute(ips2, None)

        dim, std = {'None':0, 'Affine':6, 'Homo':8}[para['trans']], para['std']/100.0

        style = para['style']=='Blue/Yellow'

        idx, msk, m = Matcher(dim, std).filter(kps1,feats1,kps2,feats2)
        # picker1 = Pick(kps1, kps2, idx, msk, ips1, ips2, True, style)
        # picker2 = Pick(kps1, kps2, idx, msk, ips1, ips2, False, style)

        # ips1.tool, ips1.mark = picker1, picker1
        # ips2.tool, ips2.mark = picker2, picker2
        if para['log']:self.log(kps1, kps2, msk, m, dim)

        tempPnt1 = np.float32([kps1[i1].pt for i1,_ in idx])
        tempPnt2 = np.float32([kps2[i2].pt for _,i2 in idx]) # tidx = self.pair[:,1-self.host][self.msk]

        newPnt1=[]
        newPnt2=[]
        for i in range(len(msk)):
            if msk[i]:
                newPnt1.append(tempPnt1[i])
                newPnt2.append(tempPnt2[i])

        # 第四个参数取值范围在 1 到 10 , 绝一个点对的阈值。原图像的点经过变换后点与目标图像上对应点的误差
        # 超过误差就认为是 outlier
        # 返回值中 H 为变换矩阵。mask是掩模，online的点
        H, _ = cv2.findHomography(tempPnt1, tempPnt2, cv2.RANSAC, 1.0)

        newImg = self.combine_images( ips2, ips1, H)
        return newImg
    #process
    def run(self, ips, imgs, para = None):
        self.myInitialize()
        self.stitchAllImgs(para)

    # print surf result to the Name 'Surf' Console
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

plgs = [ ImgsStitch]

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

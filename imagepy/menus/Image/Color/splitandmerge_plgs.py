# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 10:49:15 2016
@author: yxl
"""
import numpy as np
from sciapp.action import Simple
from skimage import color

class SplitRGB(Simple):
    title = 'Split RGB Channels'
    note = ['rgb']
    
    para = {'copy':False, 'destory':True}
    view = {(bool, 'copy', 'Copy data from view'),
            (bool, 'destory', 'Destory current image')}
    #process
    def run(self, ips, imgs, para = None):
        r,g,b = [],[],[]
        for i,n in zip(imgs,list(range(ips.slices))):
            for c,ci in zip((r,g,b),(0,1,2)):
                if self.para['copy']:c.append(i[:,:,ci].copy())
                else: c.append(i[:,:,ci])
            self.progress(n+1, len(imgs))
        for im, tl in zip([r,g,b],['red','green','blue']):
            self.app.show_img(im, ips.title+'-'+tl)
        if self.para['destory']:
            self.app.close_img(ips.title)

class ToRGB(Simple):
    title = 'RGB to RGB'
    note = ['all']
    
    #parameter
    para = {'red':'','green':'','blue':'','destory':True}

    def load(self, ips):
        r, g, b = self.titles()[1:]
        self.view = [('img', 'red', r, ''),
                    ('img', 'green', g, ''),
                    ('img', 'blue', b, ''),
                    (bool, 'destory', 'destory')]
        return True
    
    def titles(self): return 'RGB-Merge', 'red', 'green', 'blue'

    def trans(self, img1, img2, img3):
        return np.array([img1.T, img2.T, img3.T], dtype=np.uint8).T
    
    def run(self, ips, imgs, para = None):
        idx = ['red','green','blue']
        imr, img, imb = [self.app.get_img(para[i]) for i in idx]
        sr,sg,sb = [i.slices for i in [imr,img,imb]]
        
        if imr.dtype!=np.uint8 or img.dtype!=np.uint8 or imb.dtype!=np.uint8 or \
            imr.shape!=img.shape or img.shape!=imb.shape or sr!=sg or sg!=sb:
            return self.app.alert('three images must be 8-bit image, with the same size and  slices!')
            
        rgbs = []
        w,h = imr.shape
        for i in range(sr):
            self.progress(i,sr)
            rgbs.append(self.trans(imr.imgs[i], img.imgs[i], imb.imgs[i]))
        self.app.show_img(rgbs, self.titles()[0])
        if self.para['destory']:
            for title in [para[i] for i in idx]: self.app.close_img(title)

class RGB2(Simple):
    title = 'RGB To RGB'
    note = ['rgb']
    #process

    def titles(self): return 'Red', 'Green', 'Blue'
    def trans(self, img):
        return img

    def run(self, ips, imgs, para = None):
        nr, ng, nb = [],[],[]
        for i in range(ips.slices):
            nrgb = self.trans(imgs[i])
            nr.append(nrgb[:,:,0])
            ng.append(nrgb[:,:,1])
            nb.append(nrgb[:,:,2])
            self.progress(i, len(imgs))
        for im, tl in zip([nr, ng, nb], self.titles()):
            self.app.show_img(im, ips.title+'-'+tl)

class MergeRGB(ToRGB):
    title = 'Merge RGB Channels'
# ============= RGB - HSV ============
class RGB2HSV(RGB2):
    title = 'RGB To HSV'

    def titles(self):
        return 'Hue', 'Saturation', 'Value'

    def trans(self, img):
        rst = color.rgb2hsv(img)
        rst *= 255
        return rst.astype(np.uint8)

class HSV2RGB(ToRGB):
    title = 'HSV To RGB'

    #process
    def titles(self):
        return 'HSV2RGB-Merge', 'H', 'S', 'V'

    def trans(self, img1, img2, img3):
        rst = np.array((img1.T, img2.T, img3.T), dtype=np.float64)
        rst /= 255.0
        rst = color.hsv2rgb(rst.T)
        rst *= 255
        return rst.astype(np.uint8)
# ============= RGB - CIE ============
class RGB2CIE(RGB2):
    title = 'RGB To CIERGB'

    #process
    def titles(self):
        return 'Red', 'Green', 'Blue'

    def trans(self, img):
        rst = color.rgb2rgbcie(img)
        np.maximum(rst, 0, out=rst)
        print('============', rst.min(axis=(0,1)), rst.max(axis=(0,1)))
        rst *= 255/50*255
        return rst.astype(np.uint8)

class CIE2RGB(ToRGB):
    title = 'CIERGB To RGB'

    #process
    def titles(self):
        return 'CIE2RGB-Merge', 'R', 'G', 'B'

    def trans(self, img1, img2, img3):
        rst = np.maximum((img1.T, img2.T, img3.T), 0, dtype=np.float64)
        rst /= 255/50*255
        rst = color.rgbcie2rgb(rst.T)
        rst *= 255
        return (rst).astype(np.uint8)

# ============= RGB - LUV ============
class RGB2LUV(RGB2):
    title = 'RGB To LUV'

    #process
    def titles(self):
        return 'Luminance', 'UColor', 'VColor'

    def trans(self, img):
        rst = color.rgb2luv(img)+128
        #print('============', rst.min(), rst.max())
        return rst.astype(np.uint8)

class LUV2RGB(ToRGB):
    title = 'LUV To RGB'

    #process
    def titles(self):
        return 'LUV2RGB-Merge', 'L', 'U', 'V'

    def trans(self, img1, img2, img3):
        rst = np.array((img1.T, img2.T, img3.T), dtype=np.float64)
        rst -= 128
        rst = color.luv2rgb(rst.T)
        rst *= 255
        return (rst).astype(np.uint8)

# ============= RGB - Lab ============
class RGB2Lab(RGB2):
    title = 'RGB To Lab'

    #process
    def titles(self):
        return 'Luminance', 'AColor', 'BColor'

    def trans(self, img):
        rst = color.rgb2lab(img)
        rst+=100; rst*=(255/200.0)
        return (rst).astype(np.uint8)

class Lab2RGB(ToRGB):
    title = 'Lab To RGB'

    #process
    def titles(self):
        return 'Lab2RGB-Merge', 'L', 'A', 'B'

    def trans(self, img1, img2, img3):
        rst = np.array((img1.T, img2.T, img3.T), dtype=np.float64)
        rst *= (200/255.0); rst -= 100
        rst = color.lab2rgb(rst.T)
        rst *= 255
        return (rst).astype(np.uint8)

class RGB2Gray(Simple):
    title = 'RGB To Gray'
    note = ['rgb']

    def run(self, ips, imgs, para = None):
        gray = []
        for i in range(ips.slices):
            gray.append(color.rgb2gray(imgs[i])*255)
            self.progress(i, len(imgs))
        self.app.show_img(gray, ips.title+'-Gray')

# ============= RGB - XYZ ============
class RGB2XYZ(RGB2):
    title = 'RGB To XYZ'

    #process
    def titles(self):
        return 'X', 'Y', 'Z'

    def trans(self, img):
        rst = color.rgb2xyz(img)
        return (rst*(200)).astype(np.uint8)

class XYZ2RGB(ToRGB):
    title = 'XYZ To RGB'

    #process
    def titles(self):
        return 'XYZ2RGB-Merge', 'X', 'Y', 'Z'

    def trans(self, img1, img2, img3):
        rst = color.xyz2rgb(np.array((img1.T, img2.T, img3.T)).T/200.0)*255
        return rst.astype(np.uint8)

plgs = [RGB2Gray, '-', SplitRGB, MergeRGB, '-', RGB2HSV, HSV2RGB, '-', RGB2CIE, CIE2RGB, '-', RGB2LUV, LUV2RGB, '-', RGB2Lab, Lab2RGB, '-', RGB2XYZ, XYZ2RGB]
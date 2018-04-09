import cv2
from imagepy.core.engine import Filter

class PencilSketch(Filter):
    # cv2.edgePreservingFilter(img, flags=1, sigma_s = 50, sigma_r = 0.15)
    title = 'Pencil Sketch'
    note = ['rgb', 'auto_msk', 'not_channel', 'auto_snap', 'preview']
    para = {'sigma_s':50,'sigma_r':0.15,'factor':0.04,'color':False}

    view = [(int, (0,100), 0,  'sigma_s', 'sigma_s', 'pix'),
            (float, (0,1), 2,  'sigma_r', 'sigma_r', 'pix'),
            (float, (0,1), 2,  'factor', 'factor', ''),
            (bool, 'color', 'color')]

    def run(self, ips, snap, img, para = None):
        img.T[:] = cv2.pencilSketch(snap, sigma_s = para['sigma_s'], 
        	sigma_r = para['sigma_r'], shade_factor = para['factor'])[para['color']].T

class Stylization(Filter):
    # cv2.edgePreservingFilter(img, flags=1, sigma_s = 50, sigma_r = 0.15)
    title = 'Stylization'
    note = ['rgb', 'auto_msk', 'not_channel', 'auto_snap', 'preview']
    para = {'sigma_s':50,'sigma_r':0.15}

    view = [(int, (0,100), 0,  'sigma_s', 'sigma_s', 'pix'),
            (float, (0,1), 2,  'sigma_r', 'sigma_r', 'pix')]

    def run(self, ips, snap, img, para = None):
        return cv2.stylization(snap, sigma_s = para['sigma_s'], sigma_r = para['sigma_r'])

class DetailEnhance(Filter):
    # cv2.edgePreservingFilter(img, flags=1, sigma_s = 50, sigma_r = 0.15)
    title = 'Detail Enhance'
    note = ['rgb', 'auto_msk', 'not_channel', 'auto_snap', 'preview']
    para = {'sigma_s':50,'sigma_r':0.15}

    view = [(int, (0,100), 0,  'sigma_s', 'sigma_s', 'pix'),
            (float, (0,1), 2,  'sigma_r', 'sigma_r', 'pix')]

    def run(self, ips, snap, img, para = None):
        return cv2.detailEnhance(snap, sigma_s = para['sigma_s'], sigma_r = para['sigma_r'])

class EdgePreservingFilter(Filter):
    # cv2.edgePreservingFilter(img, flags=1, sigma_s = 50, sigma_r = 0.15)
    title = 'Edge Preserving'
    note = ['rgb', 'auto_msk', 'not_channel', 'auto_snap', 'preview']
    para = {'flags':1,'sigma_s':50,'sigma_r':0.15}

    view = [(int, (0,30), 0,  'flag', 'flags', ''),
            (int, (0,100), 0,  'sigma_s', 'sigma_s', 'pix'),
            (float, (0,1), 2,  'sigma_r', 'sigma_r', 'pix')]

    def run(self, ips, snap, img, para = None):
        return cv2.edgePreservingFilter(snap, flags=para['flags'], 
        	sigma_s = para['sigma_s'], sigma_r = para['sigma_r'])

plgs = [PencilSketch, Stylization, DetailEnhance, EdgePreservingFilter]

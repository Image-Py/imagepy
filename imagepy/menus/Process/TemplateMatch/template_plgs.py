import cv2
from imagepy.core.engine import Simple
import numpy as np

class MatchTemplate(Simple):
    title = 'Match Template'
    note = ['all']
    para = {'mat':'cv2.TM_CCOEFF','img':None}

    view = [(list, 'mat', ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'], str, 'match', ''),
            ('img', 'img', 'image', '')]

    def run(self, ips, imgs, para=None):
        down, up = ips.range
        ips2 = self.app.get_img(para['img'])
        ips.snapshot()

        sl1, sl2 = ips.slices, ips2.slices
        cn1, cn2 = ips.channels, ips2.channels

        if ips.dtype != ips2.dtype:
            return self.app.alert('Two stack must be equal dtype!')
        elif sl1 > 1 and sl2 > 1 and sl1 != sl2:
            return self.app.alert('Two stack must have equal slices!')
        elif cn1 > 1 and cn2 > 1 and cn1 != cn2:
            return self.app.alert('Two stack must have equal channels!')

        imgs1, imgs2 = ips.subimg(), ips2.subimg()

        '''    
        if len(imgs1) == 1: imgs1 = imgs1 * len(imgs2)
        if len(imgs2) == 1: imgs2 = imgs2 * len(imgs1)
        if imgs1[0].shape[:2] != imgs2[0].shape[:2]:
            return self.app.alert('Two image must be in equal shape')
        '''
        for i in range(len(imgs1)):
            im1, im2 = imgs1[i], imgs2[i]
            if cn1 == 1 and cn2 > 1:
                im2 = im2.mean(axis=-1, dtype=np.float32)
            if cn2 == 1 and cn1 > 1:
                im2 = im2[:, :, None] * np.ones(cn1)

            # 模板匹配
            res = cv2.matchTemplate(im1, im2, method=eval(para['mat']))
            # 寻找最值
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if para['mat'] in ['cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']:
                top_left = min_loc
            else:
                top_left = max_loc
            #彩色图
            cn1, cn2 = ips.channels, ips2.channels
            if cn2 == 3 and cn1 == 3:
                w, h, c = im2.shape[::]
            if cn2 == 1 and cn1 == 1:
                w, h = im2.shape[::]
            bottom_right = (top_left[0] + h, top_left[1] + w)
            cv2.rectangle(im1, top_left, bottom_right, 255, 2)

plgs = [MatchTemplate]

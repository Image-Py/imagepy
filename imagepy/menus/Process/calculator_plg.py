from sciapp.action import Simple
import numpy as np

class Plugin(Simple):
    title = 'Image Calculator'
    note = ['all']
    para = {'op':'add','img':None}
    
    view = [(list, 'op', ['max', 'min', 'diff', 'add', 'substract'], str, 'operator', ''),
            ('img', 'img', 'image', '')]
    
    def run(self, ips, imgs, para = None):
        down, up = ips.range
        ips2 = self.app.get_img(para['img'])
        ips.snapshot()

        sl1, sl2 = ips.slices, ips2.slices
        cn1, cn2 = ips.channels, ips2.channels

        if ips.dtype != ips2.dtype:
            return self.app.alert('Two stack must be equal dtype!')
        elif sl1>1 and sl2>1 and sl1!=sl2:
            return self.app.alert('Two stack must have equal slices!')
        elif cn1>1 and cn2>1 and cn1!=cn2:
            return self.app.alert('Two stack must have equal channels!')
        
        imgs1, imgs2 = ips.subimg(), ips2.subimg()
        if len(imgs1)==1: imgs1 = imgs1 * len(imgs2)
        if len(imgs2)==1: imgs2 = imgs2 * len(imgs1)
        if imgs1[0].shape[:2] != imgs2[0].shape[:2]:
            return self.app.alert('Two image must be in equal shape')

        for i in range(len(imgs1)):
            im1, im2 = imgs1[i], imgs2[i]
            if cn1==1 and cn2>1: 
                im2 = im2.mean(axis=-1, dtype=np.float32)
            if cn2==1 and cn1>1: 
                im2 = im2[:,:,None] * np.ones(cn1)

            if para['op'] == 'max':
                msk = im1 < im2
                im1[msk] = im2[msk]
            if para['op'] == 'min':
                msk = im1 > im2
                im1[msk] = im2[msk]
            if para['op'] == 'diff':
                dif = np.abs(im1.astype(np.float32) - im2)
                np.clip(dif, down, up, out=im1)
            if para['op'] == 'add':
                dif = im1.astype(np.float32) + im2
                np.clip(dif, down, up, out=im1)
            if para['op'] == 'substract':
                dif = im1.astype(np.float32) - im2
                np.clip(dif, down, up, out=im1)
from imagepy.core.engine import Filter
from imagepy.core.manager import ImageManager

import numpy as np
from sklearn.ensemble import RandomForestClassifier
import scipy.ndimage as ndimg
from skimage.filters import sobel
from skimage.feature import structure_tensor, structure_tensor_eigvals
from skimage.io import imread, imsave
import pandas as pd

def norm01(arr):
    arr -= arr.min()
    arr /= arr.max()
    return arr

# chans 是通道，可以是int，list，默认None，代表所有通道
def get_feature(img, chans=None, ocvs=3, w=1, ori=True, blr=True, sob=True, eig=True):
    feats, titles = [], []
    img = img.reshape(img.shape[:2]+(-1,))
    if chans is None: chans = range(img.shape[2])
    for c in [chans] if isinstance(chans, int) else chans:
        if ori:
            feats.append(norm01(img[:,:,c].ravel().astype(np.float32)))
            titles.append('c%d_ori'%c)
        for o in range(ocvs):
            blurimg = ndimg.gaussian_filter(img[:,:,c], 2**o, output=np.float32)
            feat_sobel = norm01(sobel(blurimg).ravel()) if sob else None
            if eig:
                Axx, Axy, Ayy = structure_tensor(blurimg, w)
                l1, l2 = structure_tensor_eigvals(Axx, Axy, Ayy)
                feat_l1, feat_l2 = norm01(l1.ravel()), norm01(l2.ravel())
            else: feat_l1 = feat_l2 = None
            feat_gauss = norm01(blurimg.ravel()) if blr else None
            featcr = [feat_gauss, feat_sobel, feat_l1, feat_l2]
            title = ['c%d_s%d_%s'%(c,o,i) for i in ['gauss', 'sobel', 'l1', 'l2']]
            titles.extend([title[i] for i in range(4) if not featcr[i] is None])
            feats.extend([featcr[i] for i in range(4) if not featcr[i] is None])
    return np.array(feats).T, titles

class Plugin(Filter):
    """Closing: derived from imagepy.core.engine.Filter """
    title = 'Random Forest Classify'
    note = ['8-bit', 'auto_msk', 'auto_snap', 'preview']
    para = {'img':None, 'ocvs':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 'eig':True}
    view = [('img', 'img', 'img', 'back'),
            (int, 'ocvs', (1,7), 0, 'ocvs', ''),
            (int, 'w', (0,5), 0, 'sigma', 'tensor'),
            (bool, 'ori', 'add image feature'),
            (bool, 'blr', 'add blur feature'),
            (bool, 'sob', 'add sobel feature'),
            (bool, 'eig', 'add eig feature')]

    def run(self, ips, snap, img, para = None):
        ori = ImageManager.get(para['img']).img
        lab = snap.ravel()
        msk = lab != 0

        lab_value = lab[msk].reshape(-1, 1)
        feats, titles = get_feature(ori, None, para['ocvs'], 
            para['w'], para['ori'], para['blr'], para['sob'], para['eig'])
        lab_feats = feats[msk]

        print(titles)

        model = RandomForestClassifier(n_estimators=100, random_state=42,
                    max_features = 'sqrt', n_jobs=-1, verbose = 1)

        model.fit(lab_feats, lab_value)
        rst = model.predict(feats)
        img[:] = rst.reshape(img.shape[:2])
        #imsave('rst.png', rstimg)
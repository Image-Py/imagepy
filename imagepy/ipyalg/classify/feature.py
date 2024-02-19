import numpy as np
import scipy.ndimage as ndimg
from skimage.filters import sobel
from skimage.feature import structure_tensor, structure_tensor_eigenvalues

# chans 是通道，可以是int，list，默认None，代表所有通道
para = {'chans':None, 'grade':2, 'w':1, 'items':['ori', 'blr', 'sob', 'eig']}

def get_feature_one(img, msk=None, para=para):
    chans, grade, w, items = para['chans'], para['grade'], para['w'], para['items']
    feats, titles = [], []
    img = img.reshape(img.shape[:2]+(-1,))
    if msk is None: msk = np.ones(img.shape[:2], dtype='bool')
    if chans is None: chans = range(img.shape[2])
    for c in [chans] if isinstance(chans, int) else chans:
        if 'ori' in items:
            feats.append(img[:,:,c][msk].astype(np.float32))
            titles.append('c%d_ori'%c)
        for o in range(grade):
            blurimg = ndimg.gaussian_filter(img[:,:,c], 2**o, output=np.float32)
            feat_sobel = sobel(blurimg)[msk] if 'sob' in items else None
            if 'eig' in items:
                Axx, Axy, Ayy = structure_tensor(blurimg, w)
                l1, l2 = structure_tensor_eigvals(Axx, Axy, Ayy)
                feat_l1, feat_l2 = l1[msk], l2[msk]
            else: feat_l1 = feat_l2 = None
            feat_gauss = blurimg[msk] if 'blr' in items else None
            featcr = [feat_gauss, feat_sobel, feat_l1, feat_l2]
            title = ['c%d_s%d_%s'%(c,o,i) for i in ['gauss', 'sobel', 'l1', 'l2']]
            titles.extend([title[i] for i in range(4) if not featcr[i] is None])
            feats.extend([featcr[i] for i in range(4) if not featcr[i] is None])
    return np.array(feats).T, titles

def make_slice(l, size, mar):
    xs = list(range(0, l, size))+[l]
    ins = np.array((xs[:-1], xs[1:])).T
    outs = np.clip(ins + [-mar, mar], 0, l)
    return outs, ins

def grid_slice(H, W, size, mar):
    h_out, h_in = make_slice(H, size, mar)
    w_out, w_in = make_slice(W, size, mar)
    out_slice, in_slice = [], []
    for rs, re in h_out:
        for cs, ce in w_out:
            out_slice.append((slice(rs, re), slice(cs, ce)))
    for rs, re in h_in:
        for cs, ce in w_in:
            in_slice.append((slice(rs, re), slice(cs, ce)))
    return out_slice, in_slice

def get_feature(imgs, labs, key=para, size=1024, callback=print):
    if not isinstance(labs, list) and labs.ndim==2:
        imgs, labs = [imgs], [labs]
    out_slice, in_slice = grid_slice(*imgs[0].shape[:2], size, 2**(key['grade']-1)*3)
    m, n = len(out_slice), len(labs)
    feats, vs = [], []
    msk = np.zeros(imgs[0].shape[:2], dtype='bool')
    for i, img, lab in zip(range(n), imgs, labs):
        for j, outs, ins in zip(range(m), out_slice, in_slice):
            callback(i*m+j, m*n)
            msk[outs] = 0; msk[ins] = 1;
            msk[outs][lab[outs]==0] = 0
            if msk[outs].sum()==0: continue
            feat, title = get_feature_one(img[outs], msk[outs], key)
            feats.append(feat)
            vs.append(lab[outs][msk[outs]])
    feats = np.vstack(feats)
    vs = np.hstack(vs).reshape((-1,1))
    mins, ptps = feat.min(axis=0), feat.ptp(axis=0)
    feats -= mins
    feats /= ptps
    para = key.copy()
    para['min'] = mins.tolist()
    para['ptp'] = ptps.tolist()
    para['titles'] = title
    return feats, vs, para

def get_predict(imgs, model, key=para, out=None, size=1024, callback=print):
    lut = {'ori':1, 'blr':key['grade'], 'sob':key['grade'], 'eig':key['grade']*2}
    chans = len(key['titles'])/sum([lut[i] for i in key['items']])
    print(chans)
    islist = isinstance(imgs, list)
    if islist and imgs[0].ndim == 2 and chans == 1: pass
    elif islist and imgs[0].shape[2] == chans: pass
    elif not islist and imgs.shape[2] == chans and imgs.ndim == 3: imgs = [imgs]
    elif not islist and imgs.ndim == 4 and imgs.shape[3] == chans: pass
    else: return None
    out_slice, in_slice = grid_slice(*imgs[0].shape[:2], size, 2**(key['grade']-1)*3)
    m, n = len(out_slice), len(imgs)
    if out is None: 
        temp = imgs[0] if imgs[0].ndim==2 else imgs[0][:,:,0]
        out = [temp.astype(np.uint8)]; out[0] *= 0;
        for i in range(1, len(imgs)): out.append(out[0].copy())
    msk = np.zeros(imgs[0].shape[:2], dtype='bool')
    for i, img, ot in zip(range(len(imgs)), imgs, out):
        for j, outs, ins in zip(range(len(out_slice)), out_slice, in_slice):
            callback(i*m+j, m*n)
            msk[outs] = 0; msk[ins] = 1;
            feat, title = get_feature_one(img[outs], msk[outs], key)
            feat -= key['min']
            feat /= key['ptp']
            labs = model.predict(feat)
            ot[ins] = labs.reshape(ot[ins].shape)
    return out

def dump_model(model, para, path):
    joblib.dump(path, (model, para))

def load_model(model, para, path):
    return joblib.load(path)

if __name__ == '__main__':
    from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
    #a, b = grid_slice(100, 80, 50, 5)
    from skimage.data import camera
    from skimage.io import imread
    import matplotlib.pyplot as plt
    import joblib
    img = imread('img.png')
    lab = imread('lab.png')
    
    #a, b = grid_slice(*img.shape, 500, 5)
    #feats = get_feature(img, lab>0)
    size = 512
    feat, lab, key = get_feature(img, lab, para, size=size)

    model = RandomForestClassifier(n_estimators=100, random_state=42,
                    max_features = 'sqrt', n_jobs=-1, verbose = 1)
    # model = AdaBoostClassifier()
    model.fit(feat, lab)
    rst = get_predict(img, model, key, size=size)
    '''
    para, model = joblib.load('a.clsf')
    rst = predict(img, model, para)
    '''
    plt.imshow(rst)
    plt.show()
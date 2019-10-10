from imagepy.core.engine import Filter
from imagepy.core.manager import ImageManager

import numpy as np
from sklearn.ensemble import RandomForestClassifier, \
    AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier,\
    GradientBoostingClassifier, VotingClassifier
from sklearn.dummy import DummyClassifier
from .features import get_feature, get_predict

model_para = None

class RandomForest(Filter):
    """Closing: derived from imagepy.core.engine.Filter """
    title = 'Random Forest Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'img':None, 'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':100, 'max_features':'sqrt', 'max_depth':0}
    view = [('img', 'img', 'img', 'back'),
            ('lab', None, '===== Classifier Parameter ====='),
            (int, 'n_estimators', (10,1024), 0, 'estimators', 'n'),
            (int, 'max_depth', (0,64), 0, 'depth', 'max'),
            (list, 'max_features', ['sqrt', 'log2', 'None'], str, 'features', 'max'),
            ('lab', None, '===== Feature Parameter ====='),
            (int, 'grade', (1,7), 0, 'grade', ''),
            (int, 'w', (0,5), 0, 'sigma', 'tensor'),
            (bool, 'ori', 'add image feature'),
            (bool, 'blr', 'add blur feature'),
            (bool, 'sob', 'add sobel feature'),
            (bool, 'eig', 'add eig feature')]

    def run(self, ips, snap, img, para = None):
        key = {'chans':None, 'grade':para['grade'], 'w':para['w']}
        key['items'] = [i for i in ['ori', 'blr', 'sob', 'eig'] if para[i]]
        ori = ImageManager.get(para['img']).img
        feat, lab, key = get_feature(ori, snap, key)
        feat_dic = {'sqrt':'sqrt', 'log2':'log2', 'None':None}
        max_depth = None if para['max_depth']==0 else para['max_depth']
        model = RandomForestClassifier(n_estimators=para['n_estimators'], 
            max_features = feat_dic[para['max_features']], max_depth=max_depth)
        model.fit(feat, lab)
        get_predict(ori, model, key, out=img)
        global model_para
        model_para = model, key

class AdaBoost(Filter):
    """Closing: derived from imagepy.core.engine.Filter """
    title = 'AdaBoost Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'img':None, 'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':50, 'learning_rate':1, 'algorithm':'SAMME.R'}
    view = [('img', 'img', 'img', 'back'),
            ('lab', None, '===== Classifier Parameter ====='),
            (int, 'n_estimators', (10,1024), 0, 'estimators', 'n'),
            (float, 'learning_rate', (0.1, 10), 1, 'learn', 'rate'),
            (list, 'algorithm', ['SAMME', 'SAMME.R'], str, 'algorithm', ''),
            ('lab', None, '===== Feature Parameter ====='),
            (int, 'grade', (1,7), 0, 'grade', ''),
            (int, 'w', (0,5), 0, 'sigma', 'tensor'),
            (bool, 'ori', 'add image feature'),
            (bool, 'blr', 'add blur feature'),
            (bool, 'sob', 'add sobel feature'),
            (bool, 'eig', 'add eig feature')]

    def run(self, ips, snap, img, para = None):
        key = {'chans':None, 'grade':para['grade'], 'w':para['w']}
        key['items'] = [i for i in ['ori', 'blr', 'sob', 'eig'] if para[i]]
        ori = ImageManager.get(para['img']).img
        feat, lab, key = get_feature(ori, snap, key)
        model = AdaBoostClassifier(n_estimators=para['n_estimators'], 
            learning_rate = para['learning_rate'], algorithm=para['algorithm'])
        model.fit(feat, lab)
        get_predict(ori, model, key, out=img)
        global model_para
        model_para = model, key

class Bagging(Filter):
    """Closing: derived from imagepy.core.engine.Filter """
    title = 'Bagging Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'img':None, 'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':50, 'max_features':1.0}
    view = [('img', 'img', 'img', 'back'),
            ('lab', None, '===== Classifier Parameter ====='),
            (int, 'n_estimators', (10,1024), 0, 'estimators', 'n'),
            (float, 'max_features', (0.2, 1), 1, 'features', 'k'),
            ('lab', None, '===== Feature Parameter ====='),
            (int, 'grade', (1,7), 0, 'grade', ''),
            (int, 'w', (0,5), 0, 'sigma', 'tensor'),
            (bool, 'ori', 'add image feature'),
            (bool, 'blr', 'add blur feature'),
            (bool, 'sob', 'add sobel feature'),
            (bool, 'eig', 'add eig feature')]

    def run(self, ips, snap, img, para = None):
        key = {'chans':None, 'grade':para['grade'], 'w':para['w']}
        key['items'] = [i for i in ['ori', 'blr', 'sob', 'eig'] if para[i]]
        ori = ImageManager.get(para['img']).img
        feat, lab, key = get_feature(ori, snap, key)
        model = BaggingClassifier(n_estimators=para['n_estimators'], 
            max_features = para['max_features'])
        model.fit(feat, lab)
        get_predict(ori, model, key, out=img)
        global model_para
        model_para = model, key

class ExtraTrees(Filter):
    """Closing: derived from imagepy.core.engine.Filter """
    title = 'ExtraTrees Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'img':None, 'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':10, 'max_features':'sqrt', 'max_depth':0}
    view = [('img', 'img', 'img', 'back'),
            ('lab', None, '===== Classifier Parameter ====='),
            (int, 'n_estimators', (10,1024), 0, 'estimators', 'n'),
            (int, 'max_depth', (0,64), 0, 'depth', 'max'),
            (list, 'max_features', ['sqrt', 'log2', 'None'], str, 'features', 'max'),
            ('lab', None, '===== Feature Parameter ====='),
            (int, 'grade', (1,7), 0, 'grade', ''),
            (int, 'w', (0,5), 0, 'sigma', 'tensor'),
            (bool, 'ori', 'add image feature'),
            (bool, 'blr', 'add blur feature'),
            (bool, 'sob', 'add sobel feature'),
            (bool, 'eig', 'add eig feature')]

    def run(self, ips, snap, img, para = None):
        key = {'chans':None, 'grade':para['grade'], 'w':para['w']}
        key['items'] = [i for i in ['ori', 'blr', 'sob', 'eig'] if para[i]]
        ori = ImageManager.get(para['img']).img
        feat, lab, key = get_feature(ori, snap, key)
        feat_dic = {'sqrt':'sqrt', 'log2':'log2', 'None':None}
        max_depth = None if para['max_depth']==0 else para['max_depth']
        model = ExtraTreesClassifier(n_estimators=para['n_estimators'], 
            max_features = feat_dic[para['max_features']], max_depth=max_depth)
        model.fit(feat, lab)
        get_predict(ori, model, key, out=img)
        global model_para
        model_para = model, key

class GradientBoosting(Filter):
    """Closing: derived from imagepy.core.engine.Filter """
    title = 'Gradient Boosting Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'img':None, 'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':100, 'max_features':'sqrt', 
            'max_depth':3, 'learning_rate':0.1, 'loss':'deviance'}
    view = [('img', 'img', 'img', 'back'),
            ('lab', None, '===== Classifier Parameter ====='),
            (list, 'loss', ['deviance', 'exponential'], str, 'loss', ''),
            (int, 'n_estimators', (10,1024), 0, 'estimators', 'n'),
            (int, 'max_depth', (1,10), 0, 'depth', 'max'),
            (float, 'learning_rate', (0.1, 10), 1, 'learn', 'rate'),
            (list, 'max_features', ['sqrt', 'log2', 'None'], str, 'features', 'max'),
            ('lab', None, '===== Feature Parameter ====='),
            (int, 'grade', (1,7), 0, 'grade', ''),
            (int, 'w', (0,5), 0, 'sigma', 'tensor'),
            (bool, 'ori', 'add image feature'),
            (bool, 'blr', 'add blur feature'),
            (bool, 'sob', 'add sobel feature'),
            (bool, 'eig', 'add eig feature')]

    def run(self, ips, snap, img, para = None):
        key = {'chans':None, 'grade':para['grade'], 'w':para['w']}
        key['items'] = [i for i in ['ori', 'blr', 'sob', 'eig'] if para[i]]
        ori = ImageManager.get(para['img']).img
        feat, lab, key = get_feature(ori, snap, key)
        feat_dic = {'sqrt':'sqrt', 'log2':'log2', 'None':None}
        model = GradientBoostingClassifier(n_estimators=para['n_estimators'], 
            loss=para['loss'], max_features = feat_dic[para['max_features']], 
            max_depth=para['max_depth'], learning_rate=para['learning_rate'])
        model.fit(feat, lab)
        get_predict(ori, model, key, out=img)
        global model_para
        model_para = model, key

class Voting(Filter):
    """Closing: derived from imagepy.core.engine.Filter """
    title = 'Voting Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'img':None, 'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':100, 'max_features':'sqrt', 
            'max_depth':3, 'learning_rate':0.1, 'loss':'deviance'}
    view = [('img', 'img', 'img', 'back'),
            ('lab', None, '===== Classifier Parameter ====='),
            (list, 'loss', ['deviance', 'exponential'], str, 'loss', ''),
            (int, 'n_estimators', (10,1024), 0, 'estimators', 'n'),
            (int, 'max_depth', (1,10), 0, 'depth', 'max'),
            (float, 'learning_rate', (0.1, 10), 1, 'learn', 'rate'),
            (list, 'max_features', ['sqrt', 'log2', 'None'], str, 'features', 'max'),
            ('lab', None, '===== Feature Parameter ====='),
            (int, 'grade', (1,7), 0, 'grade', ''),
            (int, 'w', (0,5), 0, 'sigma', 'tensor'),
            (bool, 'ori', 'add image feature'),
            (bool, 'blr', 'add blur feature'),
            (bool, 'sob', 'add sobel feature'),
            (bool, 'eig', 'add eig feature')]

    def run(self, ips, snap, img, para = None):
        key = {'chans':None, 'grade':para['grade'], 'w':para['w']}
        key['items'] = [i for i in ['ori', 'blr', 'sob', 'eig'] if para[i]]
        ori = ImageManager.get(para['img']).img
        feat, lab, key = get_feature(ori, snap, key)
        feat_dic = {'sqrt':'sqrt', 'log2':'log2', 'None':None}
        model = VotingClassifier(n_estimators=para['n_estimators'], 
            loss=para['loss'], max_features = feat_dic[para['max_features']], 
            max_depth=para['max_depth'], learning_rate=para['learning_rate'])
        model.fit(feat, lab)
        get_predict(ori, model, key, out=img)
        global model_para
        model_para = model, key

plgs = [RandomForest, ExtraTrees, Bagging, AdaBoost, GradientBoosting]
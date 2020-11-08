from sciapp.action import Filter, Simple
from sciapp.object import Image

import numpy as np
from sklearn.ensemble import RandomForestClassifier, \
    AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier,\
    GradientBoostingClassifier, VotingClassifier
from sklearn.dummy import DummyClassifier
from imagepy.ipyalg import feature

model_para = None

class Base(Simple):
    """Closing: derived from sciapp.action.Filter """
    def load(self, ips):
        print("len(ips.imgs) = ", len(ips.imgs))
        if len(ips.imgs)==1: ips.snapshot()
        return True

    def preview(self, ips, para): 
        if len(ips.imgs)==1: 
            ips.img[:] = ips.snap
            self.run(ips, ips.imgs, para, True)
        return True

    def cancel(self, ips): 
        if len(ips.imgs)==1: ips.swap()

    def classify(self, para): pass

    def run(self, ips, imgs, para = None, preview=False):
        if len(ips.imgs)==1: ips.img[:] = ips.snap
        key = {'chans':None, 'grade':para['grade'], 'w':para['w']}
        key['items'] = [i for i in ['ori', 'blr', 'sob', 'eig'] if para[i]]
        slir, slic = ips.rect
        labs = [i[slir, slic] for i in imgs]
        ori = ips.back.imgs
        oris = [i[slir, slic] for i in ori]

        self.app.info('extract features...')
        feat, lab, key = feature.get_feature(oris, labs, key, callback=self.progress)

        self.app.info('training data...')
        # self.progress(None, 1)
        model = self.classify(para)
        model.fit(feat, lab)

        self.app.info('predict data...')
        if preview:
            return feature.get_predict(oris, model, key, labs, callback=self.progress)
        if len(imgs) == 1: ips.swap()
        outs = feature.get_predict(oris, model, key, callback=self.progress)
        nips = Image(outs, ips.title+'rst')
        nips.range, nips.lut = ips.range, ips.lut
        nips.back, nips.mode = ips.back, 0.4
        self.app.show_img(nips)
        global model_para
        model_para = model, key

class RandomForest(Base):
    title = 'Random Forest Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':100, 'max_features':'sqrt', 'max_depth':0}
    view = [('lab', None, '===== Classifier Parameter ====='),
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

    def classify(self, para):
        feat_dic = {'sqrt':'sqrt', 'log2':'log2', 'None':None}
        max_depth = None if para['max_depth']==0 else para['max_depth']
        return RandomForestClassifier(n_estimators=para['n_estimators'], 
            max_features = feat_dic[para['max_features']], max_depth=max_depth)

class AdaBoost(Base):
    """Closing: derived from sciapp.action.Filter """
    title = 'AdaBoost Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':50, 'learning_rate':1, 'algorithm':'SAMME.R'}
    view = [('lab', None, '===== Classifier Parameter ====='),
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

    def classify(self, para):
        return AdaBoostClassifier(n_estimators=para['n_estimators'], 
            learning_rate = para['learning_rate'], algorithm=para['algorithm'])

class Bagging(Base):
    """Closing: derived from sciapp.action.Filter """
    title = 'Bagging Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':50, 'max_features':1.0}
    view = [('lab', None, '===== Classifier Parameter ====='),
            (int, 'n_estimators', (10,1024), 0, 'estimators', 'n'),
            (float, 'max_features', (0.2, 1), 1, 'features', 'k'),
            ('lab', None, '===== Feature Parameter ====='),
            (int, 'grade', (1,7), 0, 'grade', ''),
            (int, 'w', (0,5), 0, 'sigma', 'tensor'),
            (bool, 'ori', 'add image feature'),
            (bool, 'blr', 'add blur feature'),
            (bool, 'sob', 'add sobel feature'),
            (bool, 'eig', 'add eig feature')]

    def classify(self, para):
        return BaggingClassifier(n_estimators=para['n_estimators'], 
            max_features = para['max_features'])

class ExtraTrees(Base):
    """Closing: derived from sciapp.action.Filter """
    title = 'ExtraTrees Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':10, 'max_features':'sqrt', 'max_depth':0}
    view = [('lab', None, '===== Classifier Parameter ====='),
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

    def classify(self, para):
        feat_dic = {'sqrt':'sqrt', 'log2':'log2', 'None':None}
        max_depth = None if para['max_depth']==0 else para['max_depth']
        return ExtraTreesClassifier(n_estimators=para['n_estimators'], 
            max_features = feat_dic[para['max_features']], max_depth=max_depth)

class GradientBoosting(Base):
    """Closing: derived from sciapp.action.Filter """
    title = 'Gradient Boosting Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':100, 'max_features':'sqrt', 
            'max_depth':3, 'learning_rate':0.1, 'loss':'deviance'}
    view = [('lab', None, '===== Classifier Parameter ====='),
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

    def classify(self, para):
        feat_dic = {'sqrt':'sqrt', 'log2':'log2', 'None':None}
        return GradientBoostingClassifier(n_estimators=para['n_estimators'], 
            loss=para['loss'], max_features = feat_dic[para['max_features']], 
            max_depth=para['max_depth'], learning_rate=para['learning_rate'])

class Voting(Base):
    """Closing: derived from sciapp.action.Filter """
    title = 'Voting Classify'
    note = ['8-bit', 'auto_msk', 'not_slice', 'auto_snap', 'preview']
    para = {'grade':3, 'w':1, 'ori':True, 'blr':True, 'sob':True, 
            'eig':True, 'n_estimators':100, 'max_features':'sqrt', 
            'max_depth':3, 'learning_rate':0.1, 'loss':'deviance'}
    view = [('lab', None, '===== Classifier Parameter ====='),
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

    def classify(self, para):
        feat_dic = {'sqrt':'sqrt', 'log2':'log2', 'None':None}
        return VotingClassifier(n_estimators=para['n_estimators'], 
            loss=para['loss'], max_features = feat_dic[para['max_features']], 
            max_depth=para['max_depth'], learning_rate=para['learning_rate'])

plgs = [RandomForest, ExtraTrees, Bagging, AdaBoost, GradientBoosting]
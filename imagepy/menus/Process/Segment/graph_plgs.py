from sciapp.action import Simple
from skimage import data, io, segmentation, color
from skimage.future import graph
import numpy as np

class RagThreshold(Simple):
    title = 'RAG Threshold'
    note = ['all', 'preview']
    
    para = {'lab':None, 'thresh':10, 'connect':'8-connected', 'mode':'distance', 'sigma':255.0, 'stack':False}
    view = [('img', 'lab', 'label', ''),
            (int, 'thresh', (1, 1024), 0, 'threshold', ''),
            (list, 'connect', ['4-connected', '8-connected'], str, 'connectivity', ''),
            (list, 'mode', ['distance', 'similarity'], str, 'mode', ''),
            (float, 'sigma', (0, 1024), 1, 'sigma', 'similarity'),
            (bool, 'stack', 'stack')]

    def load(self, ips): return ips.snapshot()==None
    def cancel(self, ips): ips.swap()

    def preview(self, ips, para):
        lab = self.app.get_img(para['lab']).img
        connect = ['4-connected', '8-connected'].index(para['connect']) + 1
        g = graph.rag_mean_color(ips.snap, lab, connect, para['mode'], para['sigma'])
        lab = graph.cut_threshold(lab, g, para['thresh'])
        ips.img[:] = color.label2rgb(lab, ips.snap, kind='avg')

    def run(self, ips, imgs, para = None):
        if not para['stack']: 
            imgs, labs = [ips.img], [self.app.get_img(para['lab']).img]
        else:
            labs = self.app.get_img(para['lab']).imgs
            if len(imgs) != len(labs): 
                labs = [self.app.get_img(para['lab']).img] * len(imgs)
        for i in range(len(imgs)):
            img, lab = imgs[i], labs[i]
            connect = ['4-connected', '8-connected'].index(para['connect']) + 1
            g = graph.rag_mean_color(img, lab, connect, para['mode'], para['sigma'])
            lab = graph.cut_threshold(lab, g, para['thresh'])
            img[:] = color.label2rgb(lab, img, kind='avg')
            self.progress(i, len(imgs))

class NormalCut(Simple):
    title = 'RAG Cut Normalized'
    note = ['all', 'preview']
    
    para = {'lab':None, 'thresh':0.001, 'num':10, 'connect':'8-connected', 'mode':'distance', 'sigma':255.0, 'stack':False}
    view = [('img', 'lab', 'label', ''),
            (float, 'thresh', (0.001, 1), 3, 'threshold', ''),
            (int, 'num', (1, 1024), 0, 'num', 'cut'),
            (list, 'connect', ['4-connected', '8-connected'], str, 'connectivity', ''),
            (list, 'mode', ['distance', 'similarity'], str, 'mode', ''),
            (float, 'sigma', (0, 1024), 1, 'sigma', 'similarity'),
            (bool, 'stack', 'stack')]

    def load(self, ips): return ips.snapshot()==None
    def cancel(self, ips): ips.swap()

    def preview(self, ips, para):
        lab = self.app.get_img(para['lab']).img
        connect = ['4-connected', '8-connected'].index(para['connect']) + 1
        g = graph.rag_mean_color(ips.snap, lab, connect, para['mode'], para['sigma'])
        lab = graph.cut_normalized(lab, g, para['thresh'], para['num'])
        ips.img[:] = color.label2rgb(lab, ips.snap, kind='avg')

    def run(self, ips, imgs, para = None):
        if not para['stack']: 
            imgs, labs = [ips.img], [self.app.get_img(para['lab']).img]
        else:
            labs = self.app.get_img(para['lab']).imgs
            if len(imgs) != len(labs): 
                labs = [self.app.get_img(para['lab']).img] * len(imgs)
        for i in range(len(imgs)):
            img, lab = imgs[i], labs[i]
            connect = ['4-connected', '8-connected'].index(para['connect']) + 1
            g = graph.rag_mean_color(img, lab, connect, para['mode'], para['sigma'])
            lab = graph.cut_normalized(lab, g, para['thresh'], para['num'])
            img[:] = color.label2rgb(lab, img, kind='avg')
            self.progress(i, len(imgs))

def _weight_mean_color(graph, src, dst, n):
    diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}

def merge_mean_color(graph, src, dst):
    graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
    graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
    graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                     graph.nodes[dst]['pixel count'])

class MergeHierarchical(Simple):
    title = 'RAG Merge Hierarchical'
    note = ['all', 'preview']
    
    para = {'lab':None, 'thresh':35, 'connect':'8-connected', 'mode':'distance', 'sigma':255.0, 'stack':False}
    view = [('img', 'lab', 'label', ''),
            (int, 'thresh', (1, 1024), 0, 'threshold', ''),
            (list, 'connect', ['4-connected', '8-connected'], str, 'connectivity', ''),
            (list, 'mode', ['distance', 'similarity'], str, 'mode', ''),
            (float, 'sigma', (0, 1024), 1, 'sigma', 'similarity'),
            (bool, 'stack', 'stack')]

    def load(self, ips): return ips.snapshot()==None
    def cancel(self, ips): ips.swap()

    def preview(self, ips, para):
        lab = self.app.get_img(para['lab']).img
        connect = ['4-connected', '8-connected'].index(para['connect']) + 1
        g = graph.rag_mean_color(ips.snap, lab, connect, para['mode'], para['sigma'])
        lab = graph.merge_hierarchical(lab, g, thresh=para['thresh'], rag_copy=False,
                in_place_merge=True, merge_func=merge_mean_color, weight_func=_weight_mean_color)
        ips.img[:] = color.label2rgb(lab, ips.snap, kind='avg')

    def run(self, ips, imgs, para = None):
        if not para['stack']: 
            imgs, labs = [ips.img], [self.app.get_img(para['lab']).img]
        else:
            labs = self.app.get_img(para['lab']).imgs
            if len(imgs) != len(labs): 
                labs = [self.app.get_img(para['lab']).img] * len(imgs)
        for i in range(len(imgs)):
            img, lab = imgs[i], labs[i]
            connect = ['4-connected', '8-connected'].index(para['connect']) + 1
            g = graph.rag_mean_color(img, lab, connect, para['mode'], para['sigma'])
            lab = graph.merge_hierarchical(lab, g, thresh=para['thresh'], rag_copy=False,
                in_place_merge=True, merge_func=merge_mean_color, weight_func=_weight_mean_color)
            img[:] = color.label2rgb(lab, img, kind='avg')
            self.progress(i, len(imgs))

plgs = [RagThreshold, NormalCut, MergeHierarchical]
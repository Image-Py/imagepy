from scipy.misc import imread
import scipy.ndimage as ndimg
from skimage.morphology import skeletonize_3d
from glob import glob
import numpy as np
norm = np.linalg.norm
import sys
sys.path.append('C:/Users/54631/Documents/projects/imagepy/imagepy/ipyalg/graph')
sys.path.append('C:/Users/54631/Documents/projects/imagepy/imagepy/core')

import sknw, myvi
from itertools import combinations

def angles(graph):
    for s in graph.nodes():
        o = graph.node[s]['o']
        x = graph[s]
        if len(x)<=1: continue
        rst = []
        for e in x:
            eds = x[e]
            for ed in eds:
                l = eds[ed]['pts']
                if len(l)<10: continue
                if norm(l[0]-o)>norm(l[-1]-o): l=l[::-1]
                p1, p2 = l[0], l[5]
                rst.append((s, e, p2-p1))
        if len(rst)<2:continue
        com = combinations(range(len(rst)), 2)
        for i1, i2 in com:
            v1, v2 = rst[i1][2], rst[i2][2]
            a = np.arccos(np.dot(v1, v2)/norm(v1)/norm(v2))
            print(rst[i1][1], rst[i1][0], rst[i2][1], a)
    

fs = glob('C:/Users/54631/Documents/resorce/imgs/vessel/*.bmp')
imgs = np.array([imread(i) for i in fs], dtype=np.uint8)

imgs = ndimg.gaussian_filter(imgs, 2)>64
imgs = skeletonize_3d(imgs)

graph = sknw.build_sknw(imgs, True)
angs = angles(graph)


balls, rs = [], []
for idx in graph.nodes():
    balls.append(graph.node[idx]['o'])
xs, ys, zs = [], [], []
lxs, lys, lzs = [], [], []
for (s, e) in graph.edges():
    eds = graph[s][e]
    st, ed = graph.node[s]['o'], graph.node[e]['o']
    lxs.append([st[0],ed[0]])
    lys.append([st[1],ed[1]])
    lzs.append([st[2],ed[2]])
    for i in eds:
        pts = eds[i]['pts']
        xs.append(pts[:,0])
        ys.append(pts[:,1])
        zs.append(pts[:,2])

rs = [2] * len(balls)
cs = tuple(np.array((1,0,0)))
vts, fs, ns, cs = myvi.build_balls(balls, rs, cs)

txs, tys, tzs = [], [], []
for n in graph.nodes():
    o = graph.node[n]['o']
    x = graph[n]
    if len(x)<=1: continue
    for i in x:
        eds = x[i]
        for ed in eds:
            l = eds[ed]['pts']
            if len(l)<10: continue
            if norm(l[0]-o)>norm(l[-1]-o): l=l[::-1]
            txs.append([l[0][0], l[5][0]*2-l[0][0]])
            tys.append([l[0][1], l[5][1]*2-l[0][1]])
            tzs.append([l[0][2], l[5][2]*2-l[0][2]])

manager = myvi.Manager()
manager.add_obj('balls', vts, fs, ns, cs)
cs = tuple(np.array((0,0,1)))
vts, fs, ns, cs = myvi.build_lines(xs, ys, zs, cs)
obj = manager.add_obj('lines', vts, fs, ns, cs)
obj.set_style(mode='grid')
vts, fs, ns, cs = myvi.build_lines(lxs, lys, lzs, (0,1,0))
obj = manager.add_obj('vector', vts, fs, ns, cs)
obj.set_style(mode='grid')
vts, fs, ns, cs = myvi.build_lines(txs, tys, tzs, (1,1,0))
obj = manager.add_obj('tlines', vts, fs, ns, cs)
obj.set_style(mode='grid')
manager.show()

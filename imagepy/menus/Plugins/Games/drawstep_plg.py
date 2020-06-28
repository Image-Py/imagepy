from skimage.io import imread
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
from imagepy.ipyalg import distance_transform_edt
import numpy as np
from imagepy.ipyalg.graph import sknw
from sciapp.action import Simple


def draw_pixs(img, xs, ys, color=None):
    mskx = (xs>=0) * (xs<img.shape[1])
    msky = (ys>=0) * (ys<img.shape[0])
    msk = mskx * msky
    if color == None:color = ColorManager.get_front()
    img[ys[msk], xs[msk]] = color
        
def draw_point(img, x, y, r=1, color=255):
    shape = img.shape
    x, y = np.round((x,y)).astype(np.int)
    if x<0 or y<0 or x>=shape[1] or y>=shape[0]: return
    if color == None:color = ColorManager.get_front()
    if r==1: img[y,x] = color
    n = int(r)
    xs,ys = np.mgrid[-n:n+1,-n:n+1]
    msk = np.sqrt(xs**2+ys**2)<r
    draw_pixs(img, xs[msk]+x, ys[msk]+y, color)
        
def stroke(img, xs, ys, rs):
    for x,y,r in zip(xs, ys, rs):
        draw_point(img, x, y, r+1)

def draw_edge(img, dis, pts):
    xs, ys = pts[:,1], pts[:,0]
    rs = dis[ys, xs]
    stroke(img, xs, ys, rs)

def build_graph(graph, dis, step=True):
    ls = [np.zeros(dis.shape, dtype=np.uint8)]
    for (s, e) in graph.edges():
        eds = graph[s][e]
        for i in eds:
            if step:ls.append(ls[-1].copy())
            pts = eds[i]['pts']
            ptss = graph.nodes[s]['pts']
            ptse = graph.nodes[e]['pts']
            pts = np.vstack((ptss,pts,ptse))
            draw_edge(ls[-1], dis, pts)
    return ls if step else ls[0]

def build(msk):
    dis = distance_transform_edt(msk)
    ske = skeletonize(msk>128)
    graph = sknw.build_sknw(ske, True)
    rst = build_graph(graph, dis, True)
    return rst

class Plugin(Simple):
    title = 'Stroke Step'
    note = ['8-bit']

    def run(self, ips, imgs, para = None):
        rst = build(ips.img)
        print(len(rst))
        print(rst[0].shape)
        IPy.show_img(rst, 'ips.title-%s'%'stroke')
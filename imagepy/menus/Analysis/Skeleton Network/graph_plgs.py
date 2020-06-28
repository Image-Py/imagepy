from sciapp.action import Filter, Simple
from imagepy.ipyalg.graph import sknw
import numpy as np
from numpy.linalg import norm
import networkx as nx, wx
from numba import jit
import pandas as pd
from sciapp.object import mark2shp

def graph_mark(graph):
    ids = graph.nodes()
    pts = [graph.nodes[i]['o'] for i in ids]
    pts = {'type':'points', 'body':[(i[1], i[0]) for i in pts]}
    txt = [(a,b,str(c)) for (a,b),c in zip(pts['body'], ids)]
    txt = {'type':'texts', 'body':txt}
    return mark2shp({'type':'layer', 'body':[pts, txt]})

class BuildGraph(Filter):
    title = 'Build Graph'
    note = ['8-bit', 'not_slice', 'not_channel', 'auto_snap']

    #process
    def run(self, ips, snap, img, para = None):
        ips.data = sknw.build_sknw(img, True)
        sknw.draw_graph(img, ips.data)
        ips.mark = graph_mark(ips.data)

class Statistic(Simple):
    title = 'Graph Statistic'
    note = ['all']

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            self.app.alert("Please build graph!");
            return False;
        return True;

    def run(self, ips, imgs, para = None):
        edges, nodes = [], []
        ntitles = ['PartID', 'NodeID', 'Degree','X', 'Y']
        etitles = ['PartID', 'StartID', 'EndID', 'Length']
        k, unit = ips.unit
        comid = 0
        # for g in nx.connected_components(ips.data):
        #     for idx in g.nodes():
        for g in [ips.data.subgraph(c).copy() for c in nx.connected_components(ips.data)]:
            for idx in g.nodes():
                o = g.nodes[idx]['o']
                print(idx, g.degree(idx))
                nodes.append([comid, idx, g.degree(idx), round(o[1]*k,2), round(o[0]*k,2)])
            for (s, e) in g.edges():
                eds = g[s][e]
                for i in eds:
                    edges.append([comid, s, e, round(eds[i]['weight']*k, 2)])
            comid += 1

        self.app.show_table(pd.DataFrame(nodes, columns=ntitles), ips.title+'-nodes')
        self.app.show_table(pd.DataFrame(edges, columns=etitles), ips.title+'-edges')

class Sumerise(Simple):
    title = 'Graph Summarise'
    note = ['all']

    para = {'parts':False}
    view = [(bool, 'parts', 'parts')]

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            self.app.alert("Please build graph!");
            return False;
        return True;

    def run(self, ips, imgs, para = None):
        titles = ['PartID', 'Noeds', 'Edges', 'TotalLength', 'Density', 'AveConnect']
        k, unit = ips.unit
        
        gs = [ips.data.subgraph(c).copy() for c in nx.connected_components(ips.data)] if para['parts'] else [ips.data]
        comid, datas = 0, []
        for g in gs:
            sl = 0
            for (s, e) in g.edges():
                sl += sum([i['weight'] for i in g[s][e].values()])
            datas.append([comid, g.number_of_nodes(), g.number_of_edges(), round(sl*k, 2), 
                round(nx.density(g), 2), round(nx.average_node_connectivity(g),2)][1-para['parts']:])
            comid += 1
        # print('======datas=========', datas)
        # print('======columns=========', titles[1-para['parts']:])
        self.app.show_table(pd.DataFrame(datas, columns=titles[1-para['parts']:]), ips.title+'-graph')

class CutBranch(Filter):
    title = 'Cut Branch'
    note = ['8-bit', 'not_slice', 'not_channel', 'auto_snap', 'preview']

    para = {'lim':10, 'rec':False}
    view = [(int, 'lim', (0,1e6), 0, 'limit', 'uint'),
            (bool, 'rec', 'recursion')]

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            self.app.alert("Please build graph!");
            return False;
        self.buf = ips.data
        return True;

    def run(self, ips, snap, img, para = None):
        g = ips.data = self.buf.copy()
        k, unit = ips.unit
        while True:
            rm = []
            for i in g.nodes():
                if g.degree(i)!=1:continue
                s,e = list(g.edges(i))[0]
                if g[s][e][0]['weight']*k<=para['lim']:
                    rm.append(i)
            g.remove_nodes_from(rm)
            if not para['rec'] or len(rm)==0:break
        img *= 0
        sknw.draw_graph(img, g)

    def cancel(self, ips):
        if 'auto_snap' in self.note:
            ips.swap()
            ips.update()
        ips.data = self.buf

class RemoveIsolate(Filter):
    title = 'Remove Isolate Node'
    note = ['all', 'not_slice', 'not_channel', 'auto_snap']

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            self.app.alert("Please build graph!");
            return False;
        return True;

    def run(self, ips, snap, img, para = None):
        g = ips.data
        for n in list(g.nodes()):
            if len(g[n])==0: g.remove_node(n)
        img *= 0
        sknw.draw_graph(img, g)
        ips.mark = graph_mark(ips.data)

class Remove2Node(Simple):
    title = 'Remove 2Path Node'
    note = ['all']

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            self.app.alert("Please build graph!");
            return False;
        return True;

    def run(self, ips, imgs, para = None):
        g = ips.data
        for n in list(g.nodes()):
            if len(g[n])!=2 or n in g[n]: continue 
            (k1, e1), (k2, e2) = g[n].items()
            if isinstance(g, nx.MultiGraph):
                if len(e1)!=1 or len(e2)!=1: continue
                e1, e2 = e1[0], e2[0]
            l1, l2 = e1['pts'], e2['pts']
            d1 = norm(l1[0]-g.nodes[n]['o']) > norm(l1[-1]-g.nodes[n]['o'])
            d2 = norm(l2[0]-g.nodes[n]['o']) < norm(l2[-1]-g.nodes[n]['o'])
            pts = np.vstack((l1[::[-1,1][d1]], l2[::[-1,1][d2]]))
            l = np.linalg.norm(pts[1:]-pts[:-1], axis=1).sum()
            g.remove_node(n)
            g.add_edge(k1, k2, pts=pts, weight=l)
        ips.img[:] = 0
        sknw.draw_graph(ips.img, g)
        ips.mark = graph_mark(ips.data)

@jit(nopython=True)
def floodfill(img, x, y):
    buf = np.zeros((131072,2), dtype=np.uint16)
    color = img[int(y), int(x)]
    img[int(y), int(x)] = 0
    buf[0,0] = x; buf[0,1] = y;
    cur = 0; s = 1;

    while True:
        xy = buf[cur]
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                cx = xy[0]+dx; cy = xy[1]+dy
                if cx<0 or cx>=img.shape[1]:continue
                if cy<0 or cy>=img.shape[0]:continue
                if img[cy, cx]!=color:continue
                img[cy, cx] = 0
                buf[s,0] = cx; buf[s,1] = cy
                s+=1
                if s==len(buf):
                    buf[:len(buf)-cur] = buf[cur:]
                    s -= cur; cur=0
        cur += 1
        if cur==s:break

class CutROI(Filter):
    title = 'Cut By ROI'
    note = ['8-bit', 'req_roi', 'not_slice', 'not_channel', 'auto_snap', 'preview']

    def run(self, ips, snap, img, para = None):
        msk = ips.mask(3) * (img>0)
        r,c = np.where(msk)
        for x,y in zip(c,r):
            if img[y,x]>0:
                floodfill(img, x, y)
        
class ShortestPath(Simple):
    title = 'Graph Shortest Path'
    note = ['all']

    para = {'start':0, 'end':1}
    view = [(int, 'start', (0,1e8), 0, 'start', 'id'),
            (int, 'end',   (0,1e8), 0, 'end', 'id')]

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            self.app.alert("Please build graph!");
            return False;
        return True;

    def run(self, ips, imgs, para = None):
        nodes = nx.shortest_path(ips.data, source=para['start'], target=para['end'], weight='weight')
        path = zip(nodes[:-1], nodes[1:])
        paths = []
        for s,e in path:
            ps = ips.data[s][e].values()
            pts = sorted([(i['weight'], i['pts']) for i in ps])
            paths.append(((s,e), pts[0]))
        sknw.draw_graph(ips.img, ips.data)

        for i in paths:
            ips.img[i[1][1][:,0], i[1][1][:,1]] = 255

        data = [(a[0], a[1], b[0]) for a,b in paths]
        self.app.show_table(pd.DataFrame(data, columns=['from','to','l']), 'shortest-path')



plgs = [BuildGraph, Statistic, Sumerise, '-', RemoveIsolate, Remove2Node, CutBranch, CutROI, '-', ShortestPath]
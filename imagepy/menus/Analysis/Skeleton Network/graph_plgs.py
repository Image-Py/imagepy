from imagepy.core.engine import Filter, Simple
from imagepy.ipyalg.graph import sknw
import numpy as np
import networkx as nx, wx
from imagepy import IPy
from numba import jit

# build   statistic  sumerise   cut  edit
class Mark:
    def __init__(self, graph):
        self.graph = graph

    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((255,255,0), width=3, style=wx.SOLID))
        dc.SetTextForeground((255,255,0))
        font = wx.Font(8, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        dc.SetFont(font)

        ids = self.graph.nodes()
        pts = [self.graph.node[i]['o'] for i in ids]
        pts = [f(i[1], i[0]) for i in pts]
        dc.DrawPointList(pts)
        dc.DrawTextList([str(i) for i in ids], pts)

class BuildGraph(Filter):
    title = 'Build Graph'
    note = ['8-bit', 'not_slice', 'not_channel', 'auto_snap']

    #process
    def run(self, ips, snap, img, para = None):
        ips.data = sknw.build_sknw(img, True)
        sknw.draw_graph(img, ips.data)
        ips.mark = Mark(ips.data)

class Statistic(Simple):
    title = 'Graph Statistic'
    note = ['all']

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            IPy.alert("Please build graph!");
            return False;
        return True;

    def run(self, ips, imgs, para = None):
        edges, nodes = [], []
        ntitles = ['PartID', 'NodeID', 'Degree','X', 'Y']
        etitles = ['PartID', 'StartID', 'EndID', 'Length']
        k, unit = ips.unit
        comid = 0
        for g in nx.connected_component_subgraphs(ips.data, False):
            for idx in g.nodes():
                o = g.node[idx]['o']
                print(idx, g.degree(idx))
                nodes.append([comid, idx, g.degree(idx), round(o[1]*k,2), round(o[0]*k,2)])
            for (s, e) in g.edges():
                eds = g[s][e]
                for i in eds:
                    edges.append([comid, s, e, round(eds[i]['weight']*k, 2)])
            comid += 1

        IPy.table(ips.title+'-nodes', nodes, ntitles)
        IPy.table(ips.title+'-edges', edges, etitles)

class Sumerise(Simple):
    title = 'Graph Summarise'
    note = ['all']

    para = {'parts':False}
    view = [(bool, 'parts', 'parts')]

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            IPy.alert("Please build graph!");
            return False;
        return True;

    def run(self, ips, imgs, para = None):
        titles = ['PartID', 'Noeds', 'Edges', 'TotalLength', 'Density', 'AveConnect']
        k, unit = ips.unit
        
        gs = nx.connected_component_subgraphs(ips.data, False) if para['parts'] else [ips.data]
        comid, datas = 0, []
        for g in gs:
            sl = 0
            for (s, e) in g.edges():
                sl += sum([i['weight'] for i in g[s][e].values()])
            datas.append([comid, g.number_of_nodes(), g.number_of_edges(), round(sl*k, 2), 
                round(nx.density(g), 2), round(nx.average_node_connectivity(g),2)][1-para['parts']:])
            comid += 1
        print(titles, datas)
        IPy.table(ips.title+'-graph', datas, titles[1-para['parts']:])

class CutBranch(Filter):
    title = 'Cut Branch'
    note = ['8-bit', 'not_slice', 'not_channel', 'auto_snap', 'preview']

    para = {'lim':10, 'rec':False}
    view = [(int, (0,1e6), 0, 'limit', 'lim', 'uint'),
            (bool, 'recursion', 'rec')]

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            IPy.alert("Please build graph!");
            return False;
        return True;

    def run(self, ips, snap, img, para = None):
        g = ips.data.copy()
        k, unit = ips.unit
        while True:
            rm = []
            for i in g.nodes():
                if g.degree(i)!=1:continue
                s,e = g.edges(i)[0]
                if g[s][e][0]['weight']*k<=para['lim']:
                    rm.append(i)
            g.remove_nodes_from(rm)
            if not para['rec'] or len(rm)==0:break
        img *= 0
        sknw.draw_graph(img, g)

class RemoveIsolate(Filter):
    title = 'Remove Isolate Node'
    note = ['all']

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            IPy.alert("Please build graph!");
            return False;
        return True;

    def run(self, ips, snap, img, para = None):
        g = ips.data
        for n in g.nodes():
            if len(g[n])==0: g.remove_node(n)
        img *= 0
        sknw.draw_graph(img, g)

@jit
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
    note = ['8-bit', 'not_slice', 'not_channel', 'auto_snap', 'preview']

    def run(self, ips, snap, img, para = None):
        msk = ips.get_msk(3) * (img>0)
        r,c = np.where(msk)
        for x,y in zip(c,r):
            if img[y,x]>0:
                floodfill(img, x, y)
        
class ShortestPath(Simple):
    title = 'Graph Shortest Path'
    note = ['all']

    para = {'start':0, 'end':1}
    view = [(int, (0,1e8), 0, 'start', 'start', 'id'),
            (int, (0,1e8), 0, 'end', 'end', 'id')]

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            IPy.alert("Please build graph!");
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
            IPy.write('%s-%s:%.4f'%(i[0][0], i[0][1], i[1][0]), 'ShortestPath')
        IPy.write('Nodes:%s, Length:%.4f'%(len(nodes), sum([i[1][0] for i in paths])), 'ShortestPath')



plgs = [BuildGraph, Statistic, Sumerise, '-', RemoveIsolate, CutBranch, CutROI, '-', ShortestPath]
from sciapp.action import Filter, Simple
from imagepy.ipyalg.graph import sknw
from skimage.morphology import skeletonize_3d
from itertools import combinations
import networkx as nx
import numpy as np
import pandas as pd
from sciapp.object import Mesh, TextSet
from sciapp.util import meshutil
norm = np.linalg.norm

class Skeleton3D(Simple):
	title = 'Skeleton 3D'
	note = ['8-bit', 'stack3d']

	#process
	def run(self, ips, imgs, para = None):
		imgs[skeletonize_3d(imgs>0)==0] = 0

class BuildGraph(Simple):
	title = 'Build Graph 3D'
	note = ['8-bit', 'stack3d']

	#process
	def run(self, ips, imgs, para = None):
		ips.data = sknw.build_sknw(imgs, True)
		sknw.draw_graph(imgs, ips.data)

class Show3DGraph(Simple):
	title = 'Show Graph 3D'
	note = ['8-bit', 'stack3d']

	para = {'r':1, 'ncolor':(255,0,0), 'lcolor':(0,0,255), 'pcolor':(0,255,0)}
	view = [(int, 'r', (1,100), 0, 'radius', 'pix'),
			('color', 'ncolor', 'node', 'rgb'),
			('color', 'lcolor', 'line', 'rgb'),
			('color', 'pcolor', 'path', 'rgb')]

	def run(self, ips, imgs, para = None):
		balls, ids, rs, graph = [], [], [], ips.data
		for idx in graph.nodes():
			ids.append(idx)
			balls.append(graph.nodes[idx]['o'])
		xs, ys, zs = [], [], []
		lxs, lys, lzs = [], [], []
		for (s, e) in graph.edges():
			eds = graph[s][e]
			st, ed = graph.nodes[s]['o'], graph.nodes[e]['o']
			lxs.append([st[0],ed[0]])
			lys.append([st[1],ed[1]])
			lzs.append([st[2],ed[2]])
			for i in eds:
				pts = eds[i]['pts']
				xs.append(pts[:,0])
				ys.append(pts[:,1])
				zs.append(pts[:,2])

		rs = [para['r']] * len(balls)
		cs = tuple(np.array(para['ncolor'])/255.0)
		vts, fs, cs = meshutil.create_balls(balls, rs, cs)
		self.app.show_mesh(Mesh(verts=vts, faces=fs, colors=cs), 'balls')

		cs = tuple(np.array(para['lcolor'])/255.0)
		vts, fs, cs = meshutil.create_lines(xs, ys, zs, cs)
		self.app.show_mesh(Mesh(verts=vts, faces=fs, colors=cs, mode='grid'), 'path')

		cs = tuple(np.array(para['pcolor'])/255.0)
		vts, fs, cs = meshutil.create_lines(lxs, lys, lzs, cs)
		self.app.show_mesh(Mesh(verts=vts, faces=fs, colors=cs, mode='grid'), 'lines')
		
		self.app.show_mesh(TextSet(['ID:%s'%i for i in ids], verts=balls, size=para['r']*256, colors=(1,1,1)), 'txt')



class Show3DGraphR(Simple):
	title = 'Show Graph R 3D'
	note = ['8-bit', 'stack3d']

	para = {'dis':None, 'ncolor':(255,0,0), 'lcolor':(0,0,255), 'pcolor':(0,255,0)}
	view = [('img', 'dis', 'distance', 'map'),
			('color', 'ncolor', 'node', 'rgb'),
			('color', 'lcolor', 'line', 'rgb'),
			('color', 'pcolor', 'path', 'rgb')]
	#process
	def run(self, ips, imgs, para = None):
		dis = self.app.get_img(para['dis']).imgs
		balls, ids, rs, graph = [], [], [], ips.data
		for idx in graph.nodes():
			ids.append(idx)
			balls.append(graph.nodes[idx]['o'])

		xs, ys, zs = [], [], []
		v1s, v2s = [], []
		for (s, e) in graph.edges():
			eds = graph[s][e]
			st, ed = graph.nodes[s]['o'], graph.nodes[e]['o']
			v1s.append(st)
			v2s.append(ed)
			for i in eds:
				pts = eds[i]['pts']
				xs.append(pts[:,0])
				ys.append(pts[:,1])
				zs.append(pts[:,2])

		rs1 = dis[list(np.array(v1s).astype(np.int16).T)]
		rs2 = dis[list(np.array(v2s).astype(np.int16).T)]
		rs1 = list(np.clip(rs1, 2, 1e4)*0.5)
		rs2 = list(np.clip(rs2, 2, 1e4)*0.5)
		rs = dis[list(np.array(balls).astype(np.int16).T)]
		rs = list(np.clip(rs, 2, 1e4))

		print(balls, rs1, rs2, rs)

		cs = tuple(np.array(para['ncolor'])/255.0)
		vts, fs, ns, cs = surfutil.build_balls(balls, rs, cs)
		self.app.show_mesh(Surface(vts, fs, ns, cs), 'balls')

		meansize = sum(rs)/len(rs)
		vts, fs, pos, h, color = surfutil.build_marks(['ID:%s'%i for i in ids], balls, rs, meansize, (1,1,1))
		self.app.show_mesh(MarkText(vts, fs, pos, h, color), 'txt')

		cs = tuple(np.array(para['lcolor'])/255.0)
		vts, fs, ns, cs = surfutil.build_lines(xs, ys, zs, cs)
		self.app.show_mesh(Surface(vts, fs, ns, cs, mode='grid'), 'path')

		cs = tuple(np.array(para['pcolor'])/255.0)
		vts, fs, ns, cs = surfutil.build_arrows(v1s, v2s, rs1, rs2, 0, 0, cs)
		self.app.show_mesh(Surface(vts, fs, ns, cs), 'lines')

class Statistic(Simple):
	title = 'Graph Statistic 3D'
	note = ['all']

	def load(self, ips):
		if not isinstance(ips.data, nx.MultiGraph):
			IPy.alert("Please build graph!");
			return False;
		return True;

	def run(self, ips, imgs, para = None):
		edges, nodes = [], []
		ntitles = ['PartID', 'NodeID', 'Degree','X', 'Y', 'Z']
		etitles = ['PartID', 'StartID', 'EndID', 'Length', 'Distance']
		k, unit = ips.unit
		comid = 0
		for g in nx.connected_component_subgraphs(ips.data, False):
			for idx in g.nodes():
				o = g.nodes[idx]['o']
				nodes.append([comid, idx, g.degree(idx), round(o[1]*k,2), round(o[0]*k,2), round(o[2])])
			for (s, e) in g.edges():
				eds = g[s][e]
				for i in eds:
					l = round(eds[i]['weight']*k, 2)
					dis = round(np.linalg.norm(g.nodes[s]['o']-g.nodes[e]['o'])*k, 2)
					edges.append([comid, s, e, l, dis])
			comid += 1

		IPy.show_table(pd.DataFrame(nodes, columns=ntitles), ips.title+'-nodes')
		IPy.show_table(pd.DataFrame(edges, columns=etitles), ips.title+'-edges')

class Sumerise(Simple):
	title = 'Graph Summarise 3D'
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
		IPy.show_table(pd.DataFrame(datas, columns=titles[1-para['parts']:]), ips.title+'-graph')

class Angles(Simple):
	title = 'Graph Angles Count 3D'
	note = ['all']

	def load(self, ips):
		if not isinstance(ips.data, nx.MultiGraph):
			IPy.alert("Please build graph!");
			return False;
		return True;

	def run(self, ips, imgs, para = None):
		titles = ['P1', 'P2', 'P3', 'angle']
		k, unit = ips.unit
		graph = ips.data
		datas = []
		for s in graph.nodes():
			o = graph.nodes[s]['o']
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
				datas.append([rst[i1][1], rst[i1][0], rst[i2][1], round(a,4)])

		print(titles, datas)
		IPy.show_table(pd.DataFrame(datas, columns=titles), ips.title+'-graph')

class CutBranch(Simple):
	title = 'Graph Cut Branch 3D'
	note = ['all']

	para = {'lim':10, 'rec':False}
	view = [(int, 'lim', (0,1e6), 0, 'limit', 'uint'),
			(bool, 'rec', 'recursion')]

	def load(self, ips):
		if not isinstance(ips.data, nx.MultiGraph):
			IPy.alert("Please build graph!");
			return False;
		return True;

	def run(self, ips, imgs, para = None):
		g = ips.data
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
		imgs *= 0
		sknw.draw_graph(imgs, g)

class RemoveIsolate(Simple):
	title = 'Remove Isolate 3D'
	note = ['all']

	def load(self, ips):
		if not isinstance(ips.data, nx.MultiGraph):
			IPy.alert("Please build graph!");
			return False;
		return True;

	def run(self, ips, imgs, para = None):
		g = ips.data
		for n in list(g.nodes()):
			if len(g[n])==0: g.remove_node(n)
		imgs *= 0
		sknw.draw_graph(imgs, g)

class Remove2Node(Simple):
    title = 'Remove 2Path Node 3D'
    note = ['all']

    def load(self, ips):
        if not isinstance(ips.data, nx.MultiGraph):
            IPy.alert("Please build graph!");
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
        imgs *= 0
        sknw.draw_graph(imgs, g)

plgs = [Skeleton3D, BuildGraph, '-', CutBranch, RemoveIsolate, Remove2Node, '-', Statistic, Sumerise, '-', Show3DGraph, Show3DGraphR]
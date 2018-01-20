from imagepy.core.engine import Filter, Simple
from imagepy.ipyalg.graph import sknw
from skimage.morphology import skeletonize_3d
from itertools import combinations

from imagepy.core import myvi
from imagepy import IPy
import networkx as nx
import numpy as np
norm = np.linalg.norm


class Skeleton3D(Simple):
	title = 'Skeleton 3D'
	note = ['8-bit', 'stack3d']

	#process
	def run(self, ips, imgs, para = None):
		imgs[:] = skeletonize_3d(imgs>0)

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

	para = {'r':1, 'ncolor':(255,0,0), 'lcolor':(0,0,255)}
	view = [(int, (1,100), 0, 'radius', 'r', 'pix'),
			('color', 'node', 'ncolor', 'rgb'),
			('color', 'line', 'lcolor', 'rgb')]

	def load(self, ips):
		if not isinstance(ips.data, nx.MultiGraph):
			IPy.alert("Please build graph!");
			return False;
		self.frame = myvi.Frame3D.figure(IPy.curapp, title='3D Canvas')
		return True;

	#process
	def run(self, ips, imgs, para = None):
		balls, ids, rs, graph = [], [], [], ips.data
		for idx in graph.nodes():
			ids.append(idx)
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

		rs = [para['r']] * len(balls)
		cs = tuple(np.array(para['ncolor'])/255.0)
		vts, fs, ns, cs = myvi.build_balls(balls, rs, cs)
		self.frame.viewer.add_surf_asyn('balls', vts, fs, ns, cs)

		vts, fs, pos, h, color = myvi.build_marks(['ID:%s'%i for i in ids], balls, para['r'], para['r'], (1,1,1))
		self.frame.viewer.add_mark_asyn('txt', vts, fs, pos, h, color)

		cs = tuple(np.array(para['lcolor'])/255.0)
		vts, fs, ns, cs = myvi.build_lines(xs, ys, zs, cs)
		self.frame.viewer.add_surf_asyn('paths', vts, fs, ns, cs, mode='grid')
		vts, fs, ns, cs = myvi.build_lines(lxs, lys, lzs, (0,1,0))
		self.frame.viewer.add_surf_asyn('lines', vts, fs, ns, cs, mode='grid')
		self.frame.Raise()
		self.frame = None

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
				o = g.node[idx]['o']
				nodes.append([comid, idx, g.degree(idx), round(o[1]*k,2), round(o[0]*k,2), round(o[2])])
			for (s, e) in g.edges():
				eds = g[s][e]
				for i in eds:
					l = round(eds[i]['weight']*k, 2)
					dis = round(np.linalg.norm(g.node[s]['o']-g.node[e]['o'])*k, 2)
					edges.append([comid, s, e, l, dis])
			comid += 1

		IPy.table(ips.title+'-nodes', nodes, ntitles)
		IPy.table(ips.title+'-edges', edges, etitles)

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
		IPy.table(ips.title+'-graph', datas, titles[1-para['parts']:])

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
				datas.append([rst[i1][1], rst[i1][0], rst[i2][1], round(a,4)])

		print(titles, datas)
		IPy.table(ips.title+'-graph', datas, titles)

class CutBranch(Simple):
	title = 'Graph Cut Branch 3D'
	note = ['all']

	para = {'lim':10, 'rec':False}
	view = [(int, (0,1e6), 0, 'limit', 'lim', 'uint'),
			(bool, 'recursion', 'rec')]

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
				s,e = g.edges(i)[0]
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
		for n in g.nodes():
			if len(g[n])==0: g.remove_node(n)
		imgs *= 0
		sknw.draw_graph(imgs, g)

plgs = [Skeleton3D, BuildGraph, '-', CutBranch, RemoveIsolate, '-', Statistic, Sumerise, '-', Show3DGraph]
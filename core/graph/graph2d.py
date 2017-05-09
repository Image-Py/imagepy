class Graph:
    def __init__(self, nodes, arcs):
        self.nodes = {}
        self.arcs = {}
        self.net = {}
        for i in range(len(nodes)):
            self.add_node(i, nodes[i])
        for i in range(len(arcs)):
            self.add_arc(*((i,)+arcs[i]))

    def add_node(self, nid, obj):
        self.nodes[nid] = obj
        self.net[nid] = []

    def add_arc(self, aid, s, e, l, obj):
        self.arcs[aid] = (s, e, obj)
        self.net[s].append((e, l, aid))
        self.net[e].append((s, l, aid))

    def remove_node(self, nid):
        self.nodes.pop(nid)
        arcs = self.net[nid]
        for nd, l, aid in arcs:
            self.remove_arc(aid)
        del self.net[nid]

    def remove_arc(self, aid):
        s,e,obj = self.arcs.pop(aid)
        self.net[s] = [i for i in self.net[s] if i[0]!=e]
        self.net[e] = [i for i in self.net[e] if i[0]!=s]

def draw(graph, img):
    for i in list(graph.arcs.values()):
        img[i[2][:,0],i[2][:,1]] = 128
    for i in list(graph.nodes.values()):
        img[i] = 255

def cut(graph):
    lst = []
    for i in list(graph.net.keys()):
        if len(graph.net[i])==1:
            lst.append(i)
    for i in lst:
        graph.remove_node(i)
    return lst
    
def ring(graph):
    while len(cut(graph))>0:pass
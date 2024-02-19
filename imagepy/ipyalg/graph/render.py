import random

def node_render(conmap, n=4, rand=10, shuffle=True):
    nodes = list(conmap.keys())
    colors = dict(zip(nodes, [0]*len(nodes)))
    counter = dict(zip(nodes, [0]*len(nodes)))
    if shuffle: random.shuffle(nodes)
    while len(nodes)>0:
        k = nodes.pop(0)
        counter[k] += 1
        hist = [1e4] + [0] * n
        for p in conmap[k]:
            hist[colors[p]] += 1
        if min(hist)==0:
            colors[k] = hist.index(min(hist))
            counter[k] = 0
            continue
        hist[colors[k]] = 1e4
        minc = hist.index(min(hist))
        if counter[k]==rand:
            counter[k] = 0
            minc = random.randint(1,4)
        colors[k] = minc
        for p in conmap[k]:
            if colors[p] == minc:
                nodes.append(p)
    return colors
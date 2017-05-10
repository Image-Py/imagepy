def find_path(graph, start, end, nodes=[], arcs=[], s=0):
    nodes = nodes + [start]
    if start == end:
        return s, nodes, arcs
    if start not in graph:
        return None
    for node in graph[start]:
        #print(node)
        if node[0] not in nodes:
            newpath = find_path(graph, node[0], end, nodes, arcs+[node[2]], s+node[1])
            if newpath:
                return newpath
    return None

def find_all_paths(graph, start, end, nodes=[], arcs=[], s=0):
    nodes = nodes + [start]
    if start == end:
        return [(s, nodes, arcs)]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node[0] not in nodes:
            newpaths = find_all_paths(graph, node[0], end, nodes, arcs+[node[2]], s+node[1])
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def find_shortest_path(graph, start, end, nodes=[], arcs=[], s=0):
    nodes = nodes + [start]
    if start == end:
        return s, nodes, arcs
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node[0] not in nodes:
            newpath = find_shortest_path(graph, node[0], end, nodes, arcs+[node[2]], s+node[1])
            if newpath:
                if not shortest or newpath[0] < shortest[0]:
                    shortest = newpath   
    return shortest
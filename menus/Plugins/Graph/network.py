def find_path(graph, start, end, path=[], s=0):
    path = path + [start]
    if start == end:return s, path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node[0], end[0], path, s+node[1])
            if newpath:return newpath
    return None

def find_all_paths(graph, start, end, path=[], s=0):
    path = path + [start]
    if start == end:return [(s, path)]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node[0], end[0], path, s+node[1])
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def find_shortest_path(graph, start, end, path=[], s=0):
    path = path + [start]
    if start == end:
        return s, path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node[0], end[0], path, s+node[1])
            if newpath:
                if not shortest or s < shortest[0]:
                    shortest = newpath
    return shortest

graph = {'A': [('B', 4), ('C', 3),('D', 0)],
        'B': [('C', 1), ('D',3)],
        'C': [('D', 2)],
        'D': [('C', 6)],
        'E': [('F', 4)],
        'F': [('C', 1)]}

if __name__ == '__main__':
    path = find_path(graph, 'A', 'D')
    print path
    
    paths = find_all_paths(graph, 'A', 'D')
    print paths
    
    spath = find_shortest_path(graph, 'A', 'D')
    print spath
    
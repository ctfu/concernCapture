# Created at: Dec 16, 2016    
# Provided with a source class, trace through all its calling classes
# imported file format: class1;class2;label
import fileinput
import math

adjList = {}
visited = {}
vertex = []
dominate = {}
source = '_START_'

for line in fileinput.input():
  tokens = line.rstrip('\n').split(';')
  if "dashed" not in tokens[2]:
   #get all the unique nodes
    if tokens[0] not in visited:
      visited[tokens[0]] = False
    if tokens[1] not in visited:
      visited[tokens[1]] = False
    #build the adjacency list
    if tokens[0] in adjList:
      adjList[tokens[0]].append(tokens[1])
    else:
      adjList[tokens[0]] = [tokens[1]]
    if tokens[1] not in adjList:
      adjList[tokens[1]] = []

for k in visited:
    vertex.append(k)


def set_unvisited(vertex, visited):
    for node in vertex:
        visited[node] = False


def dfs_visite(adjList, visited, source):
    if (not visited[source]):
        visited[source] = True
        for v in adjList[source]:
            if(not visited[v]):
                dfs_visite(adjList, visited, v)


def count_dominatee(visited):
    donimatee = []
    for node in vertex:
        if (not visited[node]):
            donimatee.append(node)

    return donimatee


def dominate_list(adjList, vertex, visited, source):
    set_unvisited(vertex, visited)

    for node in vertex:
        visited[node] = True
        dfs_visite(adjList, visited, source)
        dominate[node] = count_dominatee(visited)
        set_unvisited(vertex, visited)

def dominate_tree(dominate, visited, source):
    visited[source] = True
    for v in dominate[source]:
        if (not visited[v]):
            print source, "->", v
            dominate_tree(dominate, visited, v)

dominate_list(adjList, vertex, visited, source)


set_unvisited(vertex, visited)

#generating dot file
print "digraph grpah {"
print "overlap=false"

dominate_tree(dominate, visited, source)

print "}"

from collections import defaultdict

import json

class Node:

    def __init__(self):
        self.index = -1
        self.children = {}
        self.children_letter = {}
        self.score_change = 0
        self.letter = "-"
    def load_json(self, j):
        self.index = j['index']
        self.score_change = j['score']
        self.letter = j['letter']
        self.children = {}
        self.children_letter = {}
        childs = j['children']
        for child in childs:
            self.children[int(child)] = childs[child]
        childsL = j['children_letter']
        for child in childsL:
            self.children_letter[int(child)] = childsL[child]
        
    def to_json(self):
        return {"index": self.index, "children_letter": self.children_letter, "children": self.children, "score": self.score_change, "letter": self.letter}
    
    def __repr__(self) -> str:
        return f'{self.index}'
    
tempNodes = {}
nodes = {}

def reverse_path(pred, at):
    path = []
    while at != 0:
        path.append(at)
        at = pred.get(at)
        if at is None:    
            break
    return [None] + path[::-1]

with open("uni_data.json", "r") as f:
#with open("test_data.json", "r") as f:
    tempNodes = json.loads(f.read().strip())
for node in tempNodes:
    nd = tempNodes[node]
    nn = Node()
    nn.load_json(nd)
    nodes[int(node)] = nn
tempNodes = None

dups = {38: {'9': [394, 239]}, 171: {'J': [361, 597]}, 238: {'v': [2, 548]}, 131: {'f': [588, 277]}, 306: {'m': [459, 367]}, 72: {'x': [143, 180]}, 482: {'n': [262, 343, 25]}, 180: {'M':
 [203, 114]}, 339: {'H': [431, 18]}, 505: {'J': [310, 567]}, 125: {'n': [272, 472]}, 472: {'Q': [592, 306]}, 277: {'3': [36, 238]}, 548: {'b': [199, 141, 561]}, 289: {'1': [9, 464
, 338, 314]}, 367: {'6': [390, 428, 339]}}

for father in dups.keys():
    curr_dup = list(dups[father].values())[0]
    fatherId = father
    fatherObj = nodes[fatherId]
    _1ChildId = curr_dup[0]
    _1ChildObj = nodes[_1ChildId]

    if len(curr_dup) > 1:
        _2ChildId = curr_dup[1]
        _2ChildObj = nodes[_2ChildId]

        new_node1 = Node()
        new_node1.index = 1000000 + fatherId * 1000 + _2ChildId                             #my index
        nodes[new_node1.index] = new_node1                                                  #store into nodes
        new_node1.letter = ''                                                               #my letter
        new_node1.score_change = _1ChildObj.score_change                                    #my weight = X
        new_node1.children[_2ChildId] = fatherObj.children[_2ChildId]                       #my children = y
        new_node1.children_letter[_2ChildId] = ''                                           #my children = y letter
        fatherObj.children[new_node1.index] = fatherObj.children[_1ChildId]                 #set me as a child
        fatherObj.children_letter[new_node1.index] = fatherObj.children_letter[_1ChildId]     #set me as a child letter
        del fatherObj.children[_2ChildId]                                                  #dels y child
        del fatherObj.children_letter[_2ChildId]                                           #dels y letter


    if len(curr_dup) > 2:
        _3ChildId = curr_dup[2]
        _3ChildObj = nodes[_3ChildId]

        new_node2 = Node()
        new_node2.index = 1000000 + fatherId * 1000 + _3ChildId                         #my index
        nodes[new_node2.index] = new_node2                                              #store into nodes
        new_node2.letter = ''                                                           #my letter
        new_node2.score_change = _2ChildObj.score_change                                #my weight = y
        new_node2.children[_3ChildId] = fatherObj.children[_3ChildId]                      #my children = z
        new_node2.children_letter[_3ChildId] = ''                                       #my children = z letter
        new_node1.children[new_node2.index] = new_node1.children[_2ChildId]                #set me as a child
        new_node1.children_letter[new_node2.index] = new_node1.children_letter[_2ChildId]  #set me as a child letter
        del fatherObj.children[_3ChildId]                                                  #dels z child
        del fatherObj.children_letter[_3ChildId]                                           #dels z letter

    if len(curr_dup) > 3:
        _4ChildId = curr_dup[3]
        _4ChildObj = nodes[_4ChildId]

        new_node3 = Node()
        new_node3.index = 1000000 + fatherId * 1000 + _4ChildId                         #my index
        nodes[new_node3.index] = new_node3                                              #store into nodes
        new_node3.letter = ''                                                           #my letter
        new_node3.score_change = _3ChildObj.score_change                                #my weight = z
        new_node3.children[_4ChildId] = fatherObj.children[_4ChildId]                      #my children = k
        new_node3.children_letter[_4ChildId] = ''                                           #my children = k letter
        new_node2.children[new_node3.index] = new_node2.children[_3ChildId]                #set me as a child
        new_node2.children_letter[new_node3.index] = new_node2.children_letter[_3ChildId]  #set me as a child letter
        del fatherObj.children[_4ChildId]                                                  #dels k child
        del fatherObj.children_letter[_4ChildId]                                           #dels k letter



# Perform a topological sort of the graph
def topological_sort(graph):
    visited = set()
    sorted_nodes = []

    def visit(node):
        if node not in visited:
            visited.add(node)
            for successor in graph[node]:
                visit(successor)
            sorted_nodes.append(node)

    for node in graph:
        visit(node)

    return sorted_nodes[::-1]

# Find the longest path in a directed acyclic graph
def longest_path(graph, weights):
    sorted_nodes = topological_sort(graph)
    dist = defaultdict(lambda: float('-inf'))
    dist[sorted_nodes[0]] = 0
    predecessors = {}
    for node in sorted_nodes:
        for successor in graph[node]:
            new_max = max(dist[successor], dist[node] + weights[(node, successor)])
            if new_max != dist[successor]:
                predecessors[successor] = node
            dist[successor] = new_max
            

    return predecessors, dist

def get_flag_from_path(path):
    flag = "L"
    score = 0x30B
    #score = 0
    for p in range(1, len(path)):
        # print(path[p])
        print(path[p-1], "->", path[p], nodes[path[p-1]].children_letter[path[p]])
        print(path[p], nodes[path[p]].letter)
        flag += nodes[path[p-1]].children_letter[path[p]]
        score += nodes[path[p-1]].children[path[p]]
        if nodes[path[p]].letter != "-":
            flag += nodes[path[p]].letter
            score += nodes[path[p]].score_change
    return flag, score

def get_path(successors, start, end):
    at = start
    path = []
    while at != end:
        path.append(at)
        at = successors[at]
    return path

# for node in nodes.keys():
#     if nodes[node].score_change > 0:
#         # print(node, nodes[node].score_change)
#         for n2 in nodes.keys():
#             if nodes[n2].children.get(node) != None:
#                 # print("---", n2, nodes[n2].children[node])
#                 nodes[n2].children[node] += nodes[node].score_change 
#                 # print("---", n2, nodes[n2].children[node])
       
graph_alt = {}
weights_alt = {}
for node in nodes.keys():
    graph_alt[node] = list(nodes[node].children.keys())

for node in nodes.keys():
    for child in nodes[node].children.keys():   
        if nodes[node].score_change == 0:
            weights_alt[(node, child)] = nodes[node].children[child]
        else:    
            weights_alt[(node, child)] = nodes[node].children[child] + nodes[node].score_change




# Example graph
# graph = {
#     'A': ['B', 'C'],
#     'B': ['D', 'E'],
#     'C': ['E'],
#     'D': [],
#     'E': []
# }

# weights = {
#     ('A', 'B'): 2,
#     ('A', 'C'): 4,
#     ('B', 'D'): 3,
#     ('B', 'E'): 1,
#     ('C', 'E'): 4
# }

predecessors, dist = longest_path(graph_alt, weights_alt)

# print(predecessors)

path = reverse_path(predecessors, at=599)
path[0] = 0
print(path)
print(get_flag_from_path(path))
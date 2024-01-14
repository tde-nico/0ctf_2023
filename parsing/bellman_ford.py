#import ida_funcs
import re
import json
from pprint import pprint

funcs = []
die_funcs = [1, 2, 5, 8, 9, 26, 36, 41, 48, 53, 57, 106, 120, 138, 141, 143, 154, 155, 165, 176, 199, 255, 262, 270, 272, 284, 292, 343, 360, 361, 366, 378, 390, 394, 403, 404, 411, 419, 426, 432, 446, 458, 459, 464, 484, 491, 507, 510, 531, 575, 588, 592, 110, 126, 129, 166, 174, 177, 203, 209, 214, 234, 276, 29, 301, 310, 326, 338, 346, 37, 371, 381, 399, 428, 431, 455, 473, 502, 511, 525, 570, 67, 98]
body_letters = {}
SCORE = 779

class Node:

	def __init__(self):
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
		return f'{self.index}[{self.score_change}]'


nodes = {}

#'''
with open("uni_data.json", "r") as f:
	tempNodes = json.load(f)
for node in tempNodes:
	nd = tempNodes[node]
	nn = Node()
	nn.load_json(nd)
	nodes[int(node)] = nn
tempNodes = None


'''
def iterate_function_symbols():
	# Get the first function
	func_qty = ida_funcs.get_func_qty()

	# Iterate through all functions
	for func_index in range(func_qty):
		# Get the function at the current index
		func = ida_funcs.getn_func(func_index)
		func_name = ida_funcs.get_func_name(func.start_ea)
		if 'eat_body' in func_name:
			funcs.append((func_name, func.start_ea, func.end_ea))

# Run the function to iterate through all function symbols
iterate_function_symbols()

def convertNoFromInstr(instr):
	no = int(instr.split("eax, ")[1].split("h")[0], 16)
	if((no & 0x80000000) != 0):
		no = (((no & 0xffffffff) ^ 0xffffffff) & 0xffffffff) + 1
		no = -no #ugly ass
	no = -no
	return no

REGEX_ID = re.compile(r'eat_body(\d+)_?(\d+)?17h')

LETTER_INSTR_OFF = 0x2b
SCORE_INSTR_OFF =  0xf6
SCORE_OR_TAG_MAIN_OFF = 0x31
TAG_MAIN_NO_SCORE_OFF = 0x4b

for func_name, func_start, func_end in funcs:

	match = REGEX_ID.search(func_name)
	if not match:
		continue
	id = int(match.group(1))
	id2 = match.group(2)

	if id not in nodes:
		node = node = id in nodes and nodes[id] or Node()
		node.index = id
		nodes[id] = node

	if id2 is not None:	
		# ++++++++++++++++++++ ARCO
		id2 = int(id2)

		letter = GetDisasm(func_start + LETTER_INSTR_OFF).split("; \"")[1][0]
		instr = GetDisasm(func_start + SCORE_INSTR_OFF)
		no = convertNoFromInstr(instr)
				
		node = id2 in nodes and nodes[id2] or Node()
		node.index = id2
		nodes[id2] = node
		# nodes[id].children[id2] = (letter, no)
		nodes[id].children[id2] = no
		nodes[id].children_letter[id2] = letter

	else:
		# ++++++++++++++++++++ NODO
		if id != 0:  
			instr = GetDisasm(func_start + SCORE_OR_TAG_MAIN_OFF)  
			if instr.startswith("sub"):
				# ++++++++++++++++++++ NODO MODIFY SCORE
				no = convertNoFromInstr(instr)
				letter = GetDisasm(func_start + TAG_MAIN_NO_SCORE_OFF).split("; \"")[1][0]
			else:
				# ++++++++++++++++++++ NODO *not* MODIFY SCORE
				letter = GetDisasm(func_start + SCORE_OR_TAG_MAIN_OFF).split("; \"")[1][0]
				no = 0
			nodes[id].letter = letter
			nodes[id].score_change = no
#'''

for node in nodes.keys():
	if nodes[node].score_change > 0:
		for n2 in nodes.keys():
			if nodes[n2].children.get(node) != None:
				nodes[n2].children[node] += nodes[node].score_change 


# pprint(nodes)
# print()

exit(0)

def bellman_ford(graph, source):
	dist, pred = dict(), dict()
	for node in graph:
		dist[node], pred[node] = float('-inf'), None
	dist[source] = 0


	for _ in range(len(graph) - 1):
		for node in graph:
			for to in graph[node]:
				if dist[to] < dist[node] + graph[node][to]:
					dist[to] = dist[node] + graph[node][to]
					pred[to] = node

	return dist, pred


def reverse_path(pred, at):
	path = []
	while at != 0:
		path.append(at)
		at = pred.get(at)
		if at is None:	
			break
	return [0] + path[::-1]


def get_flag_from_path(path):
	flag = "L"
	score = 0x30B
	for p in range(1, len(path)):
		flag += nodes[path[p-1]].children_letter[path[p]]
		score += nodes[path[p-1]].children[path[p]]
		if nodes[path[p]].letter != "-":
			flag += nodes[path[p]].letter
			score += nodes[path[p]].score_change
	return flag, score


def retrive_letters(path):
	string = ''
	for i in range(len(path) - 1):
		string += nodes[path[i]].children_letter[path[i+1]]
	return string


graph_bell = {node: nodes[node].children for node in nodes.keys()}
dist, pred = bellman_ford(graph_bell, source=0)
# pprint(dist)
# print()

'''
from pwn import *
from tqdm import tqdm
context.log_level = "ERROR"


for i in tqdm(range(0xff * 3)):
	path = reverse_path(pred, 599)
	s, score = get_flag_from_path(path)
	if i > 0xff:
		i = i - 0xff
		if i > 0xff:
			i = i - 0xff
			h = hex(i)[2:].rjust(2, '0') + 'ffff'
		else:
			h = hex(i)[2:].rjust(4, '0') + 'ff'
	else:
		h = hex(i)[2:].rjust(6, '0')
	try:
		r = process(['./parser_1e5451a5579d477d7dd2645f30d52a89', f'flag{{000000{s}}}'])
		rec = r.recv()
		if b'cannot' in rec:
			continue
		print(rec, f'flag{{000000{s}}}')
		r.close()
	except Exception as e:
		print(e)
	continue
	
exit()
'''

so = sorted(dist.items(), key=lambda x: (x[1], x[0]), reverse=True)
for item in so:
	if item[0] not in die_funcs:
		if not len(nodes[item[0]].children):
			print(item, f"SCORE={SCORE}")
			path = reverse_path(pred, at=item[0])
			retrive_letters(path)

#print(dist[592])
#pprint(dist)

'''
prev = 0
for i in range(len(path)):
	a = dist[path[i]] - prev
	print(a)
	prev = dist[path[i]]
'''

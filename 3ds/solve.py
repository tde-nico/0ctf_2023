from pwn import xor
from z3 import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

first_chunk = [
	0x6E, 0x2D, 0xED, 0xB4, 0x6A, 0x38, 0x97, 0xE3, 0x8B, 0xE7, 
	0x9D, 0x88, 0x91, 0xF6, 0x7B, 0x09, 0x62, 0xD9, 0x30, 0x0D, 
	0xC9, 0xE2, 0x87, 0x6F, 0x87, 0xA6, 0x53, 0x9B, 0xF8, 0x3C, 
	0x68, 0x91, 0x31, 0x00, 0x0A, 0xBD, 0xC2, 0xD2, 0xA7, 0xCC, 
	0x90
]

data = [-931626546, 886623296, 47397842068, -1212729222, -1104171678, -1440082573074, 527742953, -853677479, -260549124889, 1843940972, -794149381, 12042406621, -1367876832, 1552157482, 74851120326, -1562249026, 1147535664, 31096645624, 217360410, -1887097899, -284419408899, -970829113, -195729545, -721881416656, 1021242599, -706431767, 548620353326, 2052069571, 490269330, 1039231305208, -1568934698, -281815686, -783486852278, -1707988910, -1429269448, -986501763292, 1464978064, -586020306, 609116272274, 455533695, 448721399, 658195523992, -688637683, 308588200, -261717635379]


for j in range(0, len(data), 9):
	s = Solver()

	int_1 = BitVec('int_1', 8*8)
	int_2 = BitVec('int_2', 8*8)

	v4 = data[j:j+3*3]
	for i in range(0, 9, 3):
		v5 = int_1 * v4[i] + v4[i+1] * int_2
		v_pair = v4[i+2]

		#v_pair = bytes_to_long(v_pair[4:] + v_pair[:4])
		#print(v5 == v_pair, i)
		s.add(v5 == v_pair)


	if s.check() == sat:
		m = s.model()
		print(m)

	else:
		print('Unsat')

'''
key = bytes.fromhex('08418cd311')

LEN = 41

#for i in range(LEN):
print(xor(first_chunk, key))
'''
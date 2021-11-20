import math as m
import sys


inf= sys.maxint
S=7
V=[1,2,4,6,9]

def AlgoOptimise(S, V):
	k = len(V)
	M = [[0 for x in range(k+1)] for y in range(S+1)]

	for s in range(1, S+1):
		M[s][0] = inf

	for i in range(1, k+1):
		for s in range(1, S+1):
			terme2 = inf
			if (s-V[i-1]>=0):
				terme2 = M[s-V[i-1]][i]+1
			M[s][i] = min(M[s][i-1], terme2)
	return M

def AlgoOptimiseTab(S,V):
	k = len(V)
	M = [[([0 for l in range(x)],0)for x in range(k+1)] for y in range(S+1)] 

	for s in range(1, S+1):
		M[s][0] = [],inf


	for i in range(1, k+1):
		for s in range(1, S+1):
			terme2,n2 = [],inf
			if (s-V[i-1]>=0):
				terme, n = M[s-V[i-1]][i]
				terme2, n2 = [el for el in terme], n
				terme2[i-1], n2 = terme2[i-1]+1, n2+1
			M[s][i] = terme2, n2
			#print(M[s][i])

			terme1, n1=M[s][i-1]
			#print(terme1,n1)
			if (n1<n2):
				M[s][i] = terme1+[0],n1
			#print(M[s][i])
	return M

"""
def AlgoOptimiseTab2(S, V):
	k = len(V)
	M = [[([0 for l in range(x)],0)for x in range(k+1)] for y in range(S+1)] 

	for s in range(1, S+1):
		M[s][0] = [],inf
"""

def AlgoGlouton(S, V):
	L= len(V)
	A = [0 for i in range(L)]
	St = S
	if (S=0):
		return A
	elif (S<0 or L=0):
		return "Erreur, S<0 ou V=[]"
	for i in range(L-1,-1, -1):
		ResDiv = St/V[i]
		if (ResDiv>=1):
			St = St-ResDiv*V[i]
			A[i] = ResDiv
	return A


print(AlgoGlouton(S, V))

M = AlgoOptimiseTab(S, V)
for el in M:
	print el



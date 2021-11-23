import sys
from math import *
from random import seed
from random import random
from timeit import timeit
from Outils import *

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q3.1
inf= sys.maxint
S=7
V=[1,2,4,6,9]
#Algo 1
def AlgoRec(S,V):
	k = len(V)
	if (S==0):
		return 0
	elif (k==0 or S<0):
		return inf
	else:
		return min(AlgoRec(S, V[0:k-1]), AlgoRec(S-V[k-1],V)+1)

#Algo 2, dans les algo ou on calcule le tableau a chaque case, je calcule (A, n) ou A est le tableau A et n est le nommbre de bocause dans A. Ca permet aussi de ne pas compter a chaque fois le nombre de bocaux de A pour le min.
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
	return M[S][k]


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
	return M[S][k]


def AlgoOptimiseTabBack(S, V):
	if (V==[]):
		return [], inf

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



	A= [0 for i in range(k)]
	s = S
	i = k
	n = 0
	while (s!=0): #car toujours existe solution
		terme1 = M[s][i-1]
		terme2 = inf
		if (s-V[i-1]>=0):
			terme2 = M[s-V[i-1]][i]
		val = min(terme1, terme2)
		if (val == terme1):
			i = i-1
		else:
			s= s-V[i-1]
			A[i-1] = A[i-1]+1
			n=n+1
	return A,n




#Algo3
def AlgoGlouton(S, V):
	L= len(V)
	res= 0
	St = S
	if (S==0):
		return 0
	elif (S<0 or L==0):
		return inf
	for i in range(L-1,-1, -1):
		#print("Glouton: "+str(i))
		ResDiv = St/V[i]
		if (ResDiv>=1):
			St = St-ResDiv*V[i]
			res = res+ResDiv
	return res

def AlgoGloutonTab(S, V):
	L= len(V)
	A = [0 for i in range(L)]
	St = S
	if (S==0):
		return A
	elif (S<0 or L==0):
		return "Erreur, S<0 ou V=[]"
	for i in range(L-1,-1, -1):
		ResDiv = St/V[i]
		if (ResDiv>=1):
			St = St-ResDiv*V[i]
			A[i] = ResDiv
	return A



def Test(S,V):
	print("S={} et V={}".format(S,V))
	print("Rec: {}".format(AlgoRec(S,V)))
	print("Optimise: {}".format(AlgoOptimiseTab(S,V)))
	print("Optimise: {}".format(AlgoOptimiseTabBack(S,V)))
	print("Glouton: {}".format(AlgoGlouton(S, V))+"\n")

Test(0, [1,3,6,9])
Test(123, [])
Test(123, [1])
Test(11, [1,3,6,8,9])
Test(16, [1,3,6,8,9])
Test(24, [1,3,6,8,9])

#Teste d'optimisation AlgoOptimiseTab et AlgoOptimiseTabBack
print(timeit(lambda: AlgoOptimiseTab(742, [1,4,5,89,100,124]), number=100))
print(timeit(lambda: AlgoOptimiseTabBack(742, [1,4,5,89,100,124]), number=100))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q3.2

#Question 12
S=30000 #S va varier de 0 a 30000 en pas de 100
k=12  #|V| va varier de 0 a 12

def SystemeExpo(d, k):
	if (d<2):
		return "erreur d<2"
	L=[]
	for i in range(k):
		L.append(d**(i))
	return L

def TestTemps(d):
	tr=0 #temps algo rec
	to=0 #temps algo optimise
	tg=0 #temps algo glouton
	for s in range(0,S+1, 100):
		for i in range(0,k+1):
			print(s,i)

			V = SystemeExpo(d, i)
			#Rec
			if (tr<=50):
				tr= timeit(lambda: AlgoRec(s,V),number=1)
				with open("d{}Rec.txt".format(d),'a') as f:
					f.write(str(s)+" "+str(i)+" "+str(tr)+"\n")
			#Optimise
			to= timeit(lambda: AlgoOptimiseTabBack(s,V),number=1)

			with open("d{}Optimise.txt".format(d),'a') as f:
					f.write(str(s)+" "+str(i)+" "+str(to)+"\n")
			#Glouton
			tg= timeit(lambda: AlgoGlouton(s,V),number=1)
			with open("d{}Glouton.txt".format(d),'a') as f:
					f.write(str(s)+" "+str(i)+" "+str(tg)+"\n")


ClearFichiers()#permet de vider les fichiers servants a tracer les graphes a chaque execution
"""
#d=2
TestTemps(2)
#d=3
TestTemps(3)
"""
#d=4
TestTemps(4)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q3.3
def GenVal(pmax):
	return int(2+floor(random()*(pmax-2+1)))

def indice(val, L):
	res=0
	k = len(L)
	while (res<k and L[res]<=val):
		res=res+1
	if (L[res-1]==val):
		return -1
	return res

def GenCapaAlea(k, pmax): #genere liste contenants [], [1] et 10 V differents pour chaque taille k, 1<k<=12. J'ai essaye avec 100 V pour chaque taille k pour un resultat plus precis, mais ca prend beaucoup plus du temps
	L=[]
	L.append([])
	L.append([1])
	for i in range(2, k+1):
		for n in range(10):
			el = [1]
			if (i==2): #s'il n'y a que deux elements, ce n'est pas important c'est toujours compatible... 
				el.append(2+floor(random()*(pmax-2+1)))
			else:
				for j in range(1, i):
					val = 0
					ind = -1
					while (ind == -1):
						val = GenVal(pmax)
						ind = indice(val, el) #indice renvoit -1 si val invalide, sinon elle renvoit l'indice dans lequel inserer val
					el.insert(ind, val)
			L.append(el)
	return L


#Question 13
pmax= 200
T = GenCapaAlea(12, pmax)
#PrintTabDim2(T)

def TestGloutonCompatible(k, V):
	if (k>=3):
		Sdeb = V[2]+2
		Sfin = V[k-2]+V[k-1]-1
		for s in range(Sdeb, Sfin+1):
			for j in range(0, k):
				if ((V[j]<s) and (AlgoGlouton(s, V)>1+AlgoGlouton(s-V[j], V))):
					return False
	return True

def ProportionGloutonComp(T):
	l = len(T)
	cpt=0
	for i in range(l):
		comp = TestGloutonCompatible(len(T[i]),T[i])
		if (comp):
			cpt=cpt+1
		print(i)
	return float(cpt)/float(l)

#print(ProportionGloutonComp(T)) #~10% sont glouton compatible, approximee a la premiere decimale...

#Question 14
pmax= 200
S = 10*pmax

def BocMin(S, T): #pour etre le plus proche possible des resultats les plus precis sachant que le poucentage de glouton compatible doit etre 10%, j ai redemarre le programme jusqu a avoir ~0.116
	l = len(T)
	PireEcart=0
	SommeEcart=0
	CptEcart=0
	CptNonComp = 0
	for v in range(l):
		if (TestGloutonCompatible(len(T[v]),T[v])==False):
			CptNonComp=CptNonComp+1
			for s in range(pmax, S+1):
				nbminOp = AlgoOptimise(s, V)
				nbminGl = AlgoGlouton(s,V)
				ecart= nbminGl-nbminOp
				if (ecart>PireEcart):
					PireEcart=ecart
				SommeEcart = SommeEcart+ecart
				CptEcart = CptEcart+1
				print(str(v)+"/"+str(l-1)+" "+str(s)+"/"+str(S))
	print("PireEcart= "+str(PireEcart))
	print("EcartMoyen= "+str(float(SommeEcart)/float(CptEcart)))
	print("Pourcentage de glouton compatible= "+str((float(len(T)-CptNonComp)/float(len(T)))*100))

#BocMin(S, T)

"""
PireEcart= 1
EcartMoyen= 0.111049416991
Pourcentage de glouton compatible= 11.6071428571
"""




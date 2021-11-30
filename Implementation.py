import sys
from math import *
from random import seed
from random import random
from timeit import timeit
from Outils import *

inf= float('inf')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q3.1

#Lecture de fichiers
def Fusionner(tab1, tab2):
	res =[]
	k = 0 #indice de construction du tableau res 
	i = 0 #indice de parcours de tab1
	j = 0 #indice de parours de tab2
	tailleTab1 = len(tab1)
	tailleTab2 = len(tab2)
	tailleRes = tailleTab1 + tailleTab2
	while (k != tailleRes):
		if (i == tailleTab1):
			res.append(tab2[j])
			j=j+1
		elif (j== tailleTab2):
			res.append(tab1[i])
			i=i+1
		elif (tab1[i]<=tab2[j]):
			res.append(tab1[i])
			i=i+1
		else:
			res.append(tab2[j])
			j=j+1
		k=k+1
	return res

def TriFusion(tab):
	if (len(tab)==1):
		return tab
	else:
		m = len(tab)/2
		tab1 = TriFusion(tab[:m])
		tab2 = TriFusion(tab[m:])
		return Fusionner(tab1,tab2)

def LireParam(NomFichier):
	cpt=0
	L=[]
	with open(NomFichier, "r") as f:
	    for line in f:
	    	if (line[-1]=="\n"):
	    		L.append(line[:-1])
	    	else:
	    		L.append(line)

	S = L[0]
	k = L[1]
	V = L[2:]
	V = TriFusion(V)
	return S,k,V


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
	n=0
	if (S==0):
		return A, n
	elif (S<0 or L==0):
		return [], inf
	for i in range(L-1,-1, -1):
		ResDiv = St/V[i]
		if (ResDiv>=1):
			St = St-ResDiv*V[i]
			A[i] = ResDiv
			n = n +ResDiv
	return A, n


#Exemples pour tester fonctionnements
def Test(S,V):
	print("S={} et V={}".format(S,V))
	print("Rec: {}".format(AlgoRec(S,V)))
	print("OptimiseTab: {}".format(AlgoOptimiseTab(S,V)))
	print("OptimiseTabBack: {}".format(AlgoOptimiseTabBack(S,V)))
	print("Glouton: {}".format(AlgoGloutonTab(S, V))+"\n")

Test(0, [1,3,6,9])
Test(123, [])
Test(123, [1])
Test(11, [1,3,6,8,9])
Test(16, [1,3,6,8,9])
Test(24, [1,3,6,8,9])

#Teste d'optimisation AlgoOptimiseTab et AlgoOptimiseTabBack (pas demande)
print("Temps mit par OptimiseTab: "+str(timeit(lambda: AlgoOptimiseTab(742, [1,4,5,89,100,124]), number=100)))
print("Temps mit par OptimiseTabBack: "+str(timeit(lambda: AlgoOptimiseTabBack(742, [1,4,5,89,100,124]), number=100)))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Q3.2
#Question 12
def SystemeExpo(d, k):
	if (d<2):
		return "erreur d<2"
	L=[]
	for i in range(k):
		L.append(d**(i))
	return L

def TestTempsGlouton(d, S, k, Spas):
	tg=0 #temps algo glouton
	for s in range(0,S+1, Spas):
		for i in range(0,k+1):
			print(s,i)
			V = SystemeExpo(d, i)
			tg= timeit(lambda: AlgoGlouton(s,V),number=1)
			with open("d{}Glouton.txt".format(d),'a') as f:
					f.write(str(s)+" "+str(i)+" "+str(tg)+"\n")

def TestTempsOptimise(d, S, k, Spas):
	to=0 #temps algo optimise
	for s in range(0,S+1, Spas):
		for i in range(0,k+1):
			print(s,i)
			V = SystemeExpo(d, i)
			to= timeit(lambda: AlgoOptimiseTabBack(s,V),number=1)
			with open("d{}Optimise.txt".format(d),'a') as f:
					f.write(str(s)+" "+str(i)+" "+str(to)+"\n")
def TestTempsRec(d, S, k, Spas):
	tr=0 #temps algo glouton
	for s in range(0,S+1, Spas):
		for i in range(0,k+1):
			print(s,i)
			V = SystemeExpo(d, i)
			if (tr<=50):
				tr= timeit(lambda: AlgoRec(s,V),number=1)
				with open("d{}Rec.txt".format(d),'a') as f:
					f.write(str(s)+" "+str(i)+" "+str(tr)+"\n")

ClearFichiers()#permet de vider les fichiers servants a tracer les graphes a chaque execution
"""
#Test Glouton
#d=2
TestTempsGlouton(2, 1000000, 40,100)
TestTempsGlouton(2, 1000000, 1000, 100)
#d=3
TestTempsGlouton(3,1000000, 40,100)
#d=4
TestTempsGlouton(4,1000000,40,100)

#Test Optimise
#d=2
TestTempsOptimise(2,100000,12,10)
TestTempsOptimise(2, 1000, 1000, 1)
#d=3
TestTempsOptimise(3,100000,12,10)
TestTempsOptimise(3, 1000, 1000, 1)
#d=4
TestTempsOptimise(4,100000,12,10)
TestTempsOptimise(4, 1000, 1)

#Test Rec
#d=2
TestTempsRec(2,30000,10, 10)
#d=3
TestTempsRec(3,30000,10, 10)
#d=4
TestTempsRec(4,30000,10, 10)
"""
#pour voir quadratique dans optimise O(k*S)
TestTempsOptimise(2, 1000, 1000,10)
TestTempsOptimise(3, 1000, 1000,10)
TestTempsOptimise(4, 1000, 1000,10)

#pout voir lineaire en glouton O(k)
TestTempsGlouton(2, 1000000, 1000,1)
TestTempsGlouton(3,1000000, 1000,1)
TestTempsGlouton(4,1000000, 1000,1)

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

def GenCapaAlea(k, pmax): #genere liste contenants 250 V differents pour chaque taille k, 3<=k<=12. J'ai essaye avec 10000 V pour chaque taille k pour un resultat plus precis, mais ca prend beaucoup plus du temps et ca donne aussi 10% donc je me contente de 250 V par k
	L=[]
	for i in range(3, k+1):
		for n in range(250): #A changer si prend bcp de tps en 100
			el = [1]
			if (i==2): #s'il n'y a que deux elements, pas besoin de faire le tri... 
				el.append(GenVal(pmax))
			else: #sinon il faut inserer les element en ordre croissant et verifier qu'il n'y a pas un meme element deux fois
				for j in range(1, i):
					val = 0
					ind = -1
					while (ind == -1):
						val = GenVal(pmax)
						ind = indice(val, el) #indice renvoit -1 si val invalide, sinon elle renvoit l'indice dans lequel inserer val
					el.insert(ind, val)
			L.append(el)
	return L

def GenCapaAlea(k1,k2,k3, pmax): #retourne 1000 système différents par k
	L1=[]
	L2=[]
	L3=[]

	for n in range(1000):
		el = [1]
		for j in range(1,k1):
			val=0
			ind = -1 
			while (ind == -1):
				val = GenVal(pmax)
				ind = indice(val, el) #indice renvoit -1 si val invalide, sinon elle renvoit l'indice dans lequel inserer val
				el.insert(ind, val)
		L1.append(el)

		el = [1]
		for j in range(1,k2):
			val=0
			ind = -1 
			while (ind == -1):
				val = GenVal(pmax)
				ind = indice(val, el) #indice renvoit -1 si val invalide, sinon elle renvoit l'indice dans lequel inserer val
				el.insert(ind, val)
		L2.append(el)

		el = [1]
		for j in range(1,k3):
			val=0
			ind = -1 
			while (ind == -1):
				val = GenVal(pmax)
				ind = indice(val, el) #indice renvoit -1 si val invalide, sinon elle renvoit l'indice dans lequel inserer val
				el.insert(ind, val)
		L3.append(el)
	return L1, L2, L3 

#Question 13
pmax= 500
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

print("Proportion compatible: "+str(ProportionGloutonComp(T))) #~1% sont glouton compatible, approximee a la premiere decimale...

#Question 14
pmax= 500
S = 10*pmax
#T n'a pas change, T=GenCapaAlea(12, pmax) avec k=12 er pmax=200

def BocMin(S, T):#T= tableau contenant des V differents #pour etre le plus proche possible des resultats les plus precis sachant que le poucentage de glouton compatible doit etre 1%, j ai redemarre le programme jusqu a avoir ~0.0116
	l = len(T)
	PireEcart=0
	SommeEcart=0
	CptEcart=0
	CptNonComp = 0
	for v in range(l):
		if (TestGloutonCompatible(len(T[v]),T[v])==False):
			CptNonComp=CptNonComp+1
			for s in range(pmax, S+1):
				nbminOp = AlgoOptimise(s, T[v]) #nombre min de bocaux pour algo optimise
				nbminGl = AlgoGlouton(s,T[v]) #nombre min de bocaux pour algo glouton
				ecart= nbminGl-nbminOp
				if (ecart>PireEcart):
					PireEcart=ecart
				SommeEcart = SommeEcart+ecart
				CptEcart = CptEcart+1
				print(str(v)+"/"+str(l-1)+" "+str(s)+"/"+str(S))
				with open ("BocMin.txt", "a") as f:
					f.write(str(v)+"/"+str(l-1)+" "+str(s)+"/"+str(S))
	print("PireEcart= "+str(PireEcart))
	print("EcartMoyen= "+str(float(SommeEcart)/float(CptEcart)))
	print("Pourcentage de glouton compatible= "+str((float(len(T)-CptNonComp)/float(len(T)))*100))

BocMin(S, T)

"""
PireEcart= 1
EcartMoyen= 0.111049416991
Pourcentage de glouton compatible= 11.6071428571
"""





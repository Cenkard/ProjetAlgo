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
def Fusionner(tab1, tab2): #Fonction intermediaire pour triFusion. Prend deux tableaux les fusionne et rend la fusion des deux tableaux
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

def TriFusion(tab): #Fonction tri fusion. Prend un tableau et le retourne trie en ordre croissant
	if (len(tab)==1):
		return tab
	else:
		m = len(tab)/2
		tab1 = TriFusion(tab[:m])
		tab2 = TriFusion(tab[m:])
		return Fusionner(tab1,tab2)

def LireParam(NomFichier): #Fonction de lecture d'un systeme. Prend le nom de fichier, retourne S, k et V trie
	cpt=0
	L=[]
	with open(NomFichier, "r") as f:
	    for line in f:
	    	if (line[-1]=="\n"):
	    		L.append(line[:-1])
	    	else:
	    		L.append(line)

	S = L[0] #premier element S
	k = L[1] #2eme elemenent k
	V = L[2:] #le reste V
	V = TriFusion(V) #trie V en utilisant tri fusion
	return S,k,V


#Algo 1
def AlgoRec(S,V): #Algorithme 1 recursif. Prend en entre S et V, retourne le nombre minimal de bocaux necessaire
	k = len(V)
	if (S==0):
		return 0
	elif (k==0 or S<0):
		return inf
	else:
		return min(AlgoRec(S, V[0:k-1]), AlgoRec(S-V[k-1],V)+1)


#Algo 2, dans les algo ou on calcule le tableau a chaque case, je calcule (A, n) ou A est le tableau A et n est le nommbre de bocause dans A. Ca permet aussi de ne pas compter a chaque fois le nombre de bocaux de A pour le min.
def AlgoOptimise(S, V): #Algorithme 2 iteratif. Prend en entre S et V, retourne le nombre minimal de bocaux necessaire
	k = len(V)
	M = [[0 for x in range(k+1)] for y in range(S+1)]

	for s in range(1, S+1):
		M[s][0] = inf

	for i in range(1, k+1):
		for s in range(1, S+1):
			terme2 = inf
			if (s-V[i-1]>=0): #On verifie si bocal V[i-1] est utilisable
				terme2 = M[s-V[i-1]][i]+1 #si oui on le prend en consideration
			M[s][i] = min(M[s][i-1], terme2) #on l'utilise si il permet de reduir nombre de bocaux
	return M[S][k]

def AlgoOptimiseTab(S,V):  #Algorithme 2 iteratif. Prend en entre S et V, retourne couple (A,n) ou A est le tableaux de bocaux necessaires et n et le nombere de bocaux minimal
	k = len(V)
	M = [[([0 for l in range(x)],0)for x in range(k+1)] for y in range(S+1)] 

	for s in range(1, S+1):
		M[s][0] = [],inf


	for i in range(1, k+1):
		for s in range(1, S+1):
			terme2,n2 = [],inf
			if (s-V[i-1]>=0): #On verifie si bocal V[i-1] est utilisable
				terme, n = M[s-V[i-1]][i] #si oui on le prend en consideration
				terme2, n2 = [el for el in terme], n
				terme2[i-1], n2 = terme2[i-1]+1, n2+1
			M[s][i] = terme2, n2 #C'est pas sur qu'on va l'utliser, mais on dit qu'on l'utlise. Ca peut changer apres en fonction de n2
			terme1, n1=M[s][i-1]
			if (n1<n2): #S'il permet pas de reduir le nombre de bocaux on utilise M[s][i-1] plutot
				M[s][i] = terme1+[0],n1 
	return M[S][k]


def AlgoOptimiseTabBack(S, V): #Algorithme 2 iteratif version BackWard. Prend en entre S et V, retourne couple (A,n) ou A est le tableaux de bocaux necessaires et n et le nombere de bocaux minimal
	if (V==[]):
		return [], inf
	#Algorithme initial
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


	#Algorithme backward
	A= [0 for i in range(k)]
	s = S
	i = k
	n = 0
	while (s!=0): #car toujours existe solution
		terme1 = M[s][i-1]
		terme2 = inf
		if (s-V[i-1]>=0): #On verifie si bocal V[i-1] est utilisable
			terme2 = M[s-V[i-1]][i]
		val = min(terme1, terme2) #On regarde lequel etait inferieur
		if (val == terme1): #si c'est terme1, il suffit de chercher en (S,i-1)
			i = i-1
		else: #sinon on cherche en (S-V[i-1]. i) mais on fait les changement necessaire en A car on a utilise V[i-1
			s= s-V[i-1]
			A[i-1] = A[i-1]+1
			n=n+1
	return A,n




#Algo3
def AlgoGlouton(S, V): #Algorithme 3 iteratif. Prend en entre S et V, retourne couple n et le nombere de bocaux minimal
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

def AlgoGloutonTab(S, V): #Algorithme 3 iteratif. Prend en entre S et V,retourne couple (A,n) ou A est le tableaux de bocaux necessaires et n et le nombere de bocaux minimal
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
def SystemeExpo(d, k): #Prend en entre (d,k) et retourne le systeme V demande selon l'enonse
	if (d<2):
		return "erreur d<2"
	L=[]
	for i in range(k):
		L.append(d**(i))
	return L

def TestTempsGlouton(d, S, k, Spas): #Fonction teste pour l'algorithme3 (Glouton). Prend en entre d, S et k mais aussi Spas afin de accelerer le teste si necessaire
	tg=0 #temps algo glouton
	for s in range(0,S+1, Spas):
		for i in range(0,k+1):
			print(s,i)
			V = SystemeExpo(d, i)
			tg= timeit(lambda: AlgoGlouton(s,V),number=1)
			with open("d{}Glouton.txt".format(d),'a') as f:
					f.write(str(s)+" "+str(i)+" "+str(tg)+"\n")

def TestTempsOptimise(d, S, k, Spas): #Fonction teste pour l'algorithme2 (OtimiseBack). Prend en entre d, S et k mais aussi Spas afin de accelerer le teste si necessaire
	to=0 #temps algo optimise
	for s in range(0,S+1, Spas):
		for i in range(0,k+1):
			print(s,i)
			V = SystemeExpo(d, i)
			to= timeit(lambda: AlgoOptimiseTabBack(s,V),number=1)
			with open("d{}Optimise.txt".format(d),'a') as f:
					f.write(str(s)+" "+str(i)+" "+str(to)+"\n")
def TestTempsRec(d, S, k, Spas): #Fonction teste pour l'algorithme1 (Recursif). Prend en entre d, S et k mais aussi Spas afin de accelerer le teste si necessaire
	tr=0 #temps algo glouton
	for s in range(0,S+1, Spas):
		for i in range(0,k+1):
			print(s,i)
			V = SystemeExpo(d, i)
			if (tr<=60):
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
"""
TestTempsOptimise(2, 1000, 1000,10)

TestTempsOptimise(3, 1000, 1000,100)
TestTempsOptimise(4, 1000, 1000,100)

#pout voir lineaire en glouton O(k)
TestTempsGlouton(2, 1000, 1000,100)
TestTempsGlouton(3,1000, 1000,100)
TestTempsGlouton(4,1000, 1000,100)

"""
"""
#d=2
TestTempsOptimise(2,100000,12,1000)
#d=3
TestTempsOptimise(3,100000,12,1000)
#d=4
TestTempsOptimise(4,100000,12,1000)
"""
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q3.3
def GenVal(pmax): #Fonction prenant en entree pmax, et retournant une valeur aleatoire uniformement dans l'intervalle [2,pmax]
	return int(2+floor(random()*(pmax-2+1)))

def indice(val, L): #Fonction intermediarie pour GenCapaAlea et GenCapaAlea2. Prend en entree une valeur val et un tableau L, retourne -1 si val ne peux pas etre insere dans L (existe deja), sinon elle retourne l'indice dans lequel insere Val (pour garder L croissante)
	res=0
	k = len(L)
	while (res<k and L[res]<=val):
		res=res+1
	if (L[res-1]==val):
		return -1
	return res

def GenCapaAlea(k, pmax):
	#Fonction generant des systemes de capacite aleatoires en faisant verier k en fonction de pmax
	#Prend en entree k et pmax et retourne un tableau de systemes aleatoires V
	#Plus de details: elle genere un tableau contenant 100 V differents pour chaque taille k, 3<=k<=8 (ici). J'ai essaye avec 10000 V pour chaque taille k pour un resultat plus precis, mais ca prend beaucoup plus du temps et ca donne aussi 3% donc je me contente de 100 V par k
	L=[]
	for i in range(3, k+1): #pour chaque taille k
		for n in range(100): #Genere 100 systeme different et les ajoutes a L
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

def GenCapaAlea2(k1,k2,k3, pmax): #retourne 1000 systeme differents par ki, pour des test cible sur les taille de k
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
pmax= 200
T = GenCapaAlea(8, pmax)
#PrintTabDim2(T)

def TestGloutonCompatible(k, V): #fonction intermediaire de ProportionGloutonComp et BocMin. Prend k,V et retourne si V estt et Glouton compatible
	if (k>=3):
		Sdeb = V[2]+2
		Sfin = V[k-2]+V[k-1]-1
		for s in range(Sdeb, Sfin+1):
			for j in range(0, k):
				if ((V[j]<s) and (AlgoGlouton(s, V)>1+AlgoGlouton(s-V[j], V))):
					return False
	return True

def ProportionGloutonComp(T): #Prend en entre entre un tableau de systemes V, retourne la proportion de systemes V glouton compatible
	l = len(T)
	cpt=0
	for i in range(l):
		comp = TestGloutonCompatible(len(T[i]),T[i])
		if (comp):
			cpt=cpt+1
		print(i)
	return float(cpt)/float(l)

print("Proportion compatible en generale sur des tailles k variant de 3 a 12: "+str(ProportionGloutonComp(T))) #~3% sont glouton compatible, approximee a la premiere decimale

#Question 14
pmax= 200
S = 10*pmax

def BocMin(S, T):
	#Fonction calculant des statistiques pour determiner si l algorithme glouton peut etre utilise dans un cadre pratique
	#Prend S et T un tableau de systemes differents, retoure des statistiques sous format texte
	l = len(T)
	PireEcart=0 #Pire ecart entre Optimise et Glouton
	SommeEcart=0 #Somme des ecart, va servir a determiner l'ecart moyen
	CptEcart=0 #Compteur du nombre de fois ou il y a eu un ecart va servir a determiner l'ecart moyen
	CptNonComp = 0 #Compteur de systeme non Glouton Compatible
	for v in range(l):
		if (TestGloutonCompatible(len(T[v]),T[v])==False):
			CptNonComp=CptNonComp+1
			for s in range(pmax, S+1):
				nbminOp = AlgoOptimise(s, T[v]) #nombre min de bocaux pour algo optimise
				nbminGl = AlgoGlouton(s,T[v]) #nombre min de bocaux pour algo glouton
				ecart= nbminGl-nbminOp
				if (ecart>PireEcart): #On met a jour le pire ecart
					PireEcart=ecart
				SommeEcart = SommeEcart+ecart #on met a jour somme ecart
				CptEcart = CptEcart+1 #ON met a jour CptEcart
				print(str(v)+"/"+str(l-1)+" "+str(s)+"/"+str(S))
	PireEcart = "PireEcart= "+str(PireEcart)+"\n"
	EcartMoyen =  "EcartMoyen= "+str(0)+"\n"
	if (CptEcart !=0):
		EcartMoyen = "EcartMoyen= "+str(float(SommeEcart)/float(CptEcart))+"\n"
	Pourcentage_gl = "Pourcentage de glouton compatible=" +str((float(len(T)-CptNonComp)/float(len(T)))*100)+"\n"

	return (PireEcart+EcartMoyen+Pourcentage_gl)


#T n'a pas change, T=GenCapaAlea(k, pmax) avec k=8 er pmax=200
L1, L2, L3 = GenCapaAlea2(3,6,15, pmax)

with open("stat.txt", "a") as f: #Sauvegarder les statistiques
	f.write(BocMin(S, T))
	"""
	f.write(BocMin(S,L1))
	f.write(BocMin(S,L2))
	f.write(BocMin(S,L3))
	"""






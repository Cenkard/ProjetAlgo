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


print(LireParam("donnees.txt"))

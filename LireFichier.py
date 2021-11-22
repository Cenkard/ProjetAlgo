def LireParam(NomFichier):
	cpt=0
	L=[]
	with open(NomFichier) as f:
	    for line in f:
	    	val = int(line)
	        L.append(val)
	return L

res = LireParam("donnees")
S = res[0]
V = res[2:]
print(S,V)

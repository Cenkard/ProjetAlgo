def PrintTabDim2(T): #affiche un tableau 2d
	for el in T:
		print el

def ClearFichiers(): #permet de d'effacer le contenu des fichiers
	for d in range(2,5):
		with open("d{}Rec.txt".format(d),'w') as f:
				f.write('')
		with open("d{}Optimise.txt".format(d),'w') as f:
				f.write('')
		with open("d{}Glouton.txt".format(d),'w') as f:
				f.write('')
	with open ("stat.txt", "w") as f:
		f.write('')

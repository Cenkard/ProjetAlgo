def PrintTabDim2(T):
	for el in T:
		print el

def ClearFichiers():
	for d in range(2,5):
		with open("d{}Rec.txt".format(d),'w') as f:
				f.write('')
		with open("d{}Optimise.txt".format(d),'w') as f:
				f.write('')
		with open("d{}Glouton.txt".format(d),'w') as f:
				f.write('')

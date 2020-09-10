import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def readfile(filename):
	data = []
	with open(filename,"r") as f:
		start = False
		for line in f:
			if not start:
				start = line.count("-") > 20
			else:
				try:
					data.append(float(line[line.rfind(" "):]))
				except:
					break
	return np.array(data)

if __name__ == "__main__":
	names = sorted(os.listdir("./"))
	data = []
	for name in names:
		if name.split(".")[-1] == "rpt":
			print(name)
			data.append(readfile(name))
	data = np.array(data)

	#mean dif
	for i in range(len(data)):
		#for j in range(len(data)):
		print(np.mean(data[i]-data[0]),"",end="")
		print()
	print()
	#max dif
	for i in range(len(data)):
		#for j in range(len(data)):
		print(np.min(data[i])-np.min(data[0]),"",end="")
		print()
	print()
	for i in range(len(data)):
		#for j in range(len(data)):
		print(np.max(data[i])-np.max(data[0]),"",end="")
		print()
	print()
	for i in range(len(data)):
		#for j in range(len(data)):
		print(np.linalg.norm(data[i]-data[0],1)/len(data[0]),"",end="")
		print()
import numpy as np
import sys
from numpy.linalg import norm

class Node:
	def __init__(self,node_id=0,position=(0,0,0),velocity=(0,0,0)):
		self.node_id = node_id
		self.position = position
		self.velocity = velocity

def main():
	
	nodesFile = sys.argv[1]  # contém as posições correspondentes dos nós
	resultFile = sys.argv[2] # contém os resultados CFD
	nodesFileFinal = sys.argv[3] # contém as posições dos nós na placa final

	nodesCFD = np.array([])  # array com todos os nós do CFD (posição e velocidade)
	nodesSim = np.array([])  # array com os nós da simulação (posição e velocidade)

	print("Lendo arquivos...")

	with open(nodesFile,"r") as f:
		start = False
		for line in f:
			if start:
				try:
					data_line = line.replace(" ","").split(",")
					node_id = int(data_line[0])
					node_position = (float(data_line[1]),float(data_line[2]),float(data_line[3]))
					if node_position[2] == 0: # está na superfície de interesse
						nodesCFD = np.append(nodesCFD, Node(node_id=node_id, position=node_position))
				except:
					break
			elif "*Node" in line:
				start = True

	with open(resultFile,"r") as f:
		start = False
		for line in f:
			if start:
				try:
					data_line = line.split(" ")
					data_line = list(filter(lambda a: a != "", data_line))
					node_id = int(data_line[0])
					node_velocity = (float(data_line[1]),float(data_line[2]),float(data_line[3]))
					for i in range(nodesCFD.shape[0]):
						if node_id == nodesCFD[i].node_id:
							nodesCFD[i].velocity = node_velocity
							break
				except:
					break
			elif len(line)==65 and "-" in line:
				start = True

	with open(nodesFileFinal,"r") as f:
		start = False
		for line in f:
			if start:
				try:
					data_line = line.replace(" ","").split(",")
					node_id = int(data_line[0])
					node_position = (float(data_line[1]),float(data_line[2]),0.0)
					nodesSim = np.append(nodesSim, Node(node_id=node_id, position=node_position))
				except:
					break
			elif "*Node" in line:
				start = True

	print("Atribuíndo velocidades...")

	for i in range(nodesSim.shape[0]):
		min_dist, min_node_index = norm(np.array(nodesCFD[0].position) - np.array(nodesSim[i].position),2), 0
		for j in range(1,nodesCFD.shape[0]):
			dist = norm(np.array(nodesCFD[j].position) - np.array(nodesSim[i].position),2)
			if dist < min_dist:
				min_dist = dist
				min_node_index = j
		nodesSim[i].velocity = nodesCFD[min_node_index].velocity

	script_filename = "velocity.py"
	print("Prescrevendo velocidades para script "+script_filename+" ...")

	with open(script_filename,"w") as f:
		eps = 0.1
		#write preamble
		f.write("# -*- coding: mbcs -*-\nfrom part import *\nfrom material import *\nfrom section import *\nfrom assembly import *\nfrom step import *\nfrom interaction import *\nfrom load import *\nfrom mesh import *\nfrom optimization import *\nfrom job import *\nfrom sketch import *\nfrom visualization import *\nfrom connectorBehavior import *\n")
		for i in range(nodesSim.shape[0]):
			#cria um conjunto para cada ponto
			x1, y1 = nodesSim[i].position[0]-eps, nodesSim[i].position[1]-eps
			x2, y2 = nodesSim[i].position[0]+eps, nodesSim[i].position[1]+eps
			f.write("elm = mdb.models['Model-1'].rootAssembly.instances['Part-1'].elements.getByBoundingBox("+str(x1)+","+str(y1)+","+str(x2)+","+str(y2)+")\n")
			f.write("mdb.models['Model-1'].rootAssembly.Set(elements=elm, name='Group"+str(i)+"')\n")

		for i in range(nodesSim.shape[0]):
			#atribui a velocidade de cada ponto
			f.write("mdb.models['Model-1'].keywordBlock.insert("+str(30+5*i)+",'\\n** \\n** PREDEFINED FIELDS\\n** \\n*INITIAL CONDITIONS, TYPE=MASS FLOW\\nGroup"+str(i)+", "+str(nodesSim[i].velocity[0])+", "+str(nodesSim[i].velocity[1])+"\\n** Name: Predefined Field-"+str(i)+"   Type: Temperature')\n")

	print("Script completo. Execute-o manualmente no Abaqus.")

main()
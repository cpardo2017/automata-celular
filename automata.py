
import random
import threading

from deap import base
from deap import creator
from deap import tools
from datetime import datetime
from threading import Thread

lock = threading.Lock()

maxIndex = 149

idxDer1 = list()
idxDer2 = list()
idxDer3 = list()
idxIzq1 = list()
idxIzq2 = list()
idxIzq3 = list()

for i in range(maxIndex):
	if i + 1 < maxIndex:
		idxDer1.append(i + 1)
	else:
		idxDer1.append(i + 1 - maxIndex)

	if i + 2 < maxIndex:
		idxDer2.append(i + 2)
	else:
		idxDer2.append(i + 2 - maxIndex)

	if i + 3 < maxIndex:
		idxDer3.append(i + 3)
	else:
		idxDer3.append(i + 3 - maxIndex)

	if i - 1 >= 0:
		idxIzq1.append(i - 1)
	else:
		idxIzq1.append(maxIndex + (i - 1))

	if i - 2 >= 0:
		idxIzq2.append(i - 2)
	else:
		idxIzq2.append(maxIndex + (i - 2))

	if i - 3 >= 0:
		idxIzq3.append(i - 3)
	else:
		idxIzq3.append(maxIndex + (i - 3))

#funcion que crea los casos iniciales aleatorios
def crearA(cero,valor):
	casos = list() #lista donde se guardan las distintas combinaciones
	for i in range(50):
		estado = list() #lista donde se guardan los valores de la combinacion aleatoria
		a = random.randint(valor,149) # cantidad numeros predominantes que se crearan
		b = 149 - a # cantidad numeros NO predominantes que se crearan

		#dependiendo si el numero predominante debe ser 0 o 1, se crean y agregan a la lista estado
		for j in range(a):
			if cero:
				estado.append(0)
			else:
				estado.append(1)

		for j in range(b):
			if cero:
				estado.append(1)
			else:
				estado.append(0)

		random.shuffle(estado) #se desordenan los numeros
		casos.append(estado) #se agrega la combinacion

		if(len(estado) >= 150):
			print(a)
			print(b)

	return casos #se devuelven las combinaciones


#clase que reprensenta las celdas en los automatas
class Celda:
	def __init__(self,idx,estado):
		#se crean el index de la celda que almacena su posicion en el automata y los index de sus vecinos
		self.idx = idx
		if idx - 1 >= 0:
			self.vecinoIzq3 = idx - 1
		else:
			self.vecinoIzq3 = maxIndex - 1 

		if idx - 2 >= 0:
			self.vecinoIzq2 = idx - 2
		else:
			self.vecinoIzq2 = maxIndex - 2 

		if idx - 3 >= 0:
			self.vecinoIzq1 = idx - 3
		else:
			self.vecinoIzq1= maxIndex - 3

		if idx + 1 < maxIndex:
			self.vecinoDer1 = idx + 1
		else:
			self.vecinoDer1 = idx + 1 - maxIndex

		if idx + 2 < maxIndex:
			self.vecinoDer2 = idx + 2
		else:
			self.vecinoDer2 = idx + 2 - maxIndex

		if idx + 3 < maxIndex:
			self.vecinoDer3 = idx + 3
		else:
			self.vecinoDer3 = idx + 3 - maxIndex

		#se establece el estado inicial de la celda 0 o 1
		self.estado = estado

	#getters y setters de la clase automata
	def getEstado(self):
		return self.estado

	def getVecinoIzq1(self):
		return self.vecinoIzq1

	def getVecinoIzq2(self):
		return self.vecinoIzq2

	def getVecinoIzq3(self):
		return self.vecinoIzq3

	def getVecinoDer1(self):
		return self.vecinoDer1

	def getVecinoDer2(self):
		return self.vecinoDer2

	def getVecinoDer3(self):
		return self.vecinoDer3

	def setEstado(self,newEstado):
		self.estado = newEstado

#clase que representa al automata
class Automata():
	"""docstring for Automata"""
	def __init__(self, reglas, estadoInicial):
		self.reglas = reglas #se establecen las reglas

		self.celdas = list() #lista que almacena las celda del automata

		#se crean las celdas y se le asignan los valores en estadoInicial
		self.tam = len(estadoInicial)

		for i in range(self.tam):
			self.celdas.append(estadoInicial[i])


	#funcion que actualiza el automata segun su regla
	def update(self):
		newCeldas = list() #lista donde se almacenaran los valores nuevos de las celdas

		#print(self.tam)
		#por cada celda se ven los vecinos y en funcion a sus valores se elige el output en la regla
		for i in range(self.tam):

			indice = 0

			aux = idxIzq3[i]

			if self.celdas[aux] == 1:
				indice += 64

			if self.celdas[idxIzq2[i]] == 1:
				indice += 32


			if self.celdas[idxIzq1[i]] == 1:
				indice += 16

			if self.celdas[i] == 1:
				indice += 8

			if self.celdas[idxDer1[i]] == 1:
				indice += 4

			if self.celdas[idxDer2[i]] == 1:
				indice += 2

			if self.celdas[idxDer3[i]] == 1:
				indice += 1

			newCeldas.append(self.reglas[indice]) #se almacena la salida del output de la regla 

		#se almacenan cambian los valores en las celdas
		for i in range(self.tam):
			self.celdas[i] = newCeldas[i]

	# funcion de la clase automata que revisa si es un all-ones
	def revisarOnes(self):
		for i in range(self.tam):
			if self.celdas[i] == 0:
				return False

		return True

	# funcion de la clase automata que revisa si es un all-zeros
	def revisarZeros(self):
		for i in range(self.tam):
			if self.celdas[i] == 1:
				return False

		return True


#se crean las variables de deap
#NOTA: las partes del codigo de deap estan sacados del ejemplo del all-ones
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 128)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#clase que almacena las combinaciones aleatorias para probar los automatas
class Eval:

	#def __init__(self,casosZeros,casosOnes):
	#	self.casosZeros = casosZeros
	#	self.casosOnes = casosOnes

	def setVal(self,casosZeros,casosOnes):
		self.casosZeros = casosZeros #valores para probar all-zeros
		self.casosOnes = casosOnes #valores para probar all-ones


control = Eval() #se crea un objeto para almacenar las combinaciones aleatorias

global maxFitness 
global result

class Resultado:

	def setR(self,max,r):
		self.maxFitness = max
		self.result = r

	def getMax(self):
		return self.maxFitness

	def getResult(self):
		return self.result


R = Resultado()

R.setR(0,list())

fit = float(0)

def Func(individual,b):
	global fit
	for i in control.casosZeros:
		automata = Automata(individual,i)

		for j in range(len(i)*2):
			automata.update()

		#por cada all-zeros conseguido, se suma 1 al fitness
		if automata.revisarZeros():
			lock.acquire()
			fit += 1
			lock.release()

	b.wait()

#funcion que evalua los individuos


def evaluate(individual):
	global fit
	from threading import Barrier


	b = Barrier(2) 

	fit = float(0) #valor del fitness

	#por cada caso aleatorio de casosZeros se crea un automata con el caso y las reglas, y se actualiza 2*n veces
	thread1 = threading.Thread(target = Func,args = (individual,b))
	thread1.start()

	for i in control.casosOnes:
		automata = Automata(individual,i)

		for j in range(len(i)*2):
			automata.update()

		#por cada all-ones conseguido, se suma 1 al fitness
		if automata.revisarOnes():
			lock.acquire()
			fit += 1
			lock.release()

	b.wait()


	if(fit > R.getMax()):
		R.setR(fit,individual)

	return fit, #se devuelve el fitness

#se registran los metodos del deap
toolbox.register("evaluate", evaluate)


toolbox.register("mate", tools.cxUniform, indpb=0.6)

toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)

toolbox.register("select", tools.selTournament, tournsize=4)


def main():
	random.seed(datetime.now()) #se establece la semilla random

	casosZeros = crearA(True,75) #se crean los casos de all-zeros, con al menos 120 ceros
	casosOnes = crearA(False,75) #se crean los casos de all-ones, con al menos 120 unos
	control.setVal(casosZeros,casosOnes) #se setean los valores de los casos en control

	####CODIGO ESTANDAR DE DEAP######################
	####TERMINA LA DOCUMENTACION PROPIA######################

	# create an initial population of 300 individuals (where
	# each individual is a list of integers)
	pop = toolbox.population(n=10)

	CXPB, MUTPB = 0.5, 0.2 #cambiar luego

	print("Start of evolution")

	print("empezar evaluacion")
	# Evaluate the entire population
	#fitnesses = list(map(toolbox.evaluate, pop))
	#print("terminar evaluacion")

	# Evaluate the entire population
	fitnesses = list(map(toolbox.evaluate, pop))
	for ind, fit in zip(pop, fitnesses):
		ind.fitness.values = fit

	print("  Evaluated %i individuals" % len(pop))

	# Extracting all the fitnesses of 
	fits = [ind.fitness.values[0] for ind in pop]

	g = 0

	# Begin the evolution
	while g < 100:#pendiente cambiar

		print(threading.active_count())


		casosZeros = crearA(True,75)
		casosOnes = crearA(False,75)

		control.setVal(casosZeros,casosOnes)

		print(g)
		# A new generation
		g = g + 1
		print("-- Generation %i --" % g)

		# Select the next generation individuals
		offspring = toolbox.select(pop, len(pop))

		# Clone the selected individuals
		offspring = list(map(toolbox.clone, offspring))

		# Apply crossover and mutation on the offspring
		for child1, child2 in zip(offspring[::2], offspring[1::2]):

			# cross two individuals with probability CXPB
			if random.random() < CXPB:
				toolbox.mate(child1, child2)

				# fitness values of the children
				# must be recalculated later
				del child1.fitness.values
				del child2.fitness.values

		for mutant in offspring:

			# mutate an individual with probability MUTPB
			if random.random() < MUTPB:#pendiente cambiar
				toolbox.mutate(mutant)
				del mutant.fitness.values

		# Evaluate the individuals with an invalid fitness
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = map(toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit

		# The population is entirely replaced by the offspring
		pop[:] = offspring

		# Gather all the fitnesses in one list and print the stats
		fits = [ind.fitness.values[0] for ind in pop]

		length = len(pop)
		mean = sum(fits) / length
		sum2 = sum(x*x for x in fits)
		std = abs(sum2 / length - mean**2)**0.5

		print("  Min %s" % min(fits))
		print("  Max %s" % max(fits))
		print("  Avg %s" % mean)
		print("  Std %s" % std)

	print("-- End of (successful) evolution --")

	print(R.getMax())
	print(R.getResult())

	#best_ind = tools.selBest(pop, 1)[0]
	#rint("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

if __name__ == "__main__":
	main()

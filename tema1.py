# import sys

moveToTheRight = 'R'
moveToTheLeft = 'L'
hold = 'H'
hashChar = '#'

def readTM(turingMachine):
	# codificarea masinii Turing:
	nrStates = turingMachine[0]                             # numarul de stari
	finalStates = turingMachine[1].split()                  # starile finale
	transitionsList = turingMachine[2:len(turingMachine)]   # lista de tranzitii
	outputTM = {}		# formez un dictionar pentru stocarea datelor prelucrate
	outputTM["nrStates"] = nrStates
	outputTM["finalStates"] = finalStates
	outputTM["transitionsList"] = transitionsList
	return outputTM

def step(inputList, outputTM):
	emptyLeft = '('
	emptyRight = ')'
	stepOutputList = []
	false = [["False"]]
	contor = -1
	for iWord in inputList:
		word = iWord.split(',')
		for iTransition in outputTM["transitionsList"]:
			transition = iTransition.split()
			if word[1] == transition[0]:
				if word[2][0] == transition[1]:
					word[1] = transition[2]
					word[2] = transition[3] + word[2][1:]
					if transition[4] == moveToTheRight:
						word[0] += word[2][0]
						word[2] = word[2][1:]
					elif transition[4] == moveToTheLeft:
						word[2] = word[0][-1] + word[2]
						word[0] = word[0][:-1]
					elif transition[4] == hold:
						pass
					if word[0] == emptyLeft:
						word[0] = word[0] + hashChar
					if word[2] == emptyRight:
						word[2] = hashChar + word[2]
					stepOutputList.append(word)
					contor = 1
					break
				else:
					contor = 0
					continue
			else:
				contor = 0
		if contor == 0:
			stepOutputList += false
	# afisez lista de output sub forma de string
	stepListOutput = ' '.join(list(map(','.join, stepOutputList)))
	return stepListOutput

def accept(inputList, outputTM):
	acceptOutputList = []
	if outputTM["finalStates"][0] == '-':	# nu am stari finale => nu accepta
		for word in inputList:
			acceptOutputList.append("False")
		return ' '.join(acceptOutputList)
	for word in inputList:
		state = '0'
		i = contor1 = contor2 = 0
		restart = True
		while restart:
			for iTransition in outputTM["transitionsList"]:
				transition = iTransition.split()
				contor1 += 1
				if state == transition[0]:
					if word[i] == transition[1]:
						state = transition[2]
						# verific daca starea curenta este finala
						for finalState in outputTM["finalStates"]:
							if state == finalState:
								contor2 = 1
								acceptOutputList.append("True")
								restart = False
								break
						word = word[0:i] + transition[3] + word[(i + 1):]
						if transition[4] == moveToTheLeft:
							i -= 1
							if i < 0:
								i = 0
								word = hashChar + word
						elif transition[4] == moveToTheRight:
							i += 1
							if i >= len(word):
								word = word + hashChar
						elif transition[4] == hold:
							restart = False
							break

						contor1 = 0
						break
					else:
						continue
				else:
					# am ajuns la capatul listei si nu am gasit tranzitia buna
					if contor1 == len(outputTM["transitionsList"]):
						restart = False
						break
					continue
		if contor2 == 0: # m-am oprit si nu am ajuns in nicio stare finala
			acceptOutputList.append("False")
	return ' '.join(acceptOutputList)

def k_accept(inputList, outputTM):
	kAcceptOutputList = []
	if outputTM["finalStates"][0] == '-':	# nu am stari finale => nu accepta
		for word in inputList:
			kAcceptOutputList.append("False")
		return ' '.join(kAcceptOutputList)
	for element in inputList:
		# formez liste de tipul [cuvant, kPasi]
		element = element.split(',')
		word = element[0]
		kSteps = element[1]
		state = '0'
		restart = True
		i = steps = contor2 = 0
		while restart:
			contor1 = 0
			for iTransition in outputTM["transitionsList"]:
				transition = iTransition.split()
				contor1 += 1
				if state == transition[0]:
					if word[i] == transition[1]:
						steps += 1
						state = transition[2]
						# verific daca starea curenta este finala
						for finalState in outputTM["finalStates"]:
							if state == finalState:
								contor2 = 1
								kAcceptOutputList.append("True")
								restart = False
								break
						word = word[0:i] + transition[3] + word[(i + 1):]
						if transition[4] == moveToTheLeft:
							i -= 1
							if i < 0:
								i = 0
								word = hashChar + word
						elif transition[4] == moveToTheRight:
							i += 1
							if i >= len(word):
								word = word + hashChar
						elif transition[4] == hold:
							restart = False
							break
						# daca am executat kSteps pasi, ma opresc
						if steps == int(kSteps):
							restart = False
							break
						break
					else:
						continue
				else:
					# am ajuns la capatul listei si nu am gasit tranzitia buna
					if contor1 == len(outputTM["transitionsList"]):
						restart = False
						break
					continue
		if contor2 == 0:	# m-am oprit si nu am ajuns in nicio stare finala
			kAcceptOutputList.append("False")
	return ' '.join(kAcceptOutputList)


def main():
	f = open("accept5.in", "r")
	lista = f.read().splitlines()
	# lista = sys.stdin.readlines()
	lista = [x.replace('\n', '') for x in lista]
	taskType = lista[0]                 # tipul taskului
	inputList = lista[1].split()        # lista de inputuri
	turingMachine = lista[2:]           # lista cu codificarea masinii Turing
	outputTM = readTM(turingMachine)
	if taskType == "step":
		stepOutputList = step(inputList, outputTM)
		print(stepOutputList)
	elif taskType == "accept":
		acceptOutputList = accept(inputList, outputTM)
		print(acceptOutputList)
	elif taskType == "k_accept":
		kAcceptOutputList = k_accept(inputList, outputTM)
		print(kAcceptOutputList)

main()
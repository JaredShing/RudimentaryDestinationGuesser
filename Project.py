from decimal import Decimal
import numpy as np
import math

# Multiplier that scales the direction of the movement
multiplier = 5

# Creates an action list of different directions that can be taken from a
# given location
actions = {}
# stationary
actions[0] = [0, 0]
# up
actions[1] = [0, 1 * multiplier]
# down
actions[2] = [0, -1 * multiplier]
# right
actions[3] = [1 * multiplier, 0]
# left
actions[4] = [-1 * multiplier, 0]
# top right
actions[5] = [1 * multiplier, 1 * multiplier]
# top left
actions[6] = [1 * multiplier, -1 * multiplier]
# bottom right
actions[7] = [-1 * multiplier, 1 * multiplier]
# bottom left
actions[8] = [-1 * multiplier, -1 * multiplier]

statesFile = open('ParsedStates.txt', 'r')
# creates a list of the parsed states and corresponding actions
states = {}
correspondingActions = {}
count = 0
state = statesFile.readline()
# fills the list of parsed states and corresponding actions
while state != "":
	stateSplit = state.split(" | ")
	states[count] = [int(stateSplit[0]), int(stateSplit[1])]
	correspondingActions[count] = actions[int(stateSplit[2])]
	count += 1
	state = statesFile.readline()

print(states)
print(correspondingActions)

# declares the list of potential destinations
thetas = {}
count = 0

parsedFile = open('ParsedLocations.txt', 'r')

# going through the file to find the first line with locations (skips header
# info)
location = parsedFile.readline()
location = parsedFile.readline()
location = parsedFile.readline()
location = parsedFile.readline()
location = parsedFile.readline()

# beta represents the confidence that the human's actions are logical
# (currently set low because roads and actions might point the other way,
# hopefully will be offset by a multitude of actions and states pointing
# in the right action)
beta = 0.1
guessedPrior = []
visitPrior = []

# Sets the different goal locations
while location != "":
	locationSplit = location.split(" | ")
	y = int(locationSplit[2])
	x = int(locationSplit[1])
	thetas[count] = [x, y]
	guessedPrior.append(Decimal(locationSplit[3])) 
	visitPrior.append(Decimal(locationSplit[4]))
	count += 1 
	location = parsedFile.readline()

# This function returns the frobenius norm of the vector calculated from the
# goal - the (state + action)
# theta = destination
# s = state provided
# a = action taken at the s state provided
def qFunction(theta, s, a):
	return -1 * np.linalg.norm(np.subtract(theta, np.add(s, a)), ord=1)

# This function determines the probability of taking the provided action
# at a certain state given all possible actions at that state
# theta = destination
# s = state provided
# a = action taken at the s state provided
# beta = confidence provided actions are logical
# actions = the list of possible actions
def probability(theta, s, a, beta, actions):
	sum = 0
	for action in actions:
		sum += math.exp(beta * qFunction(theta, s, actions[action]))
	numerator = math.exp(beta * qFunction(theta, s, a))
	return numerator * 1.0 / sum

def compoundedProb(theta, states, corrAction, beta, actions):
	returnVal = 1
	for state in states:
		returnVal *= probability(theta, states[state], corrAction[state], beta, actions)
	return returnVal

probUniThetas = {}
probGuessedThetas = {}
probVisitThetas = {}
pUniSum = 0
pGuessedSum = 0
pVisitSum = 0

for theta in thetas:
	print(thetas[theta])
	probUniThetas[theta] = compoundedProb(thetas[theta], states, correspondingActions, beta, actions)
	pUniSum += probUniThetas[theta]
	# probGuessedThetas[theta] = guessedPrior[theta] * Decimal(compoundedProb(thetas[theta], states, correspondingActions, beta, actions))
	# pGuessedSum += probGuessedThetas[theta]
	# probVisitThetas[theta] = visitPrior[theta] * Decimal(compoundedProb(thetas[theta], states, correspondingActions, beta, actions))
	# pVisitSum += probVisitThetas[theta]
	probGuessedThetas[theta] = float(guessedPrior[theta]) * compoundedProb(thetas[theta], states, correspondingActions, beta, actions)
	pGuessedSum += probGuessedThetas[theta]
	probVisitThetas[theta] = float(visitPrior[theta]) * compoundedProb(thetas[theta], states, correspondingActions, beta, actions)
	pVisitSum += probVisitThetas[theta]

# print(probThetas)
# print(pSum)

for theta in probUniThetas:
	probUniThetas[theta] = probUniThetas[theta] / pUniSum
	probGuessedThetas[theta] = probGuessedThetas[theta] / pGuessedSum
	probVisitThetas[theta] = probVisitThetas[theta] / pVisitSum

# sumProb = 0
# for theta in probVisitThetas:
# 	sumProb += probVisitThetas[theta]

# print("Uniform Priors")
# print(probUniThetas)
# print("\nGuessed Priors")
# print(probGuessedThetas)
# print("\nVisited Priors")
# print(probVisitThetas)

print("Uniform Priors: Probability of Goal in Percentage")
for theta in probUniThetas:
	print(str(theta) + ": " + str(probUniThetas[theta] * 100))
print("\nGuessed Priors: Probability of Goal in Percentage")
for theta in probGuessedThetas:
	print(str(theta) + ": " + str(probGuessedThetas[theta] * 100))
print("\nVisited Priors: Probability of Goal in Percentage")
for theta in probVisitThetas:
	print(str(theta) + ": " + str(probVisitThetas[theta] * 100))


# print(sumProb)

statesFile.close()
parsedFile.close()
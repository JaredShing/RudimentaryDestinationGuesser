from decimal import Decimal

# opens the files to read and write to
locationFile = open('LocationInfo.txt', 'r')
parsedFile = open('ParsedLocations.txt', 'w')
location = locationFile.readline()
locationSplit = location.split(" | ")

# Variables trying to find the bounds of the locations. Finds the highest and
# lowest latitude/longitude, but starts initial values as first location read
up = float(locationSplit[1])
down = float(locationSplit[1])
left = float(locationSplit[2])
right = float(locationSplit[2])

# guessedPrior is the array of predicted priors the user input in the location
# file
guessedPrior = []
# sum of the predicted priors
guessedSum = 0
# array of the number of visits per location (will be used to determine actual
# prior)
visitPrior = []
# sum of the number of visits
visitSum = 0

# Reads through the file and finds the bottom left and top right
while location != "":
	locationSplit = location.split(" | ")
	# assigns latitude and longitude
	lat = float(locationSplit[1])
	longitude = float(locationSplit[2])

	# if the newly read latitude or longitude is higher or lower
	# than the current high/low value, the old value is replaced
	if lat > up:
		up = lat
	elif lat < down:
		down = lat

	if longitude < left:
		left = longitude
	elif longitude > right:
		right = longitude

	# updates the guessedPrior list and sum as well as the visitPrior
	# and sum
	guessedPrior.append(Decimal(locationSplit[3]))
	guessedSum += Decimal(locationSplit[3])
	visitPrior.append(Decimal(locationSplit[4]))
	visitSum += Decimal(locationSplit[4])

	location = locationFile.readline()

# Writes to the file that will be the parsed file and gives the bounds of the
parsedFile.write("BotLeft: " + str(down) + ", " + str(left) + "\n")
parsedFile.write("TopRight: " + str(up) + ", " + str(right) + "\n\n")
parsedFile.write("Location | X Coordinate | Y Coordinate | Guessed Prior "
	+ "| Visit Prior\n")

# Difference between highest and lowest longitude and latitude
latDiff = up - down
longDiff = right - left

# Creates the multiplier to make a 1000 x 1000 grid
thousandLatGrid = 1
thousandLongGrid = 1
while latDiff * thousandLatGrid < 100:
	thousandLatGrid *= 10
while longDiff * thousandLongGrid < 100:
	thousandLongGrid *= 10

while latDiff * thousandLatGrid < 200:
	thousandLatGrid *= 5
while longDiff * thousandLongGrid < 200:
	thousandLongGrid *= 5

while latDiff * thousandLatGrid < 500:
	thousandLatGrid *= 2
while longDiff * thousandLongGrid < 500:
	thousandLongGrid *= 2

locationFile.close()

# reads the location file again to write to the parsed file
locationRead2 = open('LocationInfo.txt', 'r')
location = locationRead2.readline()
count = 0

# Writes to the parsed file the locations latitude and locitude converted to
# the 1000 x 1000 grid as well as converts the number of visits to the vist
# prior
while location != "":
	locationSplit = location.split(" | ")
	lat = (float(locationSplit[1]) - down) * thousandLatGrid
	longitude = (float(locationSplit[2]) - left) *  thousandLongGrid
	parsedFile.write(str(count) + ": " + locationSplit[0] + " | " + 
		str(round(longitude)) + " | " + str(round(lat)) + " | " + 
		str(guessedPrior[count] / guessedSum) + " | " + 
		str(visitPrior[count] / visitSum)[:10] + "\n")
	location = locationRead2.readline()
	count += 1

# Reads the states
statesFile = open('States.txt', 'r')
parsedStatesFile = open('ParsedStates.txt', 'w')
state = statesFile.readline()

# Parses the states file and writes to a new file with the sates converted
# to the 1000 x 1000
while state != "":
	stateSplit = state.split(", ")
	y = (float(stateSplit[0]) - down) * thousandLatGrid
	x = (float(stateSplit[1]) - left) * thousandLongGrid
	parsedStatesFile.write(str(round(x)) + " | " + str(round(y)) + " | " + stateSplit[2])
	state = statesFile.readline()

locationRead2.close()
parsedFile.close()
statesFile.close()
parsedStatesFile.close()
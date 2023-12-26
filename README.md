# RudimentaryDestinationGuesser

This code was created to guess the destination of a user, similar to how Google Maps might try and guess a user's destination. This code uses reward learning to help identify a desired location. It takes in the locations name, latitude, longitude, user guessed prior, # of times visited. It also requires a list of locations along the route (latitude and longitude) as well as the direction taken from the location. <br />

## Setting Up LocationInfo.txt
The longitude and latitude was taken from finding the location using Google Maps. By placing a marker on the spot a latitude and longitude can be recorded. This code won't mind having a wider range of locations (rather than confining it to a town, the locations could be all over the country).
<p align="center">
  <img width="671" alt="image" src="https://github.com/JaredShing/RudimentaryDestinationGuesser/assets/76510750/7ecbfd5d-a3a6-4b14-be8c-12d5d3a37d1d">
</p>

A destination can be guessed with a list of possible destinations (thetas or goals). An example of the information required of the location is in the LocationInfo.txt file. <br />
<br />
It requires: <br />
name | latitude | longitude | guessed prior | # of times visited  <br />
<br />
The name is for the convenience of the user. The guessed prior is the user input guess probability that they are going to go to the location. The # of times visited will be used to calculate the true probability that the person is going to a location. In the code the bounds of the map will be set by finding the upper and lower bounds of both latitude and longitude of the locations provided. It will then create a 1000 by 1000 grid and calculate the new location and parse both the location and states file into a new ParsedLocations.txt and ParsedStates.txt.  <br />

## Setting Up States.txt
In the States.txt file, similar to the locations file a specific format is required. <br />
latitude | longitude | direction <br />

The direction input is represented by a number. <br />
0 = stays in same spot <br />
1 = up <br />
2 = down <br />
3 = right <br />
4 = left <br />
5 = top right <br />
6 = top left <br />
7 = bottom right <br />
8 = bottom left <br />

## Running the Program
The only two files that need to be made for the code to run are the LocationInfo.txt and the States.txt. The user can then run <br />
```
python -m Parser
python -m Project
```

## Understanding the Code
Once everything is converted to a 1000 x 1000 grid using the Parser.py file, the Project.py file will go through the ParsedStates file and create 2 lists of the locations and actions from each location to iterate through. It will use these two lists to determine the probability of being at that state and taking that action in the probability function. The probability function also takes a beta value which is the confidence variable representing the confidence that the person is taking a logical action. Currently the beta value 0.1 (which can be changed) because the human might make an illogical action with the information given. This code only knows the 1000 x 1000 empty grid and can't detect buildings. The probability function takes in a state, given action, and goal/theta/destination and determines the probability of taking that action relative to all other actions. The numerator is $e^{βq(θ, s, a)}$ and is normalized using the summation of all actions $$e^{βq(θ, s, a)} / \left( \sum_{a=0}^8 e^{βq(θ, s, a)} \right)$$
<!-- $$ \sum_{a=0}^8 e^{βq(θ, s, a)}$$ -->
<!-- Test equation $$\[ \frac{e^{βq(θ, s, a)}}{\left( \sum_{a=0}^8 e^{βq(θ, s, a)} \right)} \]$$ -->

## Things that can be Improved
One of the biggest things that could be improved is the directions from a state not making sense. Because this is a ruimentary guesser it can't understand the road existing and obstacles like buildings being in the way. Therefore the correct action from a state might be to walk away from the destination to get on the road or walk to a bus stop, but using the current qfunction it can't understand the logic of doing that.

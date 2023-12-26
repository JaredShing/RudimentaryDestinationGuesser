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

## Running Program
The only two files that need to be made for the code to run are the LocationInfo.txt and the States.txt. The user can then run <br />
```
python -m Parser
python -m Project
```
## Understanding the Code
Once everything is converted to a 1000 x 1000 grid using the Parser.py file 

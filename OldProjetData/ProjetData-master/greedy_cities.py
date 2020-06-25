import matplotlib.pyplot as plt
import numpy as np
import math as math
import scipy as sy
import time as time

'''
Class that contains datas from a city
'''


class City:
        def __init__(self, x=0, y=0, name="null"):
                self.x = x
                self.y = y
                self.name = name

'''
Calculate distance between two cities
'''


def distance(currentCity, nextCity):
        distX = int(currentCity.x) - int(nextCity.x)
        distY = int(currentCity.y) - int(nextCity.y)
        dist = math.sqrt((distX**2) + (distY**2))

        return dist

'''
Connect two cities on the map
'''


def ConnectCities(city1, city2):
        plt.plot([int(city1.x), int(city2.x)],[int(city1.y), int(city2.y)], 'r')

# Jeu de données
# size = 10
# x = [10, 83, 64, 44, 8, 34, 86, 12, 70, 87, 52, 24, 29, 66, 40]
# y = [34, 90, 43, 72, 71, 28, 20, 10, 70, 54, 90, 93, 48, 16, 10]


xi = []
yi = []

for i in range(15):
        xi.append(sy.random.randint(0,101))
        yi.append(sy.random.randint(0,101))

# City position generation
# x = int(round(random.uniform(size=15))*10)
# y = int(round(random.uniform(size=15))*10)
# tab = np.c_[x,y,z]

z = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o"]
tab = np.c_[xi,yi,z]

cities = []

# Cities creation in cities tab
for item in tab:
        cities.append(City(item[0], item[1], item[2]))

start = cities[0] # City where we start
current = cities[0] # Current city

visitedCities = [] # Already visited city
visitedCities.append(start) # Starting city is stored

remainingCities = cities.copy() # Copying list of every city
remainingCities.pop(0) # Delete starting city


# Calculate distance from current to each unvisited city
# Save the shortest
# Shortest become current, popped from remaining cities and added to visited
# Do it while there still remain unvisited cities 
while len(remainingCities) > 0:
        distMin = 0
        for city in remainingCities:
                newDist = distance(current, city)
                if distMin == 0:
                        distMin = newDist
                        saved = city
                else:
                        if distMin > newDist:
                                distMin = newDist
                                saved = city
        visitedCities.append(saved)
        remainingCities.remove(saved)
        current = saved

visitedCities.append(start) # Add the start to make it a cycle

# Plot each city on the map
plt.plot(xi, yi, 'ro')

# Connect each city to the following one in the visitedCities tab
# for i in range(len(visitedCities)):
#        if i == len(visitedCities) -1:
#                break
#        ConnectCities(visitedCities[i], visitedCities[i+1])

# Display the map
plt.axis('scaled')
plt.show()

# Connect each city to the following one in the visitedCities tab
for i in range(len(visitedCities)):
       if i == len(visitedCities) -1:
               break
       ConnectCities(visitedCities[i], visitedCities[i+1])
plt.plot(xi, yi, 'ro')
plt.axis('scaled')

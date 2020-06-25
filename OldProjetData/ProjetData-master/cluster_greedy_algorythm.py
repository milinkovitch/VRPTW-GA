import matplotlib.pyplot as plt
import scipy as sy
from sklearn.datasets import make_blobs
from numpy import *
from sklearn.cluster import KMeans
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


def distance (currentCity, nextCity):
        distX = int(currentCity.x) - int(nextCity.x)
        distY = int(currentCity.y) - int(nextCity.y)
        dist = math.sqrt((distX**2) + (distY**2))

        return dist

'''
Connect two cities on the map
'''


def ConnectCities(city1, city2):
        plt.plot([int(city1.x), int(city2.x)],[int(city1.y), int(city2.y)], 'r')

'''
Greedy Algorithm
Return 
'''
def GreedyAlgorithm (cities, start):
    visitedCities = []
    visitedCities.append(start) # Starting city is stored
    remainingCities = cities.copy() # Copying list of every city

    current = start
    totalDist = 0

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
        totalDist += distMin

    visitedCities.append(start) # Add the start to make it a cycle
    return visitedCities, totalDist

timeBeginning = time.process_time()

###########################
# Variables
N_cities = 150
N_camions = 10

xi = []
yi = []

cities = []

# Génération des villes
# x = random.uniform(size=N_cities)*100
# y = random.uniform(size=N_cities)*100


for i in range(N_cities):
        xi.append(sy.random.randint(0,101))
        yi.append(sy.random.randint(0,101))

# Set starting city & delete it from the list
start = City(xi[0], yi[0])
xi.pop(0)
yi.pop(0)

coord = c_[xi,yi]

#i = 1 #Incremental cities ID

# # Cities creation in cities tab
# for item in tab:
#         cities.append(greedy_cities.City(item[0], item[1], i))
#         i += 1

##############################
# Uncomment to plot
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax.plot(coord[:, 0], coord[:, 1], '.')

##############################
km = KMeans(n_clusters=N_camions)
# km.fit(X)
km.fit(coord)

##############################
# On dessine le résultat en choisissant une couleur
# différente pour chaque cluster.

##############################
# Uncomment to plot
cmap = plt.cm.get_cmap("hsv", km.cluster_centers_.shape[0]) #Création de la ColorMap
fig, ax = plt.subplots(1, 1, figsize=(5, 5)) #Création du repère
colors = [cmap(i) for i in km.fit_predict(coord)] # Création Clustered Color Map
ax.scatter(coord[:, 0], coord[:, 1], c=colors)

# print(cmap)
# print(colors)

# print("\nPrint End")
clusters = km.fit_predict(coord) # Regroupement par cluster en partant des cluster_centers
coordcluster = c_[coord,clusters] # Concat. tab + N° de cluster

# sortedCoord = sorted(coordcluster, key = lambda x: x[2])

# print(coordcluster)
# print(sortedCoord)

selected = []

maximalDistance = 0

for i in range(N_camions):
    selected.clear()

    for line in coordcluster:
        if (line[2] == i):
            selected.append(City(line[0], line[1]))

    path, dist = GreedyAlgorithm(selected, start)
    maximalDistance += dist

    print("\nPath in cluster => " + str(i))
    for city in path:
        print(str(city.x) + "; " + str(city.y))

    for i in range(len(path)):
        if i == len(path) -1:
            break
        plt.plot(path[i].x, path[i].y, 'bo')
        ConnectCities(path[i], path[i+1])
        

timeEnd = time.process_time()

time = timeEnd - timeBeginning
print(timeBeginning)
print(timeEnd)
print(time)

print("Maximal distance" + str(maximalDistance))

f = open("stats.csv", 'a')
f.write(str(N_cities) + "," + str(time) + "," + str(N_camions) + "\n")
f.close()
import matplotlib.pyplot as plt
import scipy as sy
from sklearn.datasets import make_blobs
from numpy import *
from sklearn.cluster import KMeans
import time as time
import sys
import csv

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


def distance(currentcity, nextcity):
    dist_x = int(currentcity.x) - int(nextcity.x)
    dist_y = int(currentcity.y) - int(nextcity.y)
    dist_current_next = math.sqrt((dist_x ** 2) + (dist_y ** 2))

    return dist_current_next


'''
Connect two cities on the map
'''


def connect_cities(city1, city2):
    plt.plot([int(city1.x), int(city2.x)], [int(city1.y), int(city2.y)], 'r')


'''
Greedy Algorithm
Return city list in visiting order + total distance traveled
'''


def greedy_algorithm(city_list, starting_city):
    visited_cities = [starting_city]  # Starting city is stored
    remaining_cities = city_list.copy()  # Copying list of every city

    current = starting_city
    total_dist = 0
    saved = 0

    # Calculate distance from current to each unvisited city
    # Save the shortest
    # Shortest become current, popped from remaining cities and added to visited
    # Do it while there still remains unvisited cities
    while len(remaining_cities) > 0:
        dist_min = 0
        for remaining_city in remaining_cities:
            new_dist = distance(current, remaining_city)
            if dist_min == 0:
                dist_min = new_dist
                saved = remaining_city
            else:
                if dist_min > new_dist:
                    dist_min = new_dist
                    saved = remaining_city
        visited_cities.append(saved)
        remaining_cities.remove(saved)
        current = saved
        total_dist += dist_min

    visited_cities.append(starting_city)  # Add the start to make it a cycle
    return visited_cities, total_dist


'''
Read city position from CSV map and return tow list with X & Y positions
'''


def read_map(filename):
    with open(filename) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        x = []
        y = []
        for row in read_csv:
            x_row = row[0]
            y_row = row[1]

            x.append(int(x_row))
            y.append(int(y_row))

        # print(x, "\n", y)
        return x, y


# +++++++++++++++++++++
# Algorithm beginning

if len(sys.argv) < 3:
    sys.exit("Not enough arguments to run the script")

else:
    mapPath = sys.argv[1]
    N_trucks = int(sys.argv[2])

# Time start
timeBeginning = time.process_time()

###########################
# Variables
x, y = read_map(mapPath)

# Put each city in a table
cities = c_[x, y]

# Set starting city & delete it from the list
start = City(x[0], y[0])
x.pop(0)
y.pop(0)

# coord table does not contains starting city
coord = c_[x, y]

# Cluster Center creation with KMeans algorithm
km = KMeans(n_clusters=N_trucks)
km.fit(coord)

##############################
# Uncomment to plot
cmap = plt.cm.get_cmap("hsv", km.cluster_centers_.shape[0]) #ColorMap creation
# fig, ax = plt.subplots(1, 1, figsize=(5, 5)) # Axis creation
colors = [cmap(i) for i in km.fit_predict(coord)] # Cluster color map
# ax.scatter(coord[:, 0], coord[:, 1], c=colors)

clusters = km.fit_predict(coord)  # Group points in clusters from cluster centers
coord_cluster = c_[coord, clusters]  # Concat city table + cluster number

selected = []
maximalDistance = 0

# Perform a greedy algorithm in each cluster to find a local optimum
for i in range(N_trucks):
    selected.clear()

    for line in coord_cluster:
        if line[2] == i:
            selected.append(City(line[0], line[1]))

    path, dist = greedy_algorithm(selected, start)
    maximalDistance += dist

    # print("\nPath in cluster => " + str(i))
    # for city in path:
        # print(str(city.x) + "; " + str(city.y))

    for j in range(len(path)):
        if j == len(path) - 1:
            break
        plt.plot(path[j].x, path[j].y, 'bo')
        connect_cities(path[j], path[j + 1])

# Time stop
timeEnd = time.process_time()

time = timeEnd - timeBeginning
# print(timeBeginning)
# print(timeEnd)
# print(time)

# print("Maximal distance" + str(maximalDistance))

f = open("stats.csv", 'a')
f.write(str(len(cities)) + "," + str(time) + "," + str(N_trucks) + "\n")
f.close()

f = open("result.csv", 'a')
f.write(str(mapPath) + "," + str(maximalDistance) + "," + str(N_trucks) + "\n")
f.close()

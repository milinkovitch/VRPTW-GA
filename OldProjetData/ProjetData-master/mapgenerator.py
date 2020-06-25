import random
import csv


# Generate random number
def rand_gen(max_range):
    return random.randint(0, max_range)


# Generate random list of points and put them in the csv file
def map_generator(cities_number, max_distance, filename):
    x = []
    y = []
    for i in range(cities_number):  # Generate x et y lists with random numbers
        x.append(rand_gen(max_distance))
        y.append(rand_gen(max_distance))
    print(x, "\n", y)
    f = open(filename, 'w')  # Open csv file
    for j, k in zip(x, y):  # For each element in lists, put them in the csv file
        f.write(str(j) + "," + str(k) + "\n")
    f.close()


# Read th csv file
def read_map(filename):
    with open(filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        x = []
        y = []
        for row in read_csv:
            x_row = row[0]
            y_row = row[1]

            x.append(int(x_row))
            y.append(int(y_row))

        print(x, "\n", y)
        return x, y
'''
class City:
    def __init__(self, x=0, y=0, name="null"):
        self.x = x
        self.y = y
        self.name = name

def listToMatrix(x, y):
    matrixLength = len(x)
    print("Le longueur est : ", matrixLength, "\n\n")
    matrix = []
    citiesList = []
    for i in range(matrixLength-1):
        matrix.append([0] * matrixLength)
#        print(matrix[i])
    for j in range(len(x)):
#        print("\nx : ", x[j], "y : ", y[j])
        citiesList.append(City(x[j], y[j], j))
        print(citiesList[j].name)'''

cities = 0
for i in range(50):
    cities = cities + 100
    map_generator(cities, 2000, "maps/map" + str(cities) + ".csv")
# x, y = read_map("maps/map1.csv")
# listToMatrix(x, y)

from sklearn import linear_model

import matplotlib.pyplot as plt
import numpy as np
import csv
from statistics import median, mean, mode


def graph(x, y, title):
    # ----------------------------------------------------------------------------------------#
    # Step 1: training data

    max_x = max(x)
    max_y = max(y)

    x = np.asarray(x)
    y = np.asarray(y)

    x = x[:, np.newaxis]
    y = y[:, np.newaxis]

    plt.scatter(x, y)

    # ----------------------------------------------------------------------------------------#
    # Step 2: define and train a model

    model = linear_model.LinearRegression()
    model.fit(x, y)

    model_coef = (str(model.coef_)).replace("[", "").replace("]", "")
    model_intercept = (str(model.intercept_)).replace("[", "").replace("]", "")
    print("y = " + model_coef + "x + (" + model_intercept + ")")

    log_to_file("The equation of the linear regression line is y = ", str(model_coef), "<br>")
    log_to_file("x + (", str(model_intercept))
    reportFile.write(")<br>")

    # ----------------------------------------------------------------------------------------#
    # Step 3: prediction

    x_new_min = 0.0
    x_new_max = (max_x + 0.2 * max_x)

    x_new = np.linspace(x_new_min, x_new_max, 100)
    x_new = x_new[:, np.newaxis]

    y_new = model.predict(x_new)

    plt.plot(x_new, y_new, color='coral', linewidth=3)

    plt.grid()
    plt.xlim(x_new_min,x_new_max)
    plt.ylim(0, (max_y + 0.2 * max_y))

    plt.title(title,fontsize=10)
    plt.xlabel('Number of cities')
    plt.ylabel('Time needed to resolve shortest path (in seconds)')

    plt.savefig("report/" + title + ".png", bbox_inches='tight')
#    plt.show()
    plt.close()


# This method read the csv stats file
def open_csv(filename):
    with open(filename) as csvFile:
        read_csv_file = csv.reader(csvFile, delimiter=',')
        cities_number_list = []
        time_list = []
        truck_number_list = []
        for row in read_csv_file: # Read line by line
            first_row = row[0]
            second_row = row[1]
            third_row = row[2]

            cities_number_list.append(float(first_row)) # Put all the data in lists
            time_list.append(float(second_row))
            truck_number_list.append((float(third_row)))

        print(cities_number_list, "\n", time_list, "\n", truck_number_list)
        return cities_number_list, time_list, truck_number_list


# This method generate statistics for all different number of truck used
def statistic_creator(cities_number_list, time_list, truck_number_list):
    sorted_truck_list = sorted(list(dict.fromkeys(truck_number_list))) # Sort list and remove duplicates
    print("sortedTruckList :", sorted_truck_list)
    for truckNumber in sorted_truck_list: # For all different number of truck used
        temp_cities_list = []
        temp_time_list = []
        temp_truck_list = []
        for i in range(len(truck_number_list)): # Get the cities and the time needed
            if truck_number_list[i] == truckNumber:
                temp_cities_list.append(cities_number_list[i])
                temp_time_list.append(time_list[i])
                temp_truck_list.append(truck_number_list[i])
        title = str(truckNumber) + " Trucks"
        stats(temp_cities_list, temp_time_list, title) # And create stats


# This method generate statistics for a specific number of truck used
def stats (cities_number_list, time_list, title):
    log_to_file("Statistics with : ", title, "\n\n<h1 align=\"center\">", "</h1>") # Write title to logfile
    reportFile.write("</h1>")
    # log_to_file("\ncities_number_list : ", str(citiesNumberList), "<br>")
    # log_to_file("\ntime_list : ", str(timeList), "<br>")
    log_to_file("\nThe lists are composed of ", str(len(cities_number_list)), "<br>")
    reportFile.write(" data <br>\n")

    graph(cities_number_list, time_list, title) # Generate the scatter graph with the regression line
    median_temp = median(time_list) # Calculate the Median
    mean_temp = mean(time_list) # Calculate the Mean
    range_temp = (max(time_list) - min(time_list)) # Calculate the range
    q1temp = np.percentile(np.asarray(time_list), 25) # Calculate the first quartile
    q3temp = np.percentile(np.asarray(time_list), 75) # Calculate the third quartile
    variance_temp = np.var(np.asarray(time_list), 0) # Calculate the variance

    log_to_file("\nThe median is : ", str(median_temp), "<br>") # Log all the statistics
    log_to_file("\nThe mean is : ", str(mean_temp), "<br>")
    log_to_file("\nThe range is : ", str(range_temp), "<br>")
    log_to_file("\nThe first quartile is : ", str(q1temp), "<br>")
    log_to_file("\nThe third quartile is : ", str(q3temp), "<br>")
    log_to_file("\nThe variance is : ", str(variance_temp), "<br>")

    reportFile.write("\n<p align=\"center\">\n\t<IMG src=\"")
    reportFile.write(title)
    reportFile.write(".png\" alt=\"")
    reportFile.write(title)
    reportFile.write("\" border=\"0\" width=\"562\" height=\"452\">\n</p>")


def log_to_file(string, value, first_html_tag = None, last_html_tag = None):
    if first_html_tag is not None:
        reportFile.write(first_html_tag)
    reportFile.write(string)
    reportFile.write(value)
    if last_html_tag is not None:
        reportFile.write(last_html_tag)


# Write the beginning of the HTML file
def init_report_file():
    reportFile.write("<!DOCTYPE html>\n<html>\n<head lang=\"en\">\n\t<meta charset=\"UTF-8\">\n"
                     "\t<title>Report of statistics</title>\n</head>\n<body>")
    reportFile.write("All the statistics have been done on the time needed to resolve the shortest path, "
                     "not on the number of cities <br>")


reportFile = open("report/report.html", "w")
init_report_file()
citiesNumberList, timeList, truckNumberList = open_csv('stats.csv')
stats(citiesNumberList, timeList, "Global stats")
statistic_creator(citiesNumberList, timeList, truckNumberList)
reportFile.close()

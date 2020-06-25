import os
import sys
import subprocess


map_directory = str(os.path.dirname(os.path.abspath(__file__))) + '\\maps'
n_trucks = 10

if len(sys.argv) == 3:
    map_directory = sys.argv[1]
    n_trucks = sys.argv[2]


for files in os.listdir(map_directory):
    print("Currently: " + str(files))
    subprocess.run(["python", "script_cluster_greedy.py", str(map_directory) + "\\" + str(files), n_trucks])


def final_time(truck_number):  # Calculate the time required for maps
    time_counter = 0
    buffer = 0
    file = reversed(list(open("stats.csv")))  # Read the file from end to the top
    for line in file:
        buffer = buffer + 1
        if buffer < int(truck_number):  # For each line
            parsed = line.rstrip().split(",")  # Parse the time
            time_counter = time_counter + float(parsed[1])  # Add the time to the finalTime
    print("\nFinal time to calculate all the maps : " + str(time_counter) + " (in seconds)")


final_time(sys.argv[2])


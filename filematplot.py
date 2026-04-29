import csv
import matplotlib.pyplot as plt

times = []

with open("times.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            times.append(float(row[0]))

plt.plot(times)
plt.title("Temps par coup")
plt.xlabel("coup")
plt.ylabel("temps (s)")
plt.savefig(    "move_times.png")

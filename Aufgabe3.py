import numpy as np
import matplotlib.pyplot as plt
import requests
import io
from itertools import combinations
from math import comb

URL_AUFGABE = "https://bwinf.de/fileadmin/wettbewerbe/bundeswettbewerb/43/1_runde/wandern7.txt"

response = requests.get(URL_AUFGABE)

data_web = response.content
data_web_file = io.BytesIO(data_web)


data = np.loadtxt(data_web_file, skiprows=1, dtype=int)

starts, ends = data[:, 0].astype(int), data[:, 1].astype(int)

min_val,max_val = starts.min(), ends.max()


candidate_pool = np.unique(data.flatten()) #create candidate pool we can count starts and ends of ranges, we can safely ingore last element


point_coverage = np.zeros(len(candidate_pool), dtype=int) #pre processing to compute coverage for each point

for i, point in enumerate(candidate_pool):
  
    point_coverage[i] = np.sum((starts <= point) & (point <= ends))  # see how many ranges are satisfied by point


point_coverage_pairs = zip(point_coverage, candidate_pool)
 
sorted_pairs = np.array(sorted(point_coverage_pairs, reverse=True)) # ascending order


sorted_points = sorted_pairs[:,1]



def generate_3_combinations(pool): #generate all combinations of the 3 points among the candidate pool
    n = len(pool)
    combinations = []
    for point_1 in range(n):
        for point_2 in range(point_1 + 1, n): # +1 to make sure it is after points_1
            for point_3 in range(point_2 + 1, n):
                combinations.append([pool[point_1], pool[point_2], pool[point_3]])
    return combinations




max_covered = 0
best_combination = None

for points in generate_3_combinations(sorted_points[:60]):                # Only consider the top 60 points for speed reasons/ imperfect
    covered_ranges = set()  
    
    for i in range(data.shape[0]):
        start, end = data[i, 0],  data[i, 1]

        if any(start <= point <= end for point in points): # see for each range if point is in any range 
            covered_ranges.add(i)  

    if len(covered_ranges) > max_covered:       # see if current best is better than total best
        max_covered = len(covered_ranges)
        best_combination = points

    if max_covered == data.shape[0]:
        break



print(f"The best combination is {best_combination}, covering {max_covered} ranges and missing {data.shape[0] - max_covered}")


counts = np.zeros(max_val - min_val + 2).astype(int) # +2 because it would be +1 without inclusive so we add 2 

np.add.at(counts, starts - min_val, 1) # normalise 
np.add.at(counts, ends - min_val + 1, -1)# +1 because it is inclusive

results = np.cumsum(counts[:-1]) #slicing last element because it can only be a decrement, only for visualisation



x_vals = np.arange(min_val, max_val + 1) # need to shift x values to the right

plt.plot(x_vals, results)

plt.scatter(best_combination, [results[point - min_val] for point in best_combination], 
            color='red', zorder=5)

plt.show()


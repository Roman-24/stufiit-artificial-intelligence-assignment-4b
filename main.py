
import random
import math
import copy
import numpy as np
import time
from tkinter import *

NUM_OF_POINTS = 1020
INTERVAL = 5000
DEVIATION = 100
WINDOW_SIZE = 720


colors = ['dodgerblue', 'red', 'gold', 'forestgreen', 'orange', 'midnightblue', 'darkgreen', 'darkkhaki',
          'salmon', 'deeppink', 'dimgrey', 'seagreen', 'cyan', 'saddlebrown', 'springgreen', 'violetred',
          'steelblue', 'lawngreen', 'hotpink', 'slateblue', 'maroon', 'darkviolet', 'black']

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# generate first 20 points
def init():
    first_20 = []
    unique_rand_nums = set()

    while True:
        rand_num = random.randint(-INTERVAL, INTERVAL)
        unique_rand_nums.add(rand_num)

        if len(unique_rand_nums) == 40:
            break

    for index in range(20):
        first_20.append(Point(unique_rand_nums.pop(), unique_rand_nums.pop()))

    return first_20


def generate_others(first_20):
    all_points = []
    all_points += first_20
    counter = 20

    while counter < NUM_OF_POINTS:
        point = random.choice(all_points)

        x_offset = int(random.gauss(-DEVIATION, DEVIATION))
        y_offset = int(random.gauss(-DEVIATION, DEVIATION))
        new_point = Point(point.x + x_offset, point.y + y_offset)
        all_points.append(new_point)
        counter += 1

    return all_points

def main():
    print("Pycharm starting..")

    first_20 = init()
    all_points = generate_others(first_20)

    user_choise = input("1) K-Means with centroid\n2) K-Means with medoid\n3) Divisive clustering\n4) Agglomerative clustering\nYour choice: ")
    start_time = time.time()

    

if __name__ == "__main__":
    main()
# end
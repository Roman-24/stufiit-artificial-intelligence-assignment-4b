
import random
import math
import copy
import time
from tkinter import *

NUM_OF_POINTS = 20000
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
        self.cluster_id = None
        self.not_in_cluster = True

# prvych 20 unikatnych points
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
    counter = 0

    while counter < NUM_OF_POINTS:
        point = random.choice(all_points)

        x_offset = int(random.gauss(-DEVIATION, DEVIATION))
        y_offset = int(random.gauss(-DEVIATION, DEVIATION))

        new_point = Point(point.x + x_offset, point.y + y_offset)
        all_points.append(new_point)
        counter += 1

    return all_points

# vypocita vzdialenost dvoch bodov
def euclidean_dist(point_1, point_2):
    return math.sqrt(math.pow(point_1.x - point_2.x, 2) + math.pow(point_1.y - point_2.y, 2))

def k_means(k, points, type):

    clusters = [[] for _ in range(k)]

    # create "k" clusters
    for cluster_num in range(k):
        centroid = random.choice(points)

        points[points.index(centroid)].cluster_id = cluster_num
        clusters[cluster_num].append(centroid)

    # rozdelenie points do clusterou podla toho k comu bude najblizsie
    for poin in points:
        best_euclid_dist = 999999999

        for cluster in clusters:
            euclid_dist = euclidean_dist(cluster[0], poin)

            if euclid_dist < best_euclid_dist:
                poin.cluster_id = clusters.index(cluster)
                best_euclid_dist = euclid_dist

    draw(points)
    pass

def coordinates(point):
    size = (INTERVAL + DEVIATION) * 4
    left = WINDOW_SIZE / 2 - 1
    right = WINDOW_SIZE / 2 + 1
    return int(point.x / size * WINDOW_SIZE + left), int(point.y / size * WINDOW_SIZE + left), int(point.x / size * WINDOW_SIZE + right), int(point.y / size * WINDOW_SIZE + right)

def draw(points):
    master = Tk()
    master.title("Clusters")
    canvas = Canvas(master, width=WINDOW_SIZE, height=WINDOW_SIZE, bg='whitesmoke')
    canvas.pack()

    for point in points:
        canvas.create_oval(coordinates(point), fill=colors[point.cluster_id], outline='')

    master.mainloop()
    pass

def main():
    print("Pycharm starting..")

    first_20 = init()
    all_points = generate_others(first_20)

    user_choise = input("1) K-Means with centroid\n2) K-Means with medoid\n3) Divisive clustering\n4) Agglomerative clustering\nYour choice: ")

    k = 20

    if user_choise == "1":
        start_time = time.time()
        clusters = k_means(k, copy.deepcopy(all_points), "centroid")
        # average = summarize(clusters)
        end_time = time.time()
        print("Time:", round((end_time - start_time) / 60, 3), "min")
        pass

    elif user_choise == "2":
        start_time = time.time()
        clusters = k_means(k, copy.deepcopy(all_points), "medoid")
        # average = summarize(clusters)
        end_time = time.time()
        print("Time:", round((end_time - start_time) / 60, 3), "min")
        pass

    elif user_choise == "3":
        pass
    elif user_choise == "4":
        pass
    pass


if __name__ == "__main__":
    main()
# end
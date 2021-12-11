
import random
import math
import time
from tkinter import *
import numpy as np

NUM_OF_POINTS = 20000
INTERVAL = 5000
OFFSET = 100
SIZE_OF_WINDOW = 720

colors = ['AntiqueWhite1', 'CadetBlue1', 'DarkGoldenrod1', 'DarkOliveGreen1', 'DarkOrange1', 'DarkSeaGreen4', 'HotPink4', 'IndianRed4', 'LavenderBlush2', 'LemonChiffon2', 'LightCyan2', 'LightGoldenrod1', 'LightPink1', 'LightSalmon3', 'LightSkyBlue4', 'LightYellow4', 'MediumOrchid1', 'MediumPurple2', 'OrangeRed3', 'PaleGreen4', 'PaleTurquoise1', 'PeachPuff2','RosyBrown1', 'RoyalBlue1', 'SlateGray2', 'SteelBlue4', 'VioletRed1', 'antique white', 'aquamarine', 'azure', 'blanched almond', 'blue', 'blue violet', 'brown1', 'burlywood4', 'cadet blue', 'chartreuse2', 'chocolate1', 'cornflower blue', 'cyan4', 'dark goldenrod', 'dark green', 'dark khaki', 'dark olive green', 'dark orange', 'dark orchid', 'dark salmon', 'dark sea green', 'dark slate blue', 'dark slate gray', 'dark turquoise', 'dark violet', 'deep pink', 'deep sky blue', 'dim gray', 'dodger blue', 'firebrick1', 'firebrick2', 'firebrick3', 'firebrick4', 'floral white', 'forest green', 'gainsboro', 'ghost white', 'gold', 'goldenrod', 'gray', 'gray99', 'green yellow', 'honeydew4', 'hot pink', 'indian red', 'ivory4', 'khaki', 'khaki4', 'lavender', 'lavender blush', 'lawn green', 'lemon chiffon', 'light blue', 'light coral', 'light cyan', 'light goldenrod', 'light goldenrod yellow', 'light grey', 'light pink', 'light salmon', 'light sea green', 'light sky blue', 'light slate blue', 'light slate gray', 'light steel blue', 'light yellow', 'lime green', 'linen', 'magenta4', 'maroon', 'maroon4', 'medium aquamarine', 'medium blue', 'medium orchid', 'medium purple', 'medium sea green', 'medium slate blue', 'medium spring green', 'medium turquoise', 'medium violet red', 'midnight blue', 'mint cream', 'misty rose', 'navajo white', 'navy', 'old lace', 'olive drab', 'orange', 'orange red', 'orange4', 'orchid1', 'orchid4', 'pale goldenrod', 'pale green', 'pale turquoise', 'pale violet red', 'papaya whip', 'peach puff', 'pink', 'pink4', 'plum1', 'plum4', 'powder blue', 'purple', 'red', 'rosy brown', 'royal blue', 'saddle brown', 'salmon', 'sandy brown', 'sea green', 'seashell2', 'sienna1', 'sky blue', 'slate blue', 'slate gray', 'snow', 'spring green', 'steel blue', 'tan1', 'thistle', 'thistle1', 'tomato', 'turquoise', 'turquoise1', 'violet red', 'wheat1', 'white smoke', 'yellow', 'yellow green']

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

        x_offset = int(random.gauss(-OFFSET, OFFSET))
        y_offset = int(random.gauss(-OFFSET, OFFSET))

        new_point = Point(point.x + x_offset, point.y + y_offset)
        all_points.append(new_point)
        counter += 1

    return all_points

# vypocita vzdialenost dvoch bodov
def euclidean_dist(point_1, point_2):
    return math.sqrt(math.pow(point_1.x - point_2.x, 2) + math.pow(point_1.y - point_2.y, 2))

def k_means(k, points, medoid_flag):

    clusters = [[] for _ in range(k)]

    # create "k" clusters
    for cluster_num in range(k):
        centroid = random.choice(points)
        points[points.index(centroid)].cluster_id = cluster_num
        clusters[cluster_num].append(centroid)

    # rozdelenie points do clusterou podla toho k comu bude najblizsie
    for point in points:
        best_euclid_dist = 999999999
        for cluster in clusters:
            euclid_dist = euclidean_dist(cluster[0], point)

            if euclid_dist < best_euclid_dist:
                point.cluster_id = clusters.index(cluster)
                best_euclid_dist = euclid_dist

        clusters[point.cluster_id].append(point)

    # 20 krat prepocitaj stred a preskup clustre
    for i in range(100):
        # print(f"Iter: {i}")
        clusters_new = []
        # vypocitanie novych centroidov
        for cluster_num in range(k):
            mean_x = np.mean([point.x for point in clusters[cluster_num]])
            mean_y = np.mean([point.y for point in clusters[cluster_num]])
            new_mid = Point(mean_x, mean_y)

            # z centroid urob medoid
            if medoid_flag:
                best_euclid_dist = 999999999
                for point_temp in points:

                    euclid_dist = euclidean_dist(new_mid, point_temp)

                    if euclid_dist < best_euclid_dist:
                        new_mid_2 = point_temp
                        best_euclid_dist = euclid_dist

                new_mid = new_mid_2

            str_temp = "medoid" if medoid_flag else "centroid"
            # print(f"Cluster: {cluster_num}, {str_temp}: x:{new_mid.x} y:{new_mid.y}")
            clusters_new.append(new_mid)

        # vytvor nove clustre na zaklade novych stredov
        del(clusters)
        clusters = [[] for _ in range(k)]
        for point in points:
            best_euclid_dist = 999999999
            for cluster_centroid in clusters_new:
                euclid_dist = euclidean_dist(cluster_centroid, point)

                if euclid_dist < best_euclid_dist:
                    point.cluster_id = clusters_new.index(cluster_centroid)
                    best_euclid_dist = euclid_dist

                if len(clusters[point.cluster_id]) == 0:
                    clusters[point.cluster_id].append(cluster_centroid)
            clusters[point.cluster_id].append(point)

    return points, clusters

def calculate_avg_dist_for_clusters(clusters):

    averages = []
    for i in range(len(clusters)):
        distances = []
        for j in range(1, len(clusters[i])):
            distances.append(euclidean_dist(clusters[i][j], clusters[i][0]))
        averages.append(sum(distances) / len(clusters[i]))

    return averages

def divisive(k, points):
    points, clusters = k_means(2, points, False)

    while len(clusters) < k:
        averages = calculate_avg_dist_for_clusters(clusters)
        cluster = clusters[averages.index(max(averages))]
        i_del = clusters.index(cluster)
        clusters.pop(i_del)
        if len(cluster) > 1:
            all_points, temp_clusters = k_means(2, cluster, False)
            clusters += temp_clusters

    for cluster in clusters:
        for point in cluster:
            point.cluster_id = clusters.index(cluster)

    return points, clusters

def agglomerative(k, all_points):

    pass

def position_data(point, size):
    size_repair = (INTERVAL + OFFSET) * 4
    left = (SIZE_OF_WINDOW / 2) - size
    right = (SIZE_OF_WINDOW / 2) + size
    return int(point.x / size_repair * SIZE_OF_WINDOW + left), int(point.y / size_repair * SIZE_OF_WINDOW + left), int(point.x / size_repair * SIZE_OF_WINDOW + right), int(point.y / size_repair * SIZE_OF_WINDOW + right)

def draw(points, title, clusters):
    master = Tk()
    master.title(title)
    canvas = Canvas(master, width=SIZE_OF_WINDOW, height=SIZE_OF_WINDOW, bg='whitesmoke')
    canvas.pack()
    for point in points:
        canvas.create_oval(position_data(point, 1), fill=colors[point.cluster_id], outline='')
    for cluster in clusters:
        canvas.create_oval(position_data(cluster[0], 3), outline="black")
    master.mainloop()
    pass

def print_results(clusters):
    averages = calculate_avg_dist_for_clusters(clusters)
    good_clesters = 0
    bad_clesters = 0
    for avg in averages:
        if avg > OFFSET * 5:
            bad_clesters += 1
        else:
            good_clesters += 1
    total_average = round(sum(averages) / len(averages), 4)
    return f"Pocet dobrych clusterov: {good_clesters}, pocet zlych clusterov: {bad_clesters}, globalny priemer vzdianosti: {total_average}"

def main():
    print("Pycharm starting..")
    my_range = 10
    user_choise = input("1) K-Means with centroid\n2) K-Means with medoid\n3) Divisive clustering\n4) Agglomerative clustering\nYour choice: ")
    k = 20

    if user_choise == "1":
        start_time = time.time()
        for i in range(my_range):
            first_20 = init()
            all_points = generate_others(first_20)
            all_points, clusters = k_means(k, all_points, False)
            #draw(all_points, "k_means, centroid", clusters)
            print(f"{i+1}: {print_results(clusters)}")
        end_time = time.time()
        print("Time:", round((end_time - start_time) / 60, 4), "min")

    elif user_choise == "2":
        start_time = time.time()
        for i in range(my_range):
            first_20 = init()
            all_points = generate_others(first_20)
            all_points, clusters = k_means(k, all_points, True)
            # draw(all_points, "k_means, medoid", clusters)
            print(f"{i+1}: {print_results(clusters)}")
        end_time = time.time()
        print("Time:", round((end_time - start_time) / 60, 4), "min")

    elif user_choise == "3":
        start_time = time.time()
        for i in range(my_range):
            first_20 = init()
            all_points = generate_others(first_20)
            all_points, clusters = divisive(k, all_points)
            # draw(all_points, "divisive, centroid", clusters)
            print(f"{i+1}: {print_results(clusters)}")
        end_time = time.time()
        print("Time:", round((end_time - start_time) / 60, 4), "min")

    elif user_choise == "4":
        start_time = time.time()
        for i in range(my_range):
            first_20 = init()
            all_points = generate_others(first_20)
            clusters = agglomerative(k, all_points)
            draw(all_points, "agglomerative, centroid", clusters)
            print(f"{i+1}: {print_results(clusters)}")
        end_time = time.time()
        print("Time:", round((end_time - start_time) / 60, 4), "min")

if __name__ == "__main__":
    # random.seed(500)
    main()
# end
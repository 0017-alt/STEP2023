import csv
import math

input_filename = ["input_0.csv", "input_1.csv", "input_2.csv", "input_3.csv", "input_4.csv", "input_5.csv", "input_6.csv"]
output_filename = ["output_0.txt", "output_1.txt", "output_2.txt", "output_3.txt", "output_4.txt", "output_5.txt", "output_6.txt"]

# 盤面を4分割して、それぞれの範囲で重みをつけて最短位置を探す関数
def get_distance_upper_right(cor2, max_x, max_y):
    return math.sqrt((max_x - float(cor2[0]))**2 + (max_y - float(cor2[1]))**2)

def get_distance(cor1, cor2):
    return math.sqrt((float(cor1[0]) - float(cor2[0]))**2 + (float(cor1[1]) - float(cor2[1]))**2)

def get_distance_lower_left(cor2, min_x, min_y):
    return math.sqrt((min_y - float(cor2[1]))**2 + (min_x - float(cor2[0]))**2)

def get_distance_lower_right(cor2, max_x, min_y):
    return math.sqrt((min_y - float(cor2[1]))**2 + (max_x - float(cor2[0]))**2)


def get_key(d, val_search):
    keys = [key for key, value in d.items() if value == val_search]
    if keys :
        return keys[0]
    else :
        return None

# 単にプリム法を使う
def tsp1(elements, size):
    current_position = [0,0]
    result = []

    values = list(elements.values())
    values.pop(0)

    for i in range(size):
        distance_list = []
        index_list = []
        for v in values:
            distance_list.append(get_distance(current_position, v))
            index_list.append(get_key(elements, v))
        min_index = 0
        for j in range(len(distance_list)):
            if distance_list[min_index] > distance_list[j]:
                min_index = j
        result.append(str(index_list[min_index] - 1) + "\n")
        current_position = values.pop(min_index)
    return result

# 重みをつけて最短経路を見つける
def tsp2(elements, size):
    if size < 128:
        tsp1(elements, size)

    cluster_size = int(size/4)

    result = []
    max_x = 0
    min_y = 0
    min_x = 0
    max_y = 0
    flag = 0

    values = list(elements.values())
    values.pop(0)

    current_position = [0,0]
    y_list = []
    x_list = []

    for k in range(4):
        if k == 0:
            for v in values:
                y_list.append(float(v[1]))
                x_list.append(float(v[0]))
            max_x = max(x_list)
            min_y = min(y_list)
            min_x = min(x_list)
            max_y = max(y_list)

        for i in range(cluster_size):
            distance_list = []
            index_list = []
            # 現在位置からの距離を全てのノードについて求める
            for v in values:
                distance_list.append(get_distance(current_position, v))
                index_list.append(get_key(elements, v))
            min_index = 0
            for j in range(len(distance_list)):
                if distance_list[min_index] > distance_list[j]:
                    min_index = j
            result.append(str(index_list[min_index] - 1) + "\n")
            current_position = values.pop(min_index)

        # 次に移動する位置の更新
        # 現在の位置によって重みを変える(盤面を4分割してなんとなく時計回りか反時計回りをするようにしたい)
        if k < 3:
            tmp_dist = []
            for v in values:
                if (float(current_position[1]) - min_y) < (max_y - min_y) / 2 or flag == 1:
                    if k == 0:
                        flag = 1
                        tmp_dist.append(get_distance_lower_left(v, min_x, min_y) + 2 * get_distance(current_position, v))
                    elif k == 1:
                        tmp_dist.append(get_distance_lower_right(v, max_x, min_y) + 2 * get_distance(current_position, v))
                    elif k == 2:
                        tmp_dist.append(get_distance_upper_right(v, max_x, max_y) + 2 * get_distance(current_position, v))
                else:
                    if k == 0:
                        tmp_dist.append(get_distance_upper_right(v, max_x, max_y) + 2 * get_distance(current_position, v))
                    elif k == 1:
                        tmp_dist.append(get_distance_lower_right(v, max_x, min_y) + 2 * get_distance(current_position, v))
                    elif k == 2:
                        tmp_dist.append(get_distance_lower_left(v, min_x, min_y) + 2 * get_distance(current_position, v))
            min_index = 0
            for j in range(len(tmp_dist)):
                if tmp_dist[min_index] > tmp_dist[j]:
                    min_index = j
                current_position = values[min_index]

    return result

for i in range(7):
    elements = {}
    counter = 0
    with open(input_filename[i], encoding='utf8', newline='') as f_in:
        csvreader = csv.reader(f_in)
        for row in csvreader:
            elements[counter] = row
            counter += 1

    result = tsp2(elements, counter - 1)
    result.insert(0, "index\n")

    f_out = open(output_filename[i], 'w')
    f_out.writelines(result)
    f_out.close

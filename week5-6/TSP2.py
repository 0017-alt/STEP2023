import csv
import math
import random
from copy import deepcopy
import bisect

random.seed(42)

input_filename = ["input_0.csv", "input_1.csv", "input_2.csv", "input_3.csv", "input_4.csv", "input_5.csv", "input_6.csv"]
output_filename = ["output_0.txt", "output_1.txt", "output_2.txt", "output_3.txt", "output_4.txt", "output_5.txt", "output_6.txt"]
vertexes = [5,8,16,64,128,512,2048]
ant_num = [10000, 10000, 10000, ]
points = []

class Parameters:
    # Set parameters
    # |mC_num_of_ants|     : the number of ants
    # |mC_num_of_vertexes| : the number of vertexes
    # |mC_Q|               : a parameter defined by users
    # |mC_alpha|           : a parameter that suggests how much we are about pheromone, which is defined by users
    # |mC_beta|            : a parameter that suggests how much we are heuristic, which is defined by users
    # |mC_rou|             : the evaporation rate
    # |mC_max_iterations|  : maxmum iteration
    # |mC_initial_vertex|  : initial_vertex
    # |mC_tau_min|         : minimum amount of serected pheromone
    # |mC_tau_max|         : maximum amount of serected pheromone
    # |mC_ant_prob_random| : a value of uniform distribution
    # |mC_super_not_change|: a value to determine if it is a local solution
    def __init__(self, num_of_ants, num_of_vertexed, Q, alpha, beta, rou, max_iterations, initial_vertex, tau_min, tau_max, ant_prob_random, super_not_change):
        self.mC_num_of_ants = num_of_ants
        self.mC_num_of_vertexes = num_of_vertexed
        self.mC_Q = Q
        self.mC_alpha = alpha
        self.mC_beta = beta
        self.mC_rou = rou
        self.mC_max_iterations = max_iterations
        self.mC_initial_vertex = initial_vertex
        self.mC_tau_min = tau_min
        self.mC_tau_max = tau_max
        self.mC_ant_prob_random = ant_prob_random
        self.mC_super_not_change = super_not_change

class Graph:
    # Create a graph.
    # |m_num_of_vertexes|    : the number of vertexes
    # |m_coordinate|         : accumulate coodinates
    # |m_edge_length|        : the length of each edge
    # |m_edge_pheromone|     : the amount of pheromone on eash edge
    # |m_edge_heuristic|     : preserve the heuristic values of the edges
    # |m_edge_next_pheromone|: preserve the amount of pheromone of the next edge
    # |m_parameters|         : parameters
    def __init__(self, parameters):
        self.m_num_of_vertexes = parameters.mC_num_of_vertexes
        self.m_coordinate = [None] * self.m_num_of_vertexes
        self.m_edge_length = [[0 for j in range(self.m_num_of_vertexes)] for i in range(self.m_num_of_vertexes)]
        self.m_edge_pheromone = [[0 for j in range(self.m_num_of_vertexes)] for i in range(self.m_num_of_vertexes)]
        self.m_edge_heuristics = [[0 for j in range(self.m_num_of_vertexes)] for i in range(self.m_num_of_vertexes)]
        self.m_edge_next_pheromone = [[0 for j in range(self.m_num_of_vertexes)] for i in range(self.m_num_of_vertexes)]
        self.m_parameters = parameters
        self.__prepare_graph()

    def __prepare_graph(self):
        for i in range(self.m_num_of_vertexes):
            self.m_coordinate[i] = points[i]
        for i in range(self.m_num_of_vertexes):
            for j in range(self.m_num_of_vertexes):
                self.m_edge_length[i][j] = Graph.__calc_edge_length(self.m_coordinate[i], self.m_coordinate[j])
        for i in range(self.m_num_of_vertexes):
            for j in range(self.m_num_of_vertexes):
                if i < j:
                    self.m_edge_next_pheromone[i][j] = self.m_parameters.mC_Q / self.m_edge_length[i][j]
                    self.m_edge_next_pheromone[j][i] = self.m_parameters.mC_Q / self.m_edge_length[i][j]
        for i in range(self.m_num_of_vertexes):
            for j in range(self.m_num_of_vertexes):
                if i < j:
                    h = self.m_parameters.mC_Q / self.m_edge_length[i][j]
                    self.m_edge_heuristics[i][j] = h
                    self.m_edge_heuristics[j][i] = h

    def reset_graph(self):
        self.m_edge_pheromone = [[0 for j in range(self.m_num_of_vertexes)] for i in range(self.m_num_of_vertexes)]

    def reset_graph_when_stagnation(self):
        for i in range(self.m_num_of_vertexes):
            for j in range(self.m_num_of_vertexes):
                if i < j:
                    h = self.m_parameters.mC_Q / self.m_edge_length[i][j]
                    self.m_edge_heuristics[i][j] = h
                    self.m_edge_heuristics[j][i] = h

    @staticmethod
    def __calc_edge_length(p1,p2):
        dx = (p1[0] - p2[0]) ** 2
        dy = (p1[1] - p2[1]) ** 2
        return math.sqrt(dx + dy)

class Ant:
    # Define the movement of ants
    # |m_graph|          : graph
    # |m_visited_vertex| : preserve vertexes that have already been visited
    # |m_num_of_vertexes|: the number of total vertexes
    # |m_parameters|     : parameters
    # |m_init_vertex|    : initial vertex
    def __init__(self, graph, parameters):
        self.m_graph = graph
        self.m_visited_vertex = [False for i in range(parameters.mC_num_of_vertexes)]
        self.m_visited_path = []
        self.m_num_of_vertexes = parameters.mC_num_of_vertexes
        self.m_parameters = parameters
        self.m_init_vertex = parameters.mC_initial_vertex

    def construct_path(self):
        self.m_visited_path.append(self.m_init_vertex)
        self.m_visited_vertex[self.m_init_vertex] = True
        for i in range(self.m_num_of_vertexes - 1):
            # Get current vertex
            v = self.m_visited_path[-1]

            # Get vertexes that can move from v and their probabilities
            to_vertexes, to_prob = self.__calc_prob_from_v(v)
            to = -1

            # If it is smaller than uniform distribution, select randomly
            if random.random() < self.m_parameters.mC_ant_prob_random:
                to = to_vertexes[random.randint(0, len(to_vertexes) - 1)]
            else:
                # Make a probability selection
                random_p = random.uniform(0.0, 0.999999999)
                to = to_vertexes[bisect.bisect_left(to_prob, random_p)]

            # Add "to" to path
            self.m_visited_path.append(to)
            self.m_visited_vertex[to] = True

        self.m_visited_path.append(self.m_init_vertex)

    def calc_next_pheromone(self):
        length = self.calc_all_path_length()
        Q = self.m_parameters.mC_Q
        for i in range(self.m_num_of_vertexes - 1):
            self.m_graph.m_edge_next_pheromone[self.m_visited_path[i]][self.m_visited_path[i + 1]] += Q / length

    def calc_all_path_length(self):
        length = 0
        for i in range(self.m_num_of_vertexes):
            length += self.m_graph.m_edge_length[self.m_visited_path[i]][self.m_visited_path[i+1]]
        return length

    def __calc_prob_from_v(self, v):
        # Total probability
        sumV = 0

        # detailed information about destination
        to_vertexes = []
        to_pheromones = []
        alpha = self.m_parameters.mC_alpha
        beta = self.m_parameters.mC_beta

        for to in range(self.m_num_of_vertexes):
            if (to == v) or self.m_visited_vertex[to]:
                continue

            # calculate numerator of pheromone
            pheromone = self.m_graph.m_edge_pheromone[v][to] ** alpha + self.m_graph.m_edge_heuristics[v][to] ** beta
            sumV += pheromone

            # add to candidate
            to_vertexes.append(to)
            to_pheromones.append(pheromone)

        to_prob = [x / sumV for x in to_pheromones]

        # Get cumulative sum of probabilities
        for i in range(len(to_prob)-1):
            to_prob[i + 1] += to_prob[i]

        return to_vertexes, to_prob

    def reset_ant(self):
        self.m_visited_vertex = [False for i in range(self.m_parameters.mC_num_of_vertexes)]
        self.m_visited_path = []

class Colony:
    # Caluculate colony
    # |m_num_of_ants|: the numer of ants
    # |m_parameters| : parameters
    # |m_graph|      : graph
    # |m_ants|       : the movement setting of ants
    def __init__(self, graph, parameters):
        self.m_num_of_ants = parameters.mC_num_of_ants
        self.m_parameters = parameters
        self.m_graph = graph
        self.m_ants = [Ant(self.m_graph, self.m_parameters) for i in range(self.m_num_of_ants)]

    def update_colony(self):
        self.__construct_ants()
        self.__calc_next_pheromones()

    def get_best_ant_path(self):
        length = 1e20
        path = []
        for ant in self.m_ants:
            if ant.calc_all_path_length() < length:
                length = ant.calc_all_path_length()
                path = deepcopy(ant.m_visited_path)
        return [length, path]

    def reset_colony(self):
        for ant in self.m_ants:
            ant.reset_ant()

    def __construct_ants(self):
        for ant in self.m_ants:
            ant.construct_path()

    def __calc_next_pheromones(self):
        for ant in self.m_ants:
            ant.calc_next_pheromone()

class ACOSolver:
    # the main solver
    # |mC_parameters|         : parameters
    # |m_graph|               : graph
    # |m_colony|              : colony
    # |m_best_ant|            : the ant that has a best score
    # |m_super_ant|           : the ant that has the answer
    # |m_cnt_super_not_change|: the value to judge stagnation
    def __init__(self, num_of_ants, num_of_vertexes, Q, alpha, beta, rou, max_iterations, initial_vertex, tau_min, tau_max, ant_prob_random, super_not_change):
        self.mC_parameters = Parameters(num_of_ants, num_of_vertexes, Q, alpha, beta, rou, max_iterations, initial_vertex, tau_min, tau_max, ant_prob_random, super_not_change)
        self.m_graph = Graph(self.mC_parameters)
        self.m_colony = Colony(self.m_graph, self.mC_parameters)
        self.m_best_ant = None
        self.m_super_ant = None
        self.m_cnt_super_not_change = 0

    def run_aco(self):
        for T in range(self.mC_parameters.mC_max_iterations):
            self.__update_aco()
            self.__reset_aco()
            if self.m_super_ant is None:
                self.m_super_ant = self.m_best_ant
            if self.m_super_ant[0] > self.m_best_ant[0]:
                self.m_super_ant = self.m_best_ant
            else:
                self.m_cnt_super_not_change += 1

            if self.m_cnt_super_not_change > self.mC_parameters.mC_super_not_change:
                self.reset_pheromones()
                self.m_cnt_super_not_change = 0

        print(self.m_super_ant[0])
        return self.m_super_ant[1]

    def reset_pheromones(self):
        self.m_graph.reset_graph_when_stagnation()

    def __update_aco(self):
        self.m_colony.update_colony()
        self.__update_next_pheromones()
        self.m_best_ant = self.m_colony.get_best_ant_path()

    def __reset_aco(self):
        self.m_colony.reset_colony()
        self.m_graph.reset_graph()

    def __update_next_pheromones(self):
        num_of_vertexes = self.mC_parameters.mC_num_of_vertexes
        rou = self.mC_parameters.mC_rou
        tau_min = self.mC_parameters.mC_tau_min
        tau_max = self.mC_parameters.mC_tau_max
        for i in range(num_of_vertexes):
            for j in range(num_of_vertexes):
                self.m_graph.m_edge_pheromone[i][j] = self.m_graph.m_edge_pheromone[i][j] * rou + self.m_graph.m_edge_next_pheromone[i][j]

        for i in range(num_of_vertexes):
            for j in range(num_of_vertexes):
                self.m_graph.m_edge_pheromone[i][j] = min(tau_max, max(self.m_graph.m_edge_pheromone[i][j], tau_min))

# Calculate ditances
def get_distance_upper_right(cor2, max_x, max_y):
    return math.sqrt((max_x - float(cor2[0]))**2 + (max_y - float(cor2[1]))**2)

def get_distance(cor1, cor2):
    return math.sqrt((float(cor1[0]) - float(cor2[0]))**2 + (float(cor1[1]) - float(cor2[1]))**2)

def get_distance_lower_left(cor2, min_x, min_y):
    return math.sqrt((min_y - float(cor2[1]))**2 + (min_x - float(cor2[0]))**2)

def get_distance_lower_right(cor2, max_x, min_y):
    return math.sqrt((min_y - float(cor2[1]))**2 + (max_x - float(cor2[0]))**2)

# Get key from value
def get_key(d, val_search):
    keys = [key for key, value in d.items() if value == val_search]
    if keys :
        return keys[0]
    else :
        return None

def tsp(elements, size):
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

for i in range(3):
    with open(input_filename[i], 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header
        for row in reader:
            points.append(list(map(float, row)))

    result_int = []
    result = []

    aco_solver = ACOSolver(num_of_ants=100, num_of_vertexes=vertexes[i], Q=100, alpha=3, beta=2, rou=0.8, max_iterations=500,
                    initial_vertex=0, tau_min=0, tau_max=100, ant_prob_random=0.1, super_not_change=30)
    result_int = aco_solver.run_aco()

    result.append("index\n")
    for index in result_int:
        result.append(str(index) + "\n")

    f_out = open(output_filename[i], 'w')
    f_out.writelines(result)
    f_out.close
    points = []

for i in range(3,7):
    elements = {}
    counter = 0
    with open(input_filename[i], encoding='utf8', newline='') as f_in:
        csvreader = csv.reader(f_in)
        for row in csvreader:
            elements[counter] = row
            counter += 1

    result = tsp(elements, counter - 1)
    result.insert(0, "index\n")

    f_out = open(output_filename[i], 'w')
    f_out.writelines(result)
    f_out.close
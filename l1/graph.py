import csv
import geopy.distance
from collections import defaultdict


def str_to_seconds(time_string):
    hours, minutes, seconds = time_string.split(':')
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def seconds_to_str(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


class Edge:
    def __init__(self, line, arrive_time, depart_time, start_lat, start_lon, end_lat, end_lon):
        self.line = line
        self.arrive_time = arrive_time
        self.depart_time = depart_time
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.end_lat = end_lat
        self.end_lon = end_lon

    def __eq__(self, other):
        if isinstance(other, Edge):
            return (
                    self.line == other.line and
                    self.arrive_time == other.arrive_time and
                    self.depart_time == other.depart_time and
                    self.start_lat == other.start_lat and
                    self.start_lon == other.start_lon and
                    self.end_lat == other.end_lat and
                    self.end_lon == other.end_lon
            )
        return False

    def __repr__(self):
        return f"(Line: {self.line}, Depart time: {self.depart_time}, Arrive time: {self.arrive_time})"


class Graph:
    def __init__(self, file_path, transfer_cost_multiplier=5):
        self.nodes = defaultdict(set)  # key - start stop, value - list of possible end stops
        self.edges = defaultdict(
            list)  # key - pair of start and end stops, value - list of Edges (possible ways to travel from start stop to end stop)
        self.load_data(file_path)
        self.transfer_cost_multiplier = transfer_cost_multiplier

    def load_data(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                start_stop = row['start_stop'].lower()
                end_stop = row['end_stop'].lower()
                depart_time = str_to_seconds(row['departure_time'])
                arrive_time = str_to_seconds(row['arrival_time'])
                line = row['line']
                start_lat = float(row['start_stop_lat'])
                start_lon = float(row['start_stop_lon'])
                end_lat = float(row['end_stop_lat'])
                end_lon = float(row['end_stop_lon'])

                self.nodes[start_stop].add(end_stop)
                self.edges[(start_stop, end_stop)].append(
                    Edge(line, arrive_time, depart_time, start_lat, start_lon, end_lat, end_lon))

            for row in self.edges.values():
                row.sort(key=lambda x: x.depart_time)

    def min_cost_route(self, time, start_stop, end_stop, transfer_time, cur_line, time_criteria=True, tabu_table=None):
        possible_ways = self.edges[(start_stop, end_stop)]

        best_time = float('inf')
        best_way = None

        for possible_way in possible_ways:
            depart_time = possible_way.depart_time
            arrive_time = possible_way.arrive_time

            # Do not allow selected edge if is in tabu table
            if tabu_table is not None:
                if tabu_table.get((start_stop, end_stop), None):
                    way = tabu_table[(start_stop, end_stop)][0]
                    tenure = tabu_table[(start_stop, end_stop)][1]
                    if way == possible_way and tenure > 0:
                        tabu_table[(start_stop, end_stop)] = (way, tenure-1)  # decrease tabu tenure after each attempt of breaking it
                        continue

            # Account for transfer
            if cur_line is None or possible_way.line == cur_line:
                if time <= depart_time and arrive_time - time < best_time:
                    best_way = possible_way
                    best_time = arrive_time - time
            else:
                if time + transfer_time <= depart_time and arrive_time - time < best_time:
                    best_way = possible_way
                    best_time = arrive_time - time + transfer_time * (
                        1 if time_criteria else self.transfer_cost_multiplier)  # apply high cost for transfer

        return best_time, best_way

    def heuristic(self, start_stop, end_stop):
        # Get coordinates of both stops, usually not adjacent
        some_stop = list(self.nodes[start_stop])[0]
        edge = self.edges[(start_stop, some_stop)][0]
        start_lat, start_lon = edge.start_lat, edge.start_lon

        some_stop = list(self.nodes[end_stop])[0]
        edge = self.edges[(some_stop, end_stop)][0]
        end_lat, end_lon = edge.end_lat, edge.end_lon

        # average speed of communication is 15 km/h, so transform heuristic into estimate of seconds to end stop
        return geopy.distance.distance((start_lat, start_lon), (end_lat, end_lon)).km * 15 / 60


if __name__ == '__main__':
    graph = Graph("connection_graph.csv")
    start_time = str_to_seconds("20:05:17")
    start_stop = "PL. JANA PAWŁA II".lower()
    end_stop = "Rynek".lower()

    print(graph.min_cost_route(start_time, start_stop, end_stop))

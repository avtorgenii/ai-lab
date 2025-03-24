import heapq
from collections import defaultdict
from decorators import *
from graph import *

"""
        route_info = [{
        line: ,
        departure_time:
        start_stop:
        arrival_time:
        end_stop
        }, {...}, {...}
        ]
        cost_func_value = ...
"""


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


@found_route_details
def dijkstra(graph, start_stop, end_stop, start_time, transfer_time):
    print("DIJKSTRA TIME CRITERIA")

    unvisited = PriorityQueue()
    unvisited.put(start_stop, 0)

    time_to_stop = defaultdict(lambda: float('inf')) # default time to each stop is inf
    time_to_stop[start_stop] = 0
    best_way_to_stop = {} # key - end stop, value - (start stop, Edge)
    cur_time_on_stop = {start_stop: start_time}

    while not unvisited.empty():
        cur_stop = unvisited.get()
        if cur_stop == end_stop:
            break
        try:
            graph.nodes[cur_stop]
        except KeyError:
            logging.error(f"Unknown stop: {cur_stop}")
            continue

        for neighbor in graph.nodes[cur_stop]:
            best_time, best_way = graph.min_time_route(cur_time_on_stop[cur_stop], cur_stop, neighbor)
            new_time_to_stop = time_to_stop[cur_stop] + best_time

            if time_to_stop[neighbor] > new_time_to_stop:
                time_to_stop[neighbor] = new_time_to_stop
                unvisited.put(neighbor, new_time_to_stop)
                best_way_to_stop[neighbor] = (cur_stop, best_way)
                cur_time_on_stop[neighbor] = cur_time_on_stop[cur_stop] + best_time

    # Reconstruct path
    path = []
    cur_stop = end_stop

    while cur_stop != start_stop:
        prev_stop, best_way = best_way_to_stop[cur_stop]
        path.append((prev_stop, cur_stop, best_way))
        cur_stop = prev_stop

    path = path[::-1]


    route_info = []
    for part in path:
        start_stop, end_stop, way = part
        route_info.append({
            "Line": way.line,
            "Departure time": way.depart_time,
            "Arrival time": way.arrive_time,
            "Start stop": start_stop,
            "End stop": end_stop,
        })


    return route_info, time_to_stop[end_stop]





if __name__ == '__main__':
    start_stop = "PL. JANA PAWŁA II".lower()
    end_stop = "GALERIA DOMINIKAŃSKA".lower()
    start_time = str_to_seconds("10:03:00")
    print(f"Start time: {start_time}")
    transfer_time = str_to_seconds("00:00:02")

    graph = Graph("connection_graph.csv")
    dijkstra(graph, start_stop, end_stop, start_time, transfer_time)

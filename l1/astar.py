from utilities import *
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


@found_route_details
def astar(graph, start_stop, end_stop, start_time, transfer_time, time_criteria=True):
    print("A* TIME CRITERIA")

    unvisited = PriorityQueue()
    unvisited.put(start_stop, 0)

    cost_to_stop = defaultdict(lambda: float('inf'))  # default cost to each stop is inf
    cost_to_stop[start_stop] = 0
    best_way_to_stop = {}  # key - end stop, value - (start stop, Edge)
    cur_time_on_stop = {start_stop: start_time}  # current best time arriving at this stop

    while not unvisited.empty():
        cur_stop = unvisited.get()
        if cur_stop == end_stop:  # non-canonical dijkstra, theoretically may result in non-optimal result, but for maps is sufficient
            break
        try:
            graph.nodes[cur_stop]
        except KeyError:
            logging.error(f"Unknown stop: {cur_stop}")
            continue

        for neighbor in graph.nodes[cur_stop]:
            try:
                cur_line = best_way_to_stop[cur_stop][1].line
            except KeyError:
                cur_line = None

            best_time, best_way = graph.min_cost_route(cur_time_on_stop[cur_stop], cur_stop, neighbor,
                                                       transfer_time,
                                                       cur_line, time_criteria)

            new_cost_to_stop = cost_to_stop[cur_stop] + best_time + graph.heuristic(neighbor, end_stop)

            if cost_to_stop[neighbor] > new_cost_to_stop:
                cost_to_stop[neighbor] = new_cost_to_stop
                unvisited.put(neighbor, new_cost_to_stop)
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
            "Departure time": seconds_to_str(way.depart_time),
            "Arrival time": seconds_to_str(way.arrive_time),
            "Start stop": start_stop,
            "End stop": end_stop,
        })

    return route_info, cost_to_stop[end_stop]


if __name__ == '__main__':
    start_stop = "PILCZYCE".lower()
    end_stop = "KLECINA".lower()
    start_time = str_to_seconds("10:03:00")
    print(f"Start time: {start_time}")
    transfer_time = str_to_seconds("00:02:00")

    graph = Graph("connection_graph.csv")
    astar(graph, start_stop, end_stop, start_time, transfer_time, time_criteria=False)

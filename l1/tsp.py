import logging
from collections import defaultdict
from l1.graph import str_to_seconds, Graph, seconds_to_str
from l1.utilities import PriorityQueue, found_route_details, FIFODict


def dijkstra(graph, start_stop, end_stop, start_time, transfer_time, tabu_table, time_criteria=True):
    unvisited = PriorityQueue()
    unvisited.put(start_stop, 0)

    time_to_stop = defaultdict(lambda: float('inf'))  # default time to each stop is inf
    time_to_stop[start_stop] = 0
    best_way_to_stop = {}  # key - end stop, value - (start stop, Edge)
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
            try:
                cur_line = best_way_to_stop[cur_stop][1].line
            except KeyError:
                cur_line = None

            best_time, best_way = graph.min_cost_route(cur_time_on_stop[cur_stop], cur_stop, neighbor, transfer_time,
                                                       cur_line, time_criteria, tabu_table)

            if best_time and best_way:
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

    return path[::-1], time_to_stop[end_stop]


def extract_stop_from_path(path):
    # [('pl. strzegomski (muzeum współczesne)', 'wrocław mikołajów (zachodnia)', (Line: 10, Depart time: 44700, Arrive time: 44820))]
    visited_stops = set()

    for part in path:
        visited_stops.add(part[0])
        visited_stops.add(part[1])

    return visited_stops


def find_round_trip_path(graph, start_stop, intermediate_stops, start_time, transfer_time, tabu_table=None,
                         time_criteria=True):
    # Doesn't consider transfer_time between dijkstra's
    visited_stops = set()  # maybe we have visited target stop by accident while searching for path between two other stops, then we don't need to find way to it again
    # Forward
    cur_stop = start_stop
    new_start_time = start_time
    best_path = []
    for stop in intermediate_stops:
        if stop in visited_stops:
            continue

        next_stop = stop
        path, _ = dijkstra(graph, cur_stop, next_stop, new_start_time, transfer_time, tabu_table, time_criteria)
        best_path.extend(path)
        cur_stop = next_stop
        new_start_time = best_path[-1][2].arrive_time

        visited_stops.union(extract_stop_from_path(path))

    # Backward to the start stop
    stops = [*intermediate_stops[:-2], start_stop]
    for stop in stops:
        if stop in visited_stops:
            continue

        next_stop = stop
        path, _ = dijkstra(graph, cur_stop, next_stop, new_start_time, transfer_time, tabu_table, time_criteria)
        best_path.extend(path)
        cur_stop = next_stop
        new_start_time = best_path[-1][2].arrive_time

        visited_stops.union(extract_stop_from_path(path))

    best_cost = best_path[-1][2].arrive_time - start_time

    return best_path, best_cost


@found_route_details
def knox(graph, start_stop, intermediate_stops, start_time, transfer_time, time_criteria=True, total_steps_limit=10, tabu_tenure_init=5, tabu_table_size_multiplier=20):
    # Tabu table will be represented by FIFO dictionary: k - (start_stop, end_stop), v - (line, tabu_tenure)
    tabu_table = FIFODict(len(intermediate_stops) * tabu_table_size_multiplier)

    # Pull out solution using dijkstra
    best_path, best_cost = find_round_trip_path(graph, start_stop, intermediate_stops, start_time, transfer_time, None,
                                                time_criteria)
    print(f"Best initial path: {best_path}")
    print(f"Best initial cost: {best_cost}")

    # Fil out tabu table
    for part in best_path:
        tabu_table[(part[0], part[1])] = (part[2], tabu_tenure_init)

    # Search cycle
    total_steps_left = total_steps_limit
    while total_steps_left > 0:
        print(f"Total steps left: {total_steps_left}")
        total_steps_left -= 1
        new_path, new_cost = find_round_trip_path(graph, start_stop, intermediate_stops, start_time, transfer_time,
                                                  tabu_table, time_criteria)

        print(new_cost)

        # Fill out tabu table
        for part in new_path:
            tabu_table[(part[0], part[1])] = (part[2], tabu_tenure_init)

        if new_cost < best_cost:
            best_path = new_path
            best_cost = new_cost

    route_info = []
    for part in best_path:
        start_stop, end_stop, way = part
        route_info.append({
            "Line": way.line,
            "Departure time": seconds_to_str(way.depart_time),
            "Arrival time": seconds_to_str(way.arrive_time),
            "Start stop": start_stop,
            "End stop": end_stop,
        })

    return route_info, best_cost


if __name__ == '__main__':
    start_stop = "PILCZYCE".lower()
    intermediate_stops = [stop.lower() for stop in ["GALERIA DOMINIKAŃSKA", "Hala Targowa", "Klecina"]]
    start_time = str_to_seconds("10:03:00")
    print(f"Start time: {start_time}")
    transfer_time = str_to_seconds("00:02:00")

    graph = Graph("connection_graph.csv", 5)
    knox(graph, start_stop, intermediate_stops, start_time, transfer_time, time_criteria=True)

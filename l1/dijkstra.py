from collections import defaultdict
from decorators import *
from graph import data_to_graph
from main import load_data, str_to_seconds

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


# @found_route_details
def dijkstra_time(adj_list, start_stop, end_stop, start_time, transfer_time):
    print("DIJKSTRA TIME CRITERIA")
    # A -> [(B, "105", departure_time, arrival_time), (B, "105", departure_time, 1), (C, "105", departure_time 5)]

    unvisited = list(adj_list.keys())  # List of all nodes
    times = {stop: float('inf') for stop in unvisited}  # Initialize distances
    times[start_stop] = 0  # Time to the start node is 0
    # Where from, when arrived, by which line
    previous_stops = {stop: (None, None, None) for stop in unvisited}

    # Until all stops are explored
    while unvisited:
        # Select the unvisited stop with the smallest time to it
        current_stop = min(unvisited, key=lambda stop: times[stop])
        unvisited.remove(current_stop)

        for next_stop, line, departure_time, arrival_time in adj_list[current_stop]:
            time_to_stop = times[current_stop] + arrival_time - departure_time
            if time_to_stop < times.get(next_stop, float('inf')) and :  # Found a shorter path
                times[next_stop] = time_to_stop
                previous_stops[next_stop] = (current_stop, arrival_time, line)

    # Reconstruct path
    path = []
    current_stop = previous_stops.fil
    line = None
    while current_stop != start_stop:
        print(current_stop)
        next_stop, arrival_time, line = previous_stops[current_stop]
        path.append((current_stop, line))
        current_stop = next_stop
    # Add start stop itself
    path.append((current_stop, line))


    path = path[::-1]
    # print(previous_stops)
    print(path)

    return times[end_stop], path


if __name__ == '__main__':
    start_stop = "PL. JANA PAWŁA II"
    end_stop = "Rynek"
    criteria = "t"
    start_time = str_to_seconds("23:03:00")
    transfer_time = str_to_seconds("00:00:02")

    data = load_data()
    adj_list = data_to_graph(data, start_time)
    dijkstra_time(adj_list, start_stop, end_stop, start_time, transfer_time)  # should print 2 minutes or 120 seconds

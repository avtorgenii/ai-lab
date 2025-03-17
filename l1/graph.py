from collections import defaultdict
from main import load_data, str_to_seconds


def data_to_graph(data, start_time):
    adj_list = defaultdict(set)  # set to avoid duplicates
    for part_dict in data:
        departure_time = part_dict['departure_time']

        # we are not taking into account routes that departed before we showed up on start stop
        if departure_time < start_time:
            continue

        line = part_dict['line']
        arrival_time = part_dict['arrival_time']
        start_stop = part_dict['start_stop']
        end_stop = part_dict['end_stop']

        # A -> [(B, "105", departure_time, arrival_time), (B, "105", departure_time, 1), (C, "105", departure_time 5)]
        adj_list[start_stop].add((end_stop, line, departure_time, arrival_time))

    return adj_list


if __name__ == '__main__':
    data = load_data()
    start_time = str_to_seconds("20:05:17")
    graph = data_to_graph(data, start_time)

    print(graph)

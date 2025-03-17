import csv
import logging
# from dijkstra import *

logging.basicConfig(level=logging.INFO)


def str_to_seconds(time_string):
    hours, minutes, seconds = time_string.split(':')
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def seconds_to_str(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def load_data():
    # Load file into list of dicts
    with open('connection_graph.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [{'line': row['line'],
                 'departure_time': str_to_seconds(row['departure_time']),
                 'arrival_time': str_to_seconds(row['arrival_time']),
                 'start_stop': row['start_stop'],
                 'end_stop': row['end_stop'],
                 'start_stop_lat': float(row['start_stop_lat']),
                 'start_stop_lon': float(row['start_stop_lat']),
                 'end_stop_lat': float(row['start_stop_lat']),
                 'end_stop_lon': float(row['start_stop_lat'])
                 } for row in reader]
        return data


if __name__ == '__main__':
    data = load_data()

    print(data)

    start_stop = "PL. JANA PAWŁA II"
    end_stop = "PL. GRUNWALDZKI"
    criteria = "t"
    start_time = str_to_seconds("10:45:00")

    # 1a
    # graph = data_to_graph(data)
    # if criteria == "t":
    #     dijkstra_time(graph, start_stop, end_stop, start_time)


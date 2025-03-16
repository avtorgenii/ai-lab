import csv
import logging
import time

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
        data = [{**row,
                 'departure_time': str_to_seconds(row['departure_time']),
                 'arrival_time': str_to_seconds(row['arrival_time']),
                 'start_stop_lat': float(row['start_stop_lat']),
                 'start_stop_lon': float(row['start_stop_lat']),
                 'end_stop_lat': float(row['start_stop_lat']),
                 'end_stop_lon': float(row['start_stop_lat'])
                 } for row in reader]
        return data


"""
        route_info = [{
        line: ,
        departure_time:
        start_stop:
        arrival_time:
        end_stop
        }, {...}, {...}
        ]
"""


def found_route_details(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()

        route_info, cost_func_value = func(*args, **kwargs)

        end_time = time.time()

        logging.info("ROUTE INFO")
        for route in route_info:
            part_of_the_way = ''
            for k, v in route.items():
                part_of_the_way += f"{k}: {v}"
            logging.info(part_of_the_way)

        logging.error("COST FUNC VALUE: " + cost_func_value)
        logging.error("CALCULATION TIME: " + str(end_time - start_time))

    return wrapper


@found_route_details
def dijkstra_time(graph, start_stop, end_stop, start_time):
    pass


if __name__ == '__main__':
    graph = load_data()

    print(graph)

    start_stop = "PL. JANA PAWŁA II"
    end_stop = "PL. GRUNWALDZKI"
    criteria = "t"
    start_time = str_to_seconds("10:45:00")

    # 1a
    # dijkstra_time(graph, start_stop, end_stop, start_time)

import logging
# from dijkstra import *

logging.basicConfig(level=logging.INFO)

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


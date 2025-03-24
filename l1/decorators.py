import logging
import time

logging.basicConfig(level=logging.DEBUG)
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
                part_of_the_way += f"{k}: {v} "
            logging.info(part_of_the_way)

        logging.error(f"COST FUNC VALUE: {cost_func_value}")
        calc_time = end_time - start_time
        logging.error(f"CALCULATION TIME: {calc_time:.2f} seconds")

    return wrapper
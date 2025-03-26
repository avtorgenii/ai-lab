import logging
import time
from collections import defaultdict

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

        # Group routes by line and squash them
        squashed_routes = []
        grouped_routes = defaultdict(list)

        # Group routes by line
        for route in route_info:
            grouped_routes[route['Line']].append(route)

        # Squash the routes for the same line
        for line, routes in grouped_routes.items():
            merged_route = {
                'Line': line,
                'Departure time': routes[0]['Departure time'],
                'Start stop': routes[0]['Start stop'],
                'Arrival time': routes[-1]['Arrival time'],
                'End stop': routes[-1]['End stop']
            }
            squashed_routes.append(merged_route)

        # Logging the squashed routes
        logging.info("ROUTE INFO:")
        for route in squashed_routes:
            route_details = ", ".join(f"{k}: {v}" for k, v in route.items())
            logging.info(route_details)

        logging.error(f"COST FUNC VALUE: {cost_func_value}")
        calc_time = end_time - start_time
        logging.error(f"CALCULATION TIME: {calc_time:.2f} seconds")

    return wrapper
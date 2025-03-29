import heapq
import logging
import time
from collections import OrderedDict

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

        # Squash routes that are consecutive
        squashed_routes = []

        if not route_info:
            return route_info, cost_func_value

        # Start with the first route
        current_group = [route_info[0]]

        for route in route_info[1:]:
            # Get the last route in the current group
            prev_route = current_group[-1]

            # Check if routes are consecutive
            # Conditions for consecutive routes:
            # 1. Same line
            # 2. End stop of previous route is start stop of current route
            # 3. Departure time of current route is after or equal to arrival time of previous route
            if (route['Line'] == prev_route['Line'] and
                    route['Start stop'] == prev_route['End stop'] and
                    route['Departure time'] >= prev_route['Arrival time']):
                # Add to current group
                current_group.append(route)
            else:
                # Different route - finalize current group and start a new one
                # Create a merged route from the group
                merged_route = {
                    'Line': current_group[0]['Line'],
                    'Departure time': current_group[0]['Departure time'],
                    'Start stop': current_group[0]['Start stop'],
                    'Arrival time': current_group[-1]['Arrival time'],
                    'End stop': current_group[-1]['End stop']
                }
                squashed_routes.append(merged_route)

                # Start a new group with the current route
                current_group = [route]

        # Add the last group
        if current_group:
            merged_route = {
                'Line': current_group[0]['Line'],
                'Departure time': current_group[0]['Departure time'],
                'Start stop': current_group[0]['Start stop'],
                'Arrival time': current_group[-1]['Arrival time'],
                'End stop': current_group[-1]['End stop']
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

        return route_info, cost_func_value

    return wrapper


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class FIFODict(OrderedDict):
    def __init__(self, max_size):
        super().__init__()
        self.max_size = max_size

    def __setitem__(self, key, value):
        if len(self) >= self.max_size:
            self.popitem(last=False)  # Removes the oldest item (FIFO behavior)
        super().__setitem__(key, value)

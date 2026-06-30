import heapq

# Size of one map tile
TILE_SIZE = 48


# Manhattan Distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node):

    x, y = node

    return [

        (x + 1, y),

        (x - 1, y),

        (x, y + 1),

        (x, y - 1)

    ]


def find_path(start, goal, blocked):    

    frontier = []

    heapq.heappush(frontier, (0, start))

    came_from = {}

    cost_so_far = {}

    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:

        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        # Check every tile that can be reached
        for next_node in get_neighbors(current):

            # Ignore tiles outside the map
            if next_node[0] < 0 or next_node[1] < 0:
                continue

            # Adjust these numbers to match your map size
            if next_node[0] >= 80 or next_node[1] >= 60:
                continue
            
            # Ignore wall tiles
            if next_node in blocked:
                continue

            new_cost = cost_so_far[current] + 1

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:

                cost_so_far[next_node] = new_cost

                priority = new_cost + heuristic(goal, next_node)

                heapq.heappush(frontier, (priority, next_node))

                came_from[next_node] = current

    if goal not in came_from:
        return []

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = came_from[current]

    path.reverse()

    return path
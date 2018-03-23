from queue import PriorityQueue


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    # frontier saves all nodes
    frontier.put((0, start))
    # came_from saves all nodes
    came_from = {}
    # cost_so_far saves all nodes
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        # gets executed for every node
        current = frontier.get()[1]

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            next = tuple(next)
            # gets executed for every neighbor
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                # add in frontier with priority, low heuristic is better
                priority = new_cost + heuristic(goal, next)
                frontier.put((priority, next))
                came_from[next] = current

    return came_from, cost_so_far

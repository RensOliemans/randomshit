class Graph:

    def __init__(self, board):
        self.board = board
        self.all_nodes = self.get_nodes(board)

    def neighbors(self, node):
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = []
        for direction in dirs:
            neighbor = [node[0] + direction[0], node[1] + direction[1]]
            if neighbor in self.all_nodes:
                result.append(neighbor)
        return result

    @staticmethod
    def get_nodes(board):
        all_nodes = []
        for x, xs in enumerate(board):
            for y, tile in enumerate(xs):
                if tile == -1:
                    continue
                all_nodes.append([x, y])
        return all_nodes

    def __str__(self):
        return "{}".format(self.all_nodes)

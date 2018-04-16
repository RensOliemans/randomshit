from time import time
from PIL import Image
from graph import Graph
from astar import a_star_search, reconstruct_path


begin = time()
im = Image.open('index.png')
pix = im.load()

board = []
for x in range(im.size[0]):
    board.append([])
    for y in range(im.size[1]):
        correct = [(255, 255, 255, 255), (237, 28, 36, 255)]  # white and red
        val = 1 if pix[x, y] in correct else -1
        board[x].append(val)

graph = Graph(board)
# print(graph)
start = (14, 71)
goal = (76, 71)

print("Time taken to convert image into graph: {:.2}s".format(time() - begin))
begin = time()

came_from, cost_so_far = a_star_search(graph, start, goal)
path = reconstruct_path(came_from, start, goal)

print(path)
print("Time taken to construct path: {:.2}s".format(time() - begin))

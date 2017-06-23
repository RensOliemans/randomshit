points = [6, 6, 8, 23, 26, 12, 11, 12, 14, 21, 2, 8, 27, 15, 10, 21, 8, 19, 16, 6, 4, 20, 12, 5, 0, 22, 13, 7, 7, 9, 18, 3, 0, 12, 9, 14, 11, 15, 12, 13, 18, 9, 1, 26, 25, 20, 16, 33, 21, 2, 9, 7, 2, 14, 4, 5, 15, 9, 12, 29, 7, 22, 7, 23, 6, 2, 11, 19, 3]


def calculate(points):
    print("Without bonus: {}".format(sum(points) / len(points)))
    total = sum(points) - (10 * points.count(0))
    print("With bonus: {}".format(total / len(points)))



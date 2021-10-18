import math


class GeometryFuncs:
    @staticmethod
    def point_in_rect(point, puzzle):
        return (puzzle.x < point[0] < puzzle.x + puzzle.width) and (puzzle.y < point[1] < puzzle.y + puzzle.height)

    @staticmethod
    def mean_point(hand):
        p1 = hand[0]["lmList"][8]
        p2 = hand[0]["lmList"][12]
        return [(p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2]

    @staticmethod
    def get_dist_between_fingers(hand):
        if hand:
            p1 = hand[0]["lmList"][8]
            p2 = hand[0]["lmList"][12]
            return math.dist(p1, p2)
        else:
            return float("inf")

    @staticmethod
    def intersect_area(puzzle, puzzle_space):
        # puzzle_space - (x_cord, y_cord) - top-left corner
        dx = min(puzzle.x + puzzle.width, puzzle_space[0] + puzzle.width) - max(puzzle.x, puzzle_space[0])
        dy = min(puzzle.y + puzzle.height, puzzle_space[1] + puzzle.height) - max(puzzle.y, puzzle_space[1])
        if (dx >= 0) and (dy >= 0):
            return ((dx * dy) / (puzzle.width * puzzle.height))
        else:
            return 0.0

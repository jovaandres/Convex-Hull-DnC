from math import sqrt, pow, acos

from Area import Area


class ConvexHull:
    def __init__(self, _dataset) -> None:
        self.dataset = _dataset
        self.simplices = []
        self._buildConvexHull()

    def _leftMost(self):
        minIndex = 0
        points = self.dataset
        x = 0

        for i in range(1, len(points)):
            if points[i][x] < points[minIndex][x]:
                minIndex = i

        return minIndex

    def _rightMost(self):
        maxIndex = 0
        points = self.dataset
        x = 0

        for i in range(1, len(points)):
            if points[i][x] > points[maxIndex][x]:
                maxIndex = i

        return maxIndex

    def _distance(self, p1, p2, p3):
        points = self.dataset
        x, y = 0, 1

        dividend = ((points[p2][x] - points[p1][x]) * (points[p1][y] - points[p3][y])) - (
            (points[p1][x] - points[p3][x]) * (points[p2][y] - points[p1][y]))
        divisor = sqrt(pow(points[p2][x] - points[p1][x],
                       2) + pow(points[p2][y] - points[p1][y], 2))

        return abs(dividend) / divisor

    def _angle(self, p1, p2, p3):
        points = self.dataset
        x, y = 0, 1

        p12 = (points[p1][x] - points[p2][x], points[p1][y] - points[p2][y])
        p13 = (points[p1][x] - points[p3][x], points[p1][y] - points[p3][y])

        return acos((p12[x] * p13[x] + p12[y] * p13[y]) / (sqrt(pow(p12[x], 2) + pow(p12[y], 2)) * sqrt(pow(p13[x], 2) + pow(p13[y], 2))))

    def _defineArea(self, p1, p2, p3):
        points = self.dataset
        x, y = 0, 1

        area = points[p1][x] * points[p2][y] + points[p3][x] * points[p1][y] + points[p2][x] * points[p3][y] - \
            points[p3][x] * points[p2][y] - points[p2][x] * \
            points[p1][y] - points[p1][x] * points[p3][y]

        if area > 1e-10:
            return Area.ABOVE
        elif area < -1e-10:
            return Area.BELOW

    def _separate(self, pi, pn, points):
        aboveAreaDots = []
        belowAreaDots = []

        for i in range(0, len(points)):
            area = self._defineArea(pi, pn, points[i])
            if area == Area.BELOW:
                belowAreaDots.append(points[i])
            elif area == Area.ABOVE:
                aboveAreaDots.append(points[i])

        return aboveAreaDots, belowAreaDots

    def _dnc(self, pi, pn, parts, direction: Area):
        if len(parts) == 0:
            self.simplices.append([pi, pn])
        elif len(parts) == 1:
            self.simplices.append([pi, parts[0]])
            self.simplices.append([parts[0], pn])
        else:
            pmax = parts[0]
            maxDistance = self._distance(pi, pn, parts[0])

            for i in range(1, len(parts)):
                currentDistance = self._distance(pi, pn, parts[i])
                if currentDistance > maxDistance:
                    maxDistance = currentDistance
                    pmax = parts[i]
                elif currentDistance == maxDistance:
                    if self._angle(pi, pn, parts[i]) > self._angle(pi, pn, pmax):
                        pmax = parts[i]

            dataparts1 = self._separate(pi, pmax, parts)
            dataparts2 = self._separate(pmax, pn, parts)

            self._dnc(pi, pmax,
                      dataparts1[direction.value], direction)
            self._dnc(pmax, pn,
                      dataparts2[direction.value], direction)

    def _buildConvexHull(self):
        pi = self._leftMost()
        pn = self._rightMost()

        dataparts = self._separate(
            pi, pn, [i for i in range(0, len(self.dataset))])

        self._dnc(pi, pn, dataparts[0], Area.ABOVE)
        self._dnc(pi, pn, dataparts[1], Area.BELOW)

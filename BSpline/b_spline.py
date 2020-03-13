import numpy as np

class BSpline():

    def __init__(self, interval = 0.01, degree = 3, p_mode = 1):
        self.interpolation_points = None
        self.degree = degree
        self.interval = interval
        self.knot = None
        self.p_mode = p_mode
        self.parameterization_vector = None

    def parameterization(self,points):
        tmp = []
        if self.p_mode:
            up = np.zeros(points.shape[0])
            dis = points[1:] - points[:-1]
            dis = np.linalg.norm(dis,axis = 1)
            up[1:] = dis
            down = np.sum(up)
        else:
            up = np.ones(points.shape[0])
            # up[-1] = points.shape[0]
            up[0] = 0
            down = points.shape[0]-1

        up_n = 0
        for i , point in enumerate(points):
            if i:
                up_n +=  up[i]
                tmp.append(up_n/ down)
            else:
                tmp.append(0)
        return np.array(tmp)


    def fit(self, input):
        assert input.shape[0] > 1

        self.parameterization_vector = self.parameterization(input)

        size = input.shape[0]
        self.knot = np.linspace(0, 1, size - (self.degree-1), endpoint=True)
        self.knot = np.append([0] * self.degree, self.knot)
        self.knot = np.append(self.knot, [1] * self.degree)

        return
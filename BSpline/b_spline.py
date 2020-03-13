import numpy as np

class BSpline():
    def __init__(self, interval = 0.01, degree = 3):
        self.interpolation_points = None
        self.degree = degree
        self.interval = interval

    def fit(self, input):

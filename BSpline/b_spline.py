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

    def divide(self, i, j):
        return  i/j if j else 0

    def B_spline_basis(self, k,t,  i, j, d):
        if d == 0 :
            return 1 if i==j else 0
        return self.divide(k[j] - k[i], k[i + d] - k[i]) * self.B_spline_basis(k,t,  i, j, d-1) + \
               self.divide(k[i + d + 1] - k[j], k[i + d + 1] - k[i + 1]) * self.B_spline_basis(k,t,  i + 1, j, d-1)


    def fit(self, input):
        assert input.shape[0] > 1

        self.parameterization_vector = self.parameterization(input)

        self.size_n = input.shape[0]
        self.knot = self.parameterization_vector#np.linspace(0, 1, size - (self.degree-1), endpoint=True)
        self.knot = np.append([0] * self.degree, self.knot)
        self.knot = np.append(self.knot, [1] * self.degree)

        self.a = self.input[:,1]
        h = np.diff(input[:,0])
        A = self.__calc_A(h)
        B = self.__calc_B(h)


        return

    def __calc_A(self, h):
        u"""
        calc matrix A for spline coefficient c
        """
        A = np.zeros((self.size_n, self.size_n))
        A[0, 0] = 1.0
        for i in range(self.size_n - 1):
            if i != (self.size_n - 2):
                A[i + 1, i + 1] = 2.0 * (h[i] + h[i + 1])
            A[i + 1, i] = h[i]
            A[i, i + 1] = h[i]
        A[0, 1] = 0.0
        A[self.size_n - 1, self.size_n - 2] = 0.0
        A[self.size_n - 1, self.size_n - 1] = 1.0
        #  print(A)
        return A

    def __calc_B(self, h):
        u"""
        calc matrix B for spline coefficient c
        """
        B = np.zeros(self.size_n)
        for i in range(self.size_n - 2):
            B[i + 1] = 3.0 * (self.a[i + 2] - self.a[i + 1]) / \
                       h[i + 1] - 3.0 * (self.a[i + 1] - self.a[i]) / h[i]
        #  print(B)
        return B

    class Spline:
        u"""
        Cubic Spline class
        """

        def __init__(self, x, y):
            self.b, self.c, self.d, self.w = [], [], [], []

            self.x = x
            self.y = y

            self.nx = len(x)  # dimension of x
            h = np.diff(x)

            # calc coefficient c
            self.a = [iy for iy in y]

            # calc coefficient c
            A = self.__calc_A(h)
            B = self.__calc_B(h)
            self.c = np.linalg.solve(A, B)
            #  print(self.c1)

            # calc spline coefficient b and d
            for i in range(self.nx - 1):
                self.d.append((self.c[i + 1] - self.c[i]) / (3.0 * h[i]))
                tb = (self.a[i + 1] - self.a[i]) / h[i] - h[i] * \
                     (self.c[i + 1] + 2.0 * self.c[i]) / 3.0
                self.b.append(tb)

        def calc(self, t):
            u"""
            Calc position
            if t is outside of the input x, return None
            """

            if t < self.x[0]:
                return None
            elif t > self.x[-1]:
                return None

            i = self.__search_index(t)
            dx = t - self.x[i]
            result = self.a[i] + self.b[i] * dx + \
                     self.c[i] * dx ** 2.0 + self.d[i] * dx ** 3.0

            return result

        def calcd(self, t):
            u"""
            Calc first derivative
            if t is outside of the input x, return None
            """

            if t < self.x[0]:
                return None
            elif t > self.x[-1]:
                return None

            i = self.__search_index(t)
            dx = t - self.x[i]
            result = self.b[i] + 2.0 * self.c[i] * dx + 3.0 * self.d[i] * dx ** 2.0
            return result

        def calcdd(self, t):
            u"""
            Calc second derivative
            """

            if t < self.x[0]:
                return None
            elif t > self.x[-1]:
                return None

            i = self.__search_index(t)
            dx = t - self.x[i]
            result = 2.0 * self.c[i] + 6.0 * self.d[i] * dx
            return result

        def __search_index(self, x):
            u"""
            search data segment index
            """
            return bisect.bisect(self.x, x) - 1

        def __calc_A(self, h):
            u"""
            calc matrix A for spline coefficient c
            """
            A = np.zeros((self.nx, self.nx))
            A[0, 0] = 1.0
            for i in range(self.nx - 1):
                if i != (self.nx - 2):
                    A[i + 1, i + 1] = 2.0 * (h[i] + h[i + 1])
                A[i + 1, i] = h[i]
                A[i, i + 1] = h[i]

            A[0, 1] = 0.0
            A[self.nx - 1, self.nx - 2] = 0.0
            A[self.nx - 1, self.nx - 1] = 1.0
            #  print(A)
            return A

        def __calc_B(self, h):
            u"""
            calc matrix B for spline coefficient c
            """
            B = np.zeros(self.nx)
            for i in range(self.nx - 2):
                B[i + 1] = 3.0 * (self.a[i + 2] - self.a[i + 1]) / \
                           h[i + 1] - 3.0 * (self.a[i + 1] - self.a[i]) / h[i]
            #  print(B)
            return B
import numpy as np
from scipy.misc import derivative

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
        # tmp[-1] = tmp[-1] - 0.000001
        return np.array(tmp)

    def divide(self, i, j):
        return  i/j if j else 0


    def get_t(self,t,k):
        return 1 if k>=len(t) else (0 if k<0 else t[k] )

    def B_spline_basis(self, t,k, j, d):

        if d == 0 :
            return 1 if  (k[j] == t or (k[j+1]> t and k[j] <= t))  else 0
        return self.divide(t - k[j], k[j + d] - k[j])* self.B_spline_basis(t,  k, j, d-1) + \
               self.divide(k[j + d+1] - t, k[j + d+1]  - k[j +1]) * self.B_spline_basis(t,  k , j+ 1, d-1)

    def d_B_spline_basis(self, t,k, j, d,de):
        if de == 1 :
            return d * (
                self.divide(self.B_spline_basis(t, k, j, d - 1) , k[j + d] - k[j]) -
                self.divide(self.B_spline_basis(t, k, j+1, d - 1) , k[j + d+1] - k[j+1])
            )
        elif de > 1:
            return d * (
                    self.divide(self.d_B_spline_basis(t, k, j, d - 1,de -1), k[j + d] - k[j]) -
                    self.divide(self.d_B_spline_basis(t, k, j + 1, d - 1,de -1), k[j + d + 1] - k[j + 1])
            )

        # return self.divide(t - k[j], k[j + d] - k[j])* self.B_spline_basis(t,  k, j, d-1) + \
        #        self.divide(k[j + d+1] - t, k[j + d+1]  - k[j +1]) * self.B_spline_basis(t,  k , j+ 1, d-1)

    def fit(self, input):
        assert input.shape[0] > 1

        self.parameterization_vector = self.parameterization(input)

        self.size_n = input.shape[0]
        self.knot = np.copy(self.parameterization_vector)#np.linspace(0, 1, size - (self.degree-1), endpoint=True)
        # self.knot[-1] = self.knot[-1] - 0.000001
        self.knot = np.append([0] * self.degree, self.knot)
        self.knot = np.append(self.knot, [1] * self.degree)

        N = np.zeros([self.size_n+2,self.size_n+self.degree -1 ])
        N[0,0] = 1
        N[-1,-1] = 1
        for i in range(1,self.size_n):
            for j in range(1,self.size_n+self.degree -1):
                N[i+1,j] = self.B_spline_basis(self.parameterization_vector[i],self.knot,j,self.degree)
        pass

        for i in range(self.degree):
            N[1,i] = self.d_B_spline_basis(self.parameterization_vector[0],self.knot,i,self.degree, self.degree-1)#
            N[-2,-self.degree+i] = self.d_B_spline_basis(self.parameterization_vector[-1] - 0.000001,self.knot,i + self.size_n -1,self.degree, self.degree-1)
            # N[-2,-1-i] = self.d_B_spline_basis(self.parameterization_vector[0],self.knot,i,self.degree, self.degree-1)#

        D = np.zeros([self.size_n+2,2])
        D[2:-2] =input[1 : -1]
        D[0] = input[0]
        D[-1] = input[-1]
        # self.a = self.input[:,1]
        c_0 = np.linalg.solve(N, D[:,0])#.astype(np.float16)
        c_1 = np.linalg.solve(N, D[:,1])#.astype(np.float16)
        self.c = np.hstack((c_0.reshape(-1,1),c_1.reshape(-1,1)))
        # h = np.diff(input[:,0])
        # A = self.__calc_A(h)
        # B = self.__calc_B(h)
        # return

    def get_interpolation(self,d = 0.0001):
        # t = np.arange(0.,1.0,d)
        # j = 0
        time = np.arange(0.,1.0,d)
        a = np.zeros((time.shape[0]+1 ,2))
        for ind , t in enumerate(time):
            N = np.zeros(self.c.shape[0])
            n_p = np.zeros((self.c.shape[0],2))
            for i,p in enumerate(self.c):
                N[i] = self.B_spline_basis(t,self.knot,i,self.degree)
                n_p[i] =  p * N[i]
            a[ind] = np.sum(n_p,0)

        a[-1] = self.c[-1]
        return a

    def org_config(self):
        txt = ''
        txt += '{:0>2d}\n'.format(self.degree)
        txt += '{:0>2d}\n'.format(self.c.shape[0])
        tmp = ''
        for x in self.knot:
            tmp+= '{} '.format(x)
        txt += tmp + '\n'
        for x in self.c:
            txt+= '{} {}\n'.format(x[0],x[1])

        return txt


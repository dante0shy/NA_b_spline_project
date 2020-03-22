import sys, os
import numpy as np
from BSpline import BSpline
import matplotlib.pyplot as plt
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "")
)


if __name__ == "__main__":
    control_points = open(
        os.path.join(
            os.path.dirname(
                os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
            ),
            "extras",
            "test_case_0.txt",
        )
    ).readlines()
    b_splines = BSpline()
    control_points = np.array([ [float(y) for y in x.strip().split(' ')] for x in control_points  if x.strip()])
    b_splines.fit(control_points)
    curve  = b_splines.get_interpolation()
    fig = plt.figure()
    ax = fig.gca()
    ax.plot(curve[:,0], curve[:,1],  label='curve')
    ax.scatter(control_points[:,0], control_points[:,1], marker='^')

    ax.scatter(b_splines.c[:,0], b_splines.c[:,1], marker='o',c = 'b')
    ax.plot(b_splines.c[:,0], b_splines.c[:,1], "b--", linewidth=1,c = 'b')


    # ax.legend()

    plt.show()
    pass

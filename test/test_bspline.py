import sys, os
import numpy as np
from BSpline import BSpline
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
    control_points = np.array([ [int(y) for y in x.strip().split(' ')] for x in control_points  if x.strip()])
    b_splines.fit(control_points)

    pass

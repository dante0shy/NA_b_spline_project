import sys, os,shutil
import numpy as np
from BSpline import BSpline
import matplotlib.pyplot as plt
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "")
)

project_path = os.path.dirname(
                os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
            )
input_path = os.path.join(
            project_path,
            "extras"
        )
output = os.path.join(project_path,'extras', 'output_config')
if not os.path.exists(output) or not os.path.isdir(output):
    os.mkdir(output)

if __name__ == "__main__":
    f_name = "test_case_2.txt"
    file_path = os.path.join(
            input_path,
            f_name,
        )
    control_points = open(
        file_path
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

    plt.show()
    config = b_splines.org_config()
    print(config)
    with open(os.path.join(output,'o_' + f_name),'w') as f:
        f.write(config)
    pass

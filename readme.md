===BSpline visualizer

A simple visualizer for B-Spline algorithmn

Requirement:

    Python 3.7

Install:

    git clone https://github.com/dante0shy/NA_b_spline_project.git
    cd NA_b_spline_project
    pip install -r requirement.txt

The algorithmn is based on the cubic b-spline interpolation.
I realize the basic interpolation and some other function like paramerterzation method and changable degree(other degree modifies the algorithmn not to a cubic b-spline).
The visualization range of points is highter than -1 for both x and y.
Some effects of curve are as next:

![image](https://github.com/dante0shy/NA_b_spline_project/raw/master/extras/10p1.png)
![image](https://github.com/dante0shy/NA_b_spline_project/raw/master/extras/5p1.png)

Usage:

    Draw: display the curve based on the setting on the left side
    Add point: add a point for current setting
    Degree: the degree for the curve (he input should be a int)
    Paramerterzation: the paramerterzation setting
    Points input: the order of input is (x,y), del button on the left side is for removing the point for the curve

You may also want to use the script to display the results. The command is as below:

    cd ./test
    python test

The setting of b-spline can be changed in the script with:

    interval: sample points interval (default is 0.01)
    degree: degree for interpolation
    p_mode: paramerterzation methods (default is 1 for Chord length, 0 for Uniform)
    f_name: file name for points setting (place in extras)

When the script finishes, the curve setting output is in extras/output_config

##BSpline visualizer

A simple visualizer for B-Spline algorithmn

Requirement:

    Python 3.7

Install:

    git clone https://github.com/dante0shy/NA_b_spline_project.git
    cd NA_b_spline_project
    pip install -r requirement.txt

The algorithmn is based on the cubic b-spline interpolation.
I realize the basic interpolation and some other function like paramerterzation method and changable degree(other degree modifies the algorithmn not to a cubic b-spline).
Some effects of curve are as next:

![image](https://github.com/dante0shy/NA_b_spline_project/raw/master/extras/10p1.png)
![image](https://github.com/dante0shy/NA_b_spline_project/raw/master/extras/5p1.png)

Usage:

    Draw: display the curve based on the setting on the left side
    Add point: add a point for current setting
    Degree: the degree for the curve (he input should be a int)
    Paramerterzation: the paramerterzation setting
    Points input: the order of input is (x,y), del button on the left side is for removing the point for the curve

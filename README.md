# Manim Geometry Visualizer
Manim geometry visualizer. It uses a DSL (domain specific language) to define simple geomtery problems defined in school mathematics curriculum. Based on the DSL, it generates the video. This is just a proof of concept, to get familiar with the excellent [manim](https://www.manim.community/) library. The code architecture is rudimentary and will change in future. 

## DSL
```
[header]
Title("Sum of angles of a triangle is 180")

[diag]
Triangle(ABC)
Ang(A) = 90
Ang(B) = 70

[proof]
Line(DE, A) || BC #desc 1. Draw line DE parallel to BC passing thru A
ShowAngles(DAB, BAC, CAE)  #desc 2. Sum of angles $\\angle DAB$, $\\angle BAC$ and $\\angle CAE$ = 180
HighlightAngles(DAB, CBA) #desc 3. $\\angle DAB = \\angle CBA$; corresponding angles between parallel lines
HighlightAngles(CAE, ACB) #desc 4. $\\angle CAE = \\angle BCA$; corresponding angles between parallel lines
HighlightAngles(BAC, CBA, ACB) #desc 5. From (3) and (4) applying it to (2), $\\angle CBA$ + $\\angle BCA$ + $\\angle BAC$ = 180
```

## Output Video

https://user-images.githubusercontent.com/86822090/136006531-a7ffc929-db0f-487b-9484-b88d7b064526.mp4


## Run
See [manim](https://www.manim.community/) documentation to install manim and latex on your OS. Use a virtualenv for this project and once manim is installed, run manim 

`manim -pql gvmain.py`

from manim import *
from gvproblem import GVProblem
from gvrender import GVRender

# Geometry Visualizer
class GV(Scene):
  def construct(self):
    str = """
      [header]
      Title("Sum of angles of a triangle is 180")

      [diag]
      Triangle(ABC)
      Ang(A) = 90
      Ang(B) = 70

      [proof]
      Line(DE, A) || BC #desc Draw line DE parallel to BC passing thru A
      ShowAngles(DAB, BAC, CAE)  #desc sum of angles = 180

    """

    gvp = GVProblem()
    result = gvp.parse(str)
    print(result)

    gvr = GVRender(self)
    gvr.renderProblem(result)
    


# from manim import *
import math as Math
from manim import *
from manim.utils import space_ops
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

class GeomTriangle:
  def __init__(self, labels=('A', 'B', 'C'), angles=[60, 60], height=5):
    self.labels = labels
    self.angles = angles
    self.angles.append(180-(self.angles[0]+self.angles[1]))
    self.height = height
    self.midpoints = []
    self.points = {}
    self.lines = []
    self.mo_lines = []
    self.mo_labels = []
    self.mo_angles = []
    self.mo_points = []

  def addLine(self, line_name):
    self.lines.append(line_name)

  def addMidpoint(self, line_name, label='M'):
    pos0 = self.labels.index(line_name[0])
    pos1 = self.labels.index(line_name[1])
    lookup = {
      '01': LEFT,
      '10': LEFT,
      '12': DOWN,
      '21': DOWN,
      '20': RIGHT,
      '02': RIGHT
    }
    dir = lookup[str(pos0)+str(pos1)]
    self.midpoints.append([line_name, label, dir])

  def drawPoints(self):
    self.drawMidpoints()

  def drawMidpoints(self):
    for mp in self.midpoints:
      line_name, label, dir = mp
      pt = space_ops.midpoint(self.points[line_name[0]], self.points[line_name[1]])
      self.points[label] = pt
      dt = Dot(pt)
      self.mo_points.append(dt)
      mo_label = Text(label).next_to(pt, dir)
      self.mo_points.append(mo_label)

  def drawEdges(self):
    x1 = 0
    y1 = 0
    self.points[self.labels[0]] = [x1, y1, 0]
    a2 = Math.radians(self.angles[1])
    x2 = -(self.height/Math.tan(a2))
    y2 = -self.height
    self.points[self.labels[1]] = [x2, y2, 0]
    a3 = Math.radians(self.angles[2])
    y3 = -self.height
    x3 = self.height/Math.tan(a3)
    self.points[self.labels[2]] = [x3, y3, 0]
    l1 = Line([x1, y1, 0], [ x2, y2, 0])
    l2 = Line([x2, y2, 0], [ x3, y3, 0])
    l3 = Line([x3, y3, 0], [ x1, y1, 0])
    self.mo_lines.extend([l1, l2, l3])

  def drawLabels(self):
    lbl1 = Text(self.labels[0]).next_to(self.mo_lines[0].get_start(), UP)
    lbl2 = Text(self.labels[1]).next_to(self.mo_lines[1].get_start(), LEFT)
    lbl3 = Text(self.labels[2]).next_to(self.mo_lines[2].get_start(), RIGHT)
    self.mo_labels.extend([lbl1, lbl2, lbl3])

  def drawAngles(self):
    self.drawRightAngle()

  def drawLines(self):
    for line_name in self.lines:
      line = Line(self.points[line_name[0]], self.points[line_name[1]])
      self.mo_lines.append(line)

  def drawRightAngle(self):
    if 90 in self.angles:
      pos = self.angles.index(90)
      if pos == 0:
        angle_list = [self.mo_lines[2], self.mo_lines[0]]
      elif pos == 1:
        angle_list = [self.mo_lines[0], self.mo_lines[1]]
      else:
        angle_list = [self.mo_lines[1], self.mo_lines[2]]
      
      ra = RightAngle(*angle_list, length=0.5, quadrant=(-1, 1))
      self.mo_angles.append(ra)

  def draw(self):
    self.drawEdges()
    self.drawLabels()
    self.drawAngles()
    self.drawPoints()
    self.drawLines()

    gr = Group(*self.mo_lines, *self.mo_labels, *self.mo_angles, *self.mo_points)
    gr.move_to([0, 0, 0])
    return gr

# Proof Visualizer
class PV(Scene):
  def construct(self):
    grammar = Grammar(
      r"""
      problem = (line / space)+
      line = section statement*
      space = ~r"\s*"
      section = lsquarebracket lowerword rsquarebracket
      lbracket = "("
      rbracket = ")"
      lsquarebracket = "["
      rsquarebracket = "]"
      lowerword = ~"[_a-z]+"
      equals = space "=" space
      function = ~r"\w+" lbracket funcargs rbracket
      statement = space (function / expr) (equals expr)?
      funcargs = expr (space "," space expr)*
      expr =  numexpr / labels
      numexpr = ~r"\d+"
      labels = ~r"[A-Z]+"
      """
    )

    str = """
  [diag]
  Triangle(ABC)
  Ang(A) = 90
  Ang(B) = 30
  M = Mid(BC)
  LineSegment(AM)
    """

    print(str)
    tree = grammar.parse(str)
    pp = ProblemParser()
    pp.visit(tree)

    tr = GeomTriangle(angles=[10, 35])
    tr.addMidpoint('BC')
    tr.addLine('AM')
    self.add(tr.draw())

class ProblemParser(NodeVisitor):
  def visit_section(self, node, visited_children):
    _, section, _ = visited_children
    return section.text

  def visit_statement(self, node, visited_children):
    print("statement len =", len(visited_children))

  def visit_space(self, node, visited_children):
    return ' '

  def visit_expr(self, node, visited_children):
    return visited_children[0]

  def visit_numexpr(self, node, visited_children):
    return float(node.text)

  def visit_labels(self, node, visited_children):
    return str(node.text)

  def visit_funcargs(self, node, visited_children):
    result = [ visited_children[0] ]
    # if it has additional params
    if isinstance(visited_children[1], list):
      result.extend([ c[3] for c in  visited_children[1]])
    return result

  def generic_visit(self, node, visited_children):
    return visited_children or node

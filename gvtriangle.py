from manim import *
import math as Math
from manim.utils import space_ops

class GVTriangle:
  def __init__(self, labels='ABC', angles=None, height=5):
    self.labels = list(labels)
    self.angles = [0, 0, 0] if angles is None else angles
    self.height = height
    self.current_section = 'diag'
    self.diag_render_list = []
    self.proof_render_list = []
    self.comment_list = []
    self.mo_lines = {}
    self.mo_points = {}

  def setAngle(self, label, value):
    pos = self.labels.index(label)
    self.angles[pos] = value
    if self.canGetVertices():
      self.addVerticesAndEdges()

  def showAngles(self, *angles):
    angle_list = []
    for angle_name in angles:
      l1_name = angle_name[0:2]
      l1 = self.mo_lines[l1_name] if l1_name in self.mo_lines else self.mo_lines[l1_name[1::-1]]
      q1 = -1 if l1_name in self.mo_lines else 1
      l2_name = angle_name[1:]
      l2 = self.mo_lines[l2_name] if l2_name in self.mo_lines else self.mo_lines[l2_name[2::-1]]
      q2 = 1 if l2_name in self.mo_lines else -1
      angle_list.append(Angle(l1, l2, radius=1, color=GREEN, quadrant=(q1, q2)))

    self.addToRenderList(angle_list, mode="serial")

  def highlightAngles(self, *angles):
    angle_list = []
    for angle_name in angles:
      l1_name = angle_name[0:2]
      l1 = self.mo_lines[l1_name] if l1_name in self.mo_lines else self.mo_lines[l1_name[1::-1]]
      q1 = -1 if l1_name in self.mo_lines else 1
      l2_name = angle_name[1:]
      l2 = self.mo_lines[l2_name] if l2_name in self.mo_lines else self.mo_lines[l2_name[2::-1]]
      q2 = 1 if l2_name in self.mo_lines else -1
      angle_list.append(Angle(l1, l2, radius=1, color=RED, quadrant=(q1, q2)))

    self.addToRenderList(angle_list, anim_method=Indicate, run_time=6.0, scale_factor=1.5)


  def setSection(self, section_name):
    self.current_section = section_name

  def canGetVertices(self):
    return self.angles.count(0) <= 1
  
  def addToRenderList(self, rlist, anim_method=Create, mode="parallel", **kwargs):
    r = { "mo_list": rlist, "anim_method": anim_method, "mode": mode, "kwargs": kwargs  }
    if self.current_section == 'diag':
      self.diag_render_list.append(r)
    else:
      self.proof_render_list.append(r)

  def addVerticesAndEdges(self):
    if self.angles.count(0) == 1:
      #determine third angle
      pos = self.angles.index(0)
      self.angles[pos] = 180 - sum(self.angles)
    x1 = 0
    y1 = 0
    a2 = Math.radians(self.angles[1])
    x2 = -(self.height/Math.tan(a2))
    y2 = -self.height
    a3 = Math.radians(self.angles[2])
    y3 = -self.height
    x3 = self.height/Math.tan(a3)

    d1 = Dot([x1, y1, 0], radius=0.08)
    d2 = Dot([x2, y2, 0], radius=0.08)
    d3 = Dot([x3, y3, 0], radius=0.08)

    self.mo_points[self.labels[0]] = d1
    self.mo_points[self.labels[1]] = d2
    self.mo_points[self.labels[2]] = d3

    mo_l1 = Line([x1, y1, 0], [ x2, y2, 0])
    line_name = self.labels[0]+self.labels[1]
    self.mo_lines[line_name] = mo_l1

    mo_l2 = Line([x2, y2, 0], [ x3, y3, 0])
    line_name = self.labels[1]+self.labels[2]
    self.mo_lines[line_name] = mo_l2

    mo_l3 = Line([x3, y3, 0], [ x1, y1, 0])
    line_name = self.labels[2]+self.labels[0]
    self.mo_lines[line_name] = mo_l3

    self.addToRenderList([d1, d2, d3, mo_l1, mo_l2, mo_l3])
    mo_lbl1 = Text(self.labels[0]).next_to(mo_l1.get_start(), UP)
    mo_lbl2 = Text(self.labels[1]).next_to(mo_l2.get_start(), LEFT)
    mo_lbl3 = Text(self.labels[2]).next_to(mo_l3.get_start(), RIGHT)
    self.addToRenderList([mo_lbl1, mo_lbl2, mo_lbl3])
  

  def addComment(self, comment, anim_method=Create, mode="parallel", **kwargs):
    if self.current_section != 'proof': return False
    r = { "mo_list":[], "anim_method": anim_method, "mode": mode, "kwargs": kwargs }
    if comment:
      mo_text = Tex(comment, should_center=False, tex_template=TexFontTemplates.droid_sans)
      if len(self.comment_list) > 0:
        mo_text.next_to(self.comment_list[-1]["mo_list"][0], direction=DOWN, aligned_edge=LEFT)
      r["mo_list"].append(mo_text)
    
    self.comment_list.append(r)


  def setParallelLine(self, line_name, via, to):
    x1, y1, _ = self.mo_points[to[0]].get_arc_center()
    x2, y2, _ = self.mo_points[to[1]].get_arc_center()
    x3, y3, _ = self.mo_points[via].get_arc_center()

    m = (y2-y1)/(x2-x1)
    a = self.height / 2
    x4 = x3 - (a/Math.sqrt(1+m*m))
    y4 = y3 - (a*m/Math.sqrt(1+m*m))

    x5 = x3 + (a/Math.sqrt(1+m*m))
    y5 = y3 + (a*m/Math.sqrt(1+m*m))


    d1 = Dot((x4, y4, 0), radius=0.04)
    d2 = Dot((x5, y5, 0), radius=0.04)

    self.mo_points[line_name[0]] = d1
    self.mo_points[line_name[1]] = d2

    mo_line1 = Line(d1.get_arc_center(), self.mo_points[via].get_arc_center())
    self.mo_lines[line_name[0]+via] = mo_line1
    mo_line2 = Line(self.mo_points[via].get_arc_center(), d2.get_arc_center())
    self.mo_lines[via+line_name[1]] = mo_line2

    mo_lbl1 = Text(line_name[0]).next_to(mo_line1.get_start(), LEFT)
    mo_lbl2 = Text(line_name[1]).next_to(mo_line2.get_end(), RIGHT)
    self.addToRenderList([d1, d2, mo_line1, mo_line2, mo_lbl1, mo_lbl2])

  def setMidpoint(self, line_name, label):
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
    pt = space_ops.midpoint(self.points[line_name[0]], self.points[line_name[1]])
    self.points[label] = pt
    mo_dot = Dot(pt)
    mo_label = Text(label).next_to(pt, dir)
    self.render_list.append([mo_dot, mo_label])

  def drawRightAngle(self):
    if 90 in self.angles:
      pos = self.angles.index(90)     
      ra = RightAngle(self.mo_lines[pos], self.mo_lines[(pos-1+3)%3], length=0.5, quadrant=(1, -1))
      self.mo_angles.append(ra)


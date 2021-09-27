from manim import *
class GVHeader:
  def __init__(self, title=""):
    self.title = title
    self.render_list = [ [self.draw() ] ] 

  def draw(self):
    return Text(self.title).scale(0.75).set_color("#0066FF")


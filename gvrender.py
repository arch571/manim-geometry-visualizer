from helpers.common import flattenList, flattenRenderList, playRenderGroup
from gvtriangle import GVTriangle
from gvheader import GVHeader 
from manim import *

class GVRender:
  METHOD_LOOKUP = {
    "Triangle": ('c', lambda fargs: GVTriangle(labels=fargs[0])), #consructor
    "Ang": ('im', lambda diag, fargs: diag.setAngle(*fargs)), #instance method
    "Mid": ('im', lambda diag, fargs: diag.setMidpoint(*fargs)), #instance method
    "Line": ('im', lambda diag, fargs: diag.setLine(*fargs)), #instance method
    "ParallelLine": ('im', lambda diag, fargs: diag.setParallelLine(*fargs)), #instance method
    "Title": ('c', lambda fargs: GVHeader(title=fargs[0])),
    "ShowAngles": ('im', lambda diag, fargs: diag.showAngles(*fargs)), #instance method
    "HighlightAngles": ('im', lambda diag, fargs: diag.highlightAngles(*fargs)), #instance method
  }

  def __init__(self, scene):
    self.gi_list = [] # list of geometric instances
    self.scene = scene

  def renderProblem(self, problem):
    for item in problem:
      if isinstance(item, list):
        self.initSection(item[0])
        self.constructSection(item[1])
    
    self.render()

  def initSection(self, section_name):
    if section_name == 'proof':
      self.gi_list[-1].setSection(section_name)

  def constructSection(self, section_def):
    for step in section_def:
      fname = step['function']
      fargs = step['args']
      method_type, method = self.METHOD_LOOKUP[fname]
      if method_type == 'c':
        self.gi_list.append(method(fargs))
      if method_type == 'im':
        gi = self.gi_list[-1]  #geometry instance
        gi.addComment(step['comments'] if 'comments' in step else None)
        method(gi, fargs)

  def renderSection(self, section_name):
    if section_name == "header":
      self.renderHeader()
    elif section_name == "diag":
      self.renderDiag()
    else:
      self.renderProof()

  def scaleToLeft(self, vg):
    fh = config.frame_height * 0.8
    fw = config.frame_width * 0.5

    if vg.height > fh:
      vg.scale_to_fit_height(fh)

    if vg.width > fw:
      vg.scale_to_fit_width(fw)

    vg.move_to([-config.frame_width/4, 0, 0])

  def scaleToRight(self, vg):
    fh = config.frame_height * 0.8
    fw = config.frame_width * 0.5

    if vg.height > fh:
      vg.scale_to_fit_height(fh)

    if vg.width > fw:
      vg.scale_to_fit_width(fw)

    vg.move_to([config.frame_width/4, 0, 0])


  def render(self):
    self.renderHeader()
    self.renderDiag()
    self.renderProof()

  def renderHeader(self):
    #render header
    header_gi = self.gi_list[0]
    header_mo_list = flattenList(header_gi.render_list)
    mo = header_mo_list[0]
    self.scene.play(FadeIn(mo))
    self.scene.play(mo.animate.shift((0,3.5,0)))

  def renderDiag(self):
    pass

  def renderProof(self):
    diag_gi = self.gi_list[1]
    diag_mo_list = flattenRenderList(diag_gi.diag_render_list)
    diag_mo_list.extend(flattenRenderList(diag_gi.proof_render_list))
    vg = VGroup(*diag_mo_list)
    self.scaleToLeft(vg)
    # but render diag objects
    for render_group in diag_gi.diag_render_list:
      playRenderGroup(self.scene, render_group)

    # but render proof objects
    clist = flattenRenderList(diag_gi.comment_list)
    vg = VGroup(*clist)
    self.scaleToRight(vg)

    for index, render_group in enumerate(diag_gi.proof_render_list):
      if len(diag_gi.comment_list[index]) > 0:
        playRenderGroup(self.scene, diag_gi.comment_list[index])

      playRenderGroup(self.scene, render_group)

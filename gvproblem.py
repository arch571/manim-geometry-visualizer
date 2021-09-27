from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

class GVProblem(NodeVisitor):
  RULES = r"""
      problem = (section / space)+
      section = sectionstart statement*
      space = ~r"\s*"
      sectionstart = lsquarebracket lowerword rsquarebracket
      lbracket = "("
      rbracket = ")"
      lsquarebracket = "["
      rsquarebracket = "]"
      lowerword = ~"[_a-z]+"
      quote = "\""
      equals = space "=" space
      parallel = space "||" space
      function = ~r"\w+" lbracket funcargs rbracket
      statement = space (function / expr) ((equals / parallel) expr)? namedcomments?
      namedcomments = space description 
      description = "#desc" space ~r".+" 
      funcargs = expr (space "," space expr)*
      expr =  numexpr / labels / string
      string = quote ~r"[^\"]+" quote
      numexpr = ~r"\d+"
      labels = ~r"[A-Z]+"
      """

  def parse(self, str):
    grammar = Grammar(self.RULES)
    tree = grammar.parse(str)
    return self.visit(tree)

  def visit_problem(self, node, visited_children):
    return [ v[0] for v in visited_children ]
    # return visited_children

  def visit_sectionstart(self, node, visited_children):
    _, section, _ = visited_children
    return section.text

  def visit_statement(self, node, visited_children):
    rhs = visited_children[2]
    lhs = visited_children[1][0]
    if isinstance(rhs, list):
      operator, rhs_expr = rhs[0]
      if operator[0] == '||':
        lhs["function"] = "ParallelLine"
      lhs["args"].append(rhs_expr)

    if isinstance(visited_children[3] , list):
      lhs["comments"] = visited_children[3][0]
    return lhs

  def visit_section(self, node, visited_children):
    section_name, statements = visited_children
    return visited_children
    
  def visit_namedcomments(self, node, visited_children):
    return visited_children[1]

  def visit_space(self, node, visited_children):
    return ''

  def visit_function(self, node, visited_children):
    return { "function": visited_children[0].text, "args": visited_children[2] }
    
  def visit_expr(self, node, visited_children):
    return visited_children[0]

  def visit_equals(self, node, visited_children):
    return '='

  def visit_description(self, node, visited_children):
    return visited_children[2].text

  def visit_parallel(self, node, visited_children):
    return '||'

  def visit_numexpr(self, node, visited_children):
    return float(node.text)

  def visit_labels(self, node, visited_children):
    return str(node.text)

  def visit_string(self, node, visited_children):
    return node.children[1].text

  def visit_funcargs(self, node, visited_children):
    result = [ visited_children[0] ]
    # if it has additional params
    if isinstance(visited_children[1], list):
      result.extend([ c[3] for c in  visited_children[1]])
    return result

  def generic_visit(self, node, visited_children):
    return visited_children or node

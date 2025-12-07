"""
AST node definitions for ZLang.

These are simple, plain Python classes used by the parser.
They intentionally avoid heavy behavior — the analyzer and generator
should traverse these node classes to perform checks and emit code.
"""

class Node:
	pass


class Program(Node):
	def __init__(self, declarations=None):
		self.declarations = declarations or []

	def __repr__(self):
		return f"Program({self.declarations})"


class FunctionDecl(Node):
	def __init__(self, name, params, body):
		self.name = name
		self.params = params
		self.body = body or []

	def __repr__(self):
		return f"FunctionDecl({self.name}, params={self.params}, body={self.body})"


class VarDecl(Node):
	def __init__(self, name, initializer):
		self.name = name
		self.initializer = initializer

	def __repr__(self):
		return f"VarDecl({self.name} = {self.initializer})"


class Assign(Node):
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def __repr__(self):
		return f"Assign({self.name} = {self.value})"


class IfStmt(Node):
	def __init__(self, condition, then_branch, else_branch=None):
		self.condition = condition
		self.then_branch = then_branch or []
		self.else_branch = else_branch or []

	def __repr__(self):
		return f"If({self.condition}, then={self.then_branch}, else={self.else_branch})"


class WhileStmt(Node):
	def __init__(self, condition, body):
		self.condition = condition
		self.body = body or []

	def __repr__(self):
		return f"While({self.condition}, body={self.body})"


class ExprStmt(Node):
	def __init__(self, expression):
		self.expression = expression

	def __repr__(self):
		return f"ExprStmt({self.expression})"


class CallExpr(Node):
	def __init__(self, callee, args):
		self.callee = callee
		self.args = args or []

	def __repr__(self):
		return f"Call({self.callee}, args={self.args})"


class BinaryExpr(Node):
	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right

	def __repr__(self):
		return f"Binary({self.left} {self.operator} {self.right})"


class Literal(Node):
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return f"Literal({self.value})"


class Identifier(Node):
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f"Ident({self.name})"


from compiler.Parser.ast import (
    Program,
    FunctionDecl,
    VarDecl,
    Assign,
    IfStmt,
    WhileStmt,
    ExprStmt,
    CallExpr,
    BinaryExpr,
    Literal,
    Identifier,
)


class ZLangRuntimeError(Exception):
    """Runtime error raised by the ZLang interpreter."""
    pass


class Environment:
    """Lexically scoped environment for variables."""

    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        # If not previously declared, fall back to defining in current scope
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise ZLangRuntimeError(f"Undefined variable '{name}'.")


class Interpreter:
    """
    Tree-walk interpreter for the ZLang AST.

    Usage:
        interp = Interpreter()
        interp.interpret(program_ast)
    """

    def __init__(self, input_fn=input, output_fn=print):
        self.globals = Environment()
        self.env = self.globals
        self.functions = {}
        self.input_fn = input_fn
        self.output_fn = output_fn
        self._install_builtins()

    def interpret(self, program: Program):
        for decl in program.declarations:
            if isinstance(decl, FunctionDecl):
                self.functions[decl.name] = decl
            else:
                self._execute(decl, self.env)

        if "main" in self.functions:
            self._call_function("main", [])

    def _install_builtins(self):
        def _builtin_say(args):
            # say("hello"), say("a", "b") etc.
            self.output_fn(*args)

        def _builtin_spill(args):
            # spill("prompt") -> string input
            prompt = str(args[0]) if args else ""
            return self.input_fn(prompt)

        self.globals.define("say", _builtin_say)
        self.globals.define("spill", _builtin_spill)

    def _execute(self, node, env):
        if isinstance(node, VarDecl):
            value = self._evaluate(node.initializer, env)
            env.define(node.name, value)

        elif isinstance(node, Assign):
            value = self._evaluate(node.value, env)
            env.assign(node.name, value)

        elif isinstance(node, IfStmt):
            cond_val = self._evaluate(node.condition, env)
            if self._truthy(cond_val):
                for stmt in node.then_branch:
                    self._execute(stmt, env)
            elif node.else_branch:
                for stmt in node.else_branch:
                    self._execute(stmt, env)

        elif isinstance(node, WhileStmt):
            while self._truthy(self._evaluate(node.condition, env)):
                for stmt in node.body:
                    self._execute(stmt, env)

        elif isinstance(node, ExprStmt):
            self._evaluate(node.expression, env)

        elif isinstance(node, FunctionDecl):
            # Allow nested declarations too.
            self.functions[node.name] = node

        elif isinstance(node, Program):
            self.interpret(node)

        elif node is None:
            return

        else:
            raise ZLangRuntimeError(f"Cannot execute node type: {type(node).__name__}")

    def _evaluate(self, expr, env):
        if isinstance(expr, Literal):
            return self._convert_literal(expr.value)

        if isinstance(expr, Identifier):
            return env.get(expr.name)

        if isinstance(expr, BinaryExpr):
            left = self._evaluate(expr.left, env)
            right = self._evaluate(expr.right, env)
            op = expr.operator

            # Arithmetic
            if op == "+":
                return left + right
            if op == "-":
                return left - right
            if op == "*":
                return left * right
            if op == "/":
                return left / right

            # Comparisons
            if op == "==":
                return left == right
            if op == "!=":
                return left != right
            if op == ">":
                return left > right
            if op == ">=":
                return left >= right
            if op == "<":
                return left < right
            if op == "<=":
                return left <= right

            raise ZLangRuntimeError(f"Unknown binary operator '{op}'")

        if isinstance(expr, CallExpr):
            # Currently only simple identifier calls are supported (say, spill, user funcs).
            callee = expr.callee
            if not isinstance(callee, Identifier):
                raise ZLangRuntimeError("Can only call named functions.")

            name = callee.name
            args = [self._evaluate(a, env) for a in expr.args]

            try:
                builtin = self.globals.get(name)
            except ZLangRuntimeError:
                builtin = None

            if callable(builtin):
                return builtin(args)

            return self._call_function(name, args)

        raise ZLangRuntimeError(f"Unknown expression node: {type(expr).__name__}")

    def _call_function(self, name, arg_values):
        func = self.functions.get(name)
        if func is None:
            raise ZLangRuntimeError(f"Undefined function '{name}'")

        local_env = Environment(self.globals)
        previous_env = self.env
        try:
            self.env = local_env
            for stmt in func.body:
                self._execute(stmt, self.env)
        finally:
            self.env = previous_env

        return None

    def _convert_literal(self, value):
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            try:
                if value.isdigit():
                    return int(value)
                return float(value)
            except ValueError:
                return value
        return value

    def _truthy(self, value):
        return bool(value)

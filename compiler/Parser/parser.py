from compiler.lexer.TokenType import TokenType

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


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        declarations = []
        while not self._is_at_end():
            if self._match(TokenType.VIBE):
                declarations.append(self._function_decl())
            else:
                # try to parse a top-level statement as expression
                stmt = self._statement()
                if stmt:
                    declarations.append(stmt)
        return Program(declarations)

    # --- Declarations ---
    def _function_decl(self):
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected function name after 'vibe'")
        name = name_tok.lexeme
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after function name")
        # no params supported right now
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after function params")

        # optional brace start — tokenizer may or may not emit braces
        if self._check(TokenType.BRACE_LEFT):
            self._advance()
            body = self._block_until(TokenType.BRACE_RIGHT)
            if self._check(TokenType.BRACE_RIGHT):
                self._advance()
        else:
            # parse statements until next top-level keyword or EOF
            body = []
            while not self._is_at_end() and not self._check(TokenType.VIBE):
                stmt = self._statement()
                if stmt:
                    body.append(stmt)

        return FunctionDecl(name, params=[], body=body)

    # --- Statements ---
    def _statement(self):
        if self._match(TokenType.LIT):
            return self._var_decl()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.YAP):
            return self._while_statement()
        # SAY and other keywords may be calls
        if self._match(TokenType.SAY):
            return ExprStmt(self._parse_call_from_keyword('say'))

        # assignment or expression statement
        if self._check(TokenType.IDENTIFIER):
            # lookahead for assignment
            if self._lookahead_is_assign():
                return self._assignment()
            else:
                expr = self._expression()
                return ExprStmt(expr)

        # fallback: try expression
        if not self._is_at_end():
            expr = self._expression()
            return ExprStmt(expr)

        return None

    def _var_decl(self):
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'lit'")
        name = name_tok.lexeme
        self._consume(TokenType.EQUAL, "Expected '=' in variable declaration")
        initializer = self._expression()
        return VarDecl(name, initializer)

    def _assignment(self):
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected identifier for assignment")
        name = name_tok.lexeme
        self._consume(TokenType.EQUAL, "Expected '=' in assignment")
        value = self._expression()
        return Assign(name, value)

    def _if_statement(self):
        condition = self._expression()
        # allow colon or braces; consume colon if present
        if self._match(TokenType.COLON):
            then_branch = [self._statement()]
        elif self._check(TokenType.BRACE_LEFT):
            self._advance()
            then_branch = self._block_until(TokenType.BRACE_RIGHT)
            if self._check(TokenType.BRACE_RIGHT):
                self._advance()
        else:
            then_branch = [self._statement()]

        # optional else not implemented fully — return basic IfStmt
        return IfStmt(condition, then_branch)

    def _while_statement(self):
        condition = self._expression()
        if self._match(TokenType.COLON):
            body = [self._statement()]
        elif self._check(TokenType.BRACE_LEFT):
            self._advance()
            body = self._block_until(TokenType.BRACE_RIGHT)
            if self._check(TokenType.BRACE_RIGHT):
                self._advance()
        else:
            body = [self._statement()]
        return WhileStmt(condition, body)

    def _block_until(self, end_token_type):
        stmts = []
        while not self._is_at_end() and not self._check(end_token_type):
            stmt = self._statement()
            if stmt:
                stmts.append(stmt)
        return stmts

    # --- Expressions ---
    def _expression(self):
        return self._equality()

    def _equality(self):
        expr = self._comparison()
        while self._match(TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            operator = self._previous().lexeme
            right = self._comparison()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _comparison(self):
        expr = self._term()
        while self._match(TokenType.GREATER_THAN, TokenType.GREATER_THAN_EQUAL, TokenType.LESS_THAN, TokenType.LESS_THAN_EQUAL):
            operator = self._previous().lexeme
            right = self._term()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _term(self):
        expr = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().lexeme
            right = self._factor()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _factor(self):
        expr = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous().lexeme
            right = self._unary()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def _unary(self):
        # No explicit unary tokens defined in TokenType; extend as needed
        return self._call()

    def _call(self):
        expr = self._primary()
        while True:
            if self._match(TokenType.LEFT_PAREN):
                args = []
                if not self._check(TokenType.RIGHT_PAREN):
                    args.append(self._expression())
                    while self._match(TokenType.COMMA):
                        args.append(self._expression())
                self._consume(TokenType.RIGHT_PAREN, "Expected ')' after arguments")
                expr = CallExpr(expr, args)
            else:
                break
        return expr

    def _parse_call_from_keyword(self, name):
        # parse call like say("...") where SAY token already consumed
        self._consume(TokenType.LEFT_PAREN, f"Expected '(' after {name}")
        args = []
        if not self._check(TokenType.RIGHT_PAREN):
            args.append(self._expression())
            while self._match(TokenType.COMMA):
                args.append(self._expression())
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after call")
        return CallExpr(Identifier(name), args)

    def _primary(self):
        if self._match(TokenType.NUMBER):
            return Literal(self._previous().lexeme)
        if self._match(TokenType.STRING):
            return Literal(self._previous().lexeme)
        if self._match(TokenType.IDENTIFIER):
            return Identifier(self._previous().lexeme)
        # keywords like spill are tokenized as IDENTIFIER? but tokenizer has SPILL keyword
        if self._match(TokenType.SPILL):
            # treat spill like a call expression with name 'spill'
            return self._parse_call_from_keyword('spill')

        raise ParseError(f"Unexpected token: {self._peek().token_type}")

    # --- Utility parsing helpers ---
    def _match(self, *types):
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, type_, message):
        if self._check(type_):
            return self._advance()
        raise ParseError(message + f" (found {self._peek().token_type})")

    def _check(self, type_):
        if self._is_at_end():
            return False
        return self._peek().token_type == type_

    def _advance(self):
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self):
        return self._peek().token_type == TokenType.EOF

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]

    def _lookahead_is_assign(self):
        # lookahead one token to see if assignment follows an identifier
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].token_type == TokenType.EQUAL

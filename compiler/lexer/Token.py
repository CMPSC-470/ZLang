from compiler.lexer.TokenType import TokenType


class Token:
    def __init__(self, type: TokenType, lexeme):
        self._type = type
        self._lexeme = lexeme

    def __repr__(self):
        return f"[{self._type} : {self._lexeme}]"

    # Getters, Setters, deleters

    # token type
    @property
    def token_type(self):
        return self._type

    @token_type.setter
    def token_type(self, value):
        self._type = value

    @token_type.deleter
    def token_type(self):
        del self._type


    #lexeme
    @property
    def lexeme(self):
        return self._lexeme

    @lexeme.setter
    def lexeme(self, value):
        self._lexeme = value

    @lexeme.deleter
    def lexeme(self):
        del self._lexeme









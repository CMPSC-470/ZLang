from compiler.lexer.TokenType import TokenType


class Token:
    def __init__(self, type: TokenType, lexeme):
        self.type = type
        self.lexeme = lexeme

    # Getters, Setters, deleters

    # token type
    @property
    def token_type(self):
        print(f"Token type: {self.type}")
        return self.type

    @token_type.setter
    def token_type(self, value):
        print(f"Token type is now: {self.type}")
        self.type = value

    @token_type.deleter
    def token_type(self):
        print(f"{self.type} was deleted")
        del self.type


    #lexeme
    @property
    def lexeme(self):
        print(f"Lexeme: {self.lexeme}")
        return self.lexeme

    @lexeme.setter
    def lexeme(self, value):
        print(f"Lexeme is now {self.lexeme}")
        self.lexeme = value

    @lexeme.deleter
    def lexeme(self):
        print(f"{self.lexeme} was deleted")
        del self.lexeme







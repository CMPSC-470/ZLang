from curses.ascii import isdigit

from compiler.lexer import Token
from compiler.lexer.TokenType import TokenType


class Tokenizer:
    def __inti__(self, source_code):
        self.source_code = source_code
        self.current_index = 0
        self.line_num = 1
        self.tokens = []


        #Keyword hashmap
        self.keywords = {
            #Main ZLang keywords
            "lit": TokenType.LIT,
            "say":TokenType.SAY,
            "vibe": TokenType.VIBE,
            "bet": TokenType.BET,
            "cap": TokenType.CAP,
            "nocap": TokenType.NOCAP,
            "spill": TokenType.SPILL,
            "Sqaud": TokenType.SQUAD,
            "fam": TokenType.FAM,
            "yes": TokenType.YES,
            "jawn": TokenType.JAWN,

            #conditonals
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "else if": TokenType.ELSE_IF,

            #operators
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "/": TokenType.SLASH,
            "=": TokenType.EQUAL,
            "==": TokenType.EQUAL_EQUAL,
            ">=":TokenType.GREATER_THAN_EQUAL,
            ">": TokenType.GREATER_THAN,
            "<": TokenType.LESS_THAN,
            "<=": TokenType.LESS_THAN_EQUAL,
            "!=": TokenType.NOT_EQUAL,

            #Delimitors
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            "{":TokenType.BRACE_LEFT,
            "}":TokenType.BRACE_RIGHT,
            ";":TokenType.SEMICOLON,
            ":":TokenType.COLON,
            ",":TokenType.COMMA,


            #End of file
            "End of File":TokenType.EOF

        }


    #Tokennize is the only public method here
    def tokenize(self):
        while not self.__is_at_end():
            self.__scan_tokens()

        #assing an end of file token if there are no more token to be made

        eof_token = Token(TokenType.EOF, "End of File")
        self.tokens.append(eof_token)
        return self.tokens

    def __scan_tokens(self):
        self.__skip_whitespace_and_comments()

        if self.__is_at_end():
            return

        current_char = self.__advance()

        #Handling for if chracter is a letter, digit, or beginning of a string

        if current_char.isalpha():
            self.current_index -= 1
            self.__read_identifier_or_keyword()
        elif current_char.isdigit():
            self.current_index  -= 1
            self.__read_number()
        elif current_char == '"':
            self.current_index -= 1
            self.__read_string()

        #hande special operands

        if current_char == '=' and self.__peek() == '=':
            self.tokens.append(Token(TokenType.EQUAL_EQUAL, "=="))
            self.__advance()
            return
        elif current_char == '!' and self.__peek() == '=':
            self.tokens.append(Token(TokenType.NOT_EQUAL, "!="))
            self.__advance()
            return
        elif current_char == '>' and self.__peek() == '=':
            self.tokens.append(Token(TokenType.GREATER_THAN_EQUAL, ">="))
            self.__advance()
            return
        elif current_char == '<' and self.__peek() == '=':
            self.tokens.append(Token(TokenType.LESS_THAN_EQUAL, "<="))
            self.__advance()
            return

        #append tokens for single operands and delimiters (long elif/ match)

        match current_char:
            case '+':
                token_type = TokenType.PLUS
                self.tokens.append(token_type)
            case '-':
                token_type = TokenType.MINUS
                self.tokens.append(token_type)
            case '-':
                token_type = TokenType.STAR
                self.tokens.append(token_type)
            case '/':
                token_type = TokenType.SLASH
                self.tokens.append(token_type)
            case '=':
                token_type = TokenType.EQUAL
                self.tokens.append(token_type)
            case '(':
                token_type = TokenType.LEFT_PAREN
                self.tokens.append(token_type)
            case ')':
                token_type = TokenType.RIGHT_PAREN
                self.tokens.append(token_type)
            case ',':
                token_type = TokenType.COMMA
                self.tokens.append(token_type)
            case ':':
                token_type = TokenType.COLON
                self.tokens.append(token_type)
            case ';':
                token_type = TokenType.SEMICOLON
                self.tokens.append(token_type)
            case '>':
                token_type = TokenType.GREATER_THAN
                self.tokens.append(token_type)
            case '<':
                token_type = TokenType.LESS_THAN
                self.tokens.append(token_type)





    def __read_identifier_or_keyword(self):
        word = ""

        while not self.__is_at_end() and (self.__peek().isalnum() or self.__peek() == '_'):
            word += self.__advance()

        token_type = self.keywords.get(word, TokenType.IDENTIFIER)

        self.tokens.append(token_type)

    def __read_string(self):
        current_character = self.source_code[self.current_index]
        at_end = self.__is_at_end()

        self.__advance()

        read_string = ""
        if self.__peek() == '\n':
            self.line_num += 1


        while not at_end:
            if self.__peek() == '"':
                while self.__peek_next() != '"':
                    read_string += current_character

        self.tokens.append(Token(TokenType.STRING, read_string))




    def __read_number(self):
        current_char = self.source_code[self.current_index]
        number = ""
        at_end = self.__is_at_end()

        if self.__peek() == '\n':
            self.line_num += 1

        while not at_end and  isdigit(self.__peek()):
            number + self.__advance()



        self.tokens.append(Token(TokenType.NUMBER, number))



    def __skip_whitespace_and_comments(self):
        is_at_end = self.__is_at_end()

        while not is_at_end:
            character = self.source_code[self.current_index]
            next_character = self.__peek_next()

            if character == ' ' or character == '\t' or character == '\n' or character == '\r':
                self.current_index += 1
            elif character == '/' and next_character == '/' :
                self.current_index += 1
            elif character == '\n':
                self.current_index += 1
                self.line_num += 1



# Base helpers
    def __peek(self):
        end = self.__is_at_end()
        if end:
            return '\0'
        return self.source_code[self.current_index]

    def __is_at_end(self):
        return self.current_index == len(self.source_code)


    def __peek_next(self):
        if self.current_index + 1 >= len(self.source_code):
            return '\0'
        return self.source_code[self.current_index + 1]

    def __advance(self):
        self.current_index += 1
        current_character = self.source_code[self.current_index]
        return current_character

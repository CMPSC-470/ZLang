from compiler.lexer.Token import Token
from compiler.lexer.TokenType import TokenType


class Tokenizer:
    def __init__(self, source_code):
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
            "squad": TokenType.SQUAD,
            "fam": TokenType.FAM,
            "yes": TokenType.YES,
            "yap": TokenType.YAP,
            "jawn": TokenType.JAWN,


            #conditonals
            "if": TokenType.IF,
            "else": TokenType.ELSE,





        }


    #Tokennize is the only public method here
    def tokenize(self):
        while not self.__is_at_end():
            self.__scan_tokens()

        #passing an end of file token if there are no more token to be made

        eof_token = Token(TokenType.EOF, "End of File")
        self.tokens.append(eof_token)
        return self.tokens

    def __scan_tokens(self):
        self.__skip_whitespace_and_comments()

        if self.__is_at_end():
            return

        current_char = self.__advance()

        #Handling for if character is a letter, digit, or beginning of a string

        if current_char.isalpha():

            self.__read_identifier_or_keyword()
            return
        elif current_char.isdigit():
            self.__read_number()
            return
        elif current_char == '"':
            self.__read_string()
            return

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
                self.tokens.append(Token(TokenType.PLUS, "+"))
            case '-':
                self.tokens.append(Token(TokenType.MINUS, "-"))
            case '*':
                self.tokens.append(Token(TokenType.STAR, "*"))
            case '/':
                self.tokens.append(Token(TokenType.SLASH, "/"))
            case '=':
                self.tokens.append(Token(TokenType.EQUAL, "="))
            case '(':
                self.tokens.append(Token(TokenType.LEFT_PAREN, "("))
            case ')':
                self.tokens.append(Token(TokenType.RIGHT_PAREN, ")"))
            case ',':
                self.tokens.append(Token(TokenType.COMMA, ","))
            case ':':
                self.tokens.append(Token(TokenType.COLON, ":"))
            case ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ";"))
            case '>':
                self.tokens.append(Token(TokenType.GREATER_THAN, ">"))
            case '<':
                self.tokens.append(Token(TokenType.LESS_THAN, "<"))





    def __read_identifier_or_keyword(self):
        word = self.source_code[self.current_index - 1]

        while not self.__is_at_end() and (self.__peek().isalnum() or self.__peek() == '_'):
            word += self.__advance()

        token_type = self.keywords.get(word.lower(), TokenType.IDENTIFIER)

        self.tokens.append(Token(token_type, word))


    def __read_string(self):


        #skip the opening quote and read each chrater and append it to 'found_string'
        found_string = ""


        while not self.__is_at_end() and self.__peek() != '"':

            #If at the end of a line, increment the line count
            if self.__peek() == '\n':
                self.line_num += 1

            found_string += self.__advance()

            if self.__is_at_end():
                print(f"Unterminated String at line {self.line_num}: {found_string}")


        #skip closing "
        if not self.__is_at_end():
         self.__advance()

        self.tokens.append(Token(TokenType.STRING, found_string))




    def __read_number(self):
        #Back track one chracter since we skip in 'scan_tokens'
        number = self.source_code[self.current_index - 1]

        if self.__peek() == '\n':
            self.line_num += 1

        #
        while not self.__is_at_end() and self.__peek().isdigit():
            number += self.__advance()


        self.tokens.append(Token(TokenType.NUMBER, number))



    def __skip_whitespace_and_comments(self):

        while not self.__is_at_end():
            character = self.__peek()
            next_character = self.__peek_next()

            #Skip all empty spaces and advance
            if character == ' ' or character == '\t' or character == '\r':
                self.__advance()
            elif character == '\n':
                self.__advance()
                self.line_num += 1

            #All lines with // will be skipped (comments)
            elif character == '/' and next_character == '/':
                while not self.__is_at_end() and self.__peek() != '\n':
                    self.__advance()

                    #also skips newline
                if not self.__is_at_end():
                    self.__advance()
                    self.line_num += 1
                continue
            else:
                break






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
        current_character = self.source_code[self.current_index]
        self.current_index += 1
        return current_character

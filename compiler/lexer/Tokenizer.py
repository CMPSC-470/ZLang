from compiler.lexer import Token


class Tokenizer:
    def __inti__(self, source_code):
        self.source_code = source_code
        self.current_index = 0
        self.line_num = 1
        self.tokens = []


    def tokenize(self):
        pass

    def __scan_tokens(self):
        pass

    def __read_identifier_or_keyword(self):
        pass

    def __read_string(self):
        pass

    def __read_number(self):
        pass

    def __skip_whitespace_and_comments(self):
        pass



    def __peek(self):
        pass

    def __is_at_end(self):
        pass


    def __peek_next(self):
        pass

    def __advance(self):
        pass


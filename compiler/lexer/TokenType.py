from enum import Enum,auto

class TokenType(Enum):
    # keywords
    LIT = auto()
    SAY = auto()
    VIBE = auto()
    BET = auto()
    CAP = auto()
    NOCAP = auto()
    SPILL = auto()
    SQUAD = auto()
    FAM = auto()
    YES = auto()
    JAWN = auto()

    # conditionals
    IF = auto()
    ELSE = auto()



    # literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    FUNCTION = auto()

    # operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    GREATER_THAN_EQUAL = auto()
    LESS_THAN_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    EQUAL_EQUAL = auto()

    #others
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    COMMENT = auto()


    # End of file
    EOF = auto()



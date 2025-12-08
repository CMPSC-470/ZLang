import sys

from compiler.lexer.Tokenizer import Tokenizer
from compiler.Parser.parser import Parser, ParseError
from compiler.semantics.analyzer import Interpreter


def run_source(source: str):
    tokens = Tokenizer(source).tokenize()
    parser = Parser(tokens)
    try:
        program = parser.parse()
    except ParseError as e:
        print("Parse error:", e)
        return
    interp = Interpreter()
    interp.interpret(program)


def run_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    run_source(source)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python main.py <source_file.zl>")
        return
    run_file(argv[0])


if __name__ == "__main__":
    main()

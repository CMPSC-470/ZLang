import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

def run_interpreter(file):
    try:
        from compiler.lexer.Tokenizer import Tokenizer
        from compiler.Parser.parser import Parser, ParseError
        from compiler.semantics.analyzer import Interpreter
    except Exception as e:
        print('Import error while loading compiler components', e)
        return


    file_path = os.path.join(root_path, "examples", file)

    print(f"Running interpreter test with file {file}")

    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tokens = Tokenizer(source).tokenize()
        program = Parser(tokens).parse()
        interpreter = Interpreter()
        interpreter.interpret(program)
    except ParseError as e:
        print("Parse Error", e)
    except Exception as e:
        print("Runtime Error", e)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: python interpretor_test.py <file>")
        sys.exit(1)

    run_interpreter(sys.argv[1])
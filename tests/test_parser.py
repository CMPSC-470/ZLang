import os
import sys

# Ensure repository root is on sys.path so `compiler` package can be imported
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)


def run_file(filename):
    # import inside function to capture and show import-time errors
    try:
        from compiler.lexer.Tokenizer import Tokenizer
        from compiler.Parser.parser import Parser, ParseError
    except Exception as e:
        print('Import error while loading parser or tokenizer:', type(e), e)
        return

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(root, "examples", filename)
    print(f"\n--- Testing {filename} ---")
    with open(file_path, "r") as f:
        src = f.read()

    tokens = Tokenizer(src).tokenize()
    print("TOKENS:")
    for t in tokens:
        print(t)

    try:
        ast = Parser(tokens).parse()
        print("\nAST:")
        print(ast)
    except ParseError as e:
        print("ParseError:", e)


if __name__ == '__main__':
    for fname in ["hello.zl", "counter.zl"]:
        run_file(fname)

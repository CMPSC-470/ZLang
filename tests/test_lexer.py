from compiler.lexer.Tokenizer import Tokenizer
import os



# Read the file path and make the tokens and print

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to example file
file_path = os.path.join(root_dir, "examples", "hello.zl")
with open(file_path, "r") as file:
    source_code = file.read()

tokenizer = Tokenizer(source_code)
tokens = tokenizer.tokenize()

print("===============Tokens===================")

for token in tokens:
    print(token)

print("========================================")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

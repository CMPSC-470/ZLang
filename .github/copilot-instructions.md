<!-- Copilot / AI agent instructions for the ZLang compiler project -->

# ZLang — Copilot Instructions

This project is a small, in-progress compiler for a teaching language called ZLang. The repository is minimal — the lexer/tokenizer is implemented, while the parser, AST, semantic analyzer, code generator, and `main` entrypoint are scaffolds. Use these notes to jump-start changes and avoid breaking package imports.

- **Python requirement:** The codebase uses `match` statements in the tokenizer, so target Python 3.10+.

- **Big picture:**
  - `compiler/lexer`: tokenization is implemented in `Tokenizer.py` (returns a list of `Token` objects and always appends an `EOF` token).
  - `compiler/Parser`: `parser.py` and `ast.py` are currently empty — the parser should consume tokens from the tokenizer and produce an AST (abstract syntax tree).
  - `compiler/semantics`: `analyzer.py` is the type/scope checker area — run after parsing, before codegen.
  - `compiler/codegen`: `generator.py` should take a validated AST and emit target code or runtime behaviors.
  - `examples/`: language examples. Use these for tests and expected behavior: `hello.zl`, `counter.zl`.

- **Key files to inspect/edit:**
  - `compiler/lexer/Tokenizer.py` — shows tokenization rules, keywords map, string/number handling, comment rules (`//`).
  - `compiler/lexer/Token.py` and `compiler/lexer/TokenType.py` — the Token API and enums used across the project.
  - `compiler/Parser/parser.py`, `compiler/Parser/ast.py` — implement parser + AST here; keep package name `Parser` (capitalized) to match imports.
  - `compiler/semantics/analyzer.py` — semantic checks and symbol table logic.
  - `compiler/codegen/generator.py` — code emission.
  - `main.py` — project entrypoint (currently empty).

- **Language surface (observable from tokenizer + examples):**
  - Keywords: `lit`, `say`, `vibe`, `bet`, `cap`, `nocap`, `spill`, `squad`, `fam`, `yes`, `yap`, `jawn`, `if`, `else`.
  - Function syntax example: `vibe main() { ... }` (braces are used for function bodies in examples).
  - Line comments: `//` — these are skipped by the tokenizer.
  - Strings: double-quoted `"..."` (tokenizer reports unterminated strings to stdout).
  - Numbers: contiguous digits form `NUMBER` tokens.
  - Operators/tokens supported: `+ - * / = == != > < >= <= ( ) , : ;` and braces are enumerated in `TokenType`.
  - Identifiers may include underscores and alphanumeric characters.

- **Conventions & patterns (project-specific):**
  - The `Tokenizer.tokenize()` method returns a Python list of `Token` objects and always appends an `EOF` token.
  - Keywords are looked up case-insensitively using `word.lower()`.
  - The project uses the package path `compiler.<component>`. Keep imports consistent with that structure.
  - Parser and AST nodes should be plain Python classes under `compiler/Parser/ast.py` and referenced by `parser.py`.

- **Quick-start commands (from repo root):**
  - Run the lexer demo/test script:

    `python tests\test_lexer.py`

  - Tokenize an example interactively:

    `python -c "from compiler.lexer.Tokenizer import Tokenizer; print(Tokenizer(open('examples/hello.zl').read()).tokenize())"`

  - Use Python 3.10+; if `match` raises a SyntaxError, upgrade the interpreter.

- **Testing and adding tests:**
  - Existing test scripts are simple scripts (not pytest fixtures). Add similar scripts under `tests/` that import components and print/assert behaviors.
  - Keep `examples/` as canonical language inputs for integration tests.

- **Extension points and expectations for AI agents:**
  - When implementing `parser.py`, follow the Token API: `Token.token_type` and `Token.lexeme` are the accessors.
  - Add AST node classes to `compiler/Parser/ast.py` and ensure `analyzer.py` traverses those nodes.
  - `generator.py` should accept the validated AST and return or print generated output.
  - Do not rename the `Parser` directory to lowercase — imports in tests and other modules expect the current name.

- **What to avoid:**
  - Do not change token names in `TokenType.py` without updating the tokenizer and any code that pattern-matches on those enums.
  - Avoid changing package import paths; keep `compiler.*` layout stable.

- If anything is unclear or you'd like me to expand any section (for example, draft a starter `parser.py`/`ast.py` skeleton or a simple analyzer), tell me which piece to implement next.

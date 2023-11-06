# Programming Languages Course

This repository contains the coursework for the Programming Languages course at National University of Colombia. The current bigger project is a translator developed using ANTLR4, which translates the Spanish programming language LPP to Python3.

## Manually Developed Parser
As part of the course, a parser was developed manually using Python3, you can find it in the `parser/` directory. It is designed to parse LPP (a Spanish programming language) and return Lexic or Syntax Errors if any.

### Lexic analizer main Features
- Tokenization strategy with regular expressions.
- Reserved words and symbols detection.
- Error detection for invalid characters.
- Left-most longest match strategy.
- Comments skipper.

### Syntax analizer main Features
- LL(1) LPP grammar.
- Dynamic parser code generation from the grammar structure.
- LL(1) checks for the grammar, including:
    - First and Follow sets.
    - Left Recursion.
    - Unique prediction groups.

get more information about the parser [here](./parser/README.md).

## ANTLR Semantic analyzer with Python3 translator

The ANTLR translator is located in the `semantic/` directory. It is designed to translate LPP (a Spanish programming language) into Python3.

The input for ANTLR4 is the grammar [LPP.g4](./semantic/LPP.g4) that comes from a derivation from one LL(1) grammar of previous work. You can access that work [here](./parser/grammar.txt).

### Changes to the Grammar
- Converted the grammar to LL(*) as ANTLR4 does support it and its easier to work with.
- Added the logic to manage default LPP functions, new from documentation.
- Added the logic to manage files, not possible in the previous work.
- Added the logic to manage cases, missing in the previous work.

get more information about the translator [here](./semantic/README.md).
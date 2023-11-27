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

## Plagiarism Detection Project

Applying all the knowledge acquired in the course, a plagiarism detection project was developed. It is located in the directories starting with `plagium_`. The project is divided in three parts:

- [plagium_core](./plagium_core/README.md): The core of the project, it contains the logic to detect plagiarism using concurrency.
- [plagium_web](./plagium_web/README.md): A web interface to interact with the core.
- [plagium_cli](./plagium_cli/README.md): A command line interface to interact with the core.

### Architecture

The main project architecture is based on the clean architecture, allowing the core to be completely modular and independent from the web and cli interfaces. It used a REST API to communicate with the UIs, receiving the files to analyze and returning the results.

### Deployment

The project can be deployed independently, and for that purpose we recommend clicking the link above in the README of each part of the project. However, if you want to deploy the whole project at once, you can use the [docker-compose.yml](./docker-compose.yml) file to deploy the whole project at once, for this execute the following command having docker and docker-compose properly installed:

```bash
docker-compose up -d
```
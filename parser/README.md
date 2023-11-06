# LPP Parser

This directory contains a manually developed parser for the LPP language, a Spanish programming language. The parser is developed using Python3 and is designed to return Lexic or Syntax Errors if any.

## Requirements
- Python3.8 or higher.


## Usage
 I recommend using a virtual environment to run the parser, you can get more info on how to do that [here](https://docs.python.org/3/library/venv.html). Once you have your virtual environment activated, you can install the requirements with the following command:

```bash
pip3 install -r requirements.txt
```



## Lexic Analyzer

The lexic analyzer is contained inside the [lexic_analizer.py](./src/lexic_analizer.py) file. It has the job of reading the whole code input and tokenize it in concordance with the LPP language rules. It has the main job of synchronizing the tokinization with the syntax analyzer and return the next token when requested.

It uses regular expressions to analyze the code and detect the lexemes that correspond to the LPP language rules. It also has the job of detecting reserved words and symbols, as well as invalid characters and comments.

The possible token types are:

| Token Type | Description |
| ---------- | ----------- |
| `tkn_id` | Identifier |
| `tkn_assign` | Assignment operator |
| `tkn_period` | Period lexeme |
| `tkn_comma` | Comma lexeme |
| `tkn_colon` | Colon lexeme |
| `tkn_plus` | Plus lexeme |
| `tkn_minus` | Minus lexeme |
| `tkn_times` | Asterisk lexeme |
| `tkn_div` | Slash lexeme |
| `tkn_power` | Power lexeme |
| `tkn_equal` | Equal lexeme |
| `tkn_neq` | <> lexeme |
| `tkn_less` | Less than lexeme |
| `tkn_leq` | Less than or equal to lexeme |
| `tkn_greater` | Greater than lexeme |
| `tkn_geq` | Greater than or equal to lexeme |
| `tkn_opening_par` | Opening parenthesis lexeme |
| `tkn_closing_par` | Closing parenthesis lexeme |
| `tkn_opening_bra` | Opening bracket lexeme |
| `tkn_closing_bra` | Closing bracket lexeme |
| `tkn_integer` | Integer number lexeme |
| `tkn_real` | Real number lexeme |
| `tkn_str` | String lexeme |
| `tkn_char` | Character lexeme |
| `<reserved_word> ` | Reserved word lexeme |

For the reserved words, they are many that the LPP language has, so you just have to know that the token type and lexeme in the token are the same. For example for the reserverd word `si`:
- Token<si,si,row,column>

Other than that, the type always starts with `tkn_` and the lexeme is the corresponding lexeme

## Syntax Analyzer

The syntax analyzer is contained inside the [syntax_analizer.py](./src/syntax_analizer.py) file. It has the job of reading sequentially the tokens from the lexic analyzer and check if they are in concordance with the LPP language rules. It has the job of detecting syntax errors and return them if any or a success message if none, no semantic analysis planned as it will be done in ANTLR4 later.

It uses a dynamic parser code generation from the grammar structure, which is a LL(1) LPP grammar. It also has the job of checking the grammar for LL(1) errors, including:
- First and Follow sets.
- Left Recursion.
- Unique prediction groups.

### Compilation of a LL(1) grammar

The dynamic parser code generation is done by reading the grammar structure and generating the prediction groups for each rule. Then using a [template](./src/assets/template.py) it converts the rules into code with the predictions, the code is then saved in [generated_compiler](./generated_compiler.py), and can be used calling the [main](./main.py) file in this directory root.

you can use some flags to change the behavior of the parser, they are:

| Flag | Description |
| ---- | ----------- |
| --file <file> | The file path to analyze. |
| --multitest | Analize multiple codes in the same file, splited by <<nueva_linea>>. |
| --verbose | Print the grammar and the prediction groups and other information. |

so you can run the parser with the following command:

```bash
python3 main.py --file <file> --multitest --verbose
```

and the file can be formatted like this:


```txt
<code1>
<<nueva_linea>>
<code2>
<<nueva_linea>>
<code3>
```

and the output will generate three different outputs, one for each code.
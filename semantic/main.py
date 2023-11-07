import argparse
import os
import sys

from antlr4 import *
from LPP.LPPLexer import LPPLexer
from LPP.LPPParser import LPPParser
from PythonListener import PythonListener

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Traductor de un lenguaje LPP a Python"
    )

    parser.add_argument(
        "--file", metavar="file", type=str, help="Ruta del archivo de entrada"
    )

    args = parser.parse_args()

    if not args.file:
        input_stream = InputStream(sys.stdin.read())
    
    else:
        if not os.path.isfile(args.file):
            raise Exception("El archivo no existe")

        input_stream = FileStream(args.file, encoding="utf-8")
    
    lexer = LPPLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = LPPParser(token_stream)
    tree = parser.program()

    listener = PythonListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    final_code = listener.getPythonCode()

    print(final_code)
    

if __name__ == "__main__":
    main()
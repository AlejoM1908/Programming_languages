import argparse
import os

from src.lpp_compiler import LPPCompiler
from src.lexic_analizer import LexicAnalizer
from generated_compiler import SyntaxAnalizer

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analizador léxico para un lenguaje de programación LPP"
    )
    parser.add_argument(
        "--file", metavar="file", type=str, help="Ruta del archivo de entrada"
    )
    parser.add_argument(
        "--multitest", default= False, action='store_true', help="Bandera para ejecutar un archivo de prueba con varios casos"
    )
    parser.add_argument(
        "--verbose", default= False, action='store_true', help="Bandera para mostrar los grupos de predicciones"
    )
    args = parser.parse_args()

    env = {"GRAMMAR_PATH": "./grammar.txt"}

    if not args.file:
        text = []
        while True:
            try:
                line = input()
                text.append(line)
            except EOFError:
                break

        text = [text]
    else:
        if not os.path.isfile(args.file):
            raise Exception("El archivo no existe")

        with open(args.file, "r") as file:
            text = file.readlines()

        if args.multitest:
            counter = 0
            tests = [[]]

            for line in text:
                if line == "<<nueva_linea>>\n":
                    counter += 1
                    tests.append([])
                    continue

                tests[counter].append(line)

            text = tests
        else:
            text = [text] 

    compiler = LPPCompiler(env["GRAMMAR_PATH"])

    if args.verbose:
        compiler.test()
    else:
        compiler.compile()

    for test in text:
        
        compiler = SyntaxAnalizer(LexicAnalizer(test))

        try:
            compiler.compile()
        except Exception as e:
            print(e.args[0])


if __name__ == "__main__":
    main()

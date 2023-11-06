from src.syntax_analizer import SyntaxAnalizer

class LPPCompiler:
    def __init__(self, grammar:str) -> None:

        try:
            self.syntax_analizer = SyntaxAnalizer(grammar)
        except ValueError as error:
            print(error.args[0])
            exit()

    def compile(self) -> None:
        try:
            self.syntax_analizer.generateAnalizer()
        except ValueError as error:
            print(error.args[0])
            exit()

    def test(self) -> None:

        try:
            self.syntax_analizer.test()
        except ValueError as error:
            print(error.args[0])
            exit()
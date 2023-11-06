from src.lexic_analizer import LexicAnalizer, Token

class LexicError(Exception):
    """
    Exception raised for errors in the provided grammar.
    """
    def __init__(self, message:str) -> None:
        super().__init__(message)

class SyntaxError(Exception):
    """
    Exception raised for errors in the provided grammar.
    """
    def __init__(self, message:str) -> None:
        super().__init__(message)

class GrammarError(Exception):
    """
    Exception raised for errors in the provided grammar.
    """
    def __init__(self, message:str) -> None:
        super().__init__(message)

class SyntaxAnalizer:
    def __init__(self, lexicAnalizer:LexicAnalizer) -> None:
        self.lexic_analizer = lexicAnalizer
        self.token = self.lexic_analizer.next()

    def _raiseError(self, expected:set[str]) -> None:
        self.token.lexeme = self.token.lexeme.replace('$', 'final de archivo').replace('"', '').replace("'", '')

        if '$' in expected:
            expected.remove('$')
            expected.add('final de archivo')

        expected = sorted(expected.copy())

        expected = [f'"{e}"' for e in expected]
        
        raise SyntaxError(f'<{self.token.row + 1}:{self.token.column + 1}> Error sintactico: se encontro: "{self.token.lexeme}"; se esperaba: {", ".join([f"{e}" for e in expected])}.')

    def _match(self, expected:set[str]) -> None:
        if self.token.token_type in expected:
            self.token = self.lexic_analizer.next()
        else:
            self._raiseError(expected)
        
$$FUNCTIONS$$
$$MAIN$$
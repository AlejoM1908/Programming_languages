from antlr4 import *
from ..parser.Python3Lexer import Python3Lexer
from ..parser.Python3Parser import Python3Parser

def parseCode(code: str) -> dict:
    """
    Parse a code string and return a dictionary with the information

    Parameters
        code (str): Code string

    Returns
        dict: Dictionary with the information of the code
    """
    # Create the lexer and parser
    lexer = Python3Lexer(InputStream(code))
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)

    # Get the tree
    tree = parser.file_input()

    return tree
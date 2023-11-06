from dataclasses import dataclass
import string
import re

class LexicError(Exception):
    """
    Exception raised for errors in the provided grammar.
    """
    def __init__(self, message:str) -> None:
        super().__init__(message)

class Reserved:
    """
    Used to check if a lexeme is a reserved word or not in the LPP language
    """
    values: dict[str, set[str]] = {
        "word": {"para", "hasta", "haga", "escriba", "lea", "entero", "o", "real", "y", "mientras", "repita", "entonces", "inicio", "fin", "si", "no", "verdadero", "falso", "caso", "sino", "llamar", "nueva_linea", "funcion", "retorne", "var", "caracter", "cadena", "procedimiento", "booleano", "cadena", "div", "mod", "funcion", "registro", "de", "arreglo"},
        "tkn_assign": {"<-"},
        "tkn_period": {"."},
        "tkn_comma": {","},
        "tkn_colon": {":"},
        "tkn_plus": {"+"},
        "tkn_minus": {"-"},
        "tkn_times": {"*"},
        "tkn_div": {"/"},
        "tkn_power": {"^"},
        "tkn_equal": {"="},
        "tkn_neq": {"<>"},
        "tkn_less": {"<"},
        "tkn_leq": {"<="},
        "tkn_greater": {">"},
        "tkn_geq": {">="},
        "tkn_opening_par": {"("},
        "tkn_closing_par": {")"},
        "tkn_opening_bra": {"["},
        "tkn_closing_bra": {"]"},
    }

    def __contains__(self, value: str) -> bool:
        for category in self.values:
            if value in self.values[category]:
                return True

        return False
    
    def __getitem__(self, value: str) -> str:
        for category in self.values:
            if value in self.values[category]:
                return category

        return None

@dataclass
class Token:
    """
    Maps a token structure and other metadata and allows to print in a specific format

    Attributes:
        lexeme {str} -- The lexeme of the token
        token_type {str} -- The type of the token
        row {int} -- The row where the token was found
        column {int} -- The column where the token was found
    """
    lexeme: str
    token_type: str
    row: int
    column: int

    def __str__(self) -> str:
        if  self.token_type.startswith("tkn_"):
            words:list[str] = ['str', 'char', 'integer', 'real'] 

            if self.token_type[4:] not in words: 
                return f"<{self.token_type},{self.row + 1},{self.column + 1}>"
            elif self.lexeme.startswith('"') or self.lexeme.startswith("'"):
                return f"<{self.token_type},{self.lexeme[1:-1]},{self.row + 1},{self.column + 1}>"
        
        elif self.token_type == 'word':
            return f"<{self.lexeme},{self.row + 1},{self.column + 1}>"
        
        
        return f"<{self.token_type},{self.lexeme},{self.row + 1},{self.column + 1}>"


class LexicAnalizer:
    """
    Recieves an LPP code input and returns a list of tokens representing the available lexemes and structures of the language

    Attributes:
        input {list[str]} -- The input code
        position {list[int]} -- The current position of the tokenizer in the input
        reserved {Reserved} -- The reserved words and symbols of the LPP language
        patterns {dict[str, str]} -- The regex patterns to match the lexemes of the LPP language

    Methods:
        next() -> Token -- Returns the next token in the input
        getAll() -> list[Token] -- Returns all the tokens available in the input
    """
    def __init__(self, input:list[str]) -> None:
        self.patterns:dict[str, str] = {
            "str": r'"(?:\\.|[^"\\])*"',
            "char": r"'(?:\\.|[^'\\])'",
            "wrong_str": r'"(?:\\.|[^"\\])*',
            "wrong_char": r"'(?:\\.|[^'\\])",
            "real": r'\d+\.\d+',
            "id": r'[a-zA-Z_]\w*',
            "integer": r'\d+',
            "punct": r'[^\w\s"\'][^\w\s"\']|[^\w\s"\']'
        }

        self.position:list[int] = [0,0]
        self.reserved:Reserved = Reserved()
        self.input:list[str] = self._cleanInput(input)

    def _getRegexCompile(self, *args:str) -> re.Pattern:
        """
        Returns a compiled regex object from the given patterns
        """
        return re.compile(f'({"|".join(args)})')

    def _cleanInput(self, input: list[str]) -> list[str]:
        """
        From the LLP code input, removes all the comments, trailing spaces and tabs
        
        Positional arguments:
            input {list[str]} -- The input code

        return {list[str]} -- The cleaned input code
        """
        if not input:
            return []
        
        # Avoid removing comments inside strings (double quotes)
        cleaned = [re.sub(r'".*"', lambda match: match.group(0).replace("/", "<<SLASH>>").replace("/*", "<<MULTIIN>>").replace("*/", "<<MULTIOUT>>"), line) for line in input] 

        cleaned = [re.sub(r"\s*//.*|/\*.*\*/", lambda match: " " * len(match.group()), line.rstrip()) for line in cleaned] # Remove single line comments
        cleaned = [re.sub(r"(^|\s)\t+", lambda match: " " * (4 * len(match.group())), line) for line in cleaned] # Replace tabs with 4 spaces
        
        # Remove multiline comments
        multiline:bool = False
        for index, line in enumerate(cleaned):
            if '*/' in line and multiline:
                multiline = False
                line = re.sub(r".*\*/", "", line)

            if multiline:
                line = re.sub(r".*", "", line)

            if '/*' in line:
                multiline = True
                line = re.sub(r"/\*.*", "", line)

            cleaned[index] = line

        # Replace the placeholders with the original characters
        cleaned = [re.sub(r'".*"', lambda match: match.group(0).replace("<<SLASH>>", "/").replace("<<MULTIIN>>", "/*").replace("<<MULTIOUT>>", "*/"), line) for line in cleaned]

        return cleaned
    
    def _createToken(self, lexeme:str, token_type:str) -> Token:
        """
        Creates a token object from the given lexeme and token type or raises an exception if the lexeme or token type are empty

        Positional arguments:
            lexeme {str} -- The lexeme of the token
            token_type {str} -- The type of the token

        Returns:
            Token -- The token object created

        Raises:

        """
        if not token_type or not lexeme:
            raise LexicError(f"Error lexico (linea: {self.position[0] + 1}, posicion: {self.position[1] + 1})")

        token = Token(lexeme, token_type, self.position[0], self.position[1])
        self.position[1] += len(lexeme)

        return token
    
    def _moveToNextToken(self) -> None:
        # Move all the spaces to the next token or all the newlines to the next character
        for char in self.input[self.position[0]][self.position[1]:]:
            if char == " ":
                self.position[1] += 1
            else:
                return
        
        self.position[0] += 1
        self.position[1] = 0

        if self.position[0] < len(self.input):
            self._moveToNextToken()

    def next(self) -> Token:
        if self.position[0] >= len(self.input):
            return self._createToken("$", "$")
        
        # Compile the pattern into a regular expression object
        regex = self._getRegexCompile(*self.patterns.values())

        # Move the position to the next token
        self._moveToNextToken()

        # Loop over the matches in the input starting from the current position
        for match in regex.finditer(self.input[self.position[0]][self.position[1]:]):
            lexeme = match.group(0)

            # Check if the lexeme is a string
            if lexeme.startswith('"'):
                if lexeme.endswith('"'):
                    output = self._createToken(lexeme, "tkn_str")
                    break
                else:
                    self._createToken("", "")
                    break

            # Check if the lexeme is a character
            elif lexeme.startswith("'"):
                if lexeme.endswith("'"):
                    output = self._createToken(lexeme, "tkn_char")
                    break
                else:
                    self._createToken("", "")
                    break

            # Check if the lexeme has non-ascii characters
            elif len([char for char in lexeme if char not in string.printable]) > 0:
                self._createToken("", "")

            # Check if the lexeme is an identifier or reserved word
            elif lexeme[0].lower() in string.ascii_letters or lexeme[0] == "_":
                if lexeme.lower() in self.reserved:
                    output = self._createToken(lexeme.lower(), self.reserved[lexeme.lower()])
                    if output.token_type == "word":
                        output.token_type = output.lexeme
                    break
                else:
                    output = self._createToken(lexeme.lower(), "id")
                    break

            # Check if the lexeme is a number
            elif lexeme[0] in string.digits:
                if len([char for char in lexeme if char not in string.digits + "."]) > 0:
                    self._createToken("", "")

                token_type = "tkn_integer" if "." not in lexeme else "tkn_real"
                output = self._createToken(lexeme, token_type)
                break

            # Check if the lexeme is a punctuation symbol or operator
            elif lexeme[0] in string.punctuation:
                if lexeme in self.reserved:
                    output = self._createToken(lexeme, self.reserved[lexeme])
                    break
                elif len(lexeme) == 2 and lexeme[0] in self.reserved:
                    output = self._createToken(lexeme[0], self.reserved[lexeme[0]])
                    break
                
                self._createToken("", "")
            else:
                self._createToken("", "")

        if 'output' not in locals() or not output:
            self._createToken("", "")

        # The reading finished, so move the position to the next character
        self._moveToNextToken()
        return output
    
    def getAll(self) -> list[Token]:
        output: list[Token] = []
        try:
            token = self.next()

            while token.token_type != "$":
                    print(token)
                    output.append(token)
                    token = self.next()
        except LexicError as e:
            print(f">>> {str(e)}")

        return output
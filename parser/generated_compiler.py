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

        expected = sorted(expected.copy())

        expected = [f'"{e}"' for e in expected]
        
        raise SyntaxError(f'<{self.token.row + 1}:{self.token.column + 1}> Error sintactico: se encontro: "{self.token.lexeme}"; se esperaba: {", ".join([f"{e}" for e in expected])}.')

    def _match(self, expected:set[str]) -> None:
        if self.token.token_type in expected:
            self.token = self.lexic_analizer.next()
        else:
            self._raiseError(expected)
        
    def Programa(self) -> None:
        if self.token.token_type in {'id', 'real', 'registro', 'inicio', 'arreglo', '$', 'procedimiento', 'caracter', 'booleano', 'entero', 'funcion', 'cadena'}:
            self.Declaraciones()
            self.Bloque()
            return
        else:
            self._raiseError({'id', 'caracter', 'real', 'booleano', 'entero', 'cadena', 'registro', 'arreglo', '$', 'procedimiento', 'funcion', 'inicio'})

    def ProgramaSinRetorno(self) -> None:
        if self.token.token_type in {'id', 'real', 'registro', 'inicio', 'arreglo', 'procedimiento', 'caracter', 'booleano', 'entero', 'funcion', 'cadena'}:
            self.Declaraciones()
            self.BloqueSinRetorno()
            return
        else:
            self._raiseError({'id', 'caracter', 'real', 'booleano', 'entero', 'cadena', 'registro', 'arreglo', 'procedimiento', 'funcion', 'inicio'})

    def Declaraciones(self) -> None:
        if self.token.token_type in {'caracter', 'id', 'real', 'booleano', 'entero', 'registro', 'inicio', 'arreglo', 'procedimiento', 'funcion', 'cadena'}:
            self.DeclaracionesPrima()
            return
        else:
            self._raiseError({'caracter', 'id', 'real', 'booleano', 'entero', 'registro', 'inicio', 'arreglo', 'procedimiento', 'funcion', 'cadena'})

    def DeclaracionesPrima(self) -> None:
        if self.token.token_type in {'caracter', 'real', 'booleano', 'entero', 'arreglo', 'cadena'}:
            self.DeclaracionesTipos()
            self.DeclaracionesPrima()
            return
        if self.token.token_type in {'procedimiento', 'funcion', 'registro'}:
            self.DeclaracionesEstructuras()
            self.DeclaracionesPrima()
            return
        if self.token.token_type in {'id'}:
            self.Identificador()
            self.DeclaracionesPrima()
            return
        if self.token.token_type in {'inicio'}:
            return
        else:
            self._raiseError({'caracter', 'id', 'real', 'booleano', 'entero', 'registro', 'inicio', 'arreglo', 'procedimiento', 'funcion', 'cadena'})

    def DeclaracionesTipos(self) -> None:
        if self.token.token_type in {'caracter', 'real', 'booleano', 'entero'}:
            self.TipoNoIterable()
            self.ListaIdentificadores()
            return
        if self.token.token_type in {'arreglo', 'cadena'}:
            self.TipoIterable()
            self.ListaIdentificadores()
            return
        else:
            self._raiseError({'caracter', 'real', 'booleano', 'entero', 'arreglo', 'cadena'})

    def DeclaracionesEstructuras(self) -> None:
        if self.token.token_type in {'funcion'}:
            self.Funcion()
            return
        if self.token.token_type in {'procedimiento'}:
            self.Procedimiento()
            return
        if self.token.token_type in {'registro'}:
            self.Registro()
            return
        else:
            self._raiseError({'procedimiento', 'funcion', 'registro'})

    def ListaIdentificadores(self) -> None:
        if self.token.token_type in {'id'}:
            self.Identificador()
            self.ListaIdentificadoresPrima()
            return
        else:
            self._raiseError({'id'})

    def ListaIdentificadoresPrima(self) -> None:
        if self.token.token_type in {'tkn_comma'}:
            self._match({'tkn_comma'})
            self.Identificador()
            self.ListaIdentificadoresPrima()
            return
        if self.token.token_type in {'id', 'caracter', 'real', 'booleano', 'entero', 'registro', 'inicio', 'arreglo', 'procedimiento', 'fin', 'funcion', 'cadena'}:
            return
        else:
            self._raiseError({'id', 'caracter', 'real', 'booleano', 'entero', 'cadena', 'registro', 'arreglo', 'procedimiento', 'fin', 'funcion', 'tkn_comma', 'inicio'})

    def Dimensiones(self) -> None:
        if self.token.token_type in {'tkn_integer'}:
            self._match({'tkn_integer'})
            self.DimensionesPrima()
            return
        else:
            self._raiseError({'tkn_integer'})

    def DimensionesPrima(self) -> None:
        if self.token.token_type in {'tkn_comma'}:
            self._match({'tkn_comma'})
            self._match({'tkn_integer'})
            self.DimensionesPrima()
            return
        if self.token.token_type in {'tkn_closing_bra'}:
            return
        else:
            self._raiseError({'tkn_comma', 'tkn_closing_bra'})

    def Bloque(self) -> None:
        if self.token.token_type in {'inicio'}:
            self._match({'inicio'})
            self.ListaSentencias()
            self._match({'fin'})
            return
        else:
            self._raiseError({'inicio'})

    def BloqueSinRetorno(self) -> None:
        if self.token.token_type in {'inicio'}:
            self._match({'inicio'})
            self.ListaSentenciasSinRetorno()
            self._match({'fin'})
            return
        else:
            self._raiseError({'inicio'})

    def ListaSentencias(self) -> None:
        if self.token.token_type in {'si', 'mientras', 'id', 'escriba', 'para', 'caso', 'llamar', 'retorne', 'lea', 'repita'}:
            self.Sentencia()
            self.ListaSentencias()
            return
        if self.token.token_type in {'fin', 'sino', 'hasta'}:
            return
        else:
            self._raiseError({'si', 'mientras', 'id', 'sino', 'escriba', 'fin', 'para', 'caso', 'hasta', 'llamar', 'retorne', 'lea', 'repita'})

    def ListaSentenciasSinRetorno(self) -> None:
        if self.token.token_type in {'si', 'mientras', 'id', 'escriba', 'para', 'caso', 'llamar', 'lea', 'repita'}:
            self.SentenciaSinRetorno()
            self.ListaSentenciasSinRetorno()
            return
        if self.token.token_type in {'fin'}:
            return
        else:
            self._raiseError({'si', 'mientras', 'id', 'escriba', 'fin', 'para', 'caso', 'llamar', 'lea', 'repita'})

    def Sentencia(self) -> None:
        if self.token.token_type in {'id'}:
            self.Asignacion()
            return
        if self.token.token_type in {'llamar'}:
            self.Ejecucion()
            return
        if self.token.token_type in {'lea'}:
            self.Lectura()
            return
        if self.token.token_type in {'escriba'}:
            self.Escritura()
            return
        if self.token.token_type in {'retorne'}:
            self.Retornar()
            return
        if self.token.token_type in {'mientras', 'para', 'repita'}:
            self.Ciclo()
            return
        if self.token.token_type in {'si'}:
            self.Condicional()
            return
        if self.token.token_type in {'caso'}:
            self.Casos()
            return
        else:
            self._raiseError({'si', 'mientras', 'id', 'escriba', 'para', 'caso', 'llamar', 'retorne', 'lea', 'repita'})

    def SentenciaSinRetorno(self) -> None:
        if self.token.token_type in {'id'}:
            self.Asignacion()
            return
        if self.token.token_type in {'llamar'}:
            self.Ejecucion()
            return
        if self.token.token_type in {'lea'}:
            self.Lectura()
            return
        if self.token.token_type in {'escriba'}:
            self.Escritura()
            return
        if self.token.token_type in {'mientras', 'para', 'repita'}:
            self.Ciclo()
            return
        if self.token.token_type in {'si'}:
            self.Condicional()
            return
        if self.token.token_type in {'caso'}:
            self.Casos()
            return
        else:
            self._raiseError({'si', 'mientras', 'id', 'escriba', 'para', 'caso', 'llamar', 'lea', 'repita'})

    def Asignacion(self) -> None:
        if self.token.token_type in {'id'}:
            self.Identificador()
            self.AsignacionPrima()
            return
        else:
            self._raiseError({'id'})

    def AsignacionPrima(self) -> None:
        if self.token.token_type in {'tkn_assign'}:
            self._match({'tkn_assign'})
            self.Expresion()
            return
        if self.token.token_type in {'tkn_period'}:
            self._match({'tkn_period'})
            self.Identificador()
            self._match({'tkn_assign'})
            self.Expresion()
            return
        if self.token.token_type in {'tkn_opening_bra'}:
            self._match({'tkn_opening_bra'})
            self.Expresion()
            self._match({'tkn_closing_bra'})
            self._match({'tkn_assign'})
            self.Expresion()
            return
        else:
            self._raiseError({'tkn_assign', 'tkn_opening_bra', 'tkn_period'})

    def Ejecucion(self) -> None:
        if self.token.token_type in {'llamar'}:
            self._match({'llamar'})
            self.EjecucionPrima()
            return
        else:
            self._raiseError({'llamar'})

    def EjecucionPrima(self) -> None:
        if self.token.token_type in {'id'}:
            self.Identificador()
            self.ParametrosEjecucion()
            return
        if self.token.token_type in {'nueva_linea'}:
            self._match({'nueva_linea'})
            return
        else:
            self._raiseError({'id', 'nueva_linea'})

    def Lectura(self) -> None:
        if self.token.token_type in {'lea'}:
            self._match({'lea'})
            self.Identificador()
            self.LecturaPrima()
            return
        else:
            self._raiseError({'lea'})

    def LecturaPrima(self) -> None:
        if self.token.token_type in {'tkn_period'}:
            self._match({'tkn_period'})
            self.Identificador()
            self.LecturaPrima()
            return
        if self.token.token_type in {'tkn_comma'}:
            self._match({'tkn_comma'})
            self.Identificador()
            self.LecturaPrima()
            return
        if self.token.token_type in {'tkn_opening_bra'}:
            self._match({'tkn_opening_bra'})
            self.Expresion()
            self._match({'tkn_closing_bra'})
            self._match({'tkn_period'})
            self.Identificador()
            return
        if self.token.token_type in {'si', 'mientras', 'id', 'sino', 'escriba', 'fin', 'para', 'repita', 'hasta', 'llamar', 'retorne', 'lea', 'caso'}:
            return
        else:
            self._raiseError({'si', 'id', 'sino', 'para', 'llamar', 'tkn_comma', 'lea', 'caso', 'mientras', 'escriba', 'tkn_opening_bra', 'tkn_period', 'fin', 'retorne', 'hasta', 'repita'})

    def Escritura(self) -> None:
        if self.token.token_type in {'escriba'}:
            self._match({'escriba'})
            self.TipoEscritura()
            self.EscrituraPrima()
            return
        else:
            self._raiseError({'escriba'})

    def EscrituraPrima(self) -> None:
        if self.token.token_type in {'tkn_comma'}:
            self._match({'tkn_comma'})
            self.TipoEscritura()
            self.EscrituraPrima()
            return
        if self.token.token_type in {'si', 'mientras', 'id', 'sino', 'escriba', 'fin', 'para', 'repita', 'hasta', 'llamar', 'retorne', 'lea', 'caso'}:
            return
        else:
            self._raiseError({'si', 'mientras', 'id', 'sino', 'escriba', 'llamar', 'para', 'caso', 'lea', 'hasta', 'fin', 'retorne', 'tkn_comma', 'repita'})

    def TipoEscritura(self) -> None:
        if self.token.token_type in {'verdadero', 'id', 'tkn_str', 'falso', 'no', 'tkn_opening_par', 'tkn_minus', 'tkn_integer', 'tkn_real', 'tkn_char'}:
            self.Expresion()
            self.ParametrosEjecucion()
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_str', 'falso', 'no', 'tkn_opening_par', 'tkn_minus', 'tkn_integer', 'tkn_real', 'tkn_char'})

    def Funcion(self) -> None:
        if self.token.token_type in {'funcion'}:
            self._match({'funcion'})
            self.Identificador()
            self.Parametros()
            self._match({'tkn_colon'})
            self.TipoCompleto()
            self.Programa()
            return
        else:
            self._raiseError({'funcion'})

    def Parametros(self) -> None:
        if self.token.token_type in {'tkn_opening_par'}:
            self._match({'tkn_opening_par'})
            self.TipoCompleto()
            self.Identificador()
            self.ParametrosPrima()
            self._match({'tkn_closing_par'})
            return
        if self.token.token_type in {'caracter', 'id', 'real', 'booleano', 'entero', 'cadena', 'registro', 'tkn_colon', 'arreglo', 'procedimiento', 'funcion', 'inicio'}:
            return
        else:
            self._raiseError({'caracter', 'id', 'real', 'booleano', 'entero', 'registro', 'tkn_opening_par', 'tkn_colon', 'inicio', 'arreglo', 'procedimiento', 'funcion', 'cadena'})

    def ParametrosPrima(self) -> None:
        if self.token.token_type in {'tkn_comma'}:
            self._match({'tkn_comma'})
            self.TipoCompleto()
            self.Identificador()
            self.ParametrosPrima()
            return
        if self.token.token_type in {'tkn_closing_par'}:
            return
        else:
            self._raiseError({'tkn_closing_par', 'tkn_comma'})

    def ParametrosEjecucion(self) -> None:
        if self.token.token_type in {'tkn_opening_par'}:
            self._match({'tkn_opening_par'})
            self.ParametrosEjecucionPrima()
            self._match({'tkn_closing_par'})
            return
        if self.token.token_type in {'si', 'mientras', 'id', 'sino', 'escriba', 'fin', 'para', 'tkn_comma', 'repita', 'hasta', 'llamar', 'retorne', 'lea', 'caso'}:
            return
        else:
            self._raiseError({'si', 'mientras', 'id', 'sino', 'escriba', 'llamar', 'para', 'caso', 'tkn_opening_par', 'lea', 'hasta', 'fin', 'retorne', 'tkn_comma', 'repita'})

    def ParametrosEjecucionPrima(self) -> None:
        if self.token.token_type in {'verdadero', 'id', 'tkn_real', 'tkn_char', 'tkn_str', 'falso', 'tkn_integer'}:
            self.TipoDato()
            self.ParametrosEjecucionDoblePrima()
            return
        if self.token.token_type in {'tkn_closing_par'}:
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_real', 'tkn_char', 'tkn_str', 'tkn_closing_par', 'falso', 'tkn_integer'})

    def ParametrosEjecucionDoblePrima(self) -> None:
        if self.token.token_type in {'tkn_comma'}:
            self._match({'tkn_comma'})
            self.TipoDato()
            self.ParametrosEjecucionDoblePrima()
            return
        if self.token.token_type in {'tkn_closing_par'}:
            return
        else:
            self._raiseError({'tkn_closing_par', 'tkn_comma'})

    def Procedimiento(self) -> None:
        if self.token.token_type in {'procedimiento'}:
            self._match({'procedimiento'})
            self.Identificador()
            self.Parametros()
            self.ProgramaSinRetorno()
            return
        else:
            self._raiseError({'procedimiento'})

    def Registro(self) -> None:
        if self.token.token_type in {'registro'}:
            self._match({'registro'})
            self.Identificador()
            self.DeclaracionesTipos()
            self._match({'fin'})
            self._match({'registro'})
            return
        else:
            self._raiseError({'registro'})

    def Retornar(self) -> None:
        if self.token.token_type in {'retorne'}:
            self._match({'retorne'})
            self.Expresion()
            return
        else:
            self._raiseError({'retorne'})

    def Ciclo(self) -> None:
        if self.token.token_type in {'mientras'}:
            self._match({'mientras'})
            self.Expresion()
            self._match({'haga'})
            self.ListaSentencias()
            self._match({'fin'})
            self._match({'mientras'})
            return
        if self.token.token_type in {'repita'}:
            self._match({'repita'})
            self.ListaSentencias()
            self._match({'hasta'})
            self.Expresion()
            return
        if self.token.token_type in {'para'}:
            self._match({'para'})
            self.Asignacion()
            self._match({'hasta'})
            self.Expresion()
            self._match({'haga'})
            self.ListaSentencias()
            self._match({'fin'})
            self._match({'para'})
            return
        else:
            self._raiseError({'mientras', 'para', 'repita'})

    def Condicional(self) -> None:
        if self.token.token_type in {'si'}:
            self._match({'si'})
            self.Expresion()
            self._match({'entonces'})
            self.ListaSentencias()
            self.CondicionalPrima()
            return
        else:
            self._raiseError({'si'})

    def CondicionalPrima(self) -> None:
        if self.token.token_type in {'sino'}:
            self._match({'sino'})
            self.ListaSentencias()
            self._match({'fin'})
            self._match({'si'})
            return
        if self.token.token_type in {'fin'}:
            self._match({'fin'})
            self._match({'si'})
            return
        else:
            self._raiseError({'fin', 'sino'})

    def Casos(self) -> None:
        if self.token.token_type in {'caso'}:
            self._match({'caso'})
            return
        else:
            self._raiseError({'caso'})

    def Expresion(self) -> None:
        if self.token.token_type in {'verdadero', 'id', 'tkn_str', 'falso', 'no', 'tkn_opening_par', 'tkn_minus', 'tkn_integer', 'tkn_real', 'tkn_char'}:
            self.ExpresionY()
            self.ExpresionPrima()
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_str', 'falso', 'no', 'tkn_opening_par', 'tkn_minus', 'tkn_integer', 'tkn_real', 'tkn_char'})

    def ExpresionPrima(self) -> None:
        if self.token.token_type in {'o'}:
            self._match({'o'})
            self.ExpresionY()
            self.ExpresionPrima()
            return
        if self.token.token_type in {'si', 'id', 'sino', 'tkn_closing_bra', 'para', 'tkn_opening_par', 'llamar', 'tkn_closing_par', 'lea', 'caso', 'tkn_comma', 'mientras', 'haga', 'escriba', 'entonces', 'fin', 'retorne', 'hasta', 'repita'}:
            return
        else:
            self._raiseError({'si', 'id', 'sino', 'o', 'tkn_closing_bra', 'para', 'tkn_opening_par', 'llamar', 'tkn_closing_par', 'lea', 'caso', 'tkn_comma', 'mientras', 'haga', 'escriba', 'entonces', 'fin', 'retorne', 'hasta', 'repita'})

    def ExpresionY(self) -> None:
        if self.token.token_type in {'verdadero', 'id', 'tkn_str', 'falso', 'no', 'tkn_opening_par', 'tkn_minus', 'tkn_integer', 'tkn_real', 'tkn_char'}:
            self.ExpresionNo()
            self.ExpresionYPrima()
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_str', 'falso', 'no', 'tkn_opening_par', 'tkn_minus', 'tkn_integer', 'tkn_real', 'tkn_char'})

    def ExpresionYPrima(self) -> None:
        if self.token.token_type in {'y'}:
            self._match({'y'})
            self.ExpresionNo()
            self.ExpresionYPrima()
            return
        if self.token.token_type in {'si', 'id', 'sino', 'o', 'tkn_closing_bra', 'para', 'tkn_opening_par', 'llamar', 'tkn_closing_par', 'tkn_comma', 'caso', 'lea', 'mientras', 'haga', 'escriba', 'entonces', 'fin', 'retorne', 'hasta', 'repita'}:
            return
        else:
            self._raiseError({'si', 'id', 'sino', 'o', 'tkn_closing_bra', 'para', 'tkn_opening_par', 'y', 'llamar', 'tkn_closing_par', 'tkn_comma', 'caso', 'lea', 'mientras', 'haga', 'escriba', 'entonces', 'fin', 'retorne', 'hasta', 'repita'})

    def ExpresionNo(self) -> None:
        if self.token.token_type in {'no'}:
            self._match({'no'})
            self.ExpresionNo()
            return
        if self.token.token_type in {'verdadero', 'id', 'tkn_str', 'falso', 'tkn_opening_par', 'tkn_minus', 'tkn_integer', 'tkn_real', 'tkn_char'}:
            self.Comparacion()
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_str', 'falso', 'no', 'tkn_opening_par', 'tkn_minus', 'tkn_integer', 'tkn_real', 'tkn_char'})

    def Comparacion(self) -> None:
        if self.token.token_type in {'verdadero', 'id', 'tkn_str', 'falso', 'tkn_opening_par', 'tkn_minus', 'tkn_integer', 'tkn_real', 'tkn_char'}:
            self.SumRest()
            self.ComparacionPrima()
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_str', 'falso', 'tkn_opening_par', 'tkn_minus', 'tkn_integer', 'tkn_real', 'tkn_char'})

    def ComparacionPrima(self) -> None:
        if self.token.token_type in {'tkn_equal', 'tkn_less', 'tkn_neq', 'tkn_geq', 'tkn_greater', 'tkn_leq'}:
            self.Comparador()
            self.SumRest()
            return
        if self.token.token_type in {'si', 'id', 'sino', 'o', 'tkn_closing_bra', 'para', 'tkn_opening_par', 'y', 'llamar', 'tkn_closing_par', 'tkn_comma', 'caso', 'lea', 'mientras', 'haga', 'escriba', 'entonces', 'fin', 'retorne', 'hasta', 'repita'}:
            return
        else:
            self._raiseError({'tkn_equal', 'si', 'id', 'sino', 'o', 'tkn_closing_bra', 'tkn_greater', 'para', 'tkn_opening_par', 'tkn_neq', 'y', 'llamar', 'tkn_closing_par', 'tkn_comma', 'caso', 'lea', 'mientras', 'haga', 'tkn_geq', 'escriba', 'tkn_leq', 'tkn_less', 'entonces', 'fin', 'retorne', 'hasta', 'repita'})

    def SumRest(self) -> None:
        if self.token.token_type in {'tkn_minus', 'verdadero', 'id', 'tkn_integer', 'tkn_real', 'falso', 'tkn_opening_par'}:
            self.MultDiv()
            self.SumRestPrima()
            return
        if self.token.token_type in {'tkn_str', 'tkn_char'}:
            self.DatoCaracter()
            self.SumRestPrima2()
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_str', 'falso', 'tkn_integer', 'tkn_minus', 'tkn_opening_par', 'tkn_real', 'tkn_char'})

    def SumRestPrima(self) -> None:
        if self.token.token_type in {'tkn_plus'}:
            self._match({'tkn_plus'})
            self.MultDiv()
            self.SumRestPrima()
            return
        if self.token.token_type in {'tkn_minus'}:
            self._match({'tkn_minus'})
            self.MultDiv()
            self.SumRestPrima()
            return
        if self.token.token_type in {'tkn_equal', 'si', 'id', 'sino', 'o', 'tkn_closing_bra', 'tkn_greater', 'para', 'tkn_opening_par', 'tkn_neq', 'y', 'llamar', 'tkn_closing_par', 'tkn_comma', 'caso', 'lea', 'mientras', 'haga', 'tkn_geq', 'escriba', 'tkn_leq', 'tkn_less', 'entonces', 'fin', 'retorne', 'hasta', 'repita'}:
            return
        else:
            self._raiseError({'tkn_equal', 'si', 'id', 'sino', 'o', 'tkn_closing_bra', 'tkn_greater', 'para', 'tkn_opening_par', 'tkn_neq', 'y', 'hasta', 'llamar', 'tkn_closing_par', 'tkn_comma', 'caso', 'lea', 'mientras', 'haga', 'tkn_geq', 'escriba', 'tkn_leq', 'tkn_minus', 'tkn_less', 'entonces', 'fin', 'retorne', 'tkn_plus', 'repita'})

    def SumRestPrima2(self) -> None:
        if self.token.token_type in {'tkn_plus'}:
            self._match({'tkn_plus'})
            self.SumRestDoblePrima2()
            return
        if self.token.token_type in {'tkn_equal', 'si', 'id', 'sino', 'o', 'tkn_closing_bra', 'tkn_greater', 'para', 'tkn_opening_par', 'tkn_neq', 'y', 'llamar', 'tkn_closing_par', 'tkn_comma', 'caso', 'lea', 'mientras', 'haga', 'tkn_geq', 'escriba', 'tkn_leq', 'tkn_less', 'entonces', 'fin', 'retorne', 'hasta', 'repita'}:
            return
        else:
            self._raiseError({'tkn_equal', 'si', 'id', 'sino', 'o', 'tkn_closing_bra', 'tkn_greater', 'para', 'tkn_opening_par', 'tkn_neq', 'y', 'hasta', 'llamar', 'tkn_closing_par', 'tkn_comma', 'caso', 'lea', 'mientras', 'haga', 'tkn_geq', 'escriba', 'tkn_leq', 'tkn_less', 'entonces', 'fin', 'retorne', 'tkn_plus', 'repita'})

    def SumRestDoblePrima2(self) -> None:
        if self.token.token_type in {'tkn_str', 'tkn_char'}:
            self.DatoCaracter()
            self.SumRestPrima2()
            return
        if self.token.token_type in {'id'}:
            self.Identificador()
            self.SumRestPrima2()
            return
        else:
            self._raiseError({'tkn_str', 'id', 'tkn_char'})

    def MultDiv(self) -> None:
        if self.token.token_type in {'tkn_minus', 'verdadero', 'id', 'tkn_integer', 'tkn_real', 'falso', 'tkn_opening_par'}:
            self.CambiarSigno()
            self.MultDivPrima()
            return
        else:
            self._raiseError({'tkn_minus', 'verdadero', 'id', 'tkn_integer', 'tkn_real', 'falso', 'tkn_opening_par'})

    def MultDivPrima(self) -> None:
        if self.token.token_type in {'tkn_times'}:
            self._match({'tkn_times'})
            self.CambiarSigno()
            self.MultDivPrima()
            return
        if self.token.token_type in {'tkn_div'}:
            self._match({'tkn_div'})
            self.CambiarSigno()
            self.MultDivPrima()
            return
        if self.token.token_type in {'mod'}:
            self._match({'mod'})
            self.CambiarSigno()
            self.MultDivPrima()
            return
        if self.token.token_type in {'div'}:
            self._match({'div'})
            self.CambiarSigno()
            self.MultDivPrima()
            return
        if self.token.token_type in {'tkn_equal', 'si', 'id', 'sino', 'o', 'tkn_closing_bra', 'tkn_greater', 'para', 'tkn_opening_par', 'tkn_neq', 'y', 'hasta', 'llamar', 'tkn_closing_par', 'tkn_comma', 'caso', 'lea', 'mientras', 'haga', 'tkn_geq', 'escriba', 'tkn_leq', 'tkn_minus', 'tkn_less', 'entonces', 'fin', 'retorne', 'tkn_plus', 'repita'}:
            return
        else:
            self._raiseError({'tkn_equal', 'tkn_times', 'tkn_closing_bra', 'tkn_greater', 'tkn_opening_par', 'y', 'div', 'tkn_closing_par', 'tkn_comma', 'caso', 'haga', 'tkn_geq', 'tkn_leq', 'fin', 'retorne', 'tkn_plus', 'repita', 'si', 'id', 'mod', 'sino', 'o', 'tkn_div', 'para', 'tkn_neq', 'llamar', 'lea', 'mientras', 'escriba', 'tkn_minus', 'tkn_less', 'entonces', 'hasta'})

    def CambiarSigno(self) -> None:
        if self.token.token_type in {'tkn_minus'}:
            self._match({'tkn_minus'})
            self.CambiarSigno()
            return
        if self.token.token_type in {'verdadero', 'id', 'tkn_real', 'tkn_opening_par', 'falso', 'tkn_integer'}:
            self.Exponenciacion()
            return
        else:
            self._raiseError({'tkn_minus', 'verdadero', 'id', 'tkn_integer', 'tkn_real', 'falso', 'tkn_opening_par'})

    def Exponenciacion(self) -> None:
        if self.token.token_type in {'verdadero', 'id', 'tkn_real', 'tkn_opening_par', 'falso', 'tkn_integer'}:
            self.Parentesis()
            self.ExponenciacionPrima()
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_real', 'tkn_opening_par', 'falso', 'tkn_integer'})

    def ExponenciacionPrima(self) -> None:
        if self.token.token_type in {'tkn_power'}:
            self._match({'tkn_power'})
            self.Parentesis()
            self.ExponenciacionPrima()
            return
        if self.token.token_type in {'tkn_equal', 'tkn_times', 'tkn_closing_bra', 'tkn_greater', 'tkn_opening_par', 'y', 'div', 'tkn_closing_par', 'tkn_comma', 'caso', 'haga', 'tkn_geq', 'tkn_leq', 'fin', 'retorne', 'tkn_plus', 'repita', 'si', 'id', 'mod', 'sino', 'o', 'tkn_div', 'para', 'tkn_neq', 'llamar', 'lea', 'mientras', 'escriba', 'tkn_minus', 'tkn_less', 'entonces', 'hasta'}:
            return
        else:
            self._raiseError({'tkn_equal', 'tkn_times', 'tkn_closing_bra', 'tkn_greater', 'tkn_opening_par', 'y', 'div', 'tkn_closing_par', 'tkn_comma', 'caso', 'haga', 'tkn_geq', 'tkn_leq', 'fin', 'retorne', 'tkn_plus', 'repita', 'si', 'id', 'mod', 'sino', 'o', 'tkn_div', 'para', 'tkn_neq', 'llamar', 'lea', 'mientras', 'escriba', 'tkn_minus', 'tkn_less', 'entonces', 'tkn_power', 'hasta'})

    def Parentesis(self) -> None:
        if self.token.token_type in {'tkn_opening_par'}:
            self._match({'tkn_opening_par'})
            self.Expresion()
            self._match({'tkn_closing_par'})
            return
        if self.token.token_type in {'verdadero', 'id', 'tkn_real', 'falso', 'tkn_integer'}:
            self.DatosAritmeticos()
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_integer', 'tkn_real', 'falso', 'tkn_opening_par'})

    def Comparador(self) -> None:
        if self.token.token_type in {'tkn_neq'}:
            self._match({'tkn_neq'})
            return
        if self.token.token_type in {'tkn_equal'}:
            self._match({'tkn_equal'})
            return
        if self.token.token_type in {'tkn_less'}:
            self._match({'tkn_less'})
            return
        if self.token.token_type in {'tkn_leq'}:
            self._match({'tkn_leq'})
            return
        if self.token.token_type in {'tkn_greater'}:
            self._match({'tkn_greater'})
            return
        if self.token.token_type in {'tkn_geq'}:
            self._match({'tkn_geq'})
            return
        else:
            self._raiseError({'tkn_equal', 'tkn_less', 'tkn_neq', 'tkn_geq', 'tkn_greater', 'tkn_leq'})

    def TipoCompleto(self) -> None:
        if self.token.token_type in {'caracter', 'real', 'booleano', 'entero'}:
            self.TipoNoIterable()
            return
        if self.token.token_type in {'id'}:
            self.Identificador()
            return
        if self.token.token_type in {'cadena'}:
            self.Strings()
            return
        else:
            self._raiseError({'caracter', 'id', 'real', 'booleano', 'entero', 'cadena'})

    def TipoNoIterable(self) -> None:
        if self.token.token_type in {'real'}:
            self._match({'real'})
            return
        if self.token.token_type in {'entero'}:
            self._match({'entero'})
            return
        if self.token.token_type in {'booleano'}:
            self._match({'booleano'})
            return
        if self.token.token_type in {'caracter'}:
            self._match({'caracter'})
            return
        else:
            self._raiseError({'caracter', 'real', 'booleano', 'entero'})

    def TipoIterable(self) -> None:
        if self.token.token_type in {'arreglo'}:
            self.MultiDimensional()
            return
        if self.token.token_type in {'cadena'}:
            self.Strings()
            return
        else:
            self._raiseError({'arreglo', 'cadena'})

    def MultiDimensional(self) -> None:
        if self.token.token_type in {'arreglo'}:
            self._match({'arreglo'})
            self._match({'tkn_opening_bra'})
            self.Dimensiones()
            self._match({'tkn_closing_bra'})
            self._match({'de'})
            self.TipoNoIterable()
            return
        else:
            self._raiseError({'arreglo'})

    def Strings(self) -> None:
        if self.token.token_type in {'cadena'}:
            self._match({'cadena'})
            self._match({'tkn_opening_bra'})
            self._match({'tkn_integer'})
            self._match({'tkn_closing_bra'})
            return
        else:
            self._raiseError({'cadena'})

    def TipoDato(self) -> None:
        if self.token.token_type in {'verdadero', 'id', 'tkn_real', 'falso', 'tkn_integer'}:
            self.DatosAritmeticos()
            return
        if self.token.token_type in {'tkn_str', 'tkn_char'}:
            self.DatoCaracter()
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_real', 'tkn_char', 'tkn_str', 'falso', 'tkn_integer'})

    def DatosAritmeticos(self) -> None:
        if self.token.token_type in {'verdadero', 'falso', 'tkn_real', 'tkn_integer'}:
            self.DatoOperable()
            return
        if self.token.token_type in {'id'}:
            self.Identificador()
            self.DatosAritmeticosPrima()
            return
        else:
            self._raiseError({'verdadero', 'id', 'tkn_real', 'falso', 'tkn_integer'})

    def DatosAritmeticosPrima(self) -> None:
        if self.token.token_type in {'tkn_opening_bra'}:
            self._match({'tkn_opening_bra'})
            self._match({'tkn_integer'})
            self.DatosAritmeticosDoblePrima()
            self._match({'tkn_closing_bra'})
            return
        if self.token.token_type in {'tkn_equal', 'tkn_times', 'tkn_closing_bra', 'tkn_greater', 'tkn_opening_par', 'y', 'div', 'tkn_closing_par', 'tkn_comma', 'caso', 'haga', 'tkn_geq', 'tkn_leq', 'fin', 'retorne', 'tkn_plus', 'repita', 'si', 'id', 'mod', 'sino', 'o', 'tkn_div', 'para', 'tkn_neq', 'llamar', 'lea', 'mientras', 'escriba', 'tkn_minus', 'tkn_less', 'entonces', 'tkn_power', 'hasta'}:
            return
        else:
            self._raiseError({'tkn_equal', 'tkn_times', 'tkn_closing_bra', 'tkn_greater', 'tkn_opening_par', 'y', 'div', 'tkn_closing_par', 'tkn_comma', 'caso', 'haga', 'tkn_geq', 'tkn_leq', 'tkn_opening_bra', 'fin', 'retorne', 'tkn_plus', 'repita', 'si', 'id', 'mod', 'sino', 'o', 'tkn_div', 'para', 'tkn_neq', 'llamar', 'lea', 'mientras', 'escriba', 'tkn_minus', 'tkn_less', 'entonces', 'tkn_power', 'hasta'})

    def DatosAritmeticosDoblePrima(self) -> None:
        if self.token.token_type in {'tkn_comma'}:
            self._match({'tkn_comma'})
            self._match({'tkn_integer'})
            self.DatosAritmeticosDoblePrima()
            return
        if self.token.token_type in {'tkn_closing_bra'}:
            return
        else:
            self._raiseError({'tkn_comma', 'tkn_closing_bra'})

    def DatoOperable(self) -> None:
        if self.token.token_type in {'tkn_real', 'tkn_integer'}:
            self.DatoNumerico()
            return
        if self.token.token_type in {'verdadero', 'falso'}:
            self.DatoBooleano()
            return
        else:
            self._raiseError({'verdadero', 'falso', 'tkn_real', 'tkn_integer'})

    def DatoNumerico(self) -> None:
        if self.token.token_type in {'tkn_integer'}:
            self._match({'tkn_integer'})
            return
        if self.token.token_type in {'tkn_real'}:
            self._match({'tkn_real'})
            return
        else:
            self._raiseError({'tkn_real', 'tkn_integer'})

    def DatoBooleano(self) -> None:
        if self.token.token_type in {'verdadero'}:
            self._match({'verdadero'})
            return
        if self.token.token_type in {'falso'}:
            self._match({'falso'})
            return
        else:
            self._raiseError({'verdadero', 'falso'})

    def DatoCaracter(self) -> None:
        if self.token.token_type in {'tkn_char'}:
            self._match({'tkn_char'})
            return
        if self.token.token_type in {'tkn_str'}:
            self._match({'tkn_str'})
            return
        else:
            self._raiseError({'tkn_str', 'tkn_char'})

    def Identificador(self) -> None:
        if self.token.token_type in {'id'}:
            self._match({'id'})
            return
        else:
            self._raiseError({'id'})

    def compile(self) -> None:
        self.Programa()
        if self.token.token_type != '$':
            self._raiseError({'$'})
        else:
            print('El analisis sintactico ha finalizado exitosamente.')

from LPP.LPPListener import LPPListener
from LPP.LPPParser import LPPParser
import re


class PythonListener(LPPListener):
    def __init__(self):
        super().__init__()
        self.identation = 0
        self.identationString = "    "
        self.code = ""
        self.case_option_count = 0

    def getPythonCode(self):
        return self.code
    
    def getStringWithSpaces(self, node) -> str:
        """
        Recibe un nodo de contexto de ANTLR, explora sus hijos usando un algoritmo de profundidad y retorna una cadena separada por espacios
        """
        if node is None:
            return ""
        
        text = ""
        for child in node.getChildren():
            try:
                new_children = list(child.getChildren())
            except:
                new_children = []

            if len(new_children) > 0:
                text += self.getStringWithSpaces(child)
            else:
                text += child.getText().lower() + " "
        return text
    
    def cleanParameters(self, node):
        """
        Recibe un nodo de contexto de ANTLR, explora sus hijos usando un algoritmo de profundidad y retorna una cadena de parámetros separada por comas
        """
        if node is None:
            return ""
    
        text = []
        for child in node.getChildren():
            try:
                param_name = child.ID().getText().lower()

                text.append(param_name)
            except:
                continue

        return ', '.join(text)
    
    def cleanOnlyIdExpressions(self, node):
        """
        Recibe un nodo de contexto de ANTLR, explora sus hijos usando un algoritmo de profundidad y retorna una cadena de parámetros separada por comas
        """
        if node is None:
            return ""
    
        text = []
        for child in node.getChildren():
            try:
                param_name = child.getText().lower()

                text.append(param_name)
            except:
                continue

        return text

    def fixExpression(self, expression:str) -> str:
        expressions = [value for value in expression.split(" ") if value]

        for index, expr in enumerate(expressions):
            if re.match("y", expr, re.IGNORECASE): expressions[index] = " and "
            elif re.match("o", expr, re.IGNORECASE): expressions[index] = " or "
            elif re.match("no", expr, re.IGNORECASE): expressions[index] = " not "
            elif re.match("<>", expr): expressions[index] = " != "
            elif re.match("=", expr): expressions[index] = " == "
            elif re.match("mod", expr, re.IGNORECASE): expressions[index] = " % "
            elif re.match("div", expr, re.IGNORECASE): expressions[index] = " // "
            elif re.match("verdadero", expr, re.IGNORECASE): expressions[index] = " True "
            elif re.match("falso", expr, re.IGNORECASE): expressions[index] = " False "

        return ''.join(expressions)

    # Enter a parse tree produced by LPPParser#program.
    def enterProgram(self, ctx: LPPParser.ProgramContext):
        pass

    # Exit a parse tree produced by LPPParser#program.
    def exitProgram(self, ctx: LPPParser.ProgramContext):
        pass

    # Enter a parse tree produced by LPPParser#registry_declaration.
    def enterRegistry_declaration(self, ctx: LPPParser.Registry_declarationContext):
        registry_name = ctx.ID().getText().lower()
        variables_names = ','.join([value.ids_list().getText().lower() for value in ctx.registry_varibles_declaration().getChildren()])

        self.code += self.identationString * self.identation
        self.code += f"class {registry_name}:\n"
        self.identation += 1
        self.code += self.identationString * self.identation
        self.code += f"def __init__(self, {','.join([value + ' = None' for value in variables_names.split(',')])}):\n"
        self.identation += 1
        
        for value in variables_names.split(","):
            self.code += self.identationString * self.identation
            self.code += f"self.{value} = {value}\n"

        self.identation -= 2

    # Exit a parse tree produced by LPPParser#registry_declaration.
    def exitRegistry_declaration(self, ctx: LPPParser.Registry_declarationContext):
        pass

    # Enter a parse tree produced by LPPParser#procedure_declaration.
    def enterProcedure_declaration(self, ctx: LPPParser.Procedure_declarationContext):
        function_name = ctx.ID().getText().lower()
        paramaters = self.cleanParameters(ctx.parameters())
        
        self.code += self.identationString * self.identation
        self.code += f"def {function_name}( {paramaters} ):\n"
        self.identation += 1

    # Exit a parse tree produced by LPPParser#procedure_declaration.
    def exitProcedure_declaration(self, ctx: LPPParser.Procedure_declarationContext):
        self.identation -= 1

    # Enter a parse tree produced by LPPParser#function_declaration.
    def enterFunction_declaration(self, ctx: LPPParser.Function_declarationContext):
        function_name = ctx.ID().getText().lower()
        paramaters = self.cleanParameters(ctx.parameters())
        
        self.code += self.identationString * self.identation
        self.code += f"def {function_name}( {paramaters} ):\n"
        self.identation += 1

    # Exit a parse tree produced by LPPParser#function_declaration.
    def exitFunction_declaration(self, ctx: LPPParser.Function_declarationContext):
        self.identation -= 1

    # Enter a parse tree produced by LPPParser#parameters.
    def enterParameters(self, ctx: LPPParser.ParametersContext):
        pass

    # Exit a parse tree produced by LPPParser#parameters.
    def exitParameters(self, ctx: LPPParser.ParametersContext):
        pass

    # Enter a parse tree produced by LPPParser#parameter.
    def enterParameter(self, ctx: LPPParser.ParameterContext):
        pass

    # Exit a parse tree produced by LPPParser#parameter.
    def exitParameter(self, ctx: LPPParser.ParameterContext):
        pass

    # Enter a parse tree produced by LPPParser#registry_varibles_declaration.
    def enterRegistry_varibles_declaration(self, ctx:LPPParser.Registry_varibles_declarationContext):
        pass

    # Exit a parse tree produced by LPPParser#registry_varibles_declaration.
    def exitRegistry_varibles_declaration(self, ctx:LPPParser.Registry_varibles_declarationContext):
        pass

    # Enter a parse tree produced by LPPParser#variables_declaration.
    def enterVariables_declaration(self, ctx: LPPParser.Variables_declarationContext):
        pass

    # Exit a parse tree produced by LPPParser#variables_declaration.
    def exitVariables_declaration(self, ctx: LPPParser.Variables_declarationContext):
        declarations = list(ctx.getChildren())

        for node in declarations:
            var_type = node.type_()

            if var_type is None:
                continue

            if re.findall(r"arreglo", var_type.getText(), re.IGNORECASE):
                var_name = node.ids_list().getText().lower()
                var_size = node.type_().integer_list().getText()
                var_type = node.type_().type_().getText().lower()

                # for var size, split by comma and initialize with a list comprehension
                if var_type not in ["entero", "real", "caracter", "booleano", "cadena", "arreglo"]:
                    init_values = f"{var_type}()"
                else:
                    init_values = None

                    for dimension in var_size.split(","):
                        if init_values is None:
                            inside_value = 0 if var_type in ["entero", "real"] else "''"
                            init_values = f"[{inside_value} for _ in range({dimension})]"
                        else:
                            init_values = f"[{init_values} for _ in range({dimension})]"

                self.code += self.identationString * self.identation
                self.code += f"{var_name} = {init_values}\n"

    # Enter a parse tree produced by LPPParser#variable_declaration.
    def enterVariable_declaration(self, ctx: LPPParser.Variable_declarationContext):
        pass

    # Exit a parse tree produced by LPPParser#variable_declaration.
    def exitVariable_declaration(self, ctx: LPPParser.Variable_declarationContext):
        pass

    # Enter a parse tree produced by LPPParser#type.
    def enterType(self, ctx: LPPParser.TypeContext):
        pass

    # Exit a parse tree produced by LPPParser#type.
    def exitType(self, ctx: LPPParser.TypeContext):
        pass

    # Enter a parse tree produced by LPPParser#ids_list.
    def enterIds_list(self, ctx: LPPParser.Ids_listContext):
        pass

    # Exit a parse tree produced by LPPParser#ids_list.
    def exitIds_list(self, ctx: LPPParser.Ids_listContext):
        pass

    # Enter a parse tree produced by LPPParser#integer_list.
    def enterInteger_list(self, ctx: LPPParser.Integer_listContext):
        pass

    # Exit a parse tree produced by LPPParser#integer_list.
    def exitInteger_list(self, ctx: LPPParser.Integer_listContext):
        pass

    # Enter a parse tree produced by LPPParser#subprogram_body.
    def enterSubprogram_body(self, ctx: LPPParser.Subprogram_bodyContext):
        pass

    # Exit a parse tree produced by LPPParser#subprogram_body.
    def exitSubprogram_body(self, ctx: LPPParser.Subprogram_bodyContext):
        pass

    # Enter a parse tree produced by LPPParser#program_body.
    def enterProgram_body(self, ctx: LPPParser.Program_bodyContext):
        self.code += "def main():\n"
        self.identation = 1

    # Exit a parse tree produced by LPPParser#program_body.
    def exitProgram_body(self, ctx: LPPParser.Program_bodyContext):
        self.identation -= 1

        self.code += "\nif __name__ == '__main__':\n"
        self.identation = 1

        self.code += self.identationString * self.identation
        self.code += "main()"
        self.identation -= 1

    # Enter a parse tree produced by LPPParser#statements.
    def enterStatements(self, ctx: LPPParser.StatementsContext):
        pass

    # Exit a parse tree produced by LPPParser#statements.
    def exitStatements(self, ctx: LPPParser.StatementsContext):
        pass

    # Enter a parse tree produced by LPPParser#statement.
    def enterStatement(self, ctx: LPPParser.StatementContext):
        pass

    # Exit a parse tree produced by LPPParser#statement.
    def exitStatement(self, ctx: LPPParser.StatementContext):
        pass

    # Enter a parse tree produced by LPPParser#literal.
    def enterLiteral(self, ctx: LPPParser.LiteralContext):
        pass

    # Exit a parse tree produced by LPPParser#literal.
    def exitLiteral(self, ctx: LPPParser.LiteralContext):
        pass

    # Enter a parse tree produced by LPPParser#write_statement.
    def enterWrite_statement(self, ctx: LPPParser.Write_statementContext):
        self.code += self.identationString * self.identation
        self.code += "print("

    # Exit a parse tree produced by LPPParser#write_statement.
    def exitWrite_statement(self, ctx: LPPParser.Write_statementContext):
        self.code += ")\n"

    # Enter a parse tree produced by LPPParser#read_statement.
    def enterRead_statement(self, ctx: LPPParser.Read_statementContext):
        expr_list = self.cleanOnlyIdExpressions(ctx.only_id_expressions_list())
        
        for value in expr_list:
            self.code += self.identationString * self.identation
            self.code += value + " = input()\n"

    # Exit a parse tree produced by LPPParser#read_statement.
    def exitRead_statement(self, ctx: LPPParser.Read_statementContext):
        pass

    # Enter a parse tree produced by LPPParser#assignment_statement.
    def enterAssignment_statement(self, ctx: LPPParser.Assignment_statementContext):
        first_expr = self.getStringWithSpaces(ctx.expression(0)).lower()
        second_expr = self.getStringWithSpaces(ctx.expression(1)).lower()

        self.code += self.identationString * self.identation
        self.code += f"{self.fixExpression(first_expr)} = {self.fixExpression(second_expr)}\n"

    # Exit a parse tree produced by LPPParser#assignment_statement.
    def exitAssignment_statement(self, ctx: LPPParser.Assignment_statementContext):
        pass

    # Enter a parse tree produced by LPPParser#call_statement.
    def enterCall_statement(self, ctx: LPPParser.Call_statementContext):
        # Remove all newline characters and leading 'llamar' from the text
        func_name = re.sub(r"\s*llamar\s*", "", ctx.getText().replace("\n", ""), flags=re.IGNORECASE).lower()

        # Add the appropriate Python code to self.code
        self.code += self.identationString * self.identation
        if re.match(r'nueva_linea', func_name, re.IGNORECASE) is not None:
            self.code += "print()\n"
        else:
            self.code += f"{func_name}\n"

    # Exit a parse tree produced by LPPParser#call_statement.
    def exitCall_statement(self, ctx: LPPParser.Call_statementContext):
        pass

    # Enter a parse tree produced by LPPParser#if_statement.
    def enterIf_statement(self, ctx: LPPParser.If_statementContext):
        parent = ctx.parentCtx
        if(parent is not None and not isinstance(parent, LPPParser.Elif_statementContext)):
            self.code += self.identationString * self.identation

        expression = self.getStringWithSpaces(ctx.expression())

        self.code += f"if {self.fixExpression(expression)}:\n"

        self.identation += 1

    # Exit a parse tree produced by LPPParser#if_statement.
    def exitIf_statement(self, ctx: LPPParser.If_statementContext):
        self.identation -= 1

    # Enter a parse tree produced by LPPParser#elif_statement.
    def enterElif_statement(self, ctx: LPPParser.Elif_statementContext):
        self.identation -= 1
        self.code += self.identationString * self.identation

        if ctx.if_statement() is not None:
            self.code += "el"
        else:
            self.code += "else:\n"
            self.identation += 1

    # Exit a parse tree produced by LPPParser#elif_statement.
    def exitElif_statement(self, ctx: LPPParser.Elif_statementContext):
        self.identation -= 1

    # Enter a parse tree produced by LPPParser#case_statement.
    def enterCase_statement(self, ctx: LPPParser.Case_statementContext):
        self.identation += 1

    # Exit a parse tree produced by LPPParser#case_statement.
    def exitCase_statement(self, ctx: LPPParser.Case_statementContext):
        self.identation -= 1

    # Enter a parse tree produced by LPPParser#case_option.
    def enterCase_option(self, ctx: LPPParser.Case_optionContext):
        parent_expr = ctx.parentCtx.expression().getText()
        expr = ctx.expressions_list().getText()
        self.identation -= 1
        self.code += self.identationString * self.identation
        self.code += f"{'el' if self.case_option_count > 0 else ''}if {parent_expr} in [{expr}"
        self.identation += 1
        self.case_option_count += 1

    # Exit a parse tree produced by LPPParser#case_option.
    def exitCase_option(self, ctx: LPPParser.Case_optionContext):
        pass

    # Enter a parse tree produced by LPPParser#elif_case.
    def enterElif_case(self, ctx: LPPParser.Elif_caseContext):

        self.identation -= 1
        self.code += self.identationString * self.identation
        self.code += f"else:\n"
        self.identation += 1

    # Exit a parse tree produced by LPPParser#elif_case.
    def exitElif_case(self, ctx: LPPParser.Elif_caseContext):
        self.identation -= 1

    # Enter a parse tree produced by LPPParser#while_statement.
    def enterWhile_statement(self, ctx: LPPParser.While_statementContext):
        expression = ctx.expression().getText()

        self.code += self.identationString * self.identation
        self.code += f"while {expression}:\n"

        self.identation += 1

    # Exit a parse tree produced by LPPParser#while_statement.
    def exitWhile_statement(self, ctx: LPPParser.While_statementContext):
        self.identation -= 1

    # Enter a parse tree produced by LPPParser#for_statement.
    def enterFor_statement(self, ctx: LPPParser.For_statementContext):
        self.code += self.identationString * self.identation
        self.code += "for "

        for i in range(0, len(ctx.expression())):
            expression = ctx.expression(i).getText().lower()

            if i == 0:
                self.code += f"{expression} in range("
            elif i == 1:
                self.code += f"{expression}, "
            else:
                self.code += f"{expression}):\n"

        self.identation += 1

    # Exit a parse tree produced by LPPParser#for_statement.
    def exitFor_statement(self, ctx: LPPParser.For_statementContext):
        self.identation -= 1

    # Enter a parse tree produced by LPPParser#repeat_statement.
    def enterRepeat_statement(self, ctx: LPPParser.Repeat_statementContext):
        expression = self.getStringWithSpaces(ctx.expression())

        self.code += self.identationString * self.identation

        self.code += f"while True:\n"
        self.identation += 1
        self.code += self.identationString * self.identation
        self.code += f"if {self.fixExpression(expression)}: break\n"

    # Exit a parse tree produced by LPPParser#repeat_statement.
    def exitRepeat_statement(self, ctx: LPPParser.Repeat_statementContext):
        self.identation -= 1

    # Enter a parse tree produced by LPPParser#return_statement.
    def enterReturn_statement(self, ctx: LPPParser.Return_statementContext):
        expression = self.getStringWithSpaces(ctx.expression())

        self.code += self.identationString * self.identation
        self.code += f"return {self.fixExpression(expression)}\n"

    # Exit a parse tree produced by LPPParser#return_statement.
    def exitReturn_statement(self, ctx: LPPParser.Return_statementContext):
        pass

    # Enter a parse tree produced by LPPParser#expressions_list.
    def enterExpressions_list(self, ctx: LPPParser.Expressions_listContext):
        parent = ctx.parentCtx

        #! Recordar quitar ExpressionContext si hay problemas

        if isinstance(parent, (
            LPPParser.Only_id_expressionContext,
            LPPParser.Call_statementContext,
            LPPParser.Case_statementContext,
            LPPParser.ExpressionContext,
        )):
            pass

        elif isinstance(parent, LPPParser.Write_statementContext):
            text = ctx.getText().replace("\n", "").lower()

            text = [value for value in text.split(",") if value]
            text = [value[1:-1] if value.startswith("(") and value.endswith(")") else value for value in text]
    
            text = ', '.join(text)

            self.code += text
        elif isinstance(parent, LPPParser.Case_optionContext):
            self.code += "]:\n" if self.case_option_count > 0 else "\n"
            self.case_option_count += 1
        else: 
            self.code += ctx.getText()
        

    # Exit a parse tree produced by LPPParser#expressions_list.
    def exitExpressions_list(self, ctx: LPPParser.Expressions_listContext):
        pass

    # Enter a parse tree produced by LPPParser#expression.
    def enterExpression(self, ctx: LPPParser.ExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#expression.
    def exitExpression(self, ctx: LPPParser.ExpressionContext):
        pass

    # Enter a parse tree produced by LPPParser#only_id_expression.
    def enterOnly_id_expression(self, ctx:LPPParser.Only_id_expressionContext):
        pass
    
    # Exit a parse tree produced by LPPParser#only_id_expression.
    def exitOnly_id_expression(self, ctx:LPPParser.Only_id_expressionContext):
        pass

    # Enter a parse tree produced by LPPParser#only_id_expressions_list.
    def enterOnly_id_expressions_list(self, ctx: LPPParser.Only_id_expressions_listContext):
        pass

    # Exit a parse tree produced by LPPParser#only_id_expressions_list.
    def exitOnly_id_expressions_list(self, ctx: LPPParser.Only_id_expressions_listContext):
        pass

# Generated from LPP.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .LPPParser import LPPParser
else:
    from LPPParser import LPPParser

# This class defines a complete listener for a parse tree produced by LPPParser.
class LPPListener(ParseTreeListener):

    # Enter a parse tree produced by LPPParser#program.
    def enterProgram(self, ctx:LPPParser.ProgramContext):
        pass

    # Exit a parse tree produced by LPPParser#program.
    def exitProgram(self, ctx:LPPParser.ProgramContext):
        pass


    # Enter a parse tree produced by LPPParser#registry_declaration.
    def enterRegistry_declaration(self, ctx:LPPParser.Registry_declarationContext):
        pass

    # Exit a parse tree produced by LPPParser#registry_declaration.
    def exitRegistry_declaration(self, ctx:LPPParser.Registry_declarationContext):
        pass


    # Enter a parse tree produced by LPPParser#type_declaration.
    def enterType_declaration(self, ctx:LPPParser.Type_declarationContext):
        pass

    # Exit a parse tree produced by LPPParser#type_declaration.
    def exitType_declaration(self, ctx:LPPParser.Type_declarationContext):
        pass


    # Enter a parse tree produced by LPPParser#procedure_declaration.
    def enterProcedure_declaration(self, ctx:LPPParser.Procedure_declarationContext):
        pass

    # Exit a parse tree produced by LPPParser#procedure_declaration.
    def exitProcedure_declaration(self, ctx:LPPParser.Procedure_declarationContext):
        pass


    # Enter a parse tree produced by LPPParser#function_declaration.
    def enterFunction_declaration(self, ctx:LPPParser.Function_declarationContext):
        pass

    # Exit a parse tree produced by LPPParser#function_declaration.
    def exitFunction_declaration(self, ctx:LPPParser.Function_declarationContext):
        pass


    # Enter a parse tree produced by LPPParser#parameters.
    def enterParameters(self, ctx:LPPParser.ParametersContext):
        pass

    # Exit a parse tree produced by LPPParser#parameters.
    def exitParameters(self, ctx:LPPParser.ParametersContext):
        pass


    # Enter a parse tree produced by LPPParser#parameter.
    def enterParameter(self, ctx:LPPParser.ParameterContext):
        pass

    # Exit a parse tree produced by LPPParser#parameter.
    def exitParameter(self, ctx:LPPParser.ParameterContext):
        pass


    # Enter a parse tree produced by LPPParser#variables_declaration.
    def enterVariables_declaration(self, ctx:LPPParser.Variables_declarationContext):
        pass

    # Exit a parse tree produced by LPPParser#variables_declaration.
    def exitVariables_declaration(self, ctx:LPPParser.Variables_declarationContext):
        pass


    # Enter a parse tree produced by LPPParser#variable_declaration.
    def enterVariable_declaration(self, ctx:LPPParser.Variable_declarationContext):
        pass

    # Exit a parse tree produced by LPPParser#variable_declaration.
    def exitVariable_declaration(self, ctx:LPPParser.Variable_declarationContext):
        pass


    # Enter a parse tree produced by LPPParser#type.
    def enterType(self, ctx:LPPParser.TypeContext):
        pass

    # Exit a parse tree produced by LPPParser#type.
    def exitType(self, ctx:LPPParser.TypeContext):
        pass


    # Enter a parse tree produced by LPPParser#ids_list.
    def enterIds_list(self, ctx:LPPParser.Ids_listContext):
        pass

    # Exit a parse tree produced by LPPParser#ids_list.
    def exitIds_list(self, ctx:LPPParser.Ids_listContext):
        pass


    # Enter a parse tree produced by LPPParser#integer_list.
    def enterInteger_list(self, ctx:LPPParser.Integer_listContext):
        pass

    # Exit a parse tree produced by LPPParser#integer_list.
    def exitInteger_list(self, ctx:LPPParser.Integer_listContext):
        pass


    # Enter a parse tree produced by LPPParser#subprogram_body.
    def enterSubprogram_body(self, ctx:LPPParser.Subprogram_bodyContext):
        pass

    # Exit a parse tree produced by LPPParser#subprogram_body.
    def exitSubprogram_body(self, ctx:LPPParser.Subprogram_bodyContext):
        pass


    # Enter a parse tree produced by LPPParser#program_body.
    def enterProgram_body(self, ctx:LPPParser.Program_bodyContext):
        pass

    # Exit a parse tree produced by LPPParser#program_body.
    def exitProgram_body(self, ctx:LPPParser.Program_bodyContext):
        pass


    # Enter a parse tree produced by LPPParser#statements.
    def enterStatements(self, ctx:LPPParser.StatementsContext):
        pass

    # Exit a parse tree produced by LPPParser#statements.
    def exitStatements(self, ctx:LPPParser.StatementsContext):
        pass


    # Enter a parse tree produced by LPPParser#statement.
    def enterStatement(self, ctx:LPPParser.StatementContext):
        pass

    # Exit a parse tree produced by LPPParser#statement.
    def exitStatement(self, ctx:LPPParser.StatementContext):
        pass


    # Enter a parse tree produced by LPPParser#literal.
    def enterLiteral(self, ctx:LPPParser.LiteralContext):
        pass

    # Exit a parse tree produced by LPPParser#literal.
    def exitLiteral(self, ctx:LPPParser.LiteralContext):
        pass


    # Enter a parse tree produced by LPPParser#write_statement.
    def enterWrite_statement(self, ctx:LPPParser.Write_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#write_statement.
    def exitWrite_statement(self, ctx:LPPParser.Write_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#read_statement.
    def enterRead_statement(self, ctx:LPPParser.Read_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#read_statement.
    def exitRead_statement(self, ctx:LPPParser.Read_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#assignment_statement.
    def enterAssignment_statement(self, ctx:LPPParser.Assignment_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#assignment_statement.
    def exitAssignment_statement(self, ctx:LPPParser.Assignment_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#call_statement.
    def enterCall_statement(self, ctx:LPPParser.Call_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#call_statement.
    def exitCall_statement(self, ctx:LPPParser.Call_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#if_statement.
    def enterIf_statement(self, ctx:LPPParser.If_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#if_statement.
    def exitIf_statement(self, ctx:LPPParser.If_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#elif_statement.
    def enterElif_statement(self, ctx:LPPParser.Elif_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#elif_statement.
    def exitElif_statement(self, ctx:LPPParser.Elif_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#case_statement.
    def enterCase_statement(self, ctx:LPPParser.Case_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#case_statement.
    def exitCase_statement(self, ctx:LPPParser.Case_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#case_option.
    def enterCase_option(self, ctx:LPPParser.Case_optionContext):
        pass

    # Exit a parse tree produced by LPPParser#case_option.
    def exitCase_option(self, ctx:LPPParser.Case_optionContext):
        pass


    # Enter a parse tree produced by LPPParser#elif_case.
    def enterElif_case(self, ctx:LPPParser.Elif_caseContext):
        pass

    # Exit a parse tree produced by LPPParser#elif_case.
    def exitElif_case(self, ctx:LPPParser.Elif_caseContext):
        pass


    # Enter a parse tree produced by LPPParser#while_statement.
    def enterWhile_statement(self, ctx:LPPParser.While_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#while_statement.
    def exitWhile_statement(self, ctx:LPPParser.While_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#for_statement.
    def enterFor_statement(self, ctx:LPPParser.For_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#for_statement.
    def exitFor_statement(self, ctx:LPPParser.For_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#repeat_statement.
    def enterRepeat_statement(self, ctx:LPPParser.Repeat_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#repeat_statement.
    def exitRepeat_statement(self, ctx:LPPParser.Repeat_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#return_statement.
    def enterReturn_statement(self, ctx:LPPParser.Return_statementContext):
        pass

    # Exit a parse tree produced by LPPParser#return_statement.
    def exitReturn_statement(self, ctx:LPPParser.Return_statementContext):
        pass


    # Enter a parse tree produced by LPPParser#expressions_list.
    def enterExpressions_list(self, ctx:LPPParser.Expressions_listContext):
        pass

    # Exit a parse tree produced by LPPParser#expressions_list.
    def exitExpressions_list(self, ctx:LPPParser.Expressions_listContext):
        pass


    # Enter a parse tree produced by LPPParser#only_id_expressions_list.
    def enterOnly_id_expressions_list(self, ctx:LPPParser.Only_id_expressions_listContext):
        pass

    # Exit a parse tree produced by LPPParser#only_id_expressions_list.
    def exitOnly_id_expressions_list(self, ctx:LPPParser.Only_id_expressions_listContext):
        pass


    # Enter a parse tree produced by LPPParser#only_id_expression.
    def enterOnly_id_expression(self, ctx:LPPParser.Only_id_expressionContext):
        pass

    # Exit a parse tree produced by LPPParser#only_id_expression.
    def exitOnly_id_expression(self, ctx:LPPParser.Only_id_expressionContext):
        pass


    # Enter a parse tree produced by LPPParser#negativeExpression.
    def enterNegativeExpression(self, ctx:LPPParser.NegativeExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#negativeExpression.
    def exitNegativeExpression(self, ctx:LPPParser.NegativeExpressionContext):
        pass


    # Enter a parse tree produced by LPPParser#additionSubtractionExpression.
    def enterAdditionSubtractionExpression(self, ctx:LPPParser.AdditionSubtractionExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#additionSubtractionExpression.
    def exitAdditionSubtractionExpression(self, ctx:LPPParser.AdditionSubtractionExpressionContext):
        pass


    # Enter a parse tree produced by LPPParser#comparisonExpression.
    def enterComparisonExpression(self, ctx:LPPParser.ComparisonExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#comparisonExpression.
    def exitComparisonExpression(self, ctx:LPPParser.ComparisonExpressionContext):
        pass


    # Enter a parse tree produced by LPPParser#parenExpression.
    def enterParenExpression(self, ctx:LPPParser.ParenExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#parenExpression.
    def exitParenExpression(self, ctx:LPPParser.ParenExpressionContext):
        pass


    # Enter a parse tree produced by LPPParser#logicalExpression.
    def enterLogicalExpression(self, ctx:LPPParser.LogicalExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#logicalExpression.
    def exitLogicalExpression(self, ctx:LPPParser.LogicalExpressionContext):
        pass


    # Enter a parse tree produced by LPPParser#powerStatement.
    def enterPowerStatement(self, ctx:LPPParser.PowerStatementContext):
        pass

    # Exit a parse tree produced by LPPParser#powerStatement.
    def exitPowerStatement(self, ctx:LPPParser.PowerStatementContext):
        pass


    # Enter a parse tree produced by LPPParser#multiplicationDivisionStatement.
    def enterMultiplicationDivisionStatement(self, ctx:LPPParser.MultiplicationDivisionStatementContext):
        pass

    # Exit a parse tree produced by LPPParser#multiplicationDivisionStatement.
    def exitMultiplicationDivisionStatement(self, ctx:LPPParser.MultiplicationDivisionStatementContext):
        pass


    # Enter a parse tree produced by LPPParser#arrayAccessExpression.
    def enterArrayAccessExpression(self, ctx:LPPParser.ArrayAccessExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#arrayAccessExpression.
    def exitArrayAccessExpression(self, ctx:LPPParser.ArrayAccessExpressionContext):
        pass


    # Enter a parse tree produced by LPPParser#idExpression.
    def enterIdExpression(self, ctx:LPPParser.IdExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#idExpression.
    def exitIdExpression(self, ctx:LPPParser.IdExpressionContext):
        pass


    # Enter a parse tree produced by LPPParser#invertLogicalValue.
    def enterInvertLogicalValue(self, ctx:LPPParser.InvertLogicalValueContext):
        pass

    # Exit a parse tree produced by LPPParser#invertLogicalValue.
    def exitInvertLogicalValue(self, ctx:LPPParser.InvertLogicalValueContext):
        pass


    # Enter a parse tree produced by LPPParser#dotIdExpression.
    def enterDotIdExpression(self, ctx:LPPParser.DotIdExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#dotIdExpression.
    def exitDotIdExpression(self, ctx:LPPParser.DotIdExpressionContext):
        pass


    # Enter a parse tree produced by LPPParser#functionCallExpression.
    def enterFunctionCallExpression(self, ctx:LPPParser.FunctionCallExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#functionCallExpression.
    def exitFunctionCallExpression(self, ctx:LPPParser.FunctionCallExpressionContext):
        pass


    # Enter a parse tree produced by LPPParser#literalExpression.
    def enterLiteralExpression(self, ctx:LPPParser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by LPPParser#literalExpression.
    def exitLiteralExpression(self, ctx:LPPParser.LiteralExpressionContext):
        pass



del LPPParser
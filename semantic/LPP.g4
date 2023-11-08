grammar LPP;

program : NL* variables_declaration program_body ;

registry_declaration : REGISTRO ID NL+ registry_varibles_declaration FIN REGISTRO NL+ ;

procedure_declaration : PROCEDIMIENTO ID ('(' parameters ')')? NL+ variables_declaration subprogram_body ;

function_declaration : FUNCION ID ('(' parameters ')')? ':' type NL+ variables_declaration subprogram_body ;

parameters : parameter (',' parameter)* ;

parameter : VAR? type ID ;

registry_varibles_declaration : registry_varible_declaration+ ;

registry_varible_declaration : type ids_list NL+ ;

variables_declaration : variable_declaration*
| ;

variable_declaration : type ids_list NL+ 
| (registry_declaration 
| procedure_declaration
| function_declaration) ;

type : ENTERO
| REAL
| BOOLEANO
| CARACTER
| ID
| ARREGLO '[' integer_list ']' DE type
| CADENA ( '[' INTEGER_LITERAL ']' )? ;

ids_list : ID (',' ID)* ;

integer_list : INTEGER_LITERAL (',' INTEGER_LITERAL)* ;

subprogram_body : INICIO NL+ statements FIN NL+ ;

program_body : INICIO NL+ statements FIN NL* EOF ;

statements : statement* ;

statement : write_statement
| read_statement
| assignment_statement
| call_statement
| if_statement
| case_statement
| while_statement
| for_statement
| repeat_statement
| return_statement ;

literal : INTEGER_LITERAL
| STRING_LITERAL
| REAL_LITERAL
| CHAR_LITERAL
| (VERDADERO | FALSO) ;

write_statement : ESCRIBA expressions_list NL+ ;

read_statement : LEA only_id_expressions_list NL+ ;

assignment_statement : expression '<-' expression NL+ ;

call_statement : LLAMAR NEW_LINE_PROCEDURE NL+ 
| LLAMAR ID ( '(' expressions_list? ')' )? NL+ ; 

if_statement : SI expression NL* ENTONCES NL+ statements elif_statement? FIN SI NL+ ;

elif_statement : SINO if_statement
| SINO NL+ statements ;

case_statement : CASO expression NL+ case_option+ elif_case? FIN CASO NL+ ;

case_option : expressions_list ':' NL+ statements ;

elif_case : SINO ':' NL* statements ;

while_statement : MIENTRAS expression NL* HAGA NL+ statements NL* FIN MIENTRAS NL+ ;

for_statement : PARA expression ASSIGNMENT expression HASTA expression NL* HAGA NL+ statements FIN PARA NL+ ;

repeat_statement : REPITA NL+ statements HASTA expression NL+ ;

return_statement : RETORNE expression NL+ ;

expressions_list : expression (',' expression)* ;
only_id_expressions_list : only_id_expression (',' only_id_expression)* ;

only_id_expression : ID
| only_id_expression '.' ID
| only_id_expression '[' expressions_list ']'
| ID '(' expressions_list? ')' ;

expression : '(' expression ')' 
| literal 
| ID 
| expression '.' ID 
| expression '[' expressions_list ']'
| ID '(' expressions_list? ')' 
| '-' expression  
| NO expression 
| <assoc=right> expression POWER expression
| expression (MULT | DIV | MOD | INT_DIV) expression 
| expression (PLUS | MINUS) expression 
| expression (GREATER_THAN | GREATER_EQUAL | LESS_THAN | LESS_EQUAL | EQUAL | NOT_EQUAL) expression 
| expression (AND | OR) expression ;

// Data types
PROCEDIMIENTO : P R O C E D I M I E N T O ;
BOOLEANO : B O O L E A N O ;
CARACTER : C A R A C T E R ;
REGISTRO : R E G I S T R O ;
ARREGLO : A R R E G L O ;
FUNCION : F U N C I O N ;
CADENA : C A D E N A ;
ENTERO : E N T E R O ;
TIPO : T I P O ;
REAL : R E A L ;
VAR : V A R ;

// Reserved words
ENTONCES : E N T O N C E S ;
MIENTRAS : M I E N T R A S ;
ESCRIBA : E S C R I B A ;
RETORNE : R E T O R N E ;
INICIO : I N I C I O ;
LLAMAR : L L A M A R ;
REPITA : R E P I T A ;
HASTA : H A S T A ;
CASO : C A S O ;
COMO : C O M O ;
HAGA : H A G A ;
PARA : P A R A ;
SINO : S I N O ;
FIN : F I N ;
LEA : L E A ;
DE : D E ;
ES : E S ;
SI : S I ;

// Operators
GREATER_EQUAL : '>=' ;
GREATER_THAN : '>' ;
ASSIGNMENT : '<-' ;
LESS_EQUAL : '<=' ;
NOT_EQUAL : '<>' ;
INT_DIV : D I V ;
LESS_THAN : '<' ;
EQUAL : '=' ;
MOD : M O D ;
MINUS : '-' ;
POWER : '^' ;
MULT : '*' ;
PLUS : '+' ;
DIV : '/' ;
NO : N O ;
AND : Y ;
OR : O ;

// Default LPP library procedures
NEW_LINE_PROCEDURE : N U E V A '_' L I N E A ;

// Data values
REAL_LITERAL : DIGIT+ '.' DIGIT+ 
| '.' DIGIT+ ;
INTEGER_LITERAL : DIGIT+ ;
VERDADERO : V E R D A D E R O ;
FALSO : F A L S O ;
CHAR_LITERAL : '\'' .? '\'' ;
STRING_LITERAL : '"' .*? '"' ;
ID : [a-zA-Z$_][a-zA-Z0-9$_]* ;

fragment DIGIT : [0-9] ;

// Avoid parser to check case sensitivity
fragment A : [aA] ;
fragment B : [bB] ;
fragment C : [cC] ;
fragment D : [dD] ;
fragment E : [eE] ;
fragment F : [fF] ;
fragment G : [gG] ;
fragment H : [hH] ;
fragment I : [iI] ;
fragment J : [jJ] ;
fragment K : [kK] ;
fragment L : [lL] ;
fragment M : [mM] ;
fragment N : [nN] ;
fragment O : [oO] ;
fragment P : [pP] ;
fragment Q : [qQ] ;
fragment R : [rR] ;
fragment S : [sS] ;
fragment T : [tT] ;
fragment U : [uU] ;
fragment V : [vV] ;
fragment W : [wW] ;
fragment X : [xX] ;
fragment Y : [yY] ;
fragment Z : [zZ] ;


// Things in the grammat that must be skiped/ignored
NL : [\r\n]+ ; // toss out newlines
WS : [ \t]+ -> skip ; // toss out whitespace and tab
LINE_COMMENT : '//' ~[\r\n]* -> skip ; // toss out line comments
BLOCK_COMMENT : '/*' .*? '*/' -> skip ; // toss out block comments
grammar LPP;

program : NL* structures_declaration variables_declaration program_body ;

structures_declaration : (registry_declaration 
| type_declaration
| procedure_declaration
| function_declaration)
| ;

registry_declaration : REGISTRO ID NL+ variables_declaration FIN REGISTRO NL+ ;

type_declaration : TIPO ID NL+ type NL+ ;

procedure_declaration : PROCEDIMIENTO ID ('(' parameters ')')? NL+ variables_declaration subprogram_body ;

function_declaration : FUNCION ID ('(' parameters ')')? ':' type NL+ variables_declaration subprogram_body ;

parameters : parameter (',' parameter)* ;

parameter : VAR? type ID ;

variables_declaration : variable_declaration*
| ;

variable_declaration : type ids_list NL+ ;

type : ENTERO
| REAL
| BOOLEANO
| CARACTER
| ID
| ARCHIVO SECUENCIAL
| ARCHIVO DE type
| ARREGLO '[' integer_list ']' DE type
| CADENA ( '[' INTEGER_LITERAL ']' )? ;

ids_list : ID (',' ID)* ;

integer_list : INTEGER_LITERAL (',' INTEGER_LITERAL)* ;

subprogram_body : INICIO NL+ statements FIN NL+ ;

program_body : INICIO NL+ statements FIN NL+ EOF ;

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
| return_statement
| open_statement
| close_statement ;

write_statement : ESCRIBA expressions_list NL+ 
| ESCRIBIR expression ',' expressions_list NL+ ;

read_statement : LEA expressions_list NL+
| LEER expression ',' expressions_list NL+ ;

assignment_statement : expression '<-' expression NL+ ;

call_statement : LLAMAR default_procedures ( '(' expressions_list? ')' )? NL+
| LLAMAR default_functions ( '(' expressions_list? ')' )? NL+
| LLAMAR ID ( '(' expressions_list? ')' )? NL+ ;

if_statement : SI expression NL* ENTONCES NL+ statements elif_statement? FIN SI NL+ ;

elif_statement : SINO if_statement
| SINO NL+ statements ;

case_statement : CASO expression NL+ case_option+ elif_case? FIN CASO NL+ ;

case_option : option_expression_list ':' NL+ statements ;

option_expression_list : option_expression (',' option_expression)* ;

option_expression : expression
| expression '->' expression ;

elif_case : SINO ':' NL* statements ;

while_statement : MIENTRAS expression NL* HAGA NL+ statements NL+ ;

for_statement : PARA expression ASSIGNMENT expression HASTA expression NL* HAGA NL+ statements FIN PARA NL+ ;

repeat_statement : REPITA NL+ statements HASTA expression NL+ ;

return_statement : RETORNE expression NL+ ;

open_statement : ABRIR expression COMO expression PARA access_mode NL+ ;

close_statement : CERRAR expression NL+ ;

access_mode : LECTURA ( ',' ESCRITURA )? 
| ESCRITURA ( ',' LECTURA )? ;

expressions_list : expression (',' expression)* ;

expression : '(' expression ')'
| literal
| ID
| expression '.' ID
| expression '[' expressions_list ']'
| default_functions '(' expressions_list? ')'
| ID '(' expressions_list? ')'
| '-' expression
| NO expression
| <assoc=right> expression POWER expression
| expression (MULT | DIV | MOD | INT_DIV) expression
| expression (PLUS | MINUS) expression
| expression (GREATER_THAN | GREATER_EQUAL | LESS_THAN | LESS_EQUAL | EQUAL | NOT_EQUAL) expression
| expression (AND | OR) expression ;

default_procedures : RANDOM_INIT_PROCEDURE
| MOVE_CURSOR_PROCEDURE
| CLEAN_SCREEN_PROCEDURE
| BACKGROUND_COLOR_PROCEDURE
| GOTO_START_PROCEDURE
| TEXT_COLOR_PROCEDURE
| NEW_LINE_PROCEDURE
| GOTO_END_PROCEDURE
| GOTO_GENERAL_PROCEDURE
| PAUSE_PROCEDURE ;

default_functions : ACTUAL_POSITION_FUNCTION
| INT_TO_STRING_FUNCTION
| PRESSED_KEY_FUNCTION
| REAL_TO_STRING_FUNCTION
| CHAR_TO_ASCII_FUNCTION
| GET_CHAR_FUNCTION
| ASCII_VALUE_FUNCTION
| RANDOM_FUNCTION
| LENGTH_FUNCTION
| FDA_FUNCTION ;

literal : INTEGER_LITERAL
| REAL_LITERAL
| CHAR_LITERAL
| STRING_LITERAL
| (VERDADERO | FALSO) ;

// Data types
PROCEDIMIENTO : P R O C E D I M I E N T O ;
BOOLEANO : B O O L E A N O ;
CARACTER : C A R A C T E R ;
REGISTRO : R E G I S T R O ;
ARCHIVO : A R C H I V O ;
ARREGLO : A R R E G L O ;
FUNCION : F U N C I O N ;
CADENA : C A D E N A ;
ENTERO : E N T E R O ;
TIPO : T I P O ;
REAL : R E A L ;
VAR : V A R ;

// Reserved words
SECUENCIAL : S E C U E N C I A L ;
ESCRITURA : E S C R I T U R A ;
ENTONCES : E N T O N C E S ;
ESCRIBIR : E S C R I B I R ;
MIENTRAS : M I E N T R A S ;
ESCRIBA : E S C R I B A ;
LECTURA : L E C T U R A ;
RETORNE : R E T O R N E ;
CERRAR : C E R R A R ;
INICIO : I N I C I O ;
LLAMAR : L L A M A R ;
REPITA : R E P I T A ;
ABRIR : A B R I R ;
HASTA : H A S T A ;
CASO : C A S O ;
COMO : C O M O ;
HAGA : H A G A ;
LEER : L E E R ;
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
RANDOM_INIT_PROCEDURE : I N I C I A L I Z A R '_' A L E A T O R I O ;
MOVE_CURSOR_PROCEDURE : P O S I C I O N A R '_' C U R S O R ;
CLEAN_SCREEN_PROCEDURE : L I M P I A R '_' P A N T A L L A ;
BACKGROUND_COLOR_PROCEDURE : C O L O R '_' F O N D O ;
GOTO_START_PROCEDURE : I R '_' A '_' I N I C I O ;
TEXT_COLOR_PROCEDURE : C O L O R '_' T E X T O ;
NEW_LINE_PROCEDURE : N U E V A '_' L I N E A ;
GOTO_END_PROCEDURE : I R '_' A '_' F I N ;
GOTO_GENERAL_PROCEDURE : I R '_' A ;
PAUSE_PROCEDURE : P A U S A ;

// Default LPP library functions
ACTUAL_POSITION_FUNCTION : P O S I C I O N '_' A C T U A L ;
INT_TO_STRING_FUNCTION : E N T E R O '_' A '_' C A D E N A ;
PRESSED_KEY_FUNCTION : T E C L A '_' P R E S I O N A D A ;
REAL_TO_STRING_FUNCTION : R E A L '_' A '_' C A D E N A ;
CHAR_TO_ASCII_FUNCTION : C A R A C T E R '_' A S C I I ;
GET_CHAR_FUNCTION : O B T E N E R '_' C A R A C T E R ;
ASCII_VALUE_FUNCTION : V A L O R '_' A S C I I ;
RANDOM_FUNCTION : A L E A T O R I O ;
LENGTH_FUNCTION : L O N G I T U D ;
FDA_FUNCTION : F D A ;

// Data values
REAL_LITERAL : DIGIT+ '.' DIGIT+ 
| '.' DIGIT+ ;
INTEGER_LITERAL : DIGIT+ ;
VERDADERO : V E R D A D E R O ;
FALSO : F A L S O ;
CHAR_LITERAL : '\'' CHAR_VALID '\'' ;
STRING_LITERAL : '"' STRING_VALID '"' ;
ID : [a-zA-Z$_][a-zA-Z0-9$_]* ;

fragment DIGIT : [0-9] ;
fragment CHAR_VALID : ~['] 
| '\\\'' 
| '\\\\' ;
fragment STRING_VALID : ~["] 
| '\\"' 
| '\\\\' ;

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
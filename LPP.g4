grammar LPP;

no_expresion: NO no_expresion
| comparison ;

comparison: or_expr ( comparator_op or_expr )* ;

comparator_op: '=' 
| '<' 
| '>' 
| '<=' 
| '>=' 
| '<>' ;

or_expr: and_expr ( 'o' and_expr )* ;

and_expr: arith_expr ( 'y' arith_expr )* ;

arith_expr: term ( ( '+' | '-' ) term )* ;

term: factor ( ( '*' | '/' | 'div' | 'mod' ) factor )* ;

factor: ( '+' | '-' ) factor | power ;

power: atom ( '^' factor )* ;

atom: '(' comparison ')'
| 'verdadero'
| 'falso'
| number
| string
| character
| IDENTIFIER ;

number: integer | real ;

integer:  DIGIT+ ;

real: DIGIT+ '.' DIGIT+ ;

string: '"' ( LETTER | DIGIT | special_character )* '"' ;

character: '\'' LETTER '\'' ;

special_character: ' ' | '!' | '#' | '$' | '%' | '&' | '(' | ')' | '*' | '+' | ',' | '-' | '.' | '/' | ':' | ';' | '<' | '=' | '>' | '?' | '@' | '[' | ']' | '^' | '_' | '`' | '{' | '|' | '}' | '~' ;

NO: 'no' ;

IDENTIFIER: [a-zA-Z][a-zA-Z0-9]* ;
LETTER: [a-zA-Z] ;
DIGIT: [0-9] ;
WS  :   [ \t]+ -> skip ; // toss out whitespace and tab
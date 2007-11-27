lexer grammar C;
options {
  language=Python;

}

T23 : 'typedef' ;
T24 : ';' ;
T25 : ',' ;
T26 : '=' ;
T27 : 'extern' ;
T28 : 'static' ;
T29 : 'auto' ;
T30 : 'register' ;
T31 : 'void' ;
T32 : 'char' ;
T33 : 'short' ;
T34 : 'int' ;
T35 : 'long' ;
T36 : 'float' ;
T37 : 'double' ;
T38 : 'signed' ;
T39 : 'unsigned' ;
T40 : '{' ;
T41 : '}' ;
T42 : 'struct' ;
T43 : 'union' ;
T44 : ':' ;
T45 : 'enum' ;
T46 : 'const' ;
T47 : 'volatile' ;
T48 : 'IN' ;
T49 : 'OUT' ;
T50 : '(' ;
T51 : ')' ;
T52 : '[' ;
T53 : ']' ;
T54 : '*' ;
T55 : '...' ;
T56 : '+' ;
T57 : '-' ;
T58 : '/' ;
T59 : '%' ;
T60 : '++' ;
T61 : '--' ;
T62 : 'sizeof' ;
T63 : '.' ;
T64 : '->' ;
T65 : '&' ;
T66 : '~' ;
T67 : '!' ;
T68 : '*=' ;
T69 : '/=' ;
T70 : '%=' ;
T71 : '+=' ;
T72 : '-=' ;
T73 : '<<=' ;
T74 : '>>=' ;
T75 : '&=' ;
T76 : '^=' ;
T77 : '|=' ;
T78 : '?' ;
T79 : '||' ;
T80 : '&&' ;
T81 : '|' ;
T82 : '^' ;
T83 : '==' ;
T84 : '!=' ;
T85 : '<' ;
T86 : '>' ;
T87 : '<=' ;
T88 : '>=' ;
T89 : '<<' ;
T90 : '>>' ;
T91 : 'case' ;
T92 : 'default' ;
T93 : 'if' ;
T94 : 'else' ;
T95 : 'switch' ;
T96 : 'while' ;
T97 : 'do' ;
T98 : 'for' ;
T99 : 'goto' ;
T100 : 'continue' ;
T101 : 'break' ;
T102 : 'return' ;

// $ANTLR src "C.g" 486
IDENTIFIER
	:	LETTER (LETTER|'0'..'9')*
	;
	
// $ANTLR src "C.g" 490
fragment
LETTER
	:	'$'
	|	'A'..'Z'
	|	'a'..'z'
	|	'_'
	;

// $ANTLR src "C.g" 498
CHARACTER_LITERAL
    :   '\'' ( EscapeSequence | ~('\''|'\\') ) '\''
    ;

// $ANTLR src "C.g" 502
STRING_LITERAL
    :  ('L')? '"' ( EscapeSequence | ~('\\'|'"') )* '"'
    ;

// $ANTLR src "C.g" 506
HEX_LITERAL : '0' ('x'|'X') HexDigit+ IntegerTypeSuffix? ;

// $ANTLR src "C.g" 508
DECIMAL_LITERAL : ('0' | '1'..'9' '0'..'9'*) IntegerTypeSuffix? ;

// $ANTLR src "C.g" 510
OCTAL_LITERAL : '0' ('0'..'7')+ IntegerTypeSuffix? ;

// $ANTLR src "C.g" 512
fragment
HexDigit : ('0'..'9'|'a'..'f'|'A'..'F') ;

// $ANTLR src "C.g" 515
fragment
IntegerTypeSuffix
	:	('u'|'U')? ('l'|'L')
	|	('u'|'U')  ('l'|'L')?
	;

// $ANTLR src "C.g" 521
FLOATING_POINT_LITERAL
    :   ('0'..'9')+ '.' ('0'..'9')* Exponent? FloatTypeSuffix?
    |   '.' ('0'..'9')+ Exponent? FloatTypeSuffix?
    |   ('0'..'9')+ Exponent FloatTypeSuffix?
    |   ('0'..'9')+ Exponent? FloatTypeSuffix
	;

// $ANTLR src "C.g" 528
fragment
Exponent : ('e'|'E') ('+'|'-')? ('0'..'9')+ ;

// $ANTLR src "C.g" 531
fragment
FloatTypeSuffix : ('f'|'F'|'d'|'D') ;

// $ANTLR src "C.g" 534
fragment
EscapeSequence
    :   '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
    |   OctalEscape
    ;

// $ANTLR src "C.g" 540
fragment
OctalEscape
    :   '\\' ('0'..'3') ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7')
    ;

// $ANTLR src "C.g" 547
fragment
UnicodeEscape
    :   '\\' 'u' HexDigit HexDigit HexDigit HexDigit
    ;

// $ANTLR src "C.g" 552
WS  :  (' '|'\r'|'\t'|'\u000C'|'\n') {$channel=HIDDEN;}
    ;

// $ANTLR src "C.g" 555
COMMENT
    :   '/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
    ;

// $ANTLR src "C.g" 559
LINE_COMMENT
    : '//' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    ;

// ignore #line info for now
// $ANTLR src "C.g" 564
LINE_COMMAND 
    : '#' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    ;

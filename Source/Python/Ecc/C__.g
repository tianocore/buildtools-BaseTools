lexer grammar C;
options {
  language=Python;

}

T24 : 'typedef' ;
T25 : ';' ;
T26 : ',' ;
T27 : '=' ;
T28 : 'extern' ;
T29 : 'static' ;
T30 : 'auto' ;
T31 : 'register' ;
T32 : 'void' ;
T33 : 'char' ;
T34 : 'short' ;
T35 : 'int' ;
T36 : 'long' ;
T37 : 'float' ;
T38 : 'double' ;
T39 : 'signed' ;
T40 : 'unsigned' ;
T41 : '{' ;
T42 : '}' ;
T43 : 'struct' ;
T44 : 'union' ;
T45 : ':' ;
T46 : 'enum' ;
T47 : 'const' ;
T48 : 'volatile' ;
T49 : 'IN' ;
T50 : 'OUT' ;
T51 : '(' ;
T52 : ')' ;
T53 : '[' ;
T54 : ']' ;
T55 : '*' ;
T56 : '...' ;
T57 : '+' ;
T58 : '-' ;
T59 : '/' ;
T60 : '%' ;
T61 : '++' ;
T62 : '--' ;
T63 : 'sizeof' ;
T64 : '.' ;
T65 : '->' ;
T66 : '&' ;
T67 : '~' ;
T68 : '!' ;
T69 : '*=' ;
T70 : '/=' ;
T71 : '%=' ;
T72 : '+=' ;
T73 : '-=' ;
T74 : '<<=' ;
T75 : '>>=' ;
T76 : '&=' ;
T77 : '^=' ;
T78 : '|=' ;
T79 : '?' ;
T80 : '||' ;
T81 : '&&' ;
T82 : '|' ;
T83 : '^' ;
T84 : '==' ;
T85 : '!=' ;
T86 : '<' ;
T87 : '>' ;
T88 : '<=' ;
T89 : '>=' ;
T90 : '<<' ;
T91 : '>>' ;
T92 : 'case' ;
T93 : 'default' ;
T94 : 'if' ;
T95 : 'else' ;
T96 : 'switch' ;
T97 : 'while' ;
T98 : 'do' ;
T99 : 'for' ;
T100 : 'goto' ;
T101 : 'continue' ;
T102 : 'break' ;
T103 : 'return' ;

// $ANTLR src "C.g" 455
IDENTIFIER
	:	LETTER (LETTER|'0'..'9')*
	;
	
// $ANTLR src "C.g" 459
fragment
LETTER
	:	'$'
	|	'A'..'Z'
	|	'a'..'z'
	|	'_'
	;

// $ANTLR src "C.g" 467
CHARACTER_LITERAL
    :   '\'' ( EscapeSequence | ~('\''|'\\') ) '\''
    ;

// $ANTLR src "C.g" 471
STRING_LITERAL
    :  ('L')? '"' ( EscapeSequence | ~('\\'|'"') )* '"'
    ;
    
// $ANTLR src "C.g" 475
HEX_LITERAL : '0' ('x'|'X') HexDigit+ IntegerTypeSuffix? ;

// $ANTLR src "C.g" 477
DECIMAL_LITERAL : ('0' | '1'..'9' '0'..'9'*) IntegerTypeSuffix? ;

// $ANTLR src "C.g" 479
OCTAL_LITERAL : '0' ('0'..'7')+ IntegerTypeSuffix? ;

// $ANTLR src "C.g" 481
fragment
HexDigit : ('0'..'9'|'a'..'f'|'A'..'F') ;

// $ANTLR src "C.g" 484
fragment
IntegerTypeSuffix
	:	('u'|'U')? ('l'|'L')
	|	('u'|'U')  ('l'|'L')?
	;

// $ANTLR src "C.g" 490
FLOATING_POINT_LITERAL
    :   ('0'..'9')+ '.' ('0'..'9')* Exponent? FloatTypeSuffix?
    |   '.' ('0'..'9')+ Exponent? FloatTypeSuffix?
    |   ('0'..'9')+ Exponent FloatTypeSuffix?
    |   ('0'..'9')+ Exponent? FloatTypeSuffix
	;

// $ANTLR src "C.g" 497
fragment
Exponent : ('e'|'E') ('+'|'-')? ('0'..'9')+ ;

// $ANTLR src "C.g" 500
fragment
FloatTypeSuffix : ('f'|'F'|'d'|'D') ;

// $ANTLR src "C.g" 503
fragment
EscapeSequence
    :   '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
    |   OctalEscape
    ;

// $ANTLR src "C.g" 509
fragment
OctalEscape
    :   '\\' ('0'..'3') ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7')
    ;

// $ANTLR src "C.g" 516
fragment
UnicodeEscape
    :   '\\' 'u' HexDigit HexDigit HexDigit HexDigit
    ;

// $ANTLR src "C.g" 521
WS  :  (' '|'\r'|'\t'|'\u000C'|'\n') {$channel=HIDDEN;}
    ;

//COMMENT[content]
//@init{content = ''}
//    :   '/*' c=( options {greedy=false;} : . )* {content += c} '*/' {$channel=HIDDEN; print content}
//    ;
// $ANTLR src "C.g" 528
UnicodeVocabulary
    : '\u0003'..'\uFFFE'
    ;
// $ANTLR src "C.g" 531
COMMENT
    :   '/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
    ;


// $ANTLR src "C.g" 536
LINE_COMMENT
    : '//' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    ;

// ignore #line info for now
// $ANTLR src "C.g" 541
LINE_COMMAND 
    : '#' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    ;


grammar C;
options {
    language=Python;
    backtrack=true;
    memoize=true;
    k=2;
}

scope Symbols {
	types;
	inFunc;
}

@members {
    def isTypeName(self, name):
        for scope in reversed(self.Symbols_stack):
            if name in scope.types:
                return True

        return False
        
    def printTokenInfo(self, line, offset, tokenText):
    	print str(line)+ ',' + str(offset) + ':' + str(tokenText)
    	
    def printFuncHeader(self, line, offset, tokenText):
        print str(line)+ ',' + str(offset) + ':' + str(tokenText) + ' is function header.'

}

translation_unit
scope Symbols; // entire file is a scope
@init {
  $Symbols::types = set()
  $Symbols::inFunc = False
}
	: external_declaration+
	;


/*function_declaration
@after{
  print $function_declaration.text
}
	: declaration_specifiers IDENTIFIER '(' parameter_list ')' ';'
	;
*/
external_declaration
options {k=1;}
/*@after{
  print $external_declaration.text
}*/
	: ( declaration_specifiers? declarator declaration* '{' )=> function_definition
	| declaration
	| macro_statement
//	| 'EFI_PEI_CORE_ENTRY_POINT' '(' IDENTIFIER ')'
	;
	


function_definition
scope Symbols;
@init{
  $Symbols::inFunc = True
}
@after{
  print str($function_definition.stop.line) + ',' + str($function_definition.stop.charPositionInLine)
}
	:	declaration_specifiers? declarator
		(	declaration+ compound_statement	// K&R style
		|	compound_statement				// ANSI style
		) //{self.printFuncHeader($declarator.start.line, $declarator.start.charPositionInLine, $declarator.text)}
	;

declaration
scope {
  isTypedef;
}
@init {
  $declaration::isTypedef = False;
}
	: a='typedef' declaration_specifiers? //{self.printTokenInfo($a.line, $a.pos, $a.text)}
	  init_declarator_list ';' // special case, looking for typedef	
	| declaration_specifiers init_declarator_list? ';'
	//| function_declaration
	;

declaration_specifiers
	:   (   storage_class_specifier
		|   type_specifier
        |   type_qualifier
        )+
	;

init_declarator_list
	: init_declarator (',' init_declarator)*
	;

init_declarator
	: declarator ('=' initializer)? 
	//{if not $Symbols::inFunc: self.printTokenInfo($declarator.start.line, $declarator.start.charPositionInLine, $declarator.text)}
	;

storage_class_specifier
	: 'extern'
	| 'static'
	| 'auto'
	| 'register'
	;

type_specifier
options {k=3;}
	: 'void'
	| 'char'
	| 'short'
	| 'int'
	| 'long'
	| 'float'
	| 'double'
	| 'signed'
	| 'unsigned'
	| struct_or_union_specifier
	| enum_specifier
	| (IDENTIFIER declarator)=> type_id
	;

type_id
    :   IDENTIFIER 
    	//{self.printTokenInfo($a.line, $a.pos, $a.text)}
    ;

struct_or_union_specifier
options {k=3;}
scope Symbols; // structs are scopes
@init {
  $Symbols::types = set()
}
	: struct_or_union IDENTIFIER? '{' struct_declaration_list '}'
	| struct_or_union IDENTIFIER
	;

struct_or_union
	: 'struct'
	| 'union'
	;

struct_declaration_list
	: struct_declaration+
	;

struct_declaration
	: specifier_qualifier_list struct_declarator_list ';'
	;

specifier_qualifier_list
	: ( type_qualifier | type_specifier )+
	;

struct_declarator_list
	: struct_declarator (',' struct_declarator)*
	;

struct_declarator
	: declarator (':' constant_expression)?
	| ':' constant_expression
	;

enum_specifier
options {k=3;}
	: 'enum' '{' enumerator_list '}'
	| 'enum' IDENTIFIER '{' enumerator_list '}'
	| 'enum' IDENTIFIER
	;

enumerator_list
	: enumerator (',' enumerator)*
	;

enumerator
	: IDENTIFIER ('=' constant_expression)?
	;

type_qualifier
	: 'const'
	| 'volatile'
	| 'IN'
	| 'OUT'
	;

declarator
	: pointer? direct_declarator
	| pointer
	;

direct_declarator
scope Symbols;
	: IDENTIFIER declarator_suffix*
	  //{if $Symbols::inFunc: self.printFuncName($IDENTIFIER.line, $IDENTIFIER.charPositonInLine, $IDENTIFIER.text)}
	| '(' declarator ')' declarator_suffix+
	;

declarator_suffix
	:   '[' constant_expression ']'
    |   '[' ']'
    |   '(' parameter_type_list ')'
    |   '(' identifier_list ')'
    |   '(' ')'
	;

pointer
	: '*' type_qualifier+ pointer?
	| '*' pointer
	| s='*'
	;

parameter_type_list
	: parameter_list (',' '...')?
	;

parameter_list
	: parameter_declaration (',' parameter_declaration)*
	;

parameter_declaration
	: declaration_specifiers (declarator|abstract_declarator)+
	;

identifier_list
	: i=IDENTIFIER //{print str($i.line) + ":" + $i.text + " is a type"}
	(',' d=IDENTIFIER /*{print str($d.line) + ":" + $d.text + " is a type"}*/)*
	;

type_name
	: specifier_qualifier_list abstract_declarator?
	| type_id
	;

abstract_declarator
	: pointer direct_abstract_declarator?
	| direct_abstract_declarator
	;

direct_abstract_declarator
	:	( '(' abstract_declarator ')' | abstract_declarator_suffix ) abstract_declarator_suffix*
	;

abstract_declarator_suffix
	:	'[' ']'
	|	'[' constant_expression ']'
	|	'(' ')'
	|	'(' parameter_type_list ')'
	;
	
initializer

	: assignment_expression
	| '{' initializer_list ','? '}'
	;

initializer_list
	: initializer (',' initializer )*
	;

// E x p r e s s i o n s

argument_expression_list
	:   assignment_expression (',' assignment_expression)*
	;

additive_expression
	: (multiplicative_expression) ('+' multiplicative_expression | '-' multiplicative_expression)*
	;

multiplicative_expression
	: (cast_expression) ('*' cast_expression | '/' cast_expression | '%' cast_expression)*
	;

cast_expression
	: '(' type_name ')' cast_expression
	| unary_expression
	;

unary_expression
	: postfix_expression
	| '++' unary_expression
	| '--' unary_expression
	| unary_operator cast_expression
	| 'sizeof' unary_expression
	| 'sizeof' '(' type_name ')'
	;

postfix_expression
	:   primary_expression
        (   '[' expression ']'
        |   '(' ')'
        |   '(' argument_expression_list ')'
        |   '.' IDENTIFIER
        |   '*' IDENTIFIER
        |   '->' IDENTIFIER
        |   '++'
        |   '--'
        )*
	;

unary_operator
	: '&'
	| '*'
	| '+'
	| '-'
	| '~'
	| '!'
	;

primary_expression
	: IDENTIFIER
	| constant
	| '(' expression ')'
	;

constant
    :   HEX_LITERAL
    |   OCTAL_LITERAL
    |   DECIMAL_LITERAL
    |	CHARACTER_LITERAL
    |	STRING_LITERAL
    |   FLOATING_POINT_LITERAL
    ;

/////

expression
	: assignment_expression (',' assignment_expression)*
	;

constant_expression
	: conditional_expression
	;

assignment_expression
	: lvalue assignment_operator assignment_expression
	| conditional_expression
	;
	
lvalue
	:	unary_expression
	;

assignment_operator
	: '='
	| '*='
	| '/='
	| '%='
	| '+='
	| '-='
	| '<<='
	| '>>='
	| '&='
	| '^='
	| '|='
	;

conditional_expression
	: logical_or_expression ('?' expression ':' conditional_expression)?
	;

logical_or_expression
	: logical_and_expression ('||' logical_and_expression)*
	;

logical_and_expression
	: inclusive_or_expression ('&&' inclusive_or_expression)*
	;

inclusive_or_expression
	: exclusive_or_expression ('|' exclusive_or_expression)*
	;

exclusive_or_expression
	: and_expression ('^' and_expression)*
	;

and_expression
	: equality_expression ('&' equality_expression)*
	;
equality_expression
	: relational_expression (('=='|'!=') relational_expression)*
	;

relational_expression
	: shift_expression (('<'|'>'|'<='|'>=') shift_expression)*
	;

shift_expression
	: additive_expression (('<<'|'>>') additive_expression)*
	;

// S t a t e m e n t s

statement
	: labeled_statement
	| compound_statement
	| expression_statement
	| selection_statement
	| iteration_statement
	| jump_statement
	| macro_statement
	;

macro_statement
	: IDENTIFIER '(' (IDENTIFIER | declaration*  statement_list?) ')'
	;
	
labeled_statement
	: IDENTIFIER ':' statement
	| 'case' constant_expression ':' statement
	| 'default' ':' statement
	;

compound_statement
scope Symbols; // blocks have a scope of symbols
@init {
  $Symbols::types = set()
}
	: '{' declaration* statement_list? '}'
	;

statement_list
	: statement+
	;

expression_statement
	: ';'
	| expression ';'
	;

selection_statement
	: 'if' '(' expression ')' statement (options {k=1; backtrack=false;}:'else' statement)?
	| 'switch' '(' expression ')' statement
	;

iteration_statement
	: 'while' '(' expression ')' statement
	| 'do' statement 'while' '(' expression ')' ';'
	| 'for' '(' expression_statement expression_statement expression? ')' statement
	;

jump_statement
	: 'goto' IDENTIFIER ';'
	| 'continue' ';'
	| 'break' ';'
	| 'return' ';'
	| 'return' expression ';'
	;

IDENTIFIER
	:	LETTER (LETTER|'0'..'9')*
	;
	
fragment
LETTER
	:	'$'
	|	'A'..'Z'
	|	'a'..'z'
	|	'_'
	;

CHARACTER_LITERAL
    :   '\'' ( EscapeSequence | ~('\''|'\\') ) '\''
    ;

STRING_LITERAL
    :  ('L')? '"' ( EscapeSequence | ~('\\'|'"') )* '"'
    ;
    
HEX_LITERAL : '0' ('x'|'X') HexDigit+ IntegerTypeSuffix? ;

DECIMAL_LITERAL : ('0' | '1'..'9' '0'..'9'*) IntegerTypeSuffix? ;

OCTAL_LITERAL : '0' ('0'..'7')+ IntegerTypeSuffix? ;

fragment
HexDigit : ('0'..'9'|'a'..'f'|'A'..'F') ;

fragment
IntegerTypeSuffix
	:	('u'|'U')? ('l'|'L')
	|	('u'|'U')  ('l'|'L')?
	;

FLOATING_POINT_LITERAL
    :   ('0'..'9')+ '.' ('0'..'9')* Exponent? FloatTypeSuffix?
    |   '.' ('0'..'9')+ Exponent? FloatTypeSuffix?
    |   ('0'..'9')+ Exponent FloatTypeSuffix?
    |   ('0'..'9')+ Exponent? FloatTypeSuffix
	;

fragment
Exponent : ('e'|'E') ('+'|'-')? ('0'..'9')+ ;

fragment
FloatTypeSuffix : ('f'|'F'|'d'|'D') ;

fragment
EscapeSequence
    :   '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
    |   OctalEscape
    ;

fragment
OctalEscape
    :   '\\' ('0'..'3') ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7')
    ;

fragment
UnicodeEscape
    :   '\\' 'u' HexDigit HexDigit HexDigit HexDigit
    ;

WS  :  (' '|'\r'|'\t'|'\u000C'|'\n') {$channel=HIDDEN;}
    ;

//COMMENT[content]
//@init{content = ''}
//    :   '/*' c=( options {greedy=false;} : . )* {content += c} '*/' {$channel=HIDDEN; print content}
//    ;
UnicodeVocabulary
    : '\u0003'..'\uFFFE'
    ;
COMMENT
    :   '/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
    ;


LINE_COMMENT
    : '//' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    ;

// ignore #line info for now
LINE_COMMAND 
    : '#' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    ;

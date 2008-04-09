grammar Depex;
options {
    language=Python;
//    output=AST;
//    ASTLabelType=CommonTree;
//    backtrack=true;
//    memoize=true;
//    k=2;
}

@header {
    from Common.BuildToolError import *
    from Common import EdkLogger as EdkLogger
}

@init {
    self._DepexFile = ''
    self._ExclusiveOpcode = ["BEFORE", "AFTER"]
    self._AboveAllOpcode = ["SOR", "BEFORE", "AFTER"]
    self._ExpressionType = -1
    self._Parentheses = 0
    self.PostfixNotation = []
    self.TokenList = [t.text for t in self.input.tokens]
    self.OpcodeList = []
    self._DepexString = ' '.join(self.TokenList)
}

@members {
    EXPRESSION_BEFORE = 0
    EXPRESSION_AFTER = 1
    EXPRESSION_SOR = 2
    EXPRESSION_BOOL = 3
}

@rulecatch {
except BaseException,e:
    raise
}

// Rule Start
start [FilePath]
@init {self._DepexFile=FilePath}
    : depex_expression
{
    # there should be no more tokens left
    if self.input.LT(1).text != None:
        raise RecognitionException("Ending error")
    if self.PostfixNotation[-1] != 'END':
        self.PostfixNotation.append('END')
}
    ;
catch [RecognitionException, e] {
    LastToken = self.input.LT(-1)
    if LastToken != None:
        LastToken = LastToken.text
    NextToken = self.input.LT(1)
    if NextToken != None:
        NextToken = NextToken.text
    if self._Parentheses != 0:
        Msg = "Parentheses mismatched"
    elif LastToken == 'END':
        Msg = "No more opcode or operand after END"
    elif self._ExpressionType in [self.EXPRESSION_BEFORE, self.EXPRESSION_AFTER]:
        Msg = "Unnecessary expression after [\%s]" \% LastToken
    elif NextToken in ['SOR', 'BEFORE', 'AFTER']:
        Msg = "[\%s] is not expected." \% NextToken
    elif NextToken in ['AND', 'OR']:
        Msg = "Missing operand near [\%s]" \% NextToken
    elif NextToken in [')', '(']:
        Msg = "Parentheses mismatched"
    else:
        Msg = "Missing opcode or operand between [\%s] and [\%s]" \% (LastToken, NextToken)
    EdkLogger.error("GenDepex", PARAMETER_INVALID, Msg, ExtraData=self._DepexString, File=self._DepexFile)
}
catch [] {
    raise
}

depex_expression
    :   'DEPENDENCY_START'?
    	(before_expression|after_expression|sor_expression|bool_expression)
    	'END'?
    	'DEPENDENCY_END'?
    ;

before_expression
    :    Op='BEFORE' V=guid {
self.PostfixNotation.append($Op.text)
self.PostfixNotation.append(V)
self.OpcodeList.append($Op.text)
self._ExpressionType = self.EXPRESSION_BEFORE
}
    ;

after_expression
    :    Op='AFTER' V=guid
{
self.PostfixNotation.append($Op.text)
self.PostfixNotation.append(V)
self.OpcodeList.append($Op.text)
self._ExpressionType = self.EXPRESSION_AFTER
}
    ;

sor_expression
    :    Op='SOR' Expr=bool_statement
{
self.PostfixNotation.append($Op.text)
self.PostfixNotation.extend(Expr)
self.OpcodeList.append($Op.text)
self._ExpressionType = self.EXPRESSION_SOR
}
    ;
    
bool_expression
    :    Expr=bool_statement
{
self.PostfixNotation.extend(Expr)
self._ExpressionType = self.EXPRESSION_BOOL
}
;
    
bool_statement returns [ExpressionList]
@init {
ExpressionList=[]
} :
    SubExpr=bool_factor {ExpressionList.extend(SubExpr)}
    (    'AND' SubExpr=bool_statement {ExpressionList.extend(SubExpr);ExpressionList.append('AND');self.OpcodeList.append('AND')}
        |'OR' SubExpr=bool_statement {ExpressionList.extend(SubExpr);ExpressionList.append('OR');self.OpcodeList.append('OR')}
    )*
;

bool_factor returns [ExpressionList]
@init {
ExpressionList=[]
} :
        Bl='TRUE' {ExpressionList.append($Bl.text)}
    |    Bl='FALSE' {ExpressionList.append($Bl.text)}
    |    Op='NOT' Be=bool_statement {ExpressionList.extend(Be);ExpressionList.append($Op.text)}
    |    ( '(' {self._Parentheses+=1} ) Be=bool_statement {ExpressionList.extend(Be)} ( ')' {self._Parentheses-=1} )
    |    V=guid {ExpressionList.append('PUSH');ExpressionList.append(V)}
    ;
    
guid returns [GuidValue]
@init {
GuidValue = None
} :
    GuidName
{
EdkLogger.error("GenDepex", RESOURCE_NOT_AVAILABLE, "Value of GUID [\%s] is not available" \% $GuidName.text, ExtraData=self._DepexString, File=self._DepexFile)
}
    |    guid_value
{
GuidValue=$guid_value.text
}
    ;

guid_value
    :    '{' Hex ',' Hex ',' Hex ',' '{'? Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex '}'? '}'
    ;


// Token Rules
OpCode
    :    'BEFORE'
    |    'AFTER'
    |    'SOR'
    |    'TRUE'
    |    'FALSE'
    |    'AND'
    |    'OR'
    |    'NOT'
    |    'PUSH'
    |    'END'    
    ;
    
COMMENT
    :    '#' ~('\n'|'\r')* '\r'? '\n' {self.skip()};

WS    :    Whitespace {self.skip()};

GuidName
    :    (Letter|'_') (AlphaNumeric|'_')*
    ;

Hex:    '0' ('x'|'X') ('0'..'9'|'a'..'f'|'A'..'F')+;

fragment
AlphaNumeric
    :    (Letter|'0'..'9')
    ;

fragment
Letter
    :    'A'..'Z'
    |    'a'..'z'
    ;

fragment
Whitespace
    :    (' '|'\t'|'\r'|'\n')
    ;

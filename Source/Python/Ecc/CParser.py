# $ANTLR 3.0.1 C.g 2007-12-12 15:55:52

from antlr3 import *
from antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
CHARACTER_LITERAL=8
LETTER=11
Exponent=15
DECIMAL_LITERAL=7
IntegerTypeSuffix=14
UnicodeVocabulary=20
HexDigit=13
WS=19
LINE_COMMAND=23
COMMENT=21
LINE_COMMENT=22
OCTAL_LITERAL=6
HEX_LITERAL=5
FLOATING_POINT_LITERAL=10
UnicodeEscape=18
EscapeSequence=12
EOF=-1
STRING_LITERAL=9
OctalEscape=17
IDENTIFIER=4
FloatTypeSuffix=16

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "IDENTIFIER", "HEX_LITERAL", "OCTAL_LITERAL", "DECIMAL_LITERAL", "CHARACTER_LITERAL", 
    "STRING_LITERAL", "FLOATING_POINT_LITERAL", "LETTER", "EscapeSequence", 
    "HexDigit", "IntegerTypeSuffix", "Exponent", "FloatTypeSuffix", "OctalEscape", 
    "UnicodeEscape", "WS", "UnicodeVocabulary", "COMMENT", "LINE_COMMENT", 
    "LINE_COMMAND", "'typedef'", "';'", "','", "'='", "'extern'", "'static'", 
    "'auto'", "'register'", "'void'", "'char'", "'short'", "'int'", "'long'", 
    "'float'", "'double'", "'signed'", "'unsigned'", "'{'", "'}'", "'struct'", 
    "'union'", "':'", "'enum'", "'const'", "'volatile'", "'IN'", "'OUT'", 
    "'('", "')'", "'['", "']'", "'*'", "'...'", "'+'", "'-'", "'/'", "'%'", 
    "'++'", "'--'", "'sizeof'", "'.'", "'->'", "'&'", "'~'", "'!'", "'*='", 
    "'/='", "'%='", "'+='", "'-='", "'<<='", "'>>='", "'&='", "'^='", "'|='", 
    "'?'", "'||'", "'&&'", "'|'", "'^'", "'=='", "'!='", "'<'", "'>'", "'<='", 
    "'>='", "'<<'", "'>>'", "'case'", "'default'", "'if'", "'else'", "'switch'", 
    "'while'", "'do'", "'for'", "'goto'", "'continue'", "'break'", "'return'"
]

class Symbols_scope(object):
    def __init__(self):
        self.types = None
        self.inFunc = None


class declaration_scope(object):
    def __init__(self):
        self.isTypedef = None


class CParser(Parser):
    grammarFileName = "C.g"
    tokenNames = tokenNames

    def __init__(self, input):
        Parser.__init__(self, input)
        self.ruleMemo = {}

        self.Symbols_stack = []

	self.declaration_stack = []



                


              
    def isTypeName(self, name):
        for scope in reversed(self.Symbols_stack):
            if name in scope.types:
                return True
    
        return False
        
    def printTokenInfo(self, line, offset, tokenText):
    	print str(line)+ ',' + str(offset) + ':' + str(tokenText)
    	
    def printFuncHeader(self, line, offset, tokenText):
        print str(line)+ ',' + str(offset) + ':' + str(tokenText) + ' is function header.'
    



    # $ANTLR start translation_unit
    # C.g:31:1: translation_unit : ( external_declaration )+ ;
    def translation_unit(self, ):
        self.Symbols_stack.append(Symbols_scope())

        translation_unit_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()
        self.Symbols_stack[-1].inFunc = False

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 1):
                    return 

                # C.g:37:2: ( ( external_declaration )+ )
                # C.g:37:4: ( external_declaration )+
                # C.g:37:4: ( external_declaration )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == IDENTIFIER or LA1_0 == 24 or (28 <= LA1_0 <= 40) or (43 <= LA1_0 <= 44) or (46 <= LA1_0 <= 51) or LA1_0 == 55) :
                        alt1 = 1


                    if alt1 == 1:
                        # C.g:0:0: external_declaration
                        self.following.append(self.FOLLOW_external_declaration_in_translation_unit76)
                        self.external_declaration()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt1 >= 1:
                            break #loop1

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(1, self.input)
                        raise eee

                    cnt1 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 1, translation_unit_StartIndex)

            self.Symbols_stack.pop()

            pass

        return 

    # $ANTLR end translation_unit


    # $ANTLR start external_declaration
    # C.g:48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );
    def external_declaration(self, ):

        external_declaration_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 2):
                    return 

                # C.g:53:2: ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement )
                alt2 = 3
                LA2_0 = self.input.LA(1)

                if ((28 <= LA2_0 <= 31)) :
                    LA2_1 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 1, self.input)

                        raise nvae

                elif (LA2_0 == 32) :
                    LA2_2 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 2, self.input)

                        raise nvae

                elif (LA2_0 == 33) :
                    LA2_3 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 3, self.input)

                        raise nvae

                elif (LA2_0 == 34) :
                    LA2_4 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 4, self.input)

                        raise nvae

                elif (LA2_0 == 35) :
                    LA2_5 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 5, self.input)

                        raise nvae

                elif (LA2_0 == 36) :
                    LA2_6 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 6, self.input)

                        raise nvae

                elif (LA2_0 == 37) :
                    LA2_7 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 7, self.input)

                        raise nvae

                elif (LA2_0 == 38) :
                    LA2_8 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 8, self.input)

                        raise nvae

                elif (LA2_0 == 39) :
                    LA2_9 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 9, self.input)

                        raise nvae

                elif (LA2_0 == 40) :
                    LA2_10 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 10, self.input)

                        raise nvae

                elif ((43 <= LA2_0 <= 44)) :
                    LA2_11 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 11, self.input)

                        raise nvae

                elif (LA2_0 == 46) :
                    LA2_12 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 12, self.input)

                        raise nvae

                elif (LA2_0 == IDENTIFIER) :
                    LA2_13 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    elif (True) :
                        alt2 = 3
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 13, self.input)

                        raise nvae

                elif ((47 <= LA2_0 <= 50)) :
                    LA2_14 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 14, self.input)

                        raise nvae

                elif (LA2_0 == 55) and (self.synpred4()):
                    alt2 = 1
                elif (LA2_0 == 51) and (self.synpred4()):
                    alt2 = 1
                elif (LA2_0 == 24) :
                    alt2 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("48:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 0, self.input)

                    raise nvae

                if alt2 == 1:
                    # C.g:53:4: ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition
                    self.following.append(self.FOLLOW_function_definition_in_external_declaration115)
                    self.function_definition()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt2 == 2:
                    # C.g:54:4: declaration
                    self.following.append(self.FOLLOW_declaration_in_external_declaration120)
                    self.declaration()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt2 == 3:
                    # C.g:55:4: macro_statement
                    self.following.append(self.FOLLOW_macro_statement_in_external_declaration125)
                    self.macro_statement()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 2, external_declaration_StartIndex)

            pass

        return 

    # $ANTLR end external_declaration

    class function_definition_return(object):
        def __init__(self):
            self.start = None
            self.stop = None



    # $ANTLR start function_definition
    # C.g:61:1: function_definition : ( declaration_specifiers )? declarator ( ( declaration )+ compound_statement | compound_statement ) ;
    def function_definition(self, ):
        self.Symbols_stack.append(Symbols_scope())

        retval = self.function_definition_return()
        retval.start = self.input.LT(1)
        function_definition_StartIndex = self.input.index()
        declarator1 = None


              
        self.Symbols_stack[-1].inFunc = True

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 3):
                    return retval

                # C.g:70:2: ( ( declaration_specifiers )? declarator ( ( declaration )+ compound_statement | compound_statement ) )
                # C.g:70:4: ( declaration_specifiers )? declarator ( ( declaration )+ compound_statement | compound_statement )
                # C.g:70:4: ( declaration_specifiers )?
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if ((28 <= LA3_0 <= 40) or (43 <= LA3_0 <= 44) or (46 <= LA3_0 <= 50)) :
                    alt3 = 1
                elif (LA3_0 == IDENTIFIER) :
                    LA3 = self.input.LA(2)
                    if LA3 == 51:
                        LA3_18 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 28 or LA3 == 29 or LA3 == 30 or LA3 == 31:
                        LA3_20 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 32:
                        LA3_21 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 33:
                        LA3_22 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 34:
                        LA3_23 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 35:
                        LA3_24 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 36:
                        LA3_25 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 37:
                        LA3_26 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 38:
                        LA3_27 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 39:
                        LA3_28 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 40:
                        LA3_29 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 43 or LA3 == 44:
                        LA3_30 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 46:
                        LA3_31 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == IDENTIFIER:
                        LA3_32 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 47 or LA3 == 48 or LA3 == 49 or LA3 == 50:
                        LA3_33 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 55:
                        alt3 = 1
                if alt3 == 1:
                    # C.g:0:0: declaration_specifiers
                    self.following.append(self.FOLLOW_declaration_specifiers_in_function_definition153)
                    self.declaration_specifiers()
                    self.following.pop()
                    if self.failed:
                        return retval



                self.following.append(self.FOLLOW_declarator_in_function_definition156)
                declarator1 = self.declarator()
                self.following.pop()
                if self.failed:
                    return retval
                # C.g:71:3: ( ( declaration )+ compound_statement | compound_statement )
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == IDENTIFIER or LA5_0 == 24 or (28 <= LA5_0 <= 40) or (43 <= LA5_0 <= 44) or (46 <= LA5_0 <= 50)) :
                    alt5 = 1
                elif (LA5_0 == 41) :
                    alt5 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return retval

                    nvae = NoViableAltException("71:3: ( ( declaration )+ compound_statement | compound_statement )", 5, 0, self.input)

                    raise nvae

                if alt5 == 1:
                    # C.g:71:5: ( declaration )+ compound_statement
                    # C.g:71:5: ( declaration )+
                    cnt4 = 0
                    while True: #loop4
                        alt4 = 2
                        LA4_0 = self.input.LA(1)

                        if (LA4_0 == IDENTIFIER or LA4_0 == 24 or (28 <= LA4_0 <= 40) or (43 <= LA4_0 <= 44) or (46 <= LA4_0 <= 50)) :
                            alt4 = 1


                        if alt4 == 1:
                            # C.g:0:0: declaration
                            self.following.append(self.FOLLOW_declaration_in_function_definition162)
                            self.declaration()
                            self.following.pop()
                            if self.failed:
                                return retval


                        else:
                            if cnt4 >= 1:
                                break #loop4

                            if self.backtracking > 0:
                                self.failed = True
                                return retval

                            eee = EarlyExitException(4, self.input)
                            raise eee

                        cnt4 += 1


                    self.following.append(self.FOLLOW_compound_statement_in_function_definition165)
                    self.compound_statement()
                    self.following.pop()
                    if self.failed:
                        return retval


                elif alt5 == 2:
                    # C.g:72:5: compound_statement
                    self.following.append(self.FOLLOW_compound_statement_in_function_definition172)
                    self.compound_statement()
                    self.following.pop()
                    if self.failed:
                        return retval



                if self.backtracking == 0:
                    self.printFuncHeader(declarator1.start.line, declarator1.start.charPositionInLine, self.input.toString(declarator1.start,declarator1.stop))




                retval.stop = self.input.LT(-1)

                if self.backtracking == 0:
                           
                    print str(retval.start.line) + ',' + str(retval.start.charPositionInLine)
                    print str(retval.stop.line) + ',' + str(retval.stop.charPositionInLine)



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 3, function_definition_StartIndex)

            self.Symbols_stack.pop()

            pass

        return retval

    # $ANTLR end function_definition


    # $ANTLR start declaration
    # C.g:76:1: declaration : (a= 'typedef' ( declaration_specifiers )? init_declarator_list ';' | declaration_specifiers ( init_declarator_list )? ';' );
    def declaration(self, ):
        self.declaration_stack.append(declaration_scope())
        declaration_StartIndex = self.input.index()
        a = None

               
        self.declaration_stack[-1].isTypedef =  False

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 4):
                    return 

                # C.g:83:2: (a= 'typedef' ( declaration_specifiers )? init_declarator_list ';' | declaration_specifiers ( init_declarator_list )? ';' )
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if (LA8_0 == 24) :
                    alt8 = 1
                elif (LA8_0 == IDENTIFIER or (28 <= LA8_0 <= 40) or (43 <= LA8_0 <= 44) or (46 <= LA8_0 <= 50)) :
                    alt8 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("76:1: declaration : (a= 'typedef' ( declaration_specifiers )? init_declarator_list ';' | declaration_specifiers ( init_declarator_list )? ';' );", 8, 0, self.input)

                    raise nvae

                if alt8 == 1:
                    # C.g:83:4: a= 'typedef' ( declaration_specifiers )? init_declarator_list ';'
                    a = self.input.LT(1)
                    self.match(self.input, 24, self.FOLLOW_24_in_declaration204)
                    if self.failed:
                        return 
                    # C.g:83:16: ( declaration_specifiers )?
                    alt6 = 2
                    LA6_0 = self.input.LA(1)

                    if ((28 <= LA6_0 <= 40) or (43 <= LA6_0 <= 44) or (46 <= LA6_0 <= 50)) :
                        alt6 = 1
                    elif (LA6_0 == IDENTIFIER) :
                        LA6_13 = self.input.LA(2)

                        if (LA6_13 == 51) :
                            LA6_18 = self.input.LA(3)

                            if (self.synpred9()) :
                                alt6 = 1
                        elif (LA6_13 == IDENTIFIER or (28 <= LA6_13 <= 40) or (43 <= LA6_13 <= 44) or (46 <= LA6_13 <= 50) or LA6_13 == 55) :
                            alt6 = 1
                    if alt6 == 1:
                        # C.g:0:0: declaration_specifiers
                        self.following.append(self.FOLLOW_declaration_specifiers_in_declaration206)
                        self.declaration_specifiers()
                        self.following.pop()
                        if self.failed:
                            return 



                    self.following.append(self.FOLLOW_init_declarator_list_in_declaration213)
                    self.init_declarator_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 25, self.FOLLOW_25_in_declaration215)
                    if self.failed:
                        return 


                elif alt8 == 2:
                    # C.g:85:4: declaration_specifiers ( init_declarator_list )? ';'
                    self.following.append(self.FOLLOW_declaration_specifiers_in_declaration221)
                    self.declaration_specifiers()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:85:27: ( init_declarator_list )?
                    alt7 = 2
                    LA7_0 = self.input.LA(1)

                    if (LA7_0 == IDENTIFIER or LA7_0 == 51 or LA7_0 == 55) :
                        alt7 = 1
                    if alt7 == 1:
                        # C.g:0:0: init_declarator_list
                        self.following.append(self.FOLLOW_init_declarator_list_in_declaration223)
                        self.init_declarator_list()
                        self.following.pop()
                        if self.failed:
                            return 



                    self.match(self.input, 25, self.FOLLOW_25_in_declaration226)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 4, declaration_StartIndex)

            self.declaration_stack.pop()
            pass

        return 

    # $ANTLR end declaration


    # $ANTLR start declaration_specifiers
    # C.g:89:1: declaration_specifiers : ( storage_class_specifier | type_specifier | type_qualifier )+ ;
    def declaration_specifiers(self, ):

        declaration_specifiers_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 5):
                    return 

                # C.g:90:2: ( ( storage_class_specifier | type_specifier | type_qualifier )+ )
                # C.g:90:6: ( storage_class_specifier | type_specifier | type_qualifier )+
                # C.g:90:6: ( storage_class_specifier | type_specifier | type_qualifier )+
                cnt9 = 0
                while True: #loop9
                    alt9 = 4
                    LA9 = self.input.LA(1)
                    if LA9 == IDENTIFIER:
                        LA9_2 = self.input.LA(2)

                        if (self.synpred13()) :
                            alt9 = 2


                    elif LA9 == 28 or LA9 == 29 or LA9 == 30 or LA9 == 31:
                        alt9 = 1
                    elif LA9 == 32 or LA9 == 33 or LA9 == 34 or LA9 == 35 or LA9 == 36 or LA9 == 37 or LA9 == 38 or LA9 == 39 or LA9 == 40 or LA9 == 43 or LA9 == 44 or LA9 == 46:
                        alt9 = 2
                    elif LA9 == 47 or LA9 == 48 or LA9 == 49 or LA9 == 50:
                        alt9 = 3

                    if alt9 == 1:
                        # C.g:90:10: storage_class_specifier
                        self.following.append(self.FOLLOW_storage_class_specifier_in_declaration_specifiers245)
                        self.storage_class_specifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt9 == 2:
                        # C.g:91:7: type_specifier
                        self.following.append(self.FOLLOW_type_specifier_in_declaration_specifiers253)
                        self.type_specifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt9 == 3:
                        # C.g:92:13: type_qualifier
                        self.following.append(self.FOLLOW_type_qualifier_in_declaration_specifiers267)
                        self.type_qualifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt9 >= 1:
                            break #loop9

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(9, self.input)
                        raise eee

                    cnt9 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 5, declaration_specifiers_StartIndex)

            pass

        return 

    # $ANTLR end declaration_specifiers


    # $ANTLR start init_declarator_list
    # C.g:96:1: init_declarator_list : init_declarator ( ',' init_declarator )* ;
    def init_declarator_list(self, ):

        init_declarator_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 6):
                    return 

                # C.g:97:2: ( init_declarator ( ',' init_declarator )* )
                # C.g:97:4: init_declarator ( ',' init_declarator )*
                self.following.append(self.FOLLOW_init_declarator_in_init_declarator_list289)
                self.init_declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:97:20: ( ',' init_declarator )*
                while True: #loop10
                    alt10 = 2
                    LA10_0 = self.input.LA(1)

                    if (LA10_0 == 26) :
                        alt10 = 1


                    if alt10 == 1:
                        # C.g:97:21: ',' init_declarator
                        self.match(self.input, 26, self.FOLLOW_26_in_init_declarator_list292)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_init_declarator_in_init_declarator_list294)
                        self.init_declarator()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop10






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 6, init_declarator_list_StartIndex)

            pass

        return 

    # $ANTLR end init_declarator_list


    # $ANTLR start init_declarator
    # C.g:100:1: init_declarator : declarator ( '=' initializer )? ;
    def init_declarator(self, ):

        init_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 7):
                    return 

                # C.g:101:2: ( declarator ( '=' initializer )? )
                # C.g:101:4: declarator ( '=' initializer )?
                self.following.append(self.FOLLOW_declarator_in_init_declarator307)
                self.declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:101:15: ( '=' initializer )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 27) :
                    alt11 = 1
                if alt11 == 1:
                    # C.g:101:16: '=' initializer
                    self.match(self.input, 27, self.FOLLOW_27_in_init_declarator310)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_initializer_in_init_declarator312)
                    self.initializer()
                    self.following.pop()
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 7, init_declarator_StartIndex)

            pass

        return 

    # $ANTLR end init_declarator


    # $ANTLR start storage_class_specifier
    # C.g:105:1: storage_class_specifier : ( 'extern' | 'static' | 'auto' | 'register' );
    def storage_class_specifier(self, ):

        storage_class_specifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 8):
                    return 

                # C.g:106:2: ( 'extern' | 'static' | 'auto' | 'register' )
                # C.g:
                if (28 <= self.input.LA(1) <= 31):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_storage_class_specifier0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 8, storage_class_specifier_StartIndex)

            pass

        return 

    # $ANTLR end storage_class_specifier


    # $ANTLR start type_specifier
    # C.g:112:1: type_specifier options {k=3; } : ( 'void' | 'char' | 'short' | 'int' | 'long' | 'float' | 'double' | 'signed' | 'unsigned' | struct_or_union_specifier | enum_specifier | ( IDENTIFIER declarator )=> type_id );
    def type_specifier(self, ):

        type_specifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 9):
                    return 

                # C.g:114:2: ( 'void' | 'char' | 'short' | 'int' | 'long' | 'float' | 'double' | 'signed' | 'unsigned' | struct_or_union_specifier | enum_specifier | ( IDENTIFIER declarator )=> type_id )
                alt12 = 12
                LA12_0 = self.input.LA(1)

                if (LA12_0 == 32) :
                    alt12 = 1
                elif (LA12_0 == 33) :
                    alt12 = 2
                elif (LA12_0 == 34) :
                    alt12 = 3
                elif (LA12_0 == 35) :
                    alt12 = 4
                elif (LA12_0 == 36) :
                    alt12 = 5
                elif (LA12_0 == 37) :
                    alt12 = 6
                elif (LA12_0 == 38) :
                    alt12 = 7
                elif (LA12_0 == 39) :
                    alt12 = 8
                elif (LA12_0 == 40) :
                    alt12 = 9
                elif ((43 <= LA12_0 <= 44)) :
                    alt12 = 10
                elif (LA12_0 == 46) :
                    alt12 = 11
                elif (LA12_0 == IDENTIFIER) and (self.synpred31()):
                    alt12 = 12
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("112:1: type_specifier options {k=3; } : ( 'void' | 'char' | 'short' | 'int' | 'long' | 'float' | 'double' | 'signed' | 'unsigned' | struct_or_union_specifier | enum_specifier | ( IDENTIFIER declarator )=> type_id );", 12, 0, self.input)

                    raise nvae

                if alt12 == 1:
                    # C.g:114:4: 'void'
                    self.match(self.input, 32, self.FOLLOW_32_in_type_specifier361)
                    if self.failed:
                        return 


                elif alt12 == 2:
                    # C.g:115:4: 'char'
                    self.match(self.input, 33, self.FOLLOW_33_in_type_specifier366)
                    if self.failed:
                        return 


                elif alt12 == 3:
                    # C.g:116:4: 'short'
                    self.match(self.input, 34, self.FOLLOW_34_in_type_specifier371)
                    if self.failed:
                        return 


                elif alt12 == 4:
                    # C.g:117:4: 'int'
                    self.match(self.input, 35, self.FOLLOW_35_in_type_specifier376)
                    if self.failed:
                        return 


                elif alt12 == 5:
                    # C.g:118:4: 'long'
                    self.match(self.input, 36, self.FOLLOW_36_in_type_specifier381)
                    if self.failed:
                        return 


                elif alt12 == 6:
                    # C.g:119:4: 'float'
                    self.match(self.input, 37, self.FOLLOW_37_in_type_specifier386)
                    if self.failed:
                        return 


                elif alt12 == 7:
                    # C.g:120:4: 'double'
                    self.match(self.input, 38, self.FOLLOW_38_in_type_specifier391)
                    if self.failed:
                        return 


                elif alt12 == 8:
                    # C.g:121:4: 'signed'
                    self.match(self.input, 39, self.FOLLOW_39_in_type_specifier396)
                    if self.failed:
                        return 


                elif alt12 == 9:
                    # C.g:122:4: 'unsigned'
                    self.match(self.input, 40, self.FOLLOW_40_in_type_specifier401)
                    if self.failed:
                        return 


                elif alt12 == 10:
                    # C.g:123:4: struct_or_union_specifier
                    self.following.append(self.FOLLOW_struct_or_union_specifier_in_type_specifier406)
                    self.struct_or_union_specifier()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt12 == 11:
                    # C.g:124:4: enum_specifier
                    self.following.append(self.FOLLOW_enum_specifier_in_type_specifier411)
                    self.enum_specifier()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt12 == 12:
                    # C.g:125:4: ( IDENTIFIER declarator )=> type_id
                    self.following.append(self.FOLLOW_type_id_in_type_specifier423)
                    self.type_id()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 9, type_specifier_StartIndex)

            pass

        return 

    # $ANTLR end type_specifier


    # $ANTLR start type_id
    # C.g:128:1: type_id : IDENTIFIER ;
    def type_id(self, ):

        type_id_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 10):
                    return 

                # C.g:129:5: ( IDENTIFIER )
                # C.g:129:9: IDENTIFIER
                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_type_id439)
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 10, type_id_StartIndex)

            pass

        return 

    # $ANTLR end type_id


    # $ANTLR start struct_or_union_specifier
    # C.g:133:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );
    def struct_or_union_specifier(self, ):
        self.Symbols_stack.append(Symbols_scope())

        struct_or_union_specifier_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 11):
                    return 

                # C.g:139:2: ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER )
                alt14 = 2
                LA14_0 = self.input.LA(1)

                if ((43 <= LA14_0 <= 44)) :
                    LA14_1 = self.input.LA(2)

                    if (LA14_1 == IDENTIFIER) :
                        LA14_2 = self.input.LA(3)

                        if (LA14_2 == 41) :
                            alt14 = 1
                        elif (LA14_2 == EOF or LA14_2 == IDENTIFIER or LA14_2 == 25 or (28 <= LA14_2 <= 40) or (43 <= LA14_2 <= 53) or LA14_2 == 55) :
                            alt14 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("133:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );", 14, 2, self.input)

                            raise nvae

                    elif (LA14_1 == 41) :
                        alt14 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("133:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );", 14, 1, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("133:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );", 14, 0, self.input)

                    raise nvae

                if alt14 == 1:
                    # C.g:139:4: struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}'
                    self.following.append(self.FOLLOW_struct_or_union_in_struct_or_union_specifier478)
                    self.struct_or_union()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:139:20: ( IDENTIFIER )?
                    alt13 = 2
                    LA13_0 = self.input.LA(1)

                    if (LA13_0 == IDENTIFIER) :
                        alt13 = 1
                    if alt13 == 1:
                        # C.g:0:0: IDENTIFIER
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_struct_or_union_specifier480)
                        if self.failed:
                            return 



                    self.match(self.input, 41, self.FOLLOW_41_in_struct_or_union_specifier483)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_struct_declaration_list_in_struct_or_union_specifier485)
                    self.struct_declaration_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 42, self.FOLLOW_42_in_struct_or_union_specifier487)
                    if self.failed:
                        return 


                elif alt14 == 2:
                    # C.g:140:4: struct_or_union IDENTIFIER
                    self.following.append(self.FOLLOW_struct_or_union_in_struct_or_union_specifier492)
                    self.struct_or_union()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_struct_or_union_specifier494)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 11, struct_or_union_specifier_StartIndex)

            self.Symbols_stack.pop()

            pass

        return 

    # $ANTLR end struct_or_union_specifier


    # $ANTLR start struct_or_union
    # C.g:143:1: struct_or_union : ( 'struct' | 'union' );
    def struct_or_union(self, ):

        struct_or_union_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 12):
                    return 

                # C.g:144:2: ( 'struct' | 'union' )
                # C.g:
                if (43 <= self.input.LA(1) <= 44):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_struct_or_union0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 12, struct_or_union_StartIndex)

            pass

        return 

    # $ANTLR end struct_or_union


    # $ANTLR start struct_declaration_list
    # C.g:148:1: struct_declaration_list : ( struct_declaration )+ ;
    def struct_declaration_list(self, ):

        struct_declaration_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 13):
                    return 

                # C.g:149:2: ( ( struct_declaration )+ )
                # C.g:149:4: ( struct_declaration )+
                # C.g:149:4: ( struct_declaration )+
                cnt15 = 0
                while True: #loop15
                    alt15 = 2
                    LA15_0 = self.input.LA(1)

                    if (LA15_0 == IDENTIFIER or (32 <= LA15_0 <= 40) or (43 <= LA15_0 <= 44) or (46 <= LA15_0 <= 50)) :
                        alt15 = 1


                    if alt15 == 1:
                        # C.g:0:0: struct_declaration
                        self.following.append(self.FOLLOW_struct_declaration_in_struct_declaration_list521)
                        self.struct_declaration()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt15 >= 1:
                            break #loop15

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(15, self.input)
                        raise eee

                    cnt15 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 13, struct_declaration_list_StartIndex)

            pass

        return 

    # $ANTLR end struct_declaration_list


    # $ANTLR start struct_declaration
    # C.g:152:1: struct_declaration : specifier_qualifier_list struct_declarator_list ';' ;
    def struct_declaration(self, ):

        struct_declaration_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 14):
                    return 

                # C.g:153:2: ( specifier_qualifier_list struct_declarator_list ';' )
                # C.g:153:4: specifier_qualifier_list struct_declarator_list ';'
                self.following.append(self.FOLLOW_specifier_qualifier_list_in_struct_declaration533)
                self.specifier_qualifier_list()
                self.following.pop()
                if self.failed:
                    return 
                self.following.append(self.FOLLOW_struct_declarator_list_in_struct_declaration535)
                self.struct_declarator_list()
                self.following.pop()
                if self.failed:
                    return 
                self.match(self.input, 25, self.FOLLOW_25_in_struct_declaration537)
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 14, struct_declaration_StartIndex)

            pass

        return 

    # $ANTLR end struct_declaration


    # $ANTLR start specifier_qualifier_list
    # C.g:156:1: specifier_qualifier_list : ( type_qualifier | type_specifier )+ ;
    def specifier_qualifier_list(self, ):

        specifier_qualifier_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 15):
                    return 

                # C.g:157:2: ( ( type_qualifier | type_specifier )+ )
                # C.g:157:4: ( type_qualifier | type_specifier )+
                # C.g:157:4: ( type_qualifier | type_specifier )+
                cnt16 = 0
                while True: #loop16
                    alt16 = 3
                    LA16 = self.input.LA(1)
                    if LA16 == IDENTIFIER:
                        LA16 = self.input.LA(2)
                        if LA16 == 53:
                            LA16_20 = self.input.LA(3)

                            if (self.synpred37()) :
                                alt16 = 2


                        elif LA16 == 51:
                            LA16_21 = self.input.LA(3)

                            if (self.synpred37()) :
                                alt16 = 2


                        elif LA16 == 45:
                            LA16_22 = self.input.LA(3)

                            if (self.synpred37()) :
                                alt16 = 2


                        elif LA16 == EOF or LA16 == IDENTIFIER or LA16 == 32 or LA16 == 33 or LA16 == 34 or LA16 == 35 or LA16 == 36 or LA16 == 37 or LA16 == 38 or LA16 == 39 or LA16 == 40 or LA16 == 43 or LA16 == 44 or LA16 == 46 or LA16 == 47 or LA16 == 48 or LA16 == 49 or LA16 == 50 or LA16 == 52 or LA16 == 55:
                            alt16 = 2

                    elif LA16 == 47 or LA16 == 48 or LA16 == 49 or LA16 == 50:
                        alt16 = 1
                    elif LA16 == 32 or LA16 == 33 or LA16 == 34 or LA16 == 35 or LA16 == 36 or LA16 == 37 or LA16 == 38 or LA16 == 39 or LA16 == 40 or LA16 == 43 or LA16 == 44 or LA16 == 46:
                        alt16 = 2

                    if alt16 == 1:
                        # C.g:157:6: type_qualifier
                        self.following.append(self.FOLLOW_type_qualifier_in_specifier_qualifier_list550)
                        self.type_qualifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt16 == 2:
                        # C.g:157:23: type_specifier
                        self.following.append(self.FOLLOW_type_specifier_in_specifier_qualifier_list554)
                        self.type_specifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt16 >= 1:
                            break #loop16

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(16, self.input)
                        raise eee

                    cnt16 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 15, specifier_qualifier_list_StartIndex)

            pass

        return 

    # $ANTLR end specifier_qualifier_list


    # $ANTLR start struct_declarator_list
    # C.g:160:1: struct_declarator_list : struct_declarator ( ',' struct_declarator )* ;
    def struct_declarator_list(self, ):

        struct_declarator_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 16):
                    return 

                # C.g:161:2: ( struct_declarator ( ',' struct_declarator )* )
                # C.g:161:4: struct_declarator ( ',' struct_declarator )*
                self.following.append(self.FOLLOW_struct_declarator_in_struct_declarator_list568)
                self.struct_declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:161:22: ( ',' struct_declarator )*
                while True: #loop17
                    alt17 = 2
                    LA17_0 = self.input.LA(1)

                    if (LA17_0 == 26) :
                        alt17 = 1


                    if alt17 == 1:
                        # C.g:161:23: ',' struct_declarator
                        self.match(self.input, 26, self.FOLLOW_26_in_struct_declarator_list571)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_struct_declarator_in_struct_declarator_list573)
                        self.struct_declarator()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop17






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 16, struct_declarator_list_StartIndex)

            pass

        return 

    # $ANTLR end struct_declarator_list


    # $ANTLR start struct_declarator
    # C.g:164:1: struct_declarator : ( declarator ( ':' constant_expression )? | ':' constant_expression );
    def struct_declarator(self, ):

        struct_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 17):
                    return 

                # C.g:165:2: ( declarator ( ':' constant_expression )? | ':' constant_expression )
                alt19 = 2
                LA19_0 = self.input.LA(1)

                if (LA19_0 == IDENTIFIER or LA19_0 == 51 or LA19_0 == 55) :
                    alt19 = 1
                elif (LA19_0 == 45) :
                    alt19 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("164:1: struct_declarator : ( declarator ( ':' constant_expression )? | ':' constant_expression );", 19, 0, self.input)

                    raise nvae

                if alt19 == 1:
                    # C.g:165:4: declarator ( ':' constant_expression )?
                    self.following.append(self.FOLLOW_declarator_in_struct_declarator586)
                    self.declarator()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:165:15: ( ':' constant_expression )?
                    alt18 = 2
                    LA18_0 = self.input.LA(1)

                    if (LA18_0 == 45) :
                        alt18 = 1
                    if alt18 == 1:
                        # C.g:165:16: ':' constant_expression
                        self.match(self.input, 45, self.FOLLOW_45_in_struct_declarator589)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_constant_expression_in_struct_declarator591)
                        self.constant_expression()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt19 == 2:
                    # C.g:166:4: ':' constant_expression
                    self.match(self.input, 45, self.FOLLOW_45_in_struct_declarator598)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_struct_declarator600)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 17, struct_declarator_StartIndex)

            pass

        return 

    # $ANTLR end struct_declarator


    # $ANTLR start enum_specifier
    # C.g:169:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );
    def enum_specifier(self, ):

        enum_specifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 18):
                    return 

                # C.g:171:2: ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER )
                alt20 = 3
                LA20_0 = self.input.LA(1)

                if (LA20_0 == 46) :
                    LA20_1 = self.input.LA(2)

                    if (LA20_1 == IDENTIFIER) :
                        LA20_2 = self.input.LA(3)

                        if (LA20_2 == 41) :
                            alt20 = 2
                        elif (LA20_2 == EOF or LA20_2 == IDENTIFIER or LA20_2 == 25 or (28 <= LA20_2 <= 40) or (43 <= LA20_2 <= 53) or LA20_2 == 55) :
                            alt20 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("169:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );", 20, 2, self.input)

                            raise nvae

                    elif (LA20_1 == 41) :
                        alt20 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("169:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );", 20, 1, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("169:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );", 20, 0, self.input)

                    raise nvae

                if alt20 == 1:
                    # C.g:171:4: 'enum' '{' enumerator_list '}'
                    self.match(self.input, 46, self.FOLLOW_46_in_enum_specifier618)
                    if self.failed:
                        return 
                    self.match(self.input, 41, self.FOLLOW_41_in_enum_specifier620)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_enumerator_list_in_enum_specifier622)
                    self.enumerator_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 42, self.FOLLOW_42_in_enum_specifier624)
                    if self.failed:
                        return 


                elif alt20 == 2:
                    # C.g:172:4: 'enum' IDENTIFIER '{' enumerator_list '}'
                    self.match(self.input, 46, self.FOLLOW_46_in_enum_specifier629)
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_enum_specifier631)
                    if self.failed:
                        return 
                    self.match(self.input, 41, self.FOLLOW_41_in_enum_specifier633)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_enumerator_list_in_enum_specifier635)
                    self.enumerator_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 42, self.FOLLOW_42_in_enum_specifier637)
                    if self.failed:
                        return 


                elif alt20 == 3:
                    # C.g:173:4: 'enum' IDENTIFIER
                    self.match(self.input, 46, self.FOLLOW_46_in_enum_specifier642)
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_enum_specifier644)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 18, enum_specifier_StartIndex)

            pass

        return 

    # $ANTLR end enum_specifier


    # $ANTLR start enumerator_list
    # C.g:176:1: enumerator_list : enumerator ( ',' enumerator )* ;
    def enumerator_list(self, ):

        enumerator_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 19):
                    return 

                # C.g:177:2: ( enumerator ( ',' enumerator )* )
                # C.g:177:4: enumerator ( ',' enumerator )*
                self.following.append(self.FOLLOW_enumerator_in_enumerator_list655)
                self.enumerator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:177:15: ( ',' enumerator )*
                while True: #loop21
                    alt21 = 2
                    LA21_0 = self.input.LA(1)

                    if (LA21_0 == 26) :
                        alt21 = 1


                    if alt21 == 1:
                        # C.g:177:16: ',' enumerator
                        self.match(self.input, 26, self.FOLLOW_26_in_enumerator_list658)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_enumerator_in_enumerator_list660)
                        self.enumerator()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop21






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 19, enumerator_list_StartIndex)

            pass

        return 

    # $ANTLR end enumerator_list


    # $ANTLR start enumerator
    # C.g:180:1: enumerator : IDENTIFIER ( '=' constant_expression )? ;
    def enumerator(self, ):

        enumerator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 20):
                    return 

                # C.g:181:2: ( IDENTIFIER ( '=' constant_expression )? )
                # C.g:181:4: IDENTIFIER ( '=' constant_expression )?
                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_enumerator673)
                if self.failed:
                    return 
                # C.g:181:15: ( '=' constant_expression )?
                alt22 = 2
                LA22_0 = self.input.LA(1)

                if (LA22_0 == 27) :
                    alt22 = 1
                if alt22 == 1:
                    # C.g:181:16: '=' constant_expression
                    self.match(self.input, 27, self.FOLLOW_27_in_enumerator676)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_enumerator678)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 20, enumerator_StartIndex)

            pass

        return 

    # $ANTLR end enumerator


    # $ANTLR start type_qualifier
    # C.g:184:1: type_qualifier : ( 'const' | 'volatile' | 'IN' | 'OUT' );
    def type_qualifier(self, ):

        type_qualifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 21):
                    return 

                # C.g:185:2: ( 'const' | 'volatile' | 'IN' | 'OUT' )
                # C.g:
                if (47 <= self.input.LA(1) <= 50):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_type_qualifier0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 21, type_qualifier_StartIndex)

            pass

        return 

    # $ANTLR end type_qualifier

    class declarator_return(object):
        def __init__(self):
            self.start = None
            self.stop = None



    # $ANTLR start declarator
    # C.g:191:1: declarator : ( ( pointer )? direct_declarator | pointer );
    def declarator(self, ):

        retval = self.declarator_return()
        retval.start = self.input.LT(1)
        declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 22):
                    return retval

                # C.g:192:2: ( ( pointer )? direct_declarator | pointer )
                alt24 = 2
                LA24_0 = self.input.LA(1)

                if (LA24_0 == 55) :
                    LA24_1 = self.input.LA(2)

                    if (self.synpred49()) :
                        alt24 = 1
                    elif (True) :
                        alt24 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return retval

                        nvae = NoViableAltException("191:1: declarator : ( ( pointer )? direct_declarator | pointer );", 24, 1, self.input)

                        raise nvae

                elif (LA24_0 == IDENTIFIER or LA24_0 == 51) :
                    alt24 = 1
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return retval

                    nvae = NoViableAltException("191:1: declarator : ( ( pointer )? direct_declarator | pointer );", 24, 0, self.input)

                    raise nvae

                if alt24 == 1:
                    # C.g:192:4: ( pointer )? direct_declarator
                    # C.g:192:4: ( pointer )?
                    alt23 = 2
                    LA23_0 = self.input.LA(1)

                    if (LA23_0 == 55) :
                        alt23 = 1
                    if alt23 == 1:
                        # C.g:0:0: pointer
                        self.following.append(self.FOLLOW_pointer_in_declarator717)
                        self.pointer()
                        self.following.pop()
                        if self.failed:
                            return retval



                    self.following.append(self.FOLLOW_direct_declarator_in_declarator720)
                    self.direct_declarator()
                    self.following.pop()
                    if self.failed:
                        return retval


                elif alt24 == 2:
                    # C.g:193:4: pointer
                    self.following.append(self.FOLLOW_pointer_in_declarator725)
                    self.pointer()
                    self.following.pop()
                    if self.failed:
                        return retval


                retval.stop = self.input.LT(-1)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 22, declarator_StartIndex)

            pass

        return retval

    # $ANTLR end declarator


    # $ANTLR start direct_declarator
    # C.g:196:1: direct_declarator : ( IDENTIFIER ( declarator_suffix )* | '(' declarator ')' ( declarator_suffix )+ );
    def direct_declarator(self, ):
        self.Symbols_stack.append(Symbols_scope())

        direct_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 23):
                    return 

                # C.g:198:2: ( IDENTIFIER ( declarator_suffix )* | '(' declarator ')' ( declarator_suffix )+ )
                alt27 = 2
                LA27_0 = self.input.LA(1)

                if (LA27_0 == IDENTIFIER) :
                    alt27 = 1
                elif (LA27_0 == 51) :
                    alt27 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("196:1: direct_declarator : ( IDENTIFIER ( declarator_suffix )* | '(' declarator ')' ( declarator_suffix )+ );", 27, 0, self.input)

                    raise nvae

                if alt27 == 1:
                    # C.g:198:4: IDENTIFIER ( declarator_suffix )*
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_direct_declarator741)
                    if self.failed:
                        return 
                    # C.g:198:15: ( declarator_suffix )*
                    while True: #loop25
                        alt25 = 2
                        LA25_0 = self.input.LA(1)

                        if (LA25_0 == 51) :
                            LA25 = self.input.LA(2)
                            if LA25 == 52:
                                LA25_26 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == IDENTIFIER:
                                LA25_27 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 28 or LA25 == 29 or LA25 == 30 or LA25 == 31:
                                LA25_28 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 32:
                                LA25_29 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 33:
                                LA25_30 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 34:
                                LA25_31 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 35:
                                LA25_32 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 36:
                                LA25_33 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 37:
                                LA25_34 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 38:
                                LA25_35 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 39:
                                LA25_36 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 40:
                                LA25_37 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 43 or LA25 == 44:
                                LA25_38 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 46:
                                LA25_39 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 47 or LA25 == 48 or LA25 == 49 or LA25 == 50:
                                LA25_40 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1



                        elif (LA25_0 == 53) :
                            LA25 = self.input.LA(2)
                            if LA25 == 54:
                                LA25_44 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 51:
                                LA25_45 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == IDENTIFIER:
                                LA25_46 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == HEX_LITERAL or LA25 == OCTAL_LITERAL or LA25 == DECIMAL_LITERAL or LA25 == CHARACTER_LITERAL or LA25 == STRING_LITERAL or LA25 == FLOATING_POINT_LITERAL:
                                LA25_47 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 61:
                                LA25_48 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 62:
                                LA25_49 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 55 or LA25 == 57 or LA25 == 58 or LA25 == 66 or LA25 == 67 or LA25 == 68:
                                LA25_50 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 63:
                                LA25_51 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1





                        if alt25 == 1:
                            # C.g:0:0: declarator_suffix
                            self.following.append(self.FOLLOW_declarator_suffix_in_direct_declarator743)
                            self.declarator_suffix()
                            self.following.pop()
                            if self.failed:
                                return 


                        else:
                            break #loop25




                elif alt27 == 2:
                    # C.g:200:4: '(' declarator ')' ( declarator_suffix )+
                    self.match(self.input, 51, self.FOLLOW_51_in_direct_declarator753)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_declarator_in_direct_declarator755)
                    self.declarator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_direct_declarator757)
                    if self.failed:
                        return 
                    # C.g:200:23: ( declarator_suffix )+
                    cnt26 = 0
                    while True: #loop26
                        alt26 = 2
                        LA26_0 = self.input.LA(1)

                        if (LA26_0 == 51) :
                            LA26 = self.input.LA(2)
                            if LA26 == 52:
                                LA26_26 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 28 or LA26 == 29 or LA26 == 30 or LA26 == 31:
                                LA26_27 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 32:
                                LA26_28 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 33:
                                LA26_29 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 34:
                                LA26_30 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 35:
                                LA26_31 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 36:
                                LA26_32 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 37:
                                LA26_33 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 38:
                                LA26_34 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 39:
                                LA26_35 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 40:
                                LA26_36 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 43 or LA26 == 44:
                                LA26_37 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 46:
                                LA26_38 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == IDENTIFIER:
                                LA26_39 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 47 or LA26 == 48 or LA26 == 49 or LA26 == 50:
                                LA26_40 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1



                        elif (LA26_0 == 53) :
                            LA26 = self.input.LA(2)
                            if LA26 == 54:
                                LA26_44 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 51:
                                LA26_45 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == IDENTIFIER:
                                LA26_46 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == HEX_LITERAL or LA26 == OCTAL_LITERAL or LA26 == DECIMAL_LITERAL or LA26 == CHARACTER_LITERAL or LA26 == STRING_LITERAL or LA26 == FLOATING_POINT_LITERAL:
                                LA26_47 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 61:
                                LA26_48 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 62:
                                LA26_49 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 55 or LA26 == 57 or LA26 == 58 or LA26 == 66 or LA26 == 67 or LA26 == 68:
                                LA26_50 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 63:
                                LA26_51 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1





                        if alt26 == 1:
                            # C.g:0:0: declarator_suffix
                            self.following.append(self.FOLLOW_declarator_suffix_in_direct_declarator759)
                            self.declarator_suffix()
                            self.following.pop()
                            if self.failed:
                                return 


                        else:
                            if cnt26 >= 1:
                                break #loop26

                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            eee = EarlyExitException(26, self.input)
                            raise eee

                        cnt26 += 1





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 23, direct_declarator_StartIndex)

            self.Symbols_stack.pop()

            pass

        return 

    # $ANTLR end direct_declarator


    # $ANTLR start declarator_suffix
    # C.g:203:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );
    def declarator_suffix(self, ):

        declarator_suffix_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 24):
                    return 

                # C.g:204:2: ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' )
                alt28 = 5
                LA28_0 = self.input.LA(1)

                if (LA28_0 == 53) :
                    LA28_1 = self.input.LA(2)

                    if (LA28_1 == 54) :
                        alt28 = 2
                    elif ((IDENTIFIER <= LA28_1 <= FLOATING_POINT_LITERAL) or LA28_1 == 51 or LA28_1 == 55 or (57 <= LA28_1 <= 58) or (61 <= LA28_1 <= 63) or (66 <= LA28_1 <= 68)) :
                        alt28 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("203:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 28, 1, self.input)

                        raise nvae

                elif (LA28_0 == 51) :
                    LA28 = self.input.LA(2)
                    if LA28 == 52:
                        alt28 = 5
                    elif LA28 == 28 or LA28 == 29 or LA28 == 30 or LA28 == 31 or LA28 == 32 or LA28 == 33 or LA28 == 34 or LA28 == 35 or LA28 == 36 or LA28 == 37 or LA28 == 38 or LA28 == 39 or LA28 == 40 or LA28 == 43 or LA28 == 44 or LA28 == 46 or LA28 == 47 or LA28 == 48 or LA28 == 49 or LA28 == 50:
                        alt28 = 3
                    elif LA28 == IDENTIFIER:
                        LA28_24 = self.input.LA(3)

                        if (self.synpred55()) :
                            alt28 = 3
                        elif (self.synpred56()) :
                            alt28 = 4
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("203:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 28, 24, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("203:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 28, 2, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("203:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 28, 0, self.input)

                    raise nvae

                if alt28 == 1:
                    # C.g:204:6: '[' constant_expression ']'
                    self.match(self.input, 53, self.FOLLOW_53_in_declarator_suffix773)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_declarator_suffix775)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 54, self.FOLLOW_54_in_declarator_suffix777)
                    if self.failed:
                        return 


                elif alt28 == 2:
                    # C.g:205:9: '[' ']'
                    self.match(self.input, 53, self.FOLLOW_53_in_declarator_suffix787)
                    if self.failed:
                        return 
                    self.match(self.input, 54, self.FOLLOW_54_in_declarator_suffix789)
                    if self.failed:
                        return 


                elif alt28 == 3:
                    # C.g:206:9: '(' parameter_type_list ')'
                    self.match(self.input, 51, self.FOLLOW_51_in_declarator_suffix799)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_parameter_type_list_in_declarator_suffix801)
                    self.parameter_type_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_declarator_suffix803)
                    if self.failed:
                        return 


                elif alt28 == 4:
                    # C.g:207:9: '(' identifier_list ')'
                    self.match(self.input, 51, self.FOLLOW_51_in_declarator_suffix813)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_identifier_list_in_declarator_suffix815)
                    self.identifier_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_declarator_suffix817)
                    if self.failed:
                        return 


                elif alt28 == 5:
                    # C.g:208:9: '(' ')'
                    self.match(self.input, 51, self.FOLLOW_51_in_declarator_suffix827)
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_declarator_suffix829)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 24, declarator_suffix_StartIndex)

            pass

        return 

    # $ANTLR end declarator_suffix


    # $ANTLR start pointer
    # C.g:211:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | s= '*' );
    def pointer(self, ):

        pointer_StartIndex = self.input.index()
        s = None

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 25):
                    return 

                # C.g:212:2: ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | s= '*' )
                alt31 = 3
                LA31_0 = self.input.LA(1)

                if (LA31_0 == 55) :
                    LA31 = self.input.LA(2)
                    if LA31 == 55:
                        LA31_2 = self.input.LA(3)

                        if (self.synpred60()) :
                            alt31 = 2
                        elif (True) :
                            alt31 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("211:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | s= '*' );", 31, 2, self.input)

                            raise nvae

                    elif LA31 == EOF or LA31 == IDENTIFIER or LA31 == 24 or LA31 == 25 or LA31 == 26 or LA31 == 27 or LA31 == 28 or LA31 == 29 or LA31 == 30 or LA31 == 31 or LA31 == 32 or LA31 == 33 or LA31 == 34 or LA31 == 35 or LA31 == 36 or LA31 == 37 or LA31 == 38 or LA31 == 39 or LA31 == 40 or LA31 == 41 or LA31 == 43 or LA31 == 44 or LA31 == 45 or LA31 == 46 or LA31 == 51 or LA31 == 52 or LA31 == 53:
                        alt31 = 3
                    elif LA31 == 47 or LA31 == 48 or LA31 == 49 or LA31 == 50:
                        LA31_18 = self.input.LA(3)

                        if (self.synpred59()) :
                            alt31 = 1
                        elif (True) :
                            alt31 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("211:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | s= '*' );", 31, 18, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("211:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | s= '*' );", 31, 1, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("211:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | s= '*' );", 31, 0, self.input)

                    raise nvae

                if alt31 == 1:
                    # C.g:212:4: '*' ( type_qualifier )+ ( pointer )?
                    self.match(self.input, 55, self.FOLLOW_55_in_pointer840)
                    if self.failed:
                        return 
                    # C.g:212:8: ( type_qualifier )+
                    cnt29 = 0
                    while True: #loop29
                        alt29 = 2
                        LA29_0 = self.input.LA(1)

                        if ((47 <= LA29_0 <= 50)) :
                            LA29_17 = self.input.LA(2)

                            if (self.synpred57()) :
                                alt29 = 1




                        if alt29 == 1:
                            # C.g:0:0: type_qualifier
                            self.following.append(self.FOLLOW_type_qualifier_in_pointer842)
                            self.type_qualifier()
                            self.following.pop()
                            if self.failed:
                                return 


                        else:
                            if cnt29 >= 1:
                                break #loop29

                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            eee = EarlyExitException(29, self.input)
                            raise eee

                        cnt29 += 1


                    # C.g:212:24: ( pointer )?
                    alt30 = 2
                    LA30_0 = self.input.LA(1)

                    if (LA30_0 == 55) :
                        LA30_1 = self.input.LA(2)

                        if (self.synpred58()) :
                            alt30 = 1
                    if alt30 == 1:
                        # C.g:0:0: pointer
                        self.following.append(self.FOLLOW_pointer_in_pointer845)
                        self.pointer()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt31 == 2:
                    # C.g:213:4: '*' pointer
                    self.match(self.input, 55, self.FOLLOW_55_in_pointer851)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_pointer_in_pointer853)
                    self.pointer()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt31 == 3:
                    # C.g:214:4: s= '*'
                    s = self.input.LT(1)
                    self.match(self.input, 55, self.FOLLOW_55_in_pointer860)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 25, pointer_StartIndex)

            pass

        return 

    # $ANTLR end pointer


    # $ANTLR start parameter_type_list
    # C.g:217:1: parameter_type_list : parameter_list ( ',' '...' )? ;
    def parameter_type_list(self, ):

        parameter_type_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 26):
                    return 

                # C.g:218:2: ( parameter_list ( ',' '...' )? )
                # C.g:218:4: parameter_list ( ',' '...' )?
                self.following.append(self.FOLLOW_parameter_list_in_parameter_type_list871)
                self.parameter_list()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:218:19: ( ',' '...' )?
                alt32 = 2
                LA32_0 = self.input.LA(1)

                if (LA32_0 == 26) :
                    alt32 = 1
                if alt32 == 1:
                    # C.g:218:20: ',' '...'
                    self.match(self.input, 26, self.FOLLOW_26_in_parameter_type_list874)
                    if self.failed:
                        return 
                    self.match(self.input, 56, self.FOLLOW_56_in_parameter_type_list876)
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 26, parameter_type_list_StartIndex)

            pass

        return 

    # $ANTLR end parameter_type_list


    # $ANTLR start parameter_list
    # C.g:221:1: parameter_list : parameter_declaration ( ',' parameter_declaration )* ;
    def parameter_list(self, ):

        parameter_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 27):
                    return 

                # C.g:222:2: ( parameter_declaration ( ',' parameter_declaration )* )
                # C.g:222:4: parameter_declaration ( ',' parameter_declaration )*
                self.following.append(self.FOLLOW_parameter_declaration_in_parameter_list889)
                self.parameter_declaration()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:222:26: ( ',' parameter_declaration )*
                while True: #loop33
                    alt33 = 2
                    LA33_0 = self.input.LA(1)

                    if (LA33_0 == 26) :
                        LA33_1 = self.input.LA(2)

                        if (LA33_1 == IDENTIFIER or (28 <= LA33_1 <= 40) or (43 <= LA33_1 <= 44) or (46 <= LA33_1 <= 50)) :
                            alt33 = 1




                    if alt33 == 1:
                        # C.g:222:27: ',' parameter_declaration
                        self.match(self.input, 26, self.FOLLOW_26_in_parameter_list892)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_parameter_declaration_in_parameter_list894)
                        self.parameter_declaration()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop33






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 27, parameter_list_StartIndex)

            pass

        return 

    # $ANTLR end parameter_list


    # $ANTLR start parameter_declaration
    # C.g:225:1: parameter_declaration : declaration_specifiers ( declarator | abstract_declarator )+ ;
    def parameter_declaration(self, ):

        parameter_declaration_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 28):
                    return 

                # C.g:226:2: ( declaration_specifiers ( declarator | abstract_declarator )+ )
                # C.g:226:4: declaration_specifiers ( declarator | abstract_declarator )+
                self.following.append(self.FOLLOW_declaration_specifiers_in_parameter_declaration907)
                self.declaration_specifiers()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:226:27: ( declarator | abstract_declarator )+
                cnt34 = 0
                while True: #loop34
                    alt34 = 3
                    LA34 = self.input.LA(1)
                    if LA34 == 55:
                        LA34_4 = self.input.LA(2)

                        if (self.synpred63()) :
                            alt34 = 1
                        elif (self.synpred64()) :
                            alt34 = 2


                    elif LA34 == IDENTIFIER:
                        alt34 = 1
                    elif LA34 == 51:
                        LA34 = self.input.LA(2)
                        if LA34 == 28 or LA34 == 29 or LA34 == 30 or LA34 == 31 or LA34 == 32 or LA34 == 33 or LA34 == 34 or LA34 == 35 or LA34 == 36 or LA34 == 37 or LA34 == 38 or LA34 == 39 or LA34 == 40 or LA34 == 43 or LA34 == 44 or LA34 == 46 or LA34 == 47 or LA34 == 48 or LA34 == 49 or LA34 == 50 or LA34 == 52 or LA34 == 53:
                            alt34 = 2
                        elif LA34 == IDENTIFIER:
                            LA34_29 = self.input.LA(3)

                            if (self.synpred63()) :
                                alt34 = 1
                            elif (self.synpred64()) :
                                alt34 = 2


                        elif LA34 == 55:
                            LA34_31 = self.input.LA(3)

                            if (self.synpred63()) :
                                alt34 = 1
                            elif (self.synpred64()) :
                                alt34 = 2


                        elif LA34 == 51:
                            LA34_32 = self.input.LA(3)

                            if (self.synpred63()) :
                                alt34 = 1
                            elif (self.synpred64()) :
                                alt34 = 2



                    elif LA34 == 53:
                        alt34 = 2

                    if alt34 == 1:
                        # C.g:226:28: declarator
                        self.following.append(self.FOLLOW_declarator_in_parameter_declaration910)
                        self.declarator()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt34 == 2:
                        # C.g:226:39: abstract_declarator
                        self.following.append(self.FOLLOW_abstract_declarator_in_parameter_declaration912)
                        self.abstract_declarator()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt34 >= 1:
                            break #loop34

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(34, self.input)
                        raise eee

                    cnt34 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 28, parameter_declaration_StartIndex)

            pass

        return 

    # $ANTLR end parameter_declaration


    # $ANTLR start identifier_list
    # C.g:229:1: identifier_list : i= IDENTIFIER ( ',' d= IDENTIFIER )* ;
    def identifier_list(self, ):

        identifier_list_StartIndex = self.input.index()
        i = None
        d = None

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 29):
                    return 

                # C.g:230:2: (i= IDENTIFIER ( ',' d= IDENTIFIER )* )
                # C.g:230:4: i= IDENTIFIER ( ',' d= IDENTIFIER )*
                i = self.input.LT(1)
                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_identifier_list927)
                if self.failed:
                    return 
                # C.g:231:2: ( ',' d= IDENTIFIER )*
                while True: #loop35
                    alt35 = 2
                    LA35_0 = self.input.LA(1)

                    if (LA35_0 == 26) :
                        alt35 = 1


                    if alt35 == 1:
                        # C.g:231:3: ',' d= IDENTIFIER
                        self.match(self.input, 26, self.FOLLOW_26_in_identifier_list932)
                        if self.failed:
                            return 
                        d = self.input.LT(1)
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_identifier_list936)
                        if self.failed:
                            return 


                    else:
                        break #loop35






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 29, identifier_list_StartIndex)

            pass

        return 

    # $ANTLR end identifier_list


    # $ANTLR start type_name
    # C.g:234:1: type_name : ( specifier_qualifier_list ( abstract_declarator )? | type_id );
    def type_name(self, ):

        type_name_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 30):
                    return 

                # C.g:235:2: ( specifier_qualifier_list ( abstract_declarator )? | type_id )
                alt37 = 2
                LA37_0 = self.input.LA(1)

                if ((32 <= LA37_0 <= 40) or (43 <= LA37_0 <= 44) or (46 <= LA37_0 <= 50)) :
                    alt37 = 1
                elif (LA37_0 == IDENTIFIER) :
                    LA37_13 = self.input.LA(2)

                    if (self.synpred67()) :
                        alt37 = 1
                    elif (True) :
                        alt37 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("234:1: type_name : ( specifier_qualifier_list ( abstract_declarator )? | type_id );", 37, 13, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("234:1: type_name : ( specifier_qualifier_list ( abstract_declarator )? | type_id );", 37, 0, self.input)

                    raise nvae

                if alt37 == 1:
                    # C.g:235:4: specifier_qualifier_list ( abstract_declarator )?
                    self.following.append(self.FOLLOW_specifier_qualifier_list_in_type_name951)
                    self.specifier_qualifier_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:235:29: ( abstract_declarator )?
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 51 or LA36_0 == 53 or LA36_0 == 55) :
                        alt36 = 1
                    if alt36 == 1:
                        # C.g:0:0: abstract_declarator
                        self.following.append(self.FOLLOW_abstract_declarator_in_type_name953)
                        self.abstract_declarator()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt37 == 2:
                    # C.g:236:4: type_id
                    self.following.append(self.FOLLOW_type_id_in_type_name959)
                    self.type_id()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 30, type_name_StartIndex)

            pass

        return 

    # $ANTLR end type_name


    # $ANTLR start abstract_declarator
    # C.g:239:1: abstract_declarator : ( pointer ( direct_abstract_declarator )? | direct_abstract_declarator );
    def abstract_declarator(self, ):

        abstract_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 31):
                    return 

                # C.g:240:2: ( pointer ( direct_abstract_declarator )? | direct_abstract_declarator )
                alt39 = 2
                LA39_0 = self.input.LA(1)

                if (LA39_0 == 55) :
                    alt39 = 1
                elif (LA39_0 == 51 or LA39_0 == 53) :
                    alt39 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("239:1: abstract_declarator : ( pointer ( direct_abstract_declarator )? | direct_abstract_declarator );", 39, 0, self.input)

                    raise nvae

                if alt39 == 1:
                    # C.g:240:4: pointer ( direct_abstract_declarator )?
                    self.following.append(self.FOLLOW_pointer_in_abstract_declarator970)
                    self.pointer()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:240:12: ( direct_abstract_declarator )?
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 51) :
                        LA38 = self.input.LA(2)
                        if LA38 == 52:
                            LA38_8 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 28 or LA38 == 29 or LA38 == 30 or LA38 == 31:
                            LA38_9 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 32:
                            LA38_10 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 33:
                            LA38_11 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 34:
                            LA38_12 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 35:
                            LA38_13 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 36:
                            LA38_14 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 37:
                            LA38_15 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 38:
                            LA38_16 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 39:
                            LA38_17 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 40:
                            LA38_18 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 43 or LA38 == 44:
                            LA38_19 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 46:
                            LA38_20 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == IDENTIFIER:
                            LA38_21 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 47 or LA38 == 48 or LA38 == 49 or LA38 == 50:
                            LA38_22 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 55:
                            LA38_23 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 51:
                            LA38_24 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 53:
                            LA38_25 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                    elif (LA38_0 == 53) :
                        LA38 = self.input.LA(2)
                        if LA38 == 54:
                            LA38_26 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 51:
                            LA38_27 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == IDENTIFIER:
                            LA38_28 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == HEX_LITERAL or LA38 == OCTAL_LITERAL or LA38 == DECIMAL_LITERAL or LA38 == CHARACTER_LITERAL or LA38 == STRING_LITERAL or LA38 == FLOATING_POINT_LITERAL:
                            LA38_29 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 61:
                            LA38_30 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 62:
                            LA38_31 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 55 or LA38 == 57 or LA38 == 58 or LA38 == 66 or LA38 == 67 or LA38 == 68:
                            LA38_32 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 63:
                            LA38_33 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                    if alt38 == 1:
                        # C.g:0:0: direct_abstract_declarator
                        self.following.append(self.FOLLOW_direct_abstract_declarator_in_abstract_declarator972)
                        self.direct_abstract_declarator()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt39 == 2:
                    # C.g:241:4: direct_abstract_declarator
                    self.following.append(self.FOLLOW_direct_abstract_declarator_in_abstract_declarator978)
                    self.direct_abstract_declarator()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 31, abstract_declarator_StartIndex)

            pass

        return 

    # $ANTLR end abstract_declarator


    # $ANTLR start direct_abstract_declarator
    # C.g:244:1: direct_abstract_declarator : ( '(' abstract_declarator ')' | abstract_declarator_suffix ) ( abstract_declarator_suffix )* ;
    def direct_abstract_declarator(self, ):

        direct_abstract_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 32):
                    return 

                # C.g:245:2: ( ( '(' abstract_declarator ')' | abstract_declarator_suffix ) ( abstract_declarator_suffix )* )
                # C.g:245:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix ) ( abstract_declarator_suffix )*
                # C.g:245:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix )
                alt40 = 2
                LA40_0 = self.input.LA(1)

                if (LA40_0 == 51) :
                    LA40_1 = self.input.LA(2)

                    if (LA40_1 == IDENTIFIER or (28 <= LA40_1 <= 40) or (43 <= LA40_1 <= 44) or (46 <= LA40_1 <= 50) or LA40_1 == 52) :
                        alt40 = 2
                    elif (LA40_1 == 51 or LA40_1 == 53 or LA40_1 == 55) :
                        alt40 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("245:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix )", 40, 1, self.input)

                        raise nvae

                elif (LA40_0 == 53) :
                    alt40 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("245:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix )", 40, 0, self.input)

                    raise nvae

                if alt40 == 1:
                    # C.g:245:6: '(' abstract_declarator ')'
                    self.match(self.input, 51, self.FOLLOW_51_in_direct_abstract_declarator991)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_abstract_declarator_in_direct_abstract_declarator993)
                    self.abstract_declarator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_direct_abstract_declarator995)
                    if self.failed:
                        return 


                elif alt40 == 2:
                    # C.g:245:36: abstract_declarator_suffix
                    self.following.append(self.FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator999)
                    self.abstract_declarator_suffix()
                    self.following.pop()
                    if self.failed:
                        return 



                # C.g:245:65: ( abstract_declarator_suffix )*
                while True: #loop41
                    alt41 = 2
                    LA41_0 = self.input.LA(1)

                    if (LA41_0 == 51) :
                        LA41 = self.input.LA(2)
                        if LA41 == 52:
                            LA41_8 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 28 or LA41 == 29 or LA41 == 30 or LA41 == 31:
                            LA41_9 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 32:
                            LA41_10 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 33:
                            LA41_11 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 34:
                            LA41_12 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 35:
                            LA41_13 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 36:
                            LA41_14 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 37:
                            LA41_15 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 38:
                            LA41_16 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 39:
                            LA41_17 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 40:
                            LA41_18 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 43 or LA41 == 44:
                            LA41_19 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 46:
                            LA41_20 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == IDENTIFIER:
                            LA41_21 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 47 or LA41 == 48 or LA41 == 49 or LA41 == 50:
                            LA41_22 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1



                    elif (LA41_0 == 53) :
                        LA41 = self.input.LA(2)
                        if LA41 == 54:
                            LA41_26 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 51:
                            LA41_27 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == IDENTIFIER:
                            LA41_28 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == HEX_LITERAL or LA41 == OCTAL_LITERAL or LA41 == DECIMAL_LITERAL or LA41 == CHARACTER_LITERAL or LA41 == STRING_LITERAL or LA41 == FLOATING_POINT_LITERAL:
                            LA41_29 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 61:
                            LA41_30 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 62:
                            LA41_31 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 55 or LA41 == 57 or LA41 == 58 or LA41 == 66 or LA41 == 67 or LA41 == 68:
                            LA41_32 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 63:
                            LA41_33 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1





                    if alt41 == 1:
                        # C.g:0:0: abstract_declarator_suffix
                        self.following.append(self.FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator1003)
                        self.abstract_declarator_suffix()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop41






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 32, direct_abstract_declarator_StartIndex)

            pass

        return 

    # $ANTLR end direct_abstract_declarator


    # $ANTLR start abstract_declarator_suffix
    # C.g:248:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );
    def abstract_declarator_suffix(self, ):

        abstract_declarator_suffix_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 33):
                    return 

                # C.g:249:2: ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' )
                alt42 = 4
                LA42_0 = self.input.LA(1)

                if (LA42_0 == 53) :
                    LA42_1 = self.input.LA(2)

                    if (LA42_1 == 54) :
                        alt42 = 1
                    elif ((IDENTIFIER <= LA42_1 <= FLOATING_POINT_LITERAL) or LA42_1 == 51 or LA42_1 == 55 or (57 <= LA42_1 <= 58) or (61 <= LA42_1 <= 63) or (66 <= LA42_1 <= 68)) :
                        alt42 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("248:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );", 42, 1, self.input)

                        raise nvae

                elif (LA42_0 == 51) :
                    LA42_2 = self.input.LA(2)

                    if (LA42_2 == 52) :
                        alt42 = 3
                    elif (LA42_2 == IDENTIFIER or (28 <= LA42_2 <= 40) or (43 <= LA42_2 <= 44) or (46 <= LA42_2 <= 50)) :
                        alt42 = 4
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("248:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );", 42, 2, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("248:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );", 42, 0, self.input)

                    raise nvae

                if alt42 == 1:
                    # C.g:249:4: '[' ']'
                    self.match(self.input, 53, self.FOLLOW_53_in_abstract_declarator_suffix1015)
                    if self.failed:
                        return 
                    self.match(self.input, 54, self.FOLLOW_54_in_abstract_declarator_suffix1017)
                    if self.failed:
                        return 


                elif alt42 == 2:
                    # C.g:250:4: '[' constant_expression ']'
                    self.match(self.input, 53, self.FOLLOW_53_in_abstract_declarator_suffix1022)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_abstract_declarator_suffix1024)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 54, self.FOLLOW_54_in_abstract_declarator_suffix1026)
                    if self.failed:
                        return 


                elif alt42 == 3:
                    # C.g:251:4: '(' ')'
                    self.match(self.input, 51, self.FOLLOW_51_in_abstract_declarator_suffix1031)
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_abstract_declarator_suffix1033)
                    if self.failed:
                        return 


                elif alt42 == 4:
                    # C.g:252:4: '(' parameter_type_list ')'
                    self.match(self.input, 51, self.FOLLOW_51_in_abstract_declarator_suffix1038)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_parameter_type_list_in_abstract_declarator_suffix1040)
                    self.parameter_type_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_abstract_declarator_suffix1042)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 33, abstract_declarator_suffix_StartIndex)

            pass

        return 

    # $ANTLR end abstract_declarator_suffix


    # $ANTLR start initializer
    # C.g:255:1: initializer : ( assignment_expression | '{' initializer_list ( ',' )? '}' );
    def initializer(self, ):

        initializer_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 34):
                    return 

                # C.g:257:2: ( assignment_expression | '{' initializer_list ( ',' )? '}' )
                alt44 = 2
                LA44_0 = self.input.LA(1)

                if ((IDENTIFIER <= LA44_0 <= FLOATING_POINT_LITERAL) or LA44_0 == 51 or LA44_0 == 55 or (57 <= LA44_0 <= 58) or (61 <= LA44_0 <= 63) or (66 <= LA44_0 <= 68)) :
                    alt44 = 1
                elif (LA44_0 == 41) :
                    alt44 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("255:1: initializer : ( assignment_expression | '{' initializer_list ( ',' )? '}' );", 44, 0, self.input)

                    raise nvae

                if alt44 == 1:
                    # C.g:257:4: assignment_expression
                    self.following.append(self.FOLLOW_assignment_expression_in_initializer1055)
                    self.assignment_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt44 == 2:
                    # C.g:258:4: '{' initializer_list ( ',' )? '}'
                    self.match(self.input, 41, self.FOLLOW_41_in_initializer1060)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_initializer_list_in_initializer1062)
                    self.initializer_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:258:25: ( ',' )?
                    alt43 = 2
                    LA43_0 = self.input.LA(1)

                    if (LA43_0 == 26) :
                        alt43 = 1
                    if alt43 == 1:
                        # C.g:0:0: ','
                        self.match(self.input, 26, self.FOLLOW_26_in_initializer1064)
                        if self.failed:
                            return 



                    self.match(self.input, 42, self.FOLLOW_42_in_initializer1067)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 34, initializer_StartIndex)

            pass

        return 

    # $ANTLR end initializer


    # $ANTLR start initializer_list
    # C.g:261:1: initializer_list : initializer ( ',' initializer )* ;
    def initializer_list(self, ):

        initializer_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 35):
                    return 

                # C.g:262:2: ( initializer ( ',' initializer )* )
                # C.g:262:4: initializer ( ',' initializer )*
                self.following.append(self.FOLLOW_initializer_in_initializer_list1078)
                self.initializer()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:262:16: ( ',' initializer )*
                while True: #loop45
                    alt45 = 2
                    LA45_0 = self.input.LA(1)

                    if (LA45_0 == 26) :
                        LA45_1 = self.input.LA(2)

                        if ((IDENTIFIER <= LA45_1 <= FLOATING_POINT_LITERAL) or LA45_1 == 41 or LA45_1 == 51 or LA45_1 == 55 or (57 <= LA45_1 <= 58) or (61 <= LA45_1 <= 63) or (66 <= LA45_1 <= 68)) :
                            alt45 = 1




                    if alt45 == 1:
                        # C.g:262:17: ',' initializer
                        self.match(self.input, 26, self.FOLLOW_26_in_initializer_list1081)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_initializer_in_initializer_list1083)
                        self.initializer()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop45






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 35, initializer_list_StartIndex)

            pass

        return 

    # $ANTLR end initializer_list


    # $ANTLR start argument_expression_list
    # C.g:267:1: argument_expression_list : assignment_expression ( ',' assignment_expression )* ;
    def argument_expression_list(self, ):

        argument_expression_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 36):
                    return 

                # C.g:268:2: ( assignment_expression ( ',' assignment_expression )* )
                # C.g:268:6: assignment_expression ( ',' assignment_expression )*
                self.following.append(self.FOLLOW_assignment_expression_in_argument_expression_list1101)
                self.assignment_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:268:28: ( ',' assignment_expression )*
                while True: #loop46
                    alt46 = 2
                    LA46_0 = self.input.LA(1)

                    if (LA46_0 == 26) :
                        alt46 = 1


                    if alt46 == 1:
                        # C.g:268:29: ',' assignment_expression
                        self.match(self.input, 26, self.FOLLOW_26_in_argument_expression_list1104)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_assignment_expression_in_argument_expression_list1106)
                        self.assignment_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop46






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 36, argument_expression_list_StartIndex)

            pass

        return 

    # $ANTLR end argument_expression_list


    # $ANTLR start additive_expression
    # C.g:271:1: additive_expression : ( multiplicative_expression ) ( '+' multiplicative_expression | '-' multiplicative_expression )* ;
    def additive_expression(self, ):

        additive_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 37):
                    return 

                # C.g:272:2: ( ( multiplicative_expression ) ( '+' multiplicative_expression | '-' multiplicative_expression )* )
                # C.g:272:4: ( multiplicative_expression ) ( '+' multiplicative_expression | '-' multiplicative_expression )*
                # C.g:272:4: ( multiplicative_expression )
                # C.g:272:5: multiplicative_expression
                self.following.append(self.FOLLOW_multiplicative_expression_in_additive_expression1120)
                self.multiplicative_expression()
                self.following.pop()
                if self.failed:
                    return 



                # C.g:272:32: ( '+' multiplicative_expression | '-' multiplicative_expression )*
                while True: #loop47
                    alt47 = 3
                    LA47_0 = self.input.LA(1)

                    if (LA47_0 == 57) :
                        alt47 = 1
                    elif (LA47_0 == 58) :
                        alt47 = 2


                    if alt47 == 1:
                        # C.g:272:33: '+' multiplicative_expression
                        self.match(self.input, 57, self.FOLLOW_57_in_additive_expression1124)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_multiplicative_expression_in_additive_expression1126)
                        self.multiplicative_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt47 == 2:
                        # C.g:272:65: '-' multiplicative_expression
                        self.match(self.input, 58, self.FOLLOW_58_in_additive_expression1130)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_multiplicative_expression_in_additive_expression1132)
                        self.multiplicative_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop47






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 37, additive_expression_StartIndex)

            pass

        return 

    # $ANTLR end additive_expression


    # $ANTLR start multiplicative_expression
    # C.g:275:1: multiplicative_expression : ( cast_expression ) ( '*' cast_expression | '/' cast_expression | '%' cast_expression )* ;
    def multiplicative_expression(self, ):

        multiplicative_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 38):
                    return 

                # C.g:276:2: ( ( cast_expression ) ( '*' cast_expression | '/' cast_expression | '%' cast_expression )* )
                # C.g:276:4: ( cast_expression ) ( '*' cast_expression | '/' cast_expression | '%' cast_expression )*
                # C.g:276:4: ( cast_expression )
                # C.g:276:5: cast_expression
                self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1146)
                self.cast_expression()
                self.following.pop()
                if self.failed:
                    return 



                # C.g:276:22: ( '*' cast_expression | '/' cast_expression | '%' cast_expression )*
                while True: #loop48
                    alt48 = 4
                    LA48 = self.input.LA(1)
                    if LA48 == 55:
                        alt48 = 1
                    elif LA48 == 59:
                        alt48 = 2
                    elif LA48 == 60:
                        alt48 = 3

                    if alt48 == 1:
                        # C.g:276:23: '*' cast_expression
                        self.match(self.input, 55, self.FOLLOW_55_in_multiplicative_expression1150)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1152)
                        self.cast_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt48 == 2:
                        # C.g:276:45: '/' cast_expression
                        self.match(self.input, 59, self.FOLLOW_59_in_multiplicative_expression1156)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1158)
                        self.cast_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt48 == 3:
                        # C.g:276:67: '%' cast_expression
                        self.match(self.input, 60, self.FOLLOW_60_in_multiplicative_expression1162)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1164)
                        self.cast_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop48






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 38, multiplicative_expression_StartIndex)

            pass

        return 

    # $ANTLR end multiplicative_expression


    # $ANTLR start cast_expression
    # C.g:279:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );
    def cast_expression(self, ):

        cast_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 39):
                    return 

                # C.g:280:2: ( '(' type_name ')' cast_expression | unary_expression )
                alt49 = 2
                LA49_0 = self.input.LA(1)

                if (LA49_0 == 51) :
                    LA49 = self.input.LA(2)
                    if LA49 == IDENTIFIER:
                        LA49_8 = self.input.LA(3)

                        if (self.synpred84()) :
                            alt49 = 1
                        elif (True) :
                            alt49 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("279:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );", 49, 8, self.input)

                            raise nvae

                    elif LA49 == HEX_LITERAL or LA49 == OCTAL_LITERAL or LA49 == DECIMAL_LITERAL or LA49 == CHARACTER_LITERAL or LA49 == STRING_LITERAL or LA49 == FLOATING_POINT_LITERAL or LA49 == 51 or LA49 == 55 or LA49 == 57 or LA49 == 58 or LA49 == 61 or LA49 == 62 or LA49 == 63 or LA49 == 66 or LA49 == 67 or LA49 == 68:
                        alt49 = 2
                    elif LA49 == 32 or LA49 == 33 or LA49 == 34 or LA49 == 35 or LA49 == 36 or LA49 == 37 or LA49 == 38 or LA49 == 39 or LA49 == 40 or LA49 == 43 or LA49 == 44 or LA49 == 46 or LA49 == 47 or LA49 == 48 or LA49 == 49 or LA49 == 50:
                        alt49 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("279:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );", 49, 1, self.input)

                        raise nvae

                elif ((IDENTIFIER <= LA49_0 <= FLOATING_POINT_LITERAL) or LA49_0 == 55 or (57 <= LA49_0 <= 58) or (61 <= LA49_0 <= 63) or (66 <= LA49_0 <= 68)) :
                    alt49 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("279:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );", 49, 0, self.input)

                    raise nvae

                if alt49 == 1:
                    # C.g:280:4: '(' type_name ')' cast_expression
                    self.match(self.input, 51, self.FOLLOW_51_in_cast_expression1177)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_type_name_in_cast_expression1179)
                    self.type_name()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_cast_expression1181)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_cast_expression_in_cast_expression1183)
                    self.cast_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt49 == 2:
                    # C.g:281:4: unary_expression
                    self.following.append(self.FOLLOW_unary_expression_in_cast_expression1188)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 39, cast_expression_StartIndex)

            pass

        return 

    # $ANTLR end cast_expression


    # $ANTLR start unary_expression
    # C.g:284:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );
    def unary_expression(self, ):

        unary_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 40):
                    return 

                # C.g:285:2: ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' )
                alt50 = 6
                LA50 = self.input.LA(1)
                if LA50 == IDENTIFIER or LA50 == HEX_LITERAL or LA50 == OCTAL_LITERAL or LA50 == DECIMAL_LITERAL or LA50 == CHARACTER_LITERAL or LA50 == STRING_LITERAL or LA50 == FLOATING_POINT_LITERAL or LA50 == 51:
                    alt50 = 1
                elif LA50 == 61:
                    alt50 = 2
                elif LA50 == 62:
                    alt50 = 3
                elif LA50 == 55 or LA50 == 57 or LA50 == 58 or LA50 == 66 or LA50 == 67 or LA50 == 68:
                    alt50 = 4
                elif LA50 == 63:
                    LA50_7 = self.input.LA(2)

                    if (LA50_7 == 51) :
                        LA50_8 = self.input.LA(3)

                        if (self.synpred89()) :
                            alt50 = 5
                        elif (True) :
                            alt50 = 6
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("284:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );", 50, 8, self.input)

                            raise nvae

                    elif ((IDENTIFIER <= LA50_7 <= FLOATING_POINT_LITERAL) or LA50_7 == 55 or (57 <= LA50_7 <= 58) or (61 <= LA50_7 <= 63) or (66 <= LA50_7 <= 68)) :
                        alt50 = 5
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("284:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );", 50, 7, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("284:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );", 50, 0, self.input)

                    raise nvae

                if alt50 == 1:
                    # C.g:285:4: postfix_expression
                    self.following.append(self.FOLLOW_postfix_expression_in_unary_expression1199)
                    self.postfix_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 2:
                    # C.g:286:4: '++' unary_expression
                    self.match(self.input, 61, self.FOLLOW_61_in_unary_expression1204)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_unary_expression_in_unary_expression1206)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 3:
                    # C.g:287:4: '--' unary_expression
                    self.match(self.input, 62, self.FOLLOW_62_in_unary_expression1211)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_unary_expression_in_unary_expression1213)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 4:
                    # C.g:288:4: unary_operator cast_expression
                    self.following.append(self.FOLLOW_unary_operator_in_unary_expression1218)
                    self.unary_operator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_cast_expression_in_unary_expression1220)
                    self.cast_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 5:
                    # C.g:289:4: 'sizeof' unary_expression
                    self.match(self.input, 63, self.FOLLOW_63_in_unary_expression1225)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_unary_expression_in_unary_expression1227)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 6:
                    # C.g:290:4: 'sizeof' '(' type_name ')'
                    self.match(self.input, 63, self.FOLLOW_63_in_unary_expression1232)
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_unary_expression1234)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_type_name_in_unary_expression1236)
                    self.type_name()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_unary_expression1238)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 40, unary_expression_StartIndex)

            pass

        return 

    # $ANTLR end unary_expression


    # $ANTLR start postfix_expression
    # C.g:293:1: postfix_expression : primary_expression ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )* ;
    def postfix_expression(self, ):

        postfix_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 41):
                    return 

                # C.g:294:2: ( primary_expression ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )* )
                # C.g:294:6: primary_expression ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )*
                self.following.append(self.FOLLOW_primary_expression_in_postfix_expression1251)
                self.primary_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:295:9: ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )*
                while True: #loop51
                    alt51 = 9
                    LA51 = self.input.LA(1)
                    if LA51 == 55:
                        LA51_1 = self.input.LA(2)

                        if (LA51_1 == IDENTIFIER) :
                            LA51_29 = self.input.LA(3)

                            if (self.synpred94()) :
                                alt51 = 5




                    elif LA51 == 53:
                        alt51 = 1
                    elif LA51 == 51:
                        LA51_24 = self.input.LA(2)

                        if (LA51_24 == 52) :
                            alt51 = 2
                        elif ((IDENTIFIER <= LA51_24 <= FLOATING_POINT_LITERAL) or LA51_24 == 51 or LA51_24 == 55 or (57 <= LA51_24 <= 58) or (61 <= LA51_24 <= 63) or (66 <= LA51_24 <= 68)) :
                            alt51 = 3


                    elif LA51 == 64:
                        alt51 = 4
                    elif LA51 == 65:
                        alt51 = 6
                    elif LA51 == 61:
                        alt51 = 7
                    elif LA51 == 62:
                        alt51 = 8

                    if alt51 == 1:
                        # C.g:295:13: '[' expression ']'
                        self.match(self.input, 53, self.FOLLOW_53_in_postfix_expression1265)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_expression_in_postfix_expression1267)
                        self.expression()
                        self.following.pop()
                        if self.failed:
                            return 
                        self.match(self.input, 54, self.FOLLOW_54_in_postfix_expression1269)
                        if self.failed:
                            return 


                    elif alt51 == 2:
                        # C.g:296:13: '(' ')'
                        self.match(self.input, 51, self.FOLLOW_51_in_postfix_expression1283)
                        if self.failed:
                            return 
                        self.match(self.input, 52, self.FOLLOW_52_in_postfix_expression1285)
                        if self.failed:
                            return 


                    elif alt51 == 3:
                        # C.g:297:13: '(' argument_expression_list ')'
                        self.match(self.input, 51, self.FOLLOW_51_in_postfix_expression1299)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_argument_expression_list_in_postfix_expression1301)
                        self.argument_expression_list()
                        self.following.pop()
                        if self.failed:
                            return 
                        self.match(self.input, 52, self.FOLLOW_52_in_postfix_expression1303)
                        if self.failed:
                            return 


                    elif alt51 == 4:
                        # C.g:298:13: '.' IDENTIFIER
                        self.match(self.input, 64, self.FOLLOW_64_in_postfix_expression1317)
                        if self.failed:
                            return 
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_postfix_expression1319)
                        if self.failed:
                            return 


                    elif alt51 == 5:
                        # C.g:299:13: '*' IDENTIFIER
                        self.match(self.input, 55, self.FOLLOW_55_in_postfix_expression1333)
                        if self.failed:
                            return 
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_postfix_expression1335)
                        if self.failed:
                            return 


                    elif alt51 == 6:
                        # C.g:300:13: '->' IDENTIFIER
                        self.match(self.input, 65, self.FOLLOW_65_in_postfix_expression1349)
                        if self.failed:
                            return 
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_postfix_expression1351)
                        if self.failed:
                            return 


                    elif alt51 == 7:
                        # C.g:301:13: '++'
                        self.match(self.input, 61, self.FOLLOW_61_in_postfix_expression1365)
                        if self.failed:
                            return 


                    elif alt51 == 8:
                        # C.g:302:13: '--'
                        self.match(self.input, 62, self.FOLLOW_62_in_postfix_expression1379)
                        if self.failed:
                            return 


                    else:
                        break #loop51






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 41, postfix_expression_StartIndex)

            pass

        return 

    # $ANTLR end postfix_expression


    # $ANTLR start unary_operator
    # C.g:306:1: unary_operator : ( '&' | '*' | '+' | '-' | '~' | '!' );
    def unary_operator(self, ):

        unary_operator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 42):
                    return 

                # C.g:307:2: ( '&' | '*' | '+' | '-' | '~' | '!' )
                # C.g:
                if self.input.LA(1) == 55 or (57 <= self.input.LA(1) <= 58) or (66 <= self.input.LA(1) <= 68):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_unary_operator0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 42, unary_operator_StartIndex)

            pass

        return 

    # $ANTLR end unary_operator


    # $ANTLR start primary_expression
    # C.g:315:1: primary_expression : ( IDENTIFIER | constant | '(' expression ')' );
    def primary_expression(self, ):

        primary_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 43):
                    return 

                # C.g:316:2: ( IDENTIFIER | constant | '(' expression ')' )
                alt52 = 3
                LA52 = self.input.LA(1)
                if LA52 == IDENTIFIER:
                    alt52 = 1
                elif LA52 == HEX_LITERAL or LA52 == OCTAL_LITERAL or LA52 == DECIMAL_LITERAL or LA52 == CHARACTER_LITERAL or LA52 == STRING_LITERAL or LA52 == FLOATING_POINT_LITERAL:
                    alt52 = 2
                elif LA52 == 51:
                    alt52 = 3
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("315:1: primary_expression : ( IDENTIFIER | constant | '(' expression ')' );", 52, 0, self.input)

                    raise nvae

                if alt52 == 1:
                    # C.g:316:4: IDENTIFIER
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_primary_expression1437)
                    if self.failed:
                        return 


                elif alt52 == 2:
                    # C.g:317:4: constant
                    self.following.append(self.FOLLOW_constant_in_primary_expression1442)
                    self.constant()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt52 == 3:
                    # C.g:318:4: '(' expression ')'
                    self.match(self.input, 51, self.FOLLOW_51_in_primary_expression1447)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_primary_expression1449)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_primary_expression1451)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 43, primary_expression_StartIndex)

            pass

        return 

    # $ANTLR end primary_expression


    # $ANTLR start constant
    # C.g:321:1: constant : ( HEX_LITERAL | OCTAL_LITERAL | DECIMAL_LITERAL | CHARACTER_LITERAL | STRING_LITERAL | FLOATING_POINT_LITERAL );
    def constant(self, ):

        constant_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 44):
                    return 

                # C.g:322:5: ( HEX_LITERAL | OCTAL_LITERAL | DECIMAL_LITERAL | CHARACTER_LITERAL | STRING_LITERAL | FLOATING_POINT_LITERAL )
                # C.g:
                if (HEX_LITERAL <= self.input.LA(1) <= FLOATING_POINT_LITERAL):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_constant0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 44, constant_StartIndex)

            pass

        return 

    # $ANTLR end constant


    # $ANTLR start expression
    # C.g:332:1: expression : assignment_expression ( ',' assignment_expression )* ;
    def expression(self, ):

        expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 45):
                    return 

                # C.g:333:2: ( assignment_expression ( ',' assignment_expression )* )
                # C.g:333:4: assignment_expression ( ',' assignment_expression )*
                self.following.append(self.FOLLOW_assignment_expression_in_expression1529)
                self.assignment_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:333:26: ( ',' assignment_expression )*
                while True: #loop53
                    alt53 = 2
                    LA53_0 = self.input.LA(1)

                    if (LA53_0 == 26) :
                        alt53 = 1


                    if alt53 == 1:
                        # C.g:333:27: ',' assignment_expression
                        self.match(self.input, 26, self.FOLLOW_26_in_expression1532)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_assignment_expression_in_expression1534)
                        self.assignment_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop53






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 45, expression_StartIndex)

            pass

        return 

    # $ANTLR end expression


    # $ANTLR start constant_expression
    # C.g:336:1: constant_expression : conditional_expression ;
    def constant_expression(self, ):

        constant_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 46):
                    return 

                # C.g:337:2: ( conditional_expression )
                # C.g:337:4: conditional_expression
                self.following.append(self.FOLLOW_conditional_expression_in_constant_expression1547)
                self.conditional_expression()
                self.following.pop()
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 46, constant_expression_StartIndex)

            pass

        return 

    # $ANTLR end constant_expression


    # $ANTLR start assignment_expression
    # C.g:340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );
    def assignment_expression(self, ):

        assignment_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 47):
                    return 

                # C.g:341:2: ( lvalue assignment_operator assignment_expression | conditional_expression )
                alt54 = 2
                LA54 = self.input.LA(1)
                if LA54 == IDENTIFIER:
                    LA54 = self.input.LA(2)
                    if LA54 == 53:
                        LA54_8 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 8, self.input)

                            raise nvae

                    elif LA54 == 51:
                        LA54_9 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 9, self.input)

                            raise nvae

                    elif LA54 == 64:
                        LA54_10 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 10, self.input)

                            raise nvae

                    elif LA54 == 55:
                        LA54_11 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 11, self.input)

                            raise nvae

                    elif LA54 == 65:
                        LA54_12 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 12, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_13 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 13, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_14 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 14, self.input)

                            raise nvae

                    elif LA54 == 27 or LA54 == 69 or LA54 == 70 or LA54 == 71 or LA54 == 72 or LA54 == 73 or LA54 == 74 or LA54 == 75 or LA54 == 76 or LA54 == 77 or LA54 == 78:
                        alt54 = 1
                    elif LA54 == EOF or LA54 == 25 or LA54 == 26 or LA54 == 42 or LA54 == 45 or LA54 == 52 or LA54 == 54 or LA54 == 57 or LA54 == 58 or LA54 == 59 or LA54 == 60 or LA54 == 66 or LA54 == 79 or LA54 == 80 or LA54 == 81 or LA54 == 82 or LA54 == 83 or LA54 == 84 or LA54 == 85 or LA54 == 86 or LA54 == 87 or LA54 == 88 or LA54 == 89 or LA54 == 90 or LA54 == 91:
                        alt54 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 1, self.input)

                        raise nvae

                elif LA54 == HEX_LITERAL or LA54 == OCTAL_LITERAL or LA54 == DECIMAL_LITERAL or LA54 == CHARACTER_LITERAL or LA54 == STRING_LITERAL or LA54 == FLOATING_POINT_LITERAL:
                    LA54 = self.input.LA(2)
                    if LA54 == 53:
                        LA54_36 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 36, self.input)

                            raise nvae

                    elif LA54 == 51:
                        LA54_37 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 37, self.input)

                            raise nvae

                    elif LA54 == 64:
                        LA54_38 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 38, self.input)

                            raise nvae

                    elif LA54 == 55:
                        LA54_39 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 39, self.input)

                            raise nvae

                    elif LA54 == 65:
                        LA54_40 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 40, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_41 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 41, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_42 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 42, self.input)

                            raise nvae

                    elif LA54 == EOF or LA54 == 25 or LA54 == 26 or LA54 == 42 or LA54 == 45 or LA54 == 52 or LA54 == 54 or LA54 == 57 or LA54 == 58 or LA54 == 59 or LA54 == 60 or LA54 == 66 or LA54 == 79 or LA54 == 80 or LA54 == 81 or LA54 == 82 or LA54 == 83 or LA54 == 84 or LA54 == 85 or LA54 == 86 or LA54 == 87 or LA54 == 88 or LA54 == 89 or LA54 == 90 or LA54 == 91:
                        alt54 = 2
                    elif LA54 == 27 or LA54 == 69 or LA54 == 70 or LA54 == 71 or LA54 == 72 or LA54 == 73 or LA54 == 74 or LA54 == 75 or LA54 == 76 or LA54 == 77 or LA54 == 78:
                        alt54 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 2, self.input)

                        raise nvae

                elif LA54 == 51:
                    LA54 = self.input.LA(2)
                    if LA54 == IDENTIFIER:
                        LA54_64 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 64, self.input)

                            raise nvae

                    elif LA54 == HEX_LITERAL or LA54 == OCTAL_LITERAL or LA54 == DECIMAL_LITERAL or LA54 == CHARACTER_LITERAL or LA54 == STRING_LITERAL or LA54 == FLOATING_POINT_LITERAL:
                        LA54_65 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 65, self.input)

                            raise nvae

                    elif LA54 == 51:
                        LA54_66 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 66, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_67 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 67, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_68 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 68, self.input)

                            raise nvae

                    elif LA54 == 55 or LA54 == 57 or LA54 == 58 or LA54 == 66 or LA54 == 67 or LA54 == 68:
                        LA54_69 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 69, self.input)

                            raise nvae

                    elif LA54 == 63:
                        LA54_70 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 70, self.input)

                            raise nvae

                    elif LA54 == 32 or LA54 == 33 or LA54 == 34 or LA54 == 35 or LA54 == 36 or LA54 == 37 or LA54 == 38 or LA54 == 39 or LA54 == 40 or LA54 == 43 or LA54 == 44 or LA54 == 46 or LA54 == 47 or LA54 == 48 or LA54 == 49 or LA54 == 50:
                        alt54 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 3, self.input)

                        raise nvae

                elif LA54 == 61:
                    LA54 = self.input.LA(2)
                    if LA54 == IDENTIFIER:
                        LA54_83 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 83, self.input)

                            raise nvae

                    elif LA54 == HEX_LITERAL or LA54 == OCTAL_LITERAL or LA54 == DECIMAL_LITERAL or LA54 == CHARACTER_LITERAL or LA54 == STRING_LITERAL or LA54 == FLOATING_POINT_LITERAL:
                        LA54_84 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 84, self.input)

                            raise nvae

                    elif LA54 == 51:
                        LA54_85 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 85, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_86 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 86, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_87 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 87, self.input)

                            raise nvae

                    elif LA54 == 55 or LA54 == 57 or LA54 == 58 or LA54 == 66 or LA54 == 67 or LA54 == 68:
                        LA54_88 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 88, self.input)

                            raise nvae

                    elif LA54 == 63:
                        LA54_89 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 89, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 4, self.input)

                        raise nvae

                elif LA54 == 62:
                    LA54 = self.input.LA(2)
                    if LA54 == IDENTIFIER:
                        LA54_90 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 90, self.input)

                            raise nvae

                    elif LA54 == HEX_LITERAL or LA54 == OCTAL_LITERAL or LA54 == DECIMAL_LITERAL or LA54 == CHARACTER_LITERAL or LA54 == STRING_LITERAL or LA54 == FLOATING_POINT_LITERAL:
                        LA54_91 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 91, self.input)

                            raise nvae

                    elif LA54 == 51:
                        LA54_92 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 92, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_93 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 93, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_94 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 94, self.input)

                            raise nvae

                    elif LA54 == 55 or LA54 == 57 or LA54 == 58 or LA54 == 66 or LA54 == 67 or LA54 == 68:
                        LA54_95 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 95, self.input)

                            raise nvae

                    elif LA54 == 63:
                        LA54_96 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 96, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 5, self.input)

                        raise nvae

                elif LA54 == 55 or LA54 == 57 or LA54 == 58 or LA54 == 66 or LA54 == 67 or LA54 == 68:
                    LA54 = self.input.LA(2)
                    if LA54 == 51:
                        LA54_97 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 97, self.input)

                            raise nvae

                    elif LA54 == IDENTIFIER:
                        LA54_98 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 98, self.input)

                            raise nvae

                    elif LA54 == HEX_LITERAL or LA54 == OCTAL_LITERAL or LA54 == DECIMAL_LITERAL or LA54 == CHARACTER_LITERAL or LA54 == STRING_LITERAL or LA54 == FLOATING_POINT_LITERAL:
                        LA54_99 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 99, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_100 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 100, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_101 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 101, self.input)

                            raise nvae

                    elif LA54 == 55 or LA54 == 57 or LA54 == 58 or LA54 == 66 or LA54 == 67 or LA54 == 68:
                        LA54_102 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 102, self.input)

                            raise nvae

                    elif LA54 == 63:
                        LA54_103 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 103, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 6, self.input)

                        raise nvae

                elif LA54 == 63:
                    LA54 = self.input.LA(2)
                    if LA54 == 51:
                        LA54_104 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 104, self.input)

                            raise nvae

                    elif LA54 == IDENTIFIER:
                        LA54_105 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 105, self.input)

                            raise nvae

                    elif LA54 == HEX_LITERAL or LA54 == OCTAL_LITERAL or LA54 == DECIMAL_LITERAL or LA54 == CHARACTER_LITERAL or LA54 == STRING_LITERAL or LA54 == FLOATING_POINT_LITERAL:
                        LA54_106 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 106, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_107 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 107, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_108 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 108, self.input)

                            raise nvae

                    elif LA54 == 55 or LA54 == 57 or LA54 == 58 or LA54 == 66 or LA54 == 67 or LA54 == 68:
                        LA54_109 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 109, self.input)

                            raise nvae

                    elif LA54 == 63:
                        LA54_110 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 110, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 7, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("340:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 0, self.input)

                    raise nvae

                if alt54 == 1:
                    # C.g:341:4: lvalue assignment_operator assignment_expression
                    self.following.append(self.FOLLOW_lvalue_in_assignment_expression1558)
                    self.lvalue()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_assignment_operator_in_assignment_expression1560)
                    self.assignment_operator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_assignment_expression_in_assignment_expression1562)
                    self.assignment_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt54 == 2:
                    # C.g:342:4: conditional_expression
                    self.following.append(self.FOLLOW_conditional_expression_in_assignment_expression1567)
                    self.conditional_expression()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 47, assignment_expression_StartIndex)

            pass

        return 

    # $ANTLR end assignment_expression


    # $ANTLR start lvalue
    # C.g:345:1: lvalue : unary_expression ;
    def lvalue(self, ):

        lvalue_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 48):
                    return 

                # C.g:346:2: ( unary_expression )
                # C.g:346:4: unary_expression
                self.following.append(self.FOLLOW_unary_expression_in_lvalue1579)
                self.unary_expression()
                self.following.pop()
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 48, lvalue_StartIndex)

            pass

        return 

    # $ANTLR end lvalue


    # $ANTLR start assignment_operator
    # C.g:349:1: assignment_operator : ( '=' | '*=' | '/=' | '%=' | '+=' | '-=' | '<<=' | '>>=' | '&=' | '^=' | '|=' );
    def assignment_operator(self, ):

        assignment_operator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 49):
                    return 

                # C.g:350:2: ( '=' | '*=' | '/=' | '%=' | '+=' | '-=' | '<<=' | '>>=' | '&=' | '^=' | '|=' )
                # C.g:
                if self.input.LA(1) == 27 or (69 <= self.input.LA(1) <= 78):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_assignment_operator0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 49, assignment_operator_StartIndex)

            pass

        return 

    # $ANTLR end assignment_operator


    # $ANTLR start conditional_expression
    # C.g:363:1: conditional_expression : logical_or_expression ( '?' expression ':' conditional_expression )? ;
    def conditional_expression(self, ):

        conditional_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 50):
                    return 

                # C.g:364:2: ( logical_or_expression ( '?' expression ':' conditional_expression )? )
                # C.g:364:4: logical_or_expression ( '?' expression ':' conditional_expression )?
                self.following.append(self.FOLLOW_logical_or_expression_in_conditional_expression1651)
                self.logical_or_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:364:26: ( '?' expression ':' conditional_expression )?
                alt55 = 2
                LA55_0 = self.input.LA(1)

                if (LA55_0 == 79) :
                    alt55 = 1
                if alt55 == 1:
                    # C.g:364:27: '?' expression ':' conditional_expression
                    self.match(self.input, 79, self.FOLLOW_79_in_conditional_expression1654)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_conditional_expression1656)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 45, self.FOLLOW_45_in_conditional_expression1658)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_conditional_expression_in_conditional_expression1660)
                    self.conditional_expression()
                    self.following.pop()
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 50, conditional_expression_StartIndex)

            pass

        return 

    # $ANTLR end conditional_expression


    # $ANTLR start logical_or_expression
    # C.g:367:1: logical_or_expression : logical_and_expression ( '||' logical_and_expression )* ;
    def logical_or_expression(self, ):

        logical_or_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 51):
                    return 

                # C.g:368:2: ( logical_and_expression ( '||' logical_and_expression )* )
                # C.g:368:4: logical_and_expression ( '||' logical_and_expression )*
                self.following.append(self.FOLLOW_logical_and_expression_in_logical_or_expression1673)
                self.logical_and_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:368:27: ( '||' logical_and_expression )*
                while True: #loop56
                    alt56 = 2
                    LA56_0 = self.input.LA(1)

                    if (LA56_0 == 80) :
                        alt56 = 1


                    if alt56 == 1:
                        # C.g:368:28: '||' logical_and_expression
                        self.match(self.input, 80, self.FOLLOW_80_in_logical_or_expression1676)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_logical_and_expression_in_logical_or_expression1678)
                        self.logical_and_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop56






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 51, logical_or_expression_StartIndex)

            pass

        return 

    # $ANTLR end logical_or_expression


    # $ANTLR start logical_and_expression
    # C.g:371:1: logical_and_expression : inclusive_or_expression ( '&&' inclusive_or_expression )* ;
    def logical_and_expression(self, ):

        logical_and_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 52):
                    return 

                # C.g:372:2: ( inclusive_or_expression ( '&&' inclusive_or_expression )* )
                # C.g:372:4: inclusive_or_expression ( '&&' inclusive_or_expression )*
                self.following.append(self.FOLLOW_inclusive_or_expression_in_logical_and_expression1691)
                self.inclusive_or_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:372:28: ( '&&' inclusive_or_expression )*
                while True: #loop57
                    alt57 = 2
                    LA57_0 = self.input.LA(1)

                    if (LA57_0 == 81) :
                        alt57 = 1


                    if alt57 == 1:
                        # C.g:372:29: '&&' inclusive_or_expression
                        self.match(self.input, 81, self.FOLLOW_81_in_logical_and_expression1694)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_inclusive_or_expression_in_logical_and_expression1696)
                        self.inclusive_or_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop57






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 52, logical_and_expression_StartIndex)

            pass

        return 

    # $ANTLR end logical_and_expression


    # $ANTLR start inclusive_or_expression
    # C.g:375:1: inclusive_or_expression : exclusive_or_expression ( '|' exclusive_or_expression )* ;
    def inclusive_or_expression(self, ):

        inclusive_or_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 53):
                    return 

                # C.g:376:2: ( exclusive_or_expression ( '|' exclusive_or_expression )* )
                # C.g:376:4: exclusive_or_expression ( '|' exclusive_or_expression )*
                self.following.append(self.FOLLOW_exclusive_or_expression_in_inclusive_or_expression1709)
                self.exclusive_or_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:376:28: ( '|' exclusive_or_expression )*
                while True: #loop58
                    alt58 = 2
                    LA58_0 = self.input.LA(1)

                    if (LA58_0 == 82) :
                        alt58 = 1


                    if alt58 == 1:
                        # C.g:376:29: '|' exclusive_or_expression
                        self.match(self.input, 82, self.FOLLOW_82_in_inclusive_or_expression1712)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_exclusive_or_expression_in_inclusive_or_expression1714)
                        self.exclusive_or_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop58






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 53, inclusive_or_expression_StartIndex)

            pass

        return 

    # $ANTLR end inclusive_or_expression


    # $ANTLR start exclusive_or_expression
    # C.g:379:1: exclusive_or_expression : and_expression ( '^' and_expression )* ;
    def exclusive_or_expression(self, ):

        exclusive_or_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 54):
                    return 

                # C.g:380:2: ( and_expression ( '^' and_expression )* )
                # C.g:380:4: and_expression ( '^' and_expression )*
                self.following.append(self.FOLLOW_and_expression_in_exclusive_or_expression1727)
                self.and_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:380:19: ( '^' and_expression )*
                while True: #loop59
                    alt59 = 2
                    LA59_0 = self.input.LA(1)

                    if (LA59_0 == 83) :
                        alt59 = 1


                    if alt59 == 1:
                        # C.g:380:20: '^' and_expression
                        self.match(self.input, 83, self.FOLLOW_83_in_exclusive_or_expression1730)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_and_expression_in_exclusive_or_expression1732)
                        self.and_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop59






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 54, exclusive_or_expression_StartIndex)

            pass

        return 

    # $ANTLR end exclusive_or_expression


    # $ANTLR start and_expression
    # C.g:383:1: and_expression : equality_expression ( '&' equality_expression )* ;
    def and_expression(self, ):

        and_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 55):
                    return 

                # C.g:384:2: ( equality_expression ( '&' equality_expression )* )
                # C.g:384:4: equality_expression ( '&' equality_expression )*
                self.following.append(self.FOLLOW_equality_expression_in_and_expression1745)
                self.equality_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:384:24: ( '&' equality_expression )*
                while True: #loop60
                    alt60 = 2
                    LA60_0 = self.input.LA(1)

                    if (LA60_0 == 66) :
                        alt60 = 1


                    if alt60 == 1:
                        # C.g:384:25: '&' equality_expression
                        self.match(self.input, 66, self.FOLLOW_66_in_and_expression1748)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_equality_expression_in_and_expression1750)
                        self.equality_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop60






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 55, and_expression_StartIndex)

            pass

        return 

    # $ANTLR end and_expression


    # $ANTLR start equality_expression
    # C.g:386:1: equality_expression : relational_expression ( ( '==' | '!=' ) relational_expression )* ;
    def equality_expression(self, ):

        equality_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 56):
                    return 

                # C.g:387:2: ( relational_expression ( ( '==' | '!=' ) relational_expression )* )
                # C.g:387:4: relational_expression ( ( '==' | '!=' ) relational_expression )*
                self.following.append(self.FOLLOW_relational_expression_in_equality_expression1762)
                self.relational_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:387:26: ( ( '==' | '!=' ) relational_expression )*
                while True: #loop61
                    alt61 = 2
                    LA61_0 = self.input.LA(1)

                    if ((84 <= LA61_0 <= 85)) :
                        alt61 = 1


                    if alt61 == 1:
                        # C.g:387:27: ( '==' | '!=' ) relational_expression
                        if (84 <= self.input.LA(1) <= 85):
                            self.input.consume();
                            self.errorRecovery = False
                            self.failed = False

                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            mse = MismatchedSetException(None, self.input)
                            self.recoverFromMismatchedSet(
                                self.input, mse, self.FOLLOW_set_in_equality_expression1765
                                )
                            raise mse


                        self.following.append(self.FOLLOW_relational_expression_in_equality_expression1771)
                        self.relational_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop61






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 56, equality_expression_StartIndex)

            pass

        return 

    # $ANTLR end equality_expression


    # $ANTLR start relational_expression
    # C.g:390:1: relational_expression : shift_expression ( ( '<' | '>' | '<=' | '>=' ) shift_expression )* ;
    def relational_expression(self, ):

        relational_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 57):
                    return 

                # C.g:391:2: ( shift_expression ( ( '<' | '>' | '<=' | '>=' ) shift_expression )* )
                # C.g:391:4: shift_expression ( ( '<' | '>' | '<=' | '>=' ) shift_expression )*
                self.following.append(self.FOLLOW_shift_expression_in_relational_expression1784)
                self.shift_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:391:21: ( ( '<' | '>' | '<=' | '>=' ) shift_expression )*
                while True: #loop62
                    alt62 = 2
                    LA62_0 = self.input.LA(1)

                    if ((86 <= LA62_0 <= 89)) :
                        alt62 = 1


                    if alt62 == 1:
                        # C.g:391:22: ( '<' | '>' | '<=' | '>=' ) shift_expression
                        if (86 <= self.input.LA(1) <= 89):
                            self.input.consume();
                            self.errorRecovery = False
                            self.failed = False

                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            mse = MismatchedSetException(None, self.input)
                            self.recoverFromMismatchedSet(
                                self.input, mse, self.FOLLOW_set_in_relational_expression1787
                                )
                            raise mse


                        self.following.append(self.FOLLOW_shift_expression_in_relational_expression1797)
                        self.shift_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop62






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 57, relational_expression_StartIndex)

            pass

        return 

    # $ANTLR end relational_expression


    # $ANTLR start shift_expression
    # C.g:394:1: shift_expression : additive_expression ( ( '<<' | '>>' ) additive_expression )* ;
    def shift_expression(self, ):

        shift_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 58):
                    return 

                # C.g:395:2: ( additive_expression ( ( '<<' | '>>' ) additive_expression )* )
                # C.g:395:4: additive_expression ( ( '<<' | '>>' ) additive_expression )*
                self.following.append(self.FOLLOW_additive_expression_in_shift_expression1810)
                self.additive_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:395:24: ( ( '<<' | '>>' ) additive_expression )*
                while True: #loop63
                    alt63 = 2
                    LA63_0 = self.input.LA(1)

                    if ((90 <= LA63_0 <= 91)) :
                        alt63 = 1


                    if alt63 == 1:
                        # C.g:395:25: ( '<<' | '>>' ) additive_expression
                        if (90 <= self.input.LA(1) <= 91):
                            self.input.consume();
                            self.errorRecovery = False
                            self.failed = False

                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            mse = MismatchedSetException(None, self.input)
                            self.recoverFromMismatchedSet(
                                self.input, mse, self.FOLLOW_set_in_shift_expression1813
                                )
                            raise mse


                        self.following.append(self.FOLLOW_additive_expression_in_shift_expression1819)
                        self.additive_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop63






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 58, shift_expression_StartIndex)

            pass

        return 

    # $ANTLR end shift_expression


    # $ANTLR start statement
    # C.g:400:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | macro_statement );
    def statement(self, ):

        statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 59):
                    return 

                # C.g:401:2: ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | macro_statement )
                alt64 = 7
                LA64 = self.input.LA(1)
                if LA64 == IDENTIFIER:
                    LA64 = self.input.LA(2)
                    if LA64 == 45:
                        alt64 = 1
                    elif LA64 == 51:
                        LA64_22 = self.input.LA(3)

                        if (self.synpred138()) :
                            alt64 = 3
                        elif (True) :
                            alt64 = 7
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("400:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | macro_statement );", 64, 22, self.input)

                            raise nvae

                    elif LA64 == 25 or LA64 == 26 or LA64 == 27 or LA64 == 53 or LA64 == 55 or LA64 == 57 or LA64 == 58 or LA64 == 59 or LA64 == 60 or LA64 == 61 or LA64 == 62 or LA64 == 64 or LA64 == 65 or LA64 == 66 or LA64 == 69 or LA64 == 70 or LA64 == 71 or LA64 == 72 or LA64 == 73 or LA64 == 74 or LA64 == 75 or LA64 == 76 or LA64 == 77 or LA64 == 78 or LA64 == 79 or LA64 == 80 or LA64 == 81 or LA64 == 82 or LA64 == 83 or LA64 == 84 or LA64 == 85 or LA64 == 86 or LA64 == 87 or LA64 == 88 or LA64 == 89 or LA64 == 90 or LA64 == 91:
                        alt64 = 3
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("400:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | macro_statement );", 64, 1, self.input)

                        raise nvae

                elif LA64 == 92 or LA64 == 93:
                    alt64 = 1
                elif LA64 == 41:
                    alt64 = 2
                elif LA64 == HEX_LITERAL or LA64 == OCTAL_LITERAL or LA64 == DECIMAL_LITERAL or LA64 == CHARACTER_LITERAL or LA64 == STRING_LITERAL or LA64 == FLOATING_POINT_LITERAL or LA64 == 25 or LA64 == 51 or LA64 == 55 or LA64 == 57 or LA64 == 58 or LA64 == 61 or LA64 == 62 or LA64 == 63 or LA64 == 66 or LA64 == 67 or LA64 == 68:
                    alt64 = 3
                elif LA64 == 94 or LA64 == 96:
                    alt64 = 4
                elif LA64 == 97 or LA64 == 98 or LA64 == 99:
                    alt64 = 5
                elif LA64 == 100 or LA64 == 101 or LA64 == 102 or LA64 == 103:
                    alt64 = 6
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("400:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | macro_statement );", 64, 0, self.input)

                    raise nvae

                if alt64 == 1:
                    # C.g:401:4: labeled_statement
                    self.following.append(self.FOLLOW_labeled_statement_in_statement1834)
                    self.labeled_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 2:
                    # C.g:402:4: compound_statement
                    self.following.append(self.FOLLOW_compound_statement_in_statement1839)
                    self.compound_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 3:
                    # C.g:403:4: expression_statement
                    self.following.append(self.FOLLOW_expression_statement_in_statement1844)
                    self.expression_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 4:
                    # C.g:404:4: selection_statement
                    self.following.append(self.FOLLOW_selection_statement_in_statement1849)
                    self.selection_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 5:
                    # C.g:405:4: iteration_statement
                    self.following.append(self.FOLLOW_iteration_statement_in_statement1854)
                    self.iteration_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 6:
                    # C.g:406:4: jump_statement
                    self.following.append(self.FOLLOW_jump_statement_in_statement1859)
                    self.jump_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 7:
                    # C.g:407:4: macro_statement
                    self.following.append(self.FOLLOW_macro_statement_in_statement1864)
                    self.macro_statement()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 59, statement_StartIndex)

            pass

        return 

    # $ANTLR end statement


    # $ANTLR start macro_statement
    # C.g:410:1: macro_statement : IDENTIFIER '(' ( IDENTIFIER | ( declaration )* ( statement_list )? ) ')' ;
    def macro_statement(self, ):

        macro_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 60):
                    return 

                # C.g:411:2: ( IDENTIFIER '(' ( IDENTIFIER | ( declaration )* ( statement_list )? ) ')' )
                # C.g:411:4: IDENTIFIER '(' ( IDENTIFIER | ( declaration )* ( statement_list )? ) ')'
                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_macro_statement1875)
                if self.failed:
                    return 
                self.match(self.input, 51, self.FOLLOW_51_in_macro_statement1877)
                if self.failed:
                    return 
                # C.g:411:19: ( IDENTIFIER | ( declaration )* ( statement_list )? )
                alt67 = 2
                LA67_0 = self.input.LA(1)

                if (LA67_0 == IDENTIFIER) :
                    LA67_1 = self.input.LA(2)

                    if (LA67_1 == IDENTIFIER or (25 <= LA67_1 <= 40) or (43 <= LA67_1 <= 51) or LA67_1 == 53 or LA67_1 == 55 or (57 <= LA67_1 <= 62) or (64 <= LA67_1 <= 66) or (69 <= LA67_1 <= 91)) :
                        alt67 = 2
                    elif (LA67_1 == 52) :
                        alt67 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("411:19: ( IDENTIFIER | ( declaration )* ( statement_list )? )", 67, 1, self.input)

                        raise nvae

                elif ((HEX_LITERAL <= LA67_0 <= FLOATING_POINT_LITERAL) or (24 <= LA67_0 <= 25) or (28 <= LA67_0 <= 41) or (43 <= LA67_0 <= 44) or (46 <= LA67_0 <= 52) or LA67_0 == 55 or (57 <= LA67_0 <= 58) or (61 <= LA67_0 <= 63) or (66 <= LA67_0 <= 68) or (92 <= LA67_0 <= 94) or (96 <= LA67_0 <= 103)) :
                    alt67 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("411:19: ( IDENTIFIER | ( declaration )* ( statement_list )? )", 67, 0, self.input)

                    raise nvae

                if alt67 == 1:
                    # C.g:411:20: IDENTIFIER
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_macro_statement1880)
                    if self.failed:
                        return 


                elif alt67 == 2:
                    # C.g:411:33: ( declaration )* ( statement_list )?
                    # C.g:411:33: ( declaration )*
                    while True: #loop65
                        alt65 = 2
                        LA65_0 = self.input.LA(1)

                        if (LA65_0 == IDENTIFIER) :
                            LA65 = self.input.LA(2)
                            if LA65 == 51:
                                LA65_37 = self.input.LA(3)

                                if (self.synpred143()) :
                                    alt65 = 1


                            elif LA65 == 55:
                                LA65_38 = self.input.LA(3)

                                if (self.synpred143()) :
                                    alt65 = 1


                            elif LA65 == IDENTIFIER or LA65 == 28 or LA65 == 29 or LA65 == 30 or LA65 == 31 or LA65 == 32 or LA65 == 33 or LA65 == 34 or LA65 == 35 or LA65 == 36 or LA65 == 37 or LA65 == 38 or LA65 == 39 or LA65 == 40 or LA65 == 43 or LA65 == 44 or LA65 == 46 or LA65 == 47 or LA65 == 48 or LA65 == 49 or LA65 == 50:
                                alt65 = 1
                            elif LA65 == 25:
                                LA65_40 = self.input.LA(3)

                                if (self.synpred143()) :
                                    alt65 = 1



                        elif (LA65_0 == 24 or (28 <= LA65_0 <= 40) or (43 <= LA65_0 <= 44) or (46 <= LA65_0 <= 50)) :
                            alt65 = 1


                        if alt65 == 1:
                            # C.g:0:0: declaration
                            self.following.append(self.FOLLOW_declaration_in_macro_statement1884)
                            self.declaration()
                            self.following.pop()
                            if self.failed:
                                return 


                        else:
                            break #loop65


                    # C.g:411:47: ( statement_list )?
                    alt66 = 2
                    LA66_0 = self.input.LA(1)

                    if ((IDENTIFIER <= LA66_0 <= FLOATING_POINT_LITERAL) or LA66_0 == 25 or LA66_0 == 41 or LA66_0 == 51 or LA66_0 == 55 or (57 <= LA66_0 <= 58) or (61 <= LA66_0 <= 63) or (66 <= LA66_0 <= 68) or (92 <= LA66_0 <= 94) or (96 <= LA66_0 <= 103)) :
                        alt66 = 1
                    if alt66 == 1:
                        # C.g:0:0: statement_list
                        self.following.append(self.FOLLOW_statement_list_in_macro_statement1888)
                        self.statement_list()
                        self.following.pop()
                        if self.failed:
                            return 






                self.match(self.input, 52, self.FOLLOW_52_in_macro_statement1892)
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 60, macro_statement_StartIndex)

            pass

        return 

    # $ANTLR end macro_statement


    # $ANTLR start labeled_statement
    # C.g:414:1: labeled_statement : ( IDENTIFIER ':' statement | 'case' constant_expression ':' statement | 'default' ':' statement );
    def labeled_statement(self, ):

        labeled_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 61):
                    return 

                # C.g:415:2: ( IDENTIFIER ':' statement | 'case' constant_expression ':' statement | 'default' ':' statement )
                alt68 = 3
                LA68 = self.input.LA(1)
                if LA68 == IDENTIFIER:
                    alt68 = 1
                elif LA68 == 92:
                    alt68 = 2
                elif LA68 == 93:
                    alt68 = 3
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("414:1: labeled_statement : ( IDENTIFIER ':' statement | 'case' constant_expression ':' statement | 'default' ':' statement );", 68, 0, self.input)

                    raise nvae

                if alt68 == 1:
                    # C.g:415:4: IDENTIFIER ':' statement
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_labeled_statement1904)
                    if self.failed:
                        return 
                    self.match(self.input, 45, self.FOLLOW_45_in_labeled_statement1906)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_labeled_statement1908)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt68 == 2:
                    # C.g:416:4: 'case' constant_expression ':' statement
                    self.match(self.input, 92, self.FOLLOW_92_in_labeled_statement1913)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_labeled_statement1915)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 45, self.FOLLOW_45_in_labeled_statement1917)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_labeled_statement1919)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt68 == 3:
                    # C.g:417:4: 'default' ':' statement
                    self.match(self.input, 93, self.FOLLOW_93_in_labeled_statement1924)
                    if self.failed:
                        return 
                    self.match(self.input, 45, self.FOLLOW_45_in_labeled_statement1926)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_labeled_statement1928)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 61, labeled_statement_StartIndex)

            pass

        return 

    # $ANTLR end labeled_statement


    # $ANTLR start compound_statement
    # C.g:420:1: compound_statement : '{' ( declaration )* ( statement_list )? '}' ;
    def compound_statement(self, ):
        self.Symbols_stack.append(Symbols_scope())

        compound_statement_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 62):
                    return 

                # C.g:425:2: ( '{' ( declaration )* ( statement_list )? '}' )
                # C.g:425:4: '{' ( declaration )* ( statement_list )? '}'
                self.match(self.input, 41, self.FOLLOW_41_in_compound_statement1950)
                if self.failed:
                    return 
                # C.g:425:8: ( declaration )*
                while True: #loop69
                    alt69 = 2
                    LA69_0 = self.input.LA(1)

                    if (LA69_0 == IDENTIFIER) :
                        LA69 = self.input.LA(2)
                        if LA69 == 51:
                            LA69_36 = self.input.LA(3)

                            if (self.synpred147()) :
                                alt69 = 1


                        elif LA69 == 55:
                            LA69_38 = self.input.LA(3)

                            if (self.synpred147()) :
                                alt69 = 1


                        elif LA69 == IDENTIFIER or LA69 == 28 or LA69 == 29 or LA69 == 30 or LA69 == 31 or LA69 == 32 or LA69 == 33 or LA69 == 34 or LA69 == 35 or LA69 == 36 or LA69 == 37 or LA69 == 38 or LA69 == 39 or LA69 == 40 or LA69 == 43 or LA69 == 44 or LA69 == 46 or LA69 == 47 or LA69 == 48 or LA69 == 49 or LA69 == 50:
                            alt69 = 1
                        elif LA69 == 25:
                            LA69_40 = self.input.LA(3)

                            if (self.synpred147()) :
                                alt69 = 1



                    elif (LA69_0 == 24 or (28 <= LA69_0 <= 40) or (43 <= LA69_0 <= 44) or (46 <= LA69_0 <= 50)) :
                        alt69 = 1


                    if alt69 == 1:
                        # C.g:0:0: declaration
                        self.following.append(self.FOLLOW_declaration_in_compound_statement1952)
                        self.declaration()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop69


                # C.g:425:21: ( statement_list )?
                alt70 = 2
                LA70_0 = self.input.LA(1)

                if ((IDENTIFIER <= LA70_0 <= FLOATING_POINT_LITERAL) or LA70_0 == 25 or LA70_0 == 41 or LA70_0 == 51 or LA70_0 == 55 or (57 <= LA70_0 <= 58) or (61 <= LA70_0 <= 63) or (66 <= LA70_0 <= 68) or (92 <= LA70_0 <= 94) or (96 <= LA70_0 <= 103)) :
                    alt70 = 1
                if alt70 == 1:
                    # C.g:0:0: statement_list
                    self.following.append(self.FOLLOW_statement_list_in_compound_statement1955)
                    self.statement_list()
                    self.following.pop()
                    if self.failed:
                        return 



                self.match(self.input, 42, self.FOLLOW_42_in_compound_statement1958)
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 62, compound_statement_StartIndex)

            self.Symbols_stack.pop()

            pass

        return 

    # $ANTLR end compound_statement


    # $ANTLR start statement_list
    # C.g:428:1: statement_list : ( statement )+ ;
    def statement_list(self, ):

        statement_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 63):
                    return 

                # C.g:429:2: ( ( statement )+ )
                # C.g:429:4: ( statement )+
                # C.g:429:4: ( statement )+
                cnt71 = 0
                while True: #loop71
                    alt71 = 2
                    LA71_0 = self.input.LA(1)

                    if ((IDENTIFIER <= LA71_0 <= FLOATING_POINT_LITERAL) or LA71_0 == 25 or LA71_0 == 41 or LA71_0 == 51 or LA71_0 == 55 or (57 <= LA71_0 <= 58) or (61 <= LA71_0 <= 63) or (66 <= LA71_0 <= 68) or (92 <= LA71_0 <= 94) or (96 <= LA71_0 <= 103)) :
                        alt71 = 1


                    if alt71 == 1:
                        # C.g:0:0: statement
                        self.following.append(self.FOLLOW_statement_in_statement_list1969)
                        self.statement()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt71 >= 1:
                            break #loop71

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(71, self.input)
                        raise eee

                    cnt71 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 63, statement_list_StartIndex)

            pass

        return 

    # $ANTLR end statement_list


    # $ANTLR start expression_statement
    # C.g:432:1: expression_statement : ( ';' | expression ';' );
    def expression_statement(self, ):

        expression_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 64):
                    return 

                # C.g:433:2: ( ';' | expression ';' )
                alt72 = 2
                LA72_0 = self.input.LA(1)

                if (LA72_0 == 25) :
                    alt72 = 1
                elif ((IDENTIFIER <= LA72_0 <= FLOATING_POINT_LITERAL) or LA72_0 == 51 or LA72_0 == 55 or (57 <= LA72_0 <= 58) or (61 <= LA72_0 <= 63) or (66 <= LA72_0 <= 68)) :
                    alt72 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("432:1: expression_statement : ( ';' | expression ';' );", 72, 0, self.input)

                    raise nvae

                if alt72 == 1:
                    # C.g:433:4: ';'
                    self.match(self.input, 25, self.FOLLOW_25_in_expression_statement1981)
                    if self.failed:
                        return 


                elif alt72 == 2:
                    # C.g:434:4: expression ';'
                    self.following.append(self.FOLLOW_expression_in_expression_statement1986)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 25, self.FOLLOW_25_in_expression_statement1988)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 64, expression_statement_StartIndex)

            pass

        return 

    # $ANTLR end expression_statement


    # $ANTLR start selection_statement
    # C.g:437:1: selection_statement : ( 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )? | 'switch' '(' expression ')' statement );
    def selection_statement(self, ):

        selection_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 65):
                    return 

                # C.g:438:2: ( 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )? | 'switch' '(' expression ')' statement )
                alt74 = 2
                LA74_0 = self.input.LA(1)

                if (LA74_0 == 94) :
                    alt74 = 1
                elif (LA74_0 == 96) :
                    alt74 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("437:1: selection_statement : ( 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )? | 'switch' '(' expression ')' statement );", 74, 0, self.input)

                    raise nvae

                if alt74 == 1:
                    # C.g:438:4: 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )?
                    self.match(self.input, 94, self.FOLLOW_94_in_selection_statement1999)
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_selection_statement2001)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_selection_statement2003)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_selection_statement2005)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_selection_statement2007)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:438:38: ( options {k=1; backtrack=false; } : 'else' statement )?
                    alt73 = 2
                    LA73_0 = self.input.LA(1)

                    if (LA73_0 == 95) :
                        alt73 = 1
                    if alt73 == 1:
                        # C.g:438:71: 'else' statement
                        self.match(self.input, 95, self.FOLLOW_95_in_selection_statement2022)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_statement_in_selection_statement2024)
                        self.statement()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt74 == 2:
                    # C.g:439:4: 'switch' '(' expression ')' statement
                    self.match(self.input, 96, self.FOLLOW_96_in_selection_statement2031)
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_selection_statement2033)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_selection_statement2035)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_selection_statement2037)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_selection_statement2039)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 65, selection_statement_StartIndex)

            pass

        return 

    # $ANTLR end selection_statement


    # $ANTLR start iteration_statement
    # C.g:442:1: iteration_statement : ( 'while' '(' expression ')' statement | 'do' statement 'while' '(' expression ')' ';' | 'for' '(' expression_statement expression_statement ( expression )? ')' statement );
    def iteration_statement(self, ):

        iteration_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 66):
                    return 

                # C.g:443:2: ( 'while' '(' expression ')' statement | 'do' statement 'while' '(' expression ')' ';' | 'for' '(' expression_statement expression_statement ( expression )? ')' statement )
                alt76 = 3
                LA76 = self.input.LA(1)
                if LA76 == 97:
                    alt76 = 1
                elif LA76 == 98:
                    alt76 = 2
                elif LA76 == 99:
                    alt76 = 3
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("442:1: iteration_statement : ( 'while' '(' expression ')' statement | 'do' statement 'while' '(' expression ')' ';' | 'for' '(' expression_statement expression_statement ( expression )? ')' statement );", 76, 0, self.input)

                    raise nvae

                if alt76 == 1:
                    # C.g:443:4: 'while' '(' expression ')' statement
                    self.match(self.input, 97, self.FOLLOW_97_in_iteration_statement2050)
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_iteration_statement2052)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_iteration_statement2054)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_iteration_statement2056)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_iteration_statement2058)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt76 == 2:
                    # C.g:444:4: 'do' statement 'while' '(' expression ')' ';'
                    self.match(self.input, 98, self.FOLLOW_98_in_iteration_statement2063)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_iteration_statement2065)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 97, self.FOLLOW_97_in_iteration_statement2067)
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_iteration_statement2069)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_iteration_statement2071)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 52, self.FOLLOW_52_in_iteration_statement2073)
                    if self.failed:
                        return 
                    self.match(self.input, 25, self.FOLLOW_25_in_iteration_statement2075)
                    if self.failed:
                        return 


                elif alt76 == 3:
                    # C.g:445:4: 'for' '(' expression_statement expression_statement ( expression )? ')' statement
                    self.match(self.input, 99, self.FOLLOW_99_in_iteration_statement2080)
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_iteration_statement2082)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_statement_in_iteration_statement2084)
                    self.expression_statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_statement_in_iteration_statement2086)
                    self.expression_statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:445:56: ( expression )?
                    alt75 = 2
                    LA75_0 = self.input.LA(1)

                    if ((IDENTIFIER <= LA75_0 <= FLOATING_POINT_LITERAL) or LA75_0 == 51 or LA75_0 == 55 or (57 <= LA75_0 <= 58) or (61 <= LA75_0 <= 63) or (66 <= LA75_0 <= 68)) :
                        alt75 = 1
                    if alt75 == 1:
                        # C.g:0:0: expression
                        self.following.append(self.FOLLOW_expression_in_iteration_statement2088)
                        self.expression()
                        self.following.pop()
                        if self.failed:
                            return 



                    self.match(self.input, 52, self.FOLLOW_52_in_iteration_statement2091)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_iteration_statement2093)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 66, iteration_statement_StartIndex)

            pass

        return 

    # $ANTLR end iteration_statement


    # $ANTLR start jump_statement
    # C.g:448:1: jump_statement : ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' );
    def jump_statement(self, ):

        jump_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 67):
                    return 

                # C.g:449:2: ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' )
                alt77 = 5
                LA77 = self.input.LA(1)
                if LA77 == 100:
                    alt77 = 1
                elif LA77 == 101:
                    alt77 = 2
                elif LA77 == 102:
                    alt77 = 3
                elif LA77 == 103:
                    LA77_4 = self.input.LA(2)

                    if (LA77_4 == 25) :
                        alt77 = 4
                    elif ((IDENTIFIER <= LA77_4 <= FLOATING_POINT_LITERAL) or LA77_4 == 51 or LA77_4 == 55 or (57 <= LA77_4 <= 58) or (61 <= LA77_4 <= 63) or (66 <= LA77_4 <= 68)) :
                        alt77 = 5
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("448:1: jump_statement : ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' );", 77, 4, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("448:1: jump_statement : ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' );", 77, 0, self.input)

                    raise nvae

                if alt77 == 1:
                    # C.g:449:4: 'goto' IDENTIFIER ';'
                    self.match(self.input, 100, self.FOLLOW_100_in_jump_statement2104)
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_jump_statement2106)
                    if self.failed:
                        return 
                    self.match(self.input, 25, self.FOLLOW_25_in_jump_statement2108)
                    if self.failed:
                        return 


                elif alt77 == 2:
                    # C.g:450:4: 'continue' ';'
                    self.match(self.input, 101, self.FOLLOW_101_in_jump_statement2113)
                    if self.failed:
                        return 
                    self.match(self.input, 25, self.FOLLOW_25_in_jump_statement2115)
                    if self.failed:
                        return 


                elif alt77 == 3:
                    # C.g:451:4: 'break' ';'
                    self.match(self.input, 102, self.FOLLOW_102_in_jump_statement2120)
                    if self.failed:
                        return 
                    self.match(self.input, 25, self.FOLLOW_25_in_jump_statement2122)
                    if self.failed:
                        return 


                elif alt77 == 4:
                    # C.g:452:4: 'return' ';'
                    self.match(self.input, 103, self.FOLLOW_103_in_jump_statement2127)
                    if self.failed:
                        return 
                    self.match(self.input, 25, self.FOLLOW_25_in_jump_statement2129)
                    if self.failed:
                        return 


                elif alt77 == 5:
                    # C.g:453:4: 'return' expression ';'
                    self.match(self.input, 103, self.FOLLOW_103_in_jump_statement2134)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_jump_statement2136)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 25, self.FOLLOW_25_in_jump_statement2138)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 67, jump_statement_StartIndex)

            pass

        return 

    # $ANTLR end jump_statement

    # $ANTLR start synpred2
    def synpred2_fragment(self, ):
        # C.g:53:6: ( declaration_specifiers )
        # C.g:53:6: declaration_specifiers
        self.following.append(self.FOLLOW_declaration_specifiers_in_synpred2102)
        self.declaration_specifiers()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred2



    # $ANTLR start synpred4
    def synpred4_fragment(self, ):
        # C.g:53:4: ( ( declaration_specifiers )? declarator ( declaration )* '{' )
        # C.g:53:6: ( declaration_specifiers )? declarator ( declaration )* '{'
        # C.g:53:6: ( declaration_specifiers )?
        alt78 = 2
        LA78_0 = self.input.LA(1)

        if ((28 <= LA78_0 <= 40) or (43 <= LA78_0 <= 44) or (46 <= LA78_0 <= 50)) :
            alt78 = 1
        elif (LA78_0 == IDENTIFIER) :
            LA78 = self.input.LA(2)
            if LA78 == 55:
                alt78 = 1
            elif LA78 == IDENTIFIER:
                LA78_18 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 51:
                LA78_19 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 28 or LA78 == 29 or LA78 == 30 or LA78 == 31:
                LA78_20 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 32:
                LA78_21 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 33:
                LA78_22 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 34:
                LA78_23 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 35:
                LA78_24 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 36:
                LA78_25 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 37:
                LA78_26 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 38:
                LA78_27 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 39:
                LA78_28 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 40:
                LA78_29 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 43 or LA78 == 44:
                LA78_30 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 46:
                LA78_31 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
            elif LA78 == 47 or LA78 == 48 or LA78 == 49 or LA78 == 50:
                LA78_32 = self.input.LA(3)

                if (self.synpred2()) :
                    alt78 = 1
        if alt78 == 1:
            # C.g:0:0: declaration_specifiers
            self.following.append(self.FOLLOW_declaration_specifiers_in_synpred4102)
            self.declaration_specifiers()
            self.following.pop()
            if self.failed:
                return 



        self.following.append(self.FOLLOW_declarator_in_synpred4105)
        self.declarator()
        self.following.pop()
        if self.failed:
            return 
        # C.g:53:41: ( declaration )*
        while True: #loop79
            alt79 = 2
            LA79_0 = self.input.LA(1)

            if (LA79_0 == IDENTIFIER or LA79_0 == 24 or (28 <= LA79_0 <= 40) or (43 <= LA79_0 <= 44) or (46 <= LA79_0 <= 50)) :
                alt79 = 1


            if alt79 == 1:
                # C.g:0:0: declaration
                self.following.append(self.FOLLOW_declaration_in_synpred4107)
                self.declaration()
                self.following.pop()
                if self.failed:
                    return 


            else:
                break #loop79


        self.match(self.input, 41, self.FOLLOW_41_in_synpred4110)
        if self.failed:
            return 


    # $ANTLR end synpred4



    # $ANTLR start synpred5
    def synpred5_fragment(self, ):
        # C.g:54:4: ( declaration )
        # C.g:54:4: declaration
        self.following.append(self.FOLLOW_declaration_in_synpred5120)
        self.declaration()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred5



    # $ANTLR start synpred6
    def synpred6_fragment(self, ):
        # C.g:70:4: ( declaration_specifiers )
        # C.g:70:4: declaration_specifiers
        self.following.append(self.FOLLOW_declaration_specifiers_in_synpred6153)
        self.declaration_specifiers()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred6



    # $ANTLR start synpred9
    def synpred9_fragment(self, ):
        # C.g:83:16: ( declaration_specifiers )
        # C.g:83:16: declaration_specifiers
        self.following.append(self.FOLLOW_declaration_specifiers_in_synpred9206)
        self.declaration_specifiers()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred9



    # $ANTLR start synpred13
    def synpred13_fragment(self, ):
        # C.g:91:7: ( type_specifier )
        # C.g:91:7: type_specifier
        self.following.append(self.FOLLOW_type_specifier_in_synpred13253)
        self.type_specifier()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred13



    # $ANTLR start synpred31
    def synpred31_fragment(self, ):
        # C.g:125:4: ( IDENTIFIER declarator )
        # C.g:125:5: IDENTIFIER declarator
        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_synpred31417)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_declarator_in_synpred31419)
        self.declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred31



    # $ANTLR start synpred37
    def synpred37_fragment(self, ):
        # C.g:157:23: ( type_specifier )
        # C.g:157:23: type_specifier
        self.following.append(self.FOLLOW_type_specifier_in_synpred37554)
        self.type_specifier()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred37



    # $ANTLR start synpred49
    def synpred49_fragment(self, ):
        # C.g:192:4: ( ( pointer )? direct_declarator )
        # C.g:192:4: ( pointer )? direct_declarator
        # C.g:192:4: ( pointer )?
        alt84 = 2
        LA84_0 = self.input.LA(1)

        if (LA84_0 == 55) :
            alt84 = 1
        if alt84 == 1:
            # C.g:0:0: pointer
            self.following.append(self.FOLLOW_pointer_in_synpred49717)
            self.pointer()
            self.following.pop()
            if self.failed:
                return 



        self.following.append(self.FOLLOW_direct_declarator_in_synpred49720)
        self.direct_declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred49



    # $ANTLR start synpred50
    def synpred50_fragment(self, ):
        # C.g:198:15: ( declarator_suffix )
        # C.g:198:15: declarator_suffix
        self.following.append(self.FOLLOW_declarator_suffix_in_synpred50743)
        self.declarator_suffix()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred50



    # $ANTLR start synpred52
    def synpred52_fragment(self, ):
        # C.g:200:23: ( declarator_suffix )
        # C.g:200:23: declarator_suffix
        self.following.append(self.FOLLOW_declarator_suffix_in_synpred52759)
        self.declarator_suffix()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred52



    # $ANTLR start synpred55
    def synpred55_fragment(self, ):
        # C.g:206:9: ( '(' parameter_type_list ')' )
        # C.g:206:9: '(' parameter_type_list ')'
        self.match(self.input, 51, self.FOLLOW_51_in_synpred55799)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_parameter_type_list_in_synpred55801)
        self.parameter_type_list()
        self.following.pop()
        if self.failed:
            return 
        self.match(self.input, 52, self.FOLLOW_52_in_synpred55803)
        if self.failed:
            return 


    # $ANTLR end synpred55



    # $ANTLR start synpred56
    def synpred56_fragment(self, ):
        # C.g:207:9: ( '(' identifier_list ')' )
        # C.g:207:9: '(' identifier_list ')'
        self.match(self.input, 51, self.FOLLOW_51_in_synpred56813)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_identifier_list_in_synpred56815)
        self.identifier_list()
        self.following.pop()
        if self.failed:
            return 
        self.match(self.input, 52, self.FOLLOW_52_in_synpred56817)
        if self.failed:
            return 


    # $ANTLR end synpred56



    # $ANTLR start synpred57
    def synpred57_fragment(self, ):
        # C.g:212:8: ( type_qualifier )
        # C.g:212:8: type_qualifier
        self.following.append(self.FOLLOW_type_qualifier_in_synpred57842)
        self.type_qualifier()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred57



    # $ANTLR start synpred58
    def synpred58_fragment(self, ):
        # C.g:212:24: ( pointer )
        # C.g:212:24: pointer
        self.following.append(self.FOLLOW_pointer_in_synpred58845)
        self.pointer()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred58



    # $ANTLR start synpred59
    def synpred59_fragment(self, ):
        # C.g:212:4: ( '*' ( type_qualifier )+ ( pointer )? )
        # C.g:212:4: '*' ( type_qualifier )+ ( pointer )?
        self.match(self.input, 55, self.FOLLOW_55_in_synpred59840)
        if self.failed:
            return 
        # C.g:212:8: ( type_qualifier )+
        cnt86 = 0
        while True: #loop86
            alt86 = 2
            LA86_0 = self.input.LA(1)

            if ((47 <= LA86_0 <= 50)) :
                alt86 = 1


            if alt86 == 1:
                # C.g:0:0: type_qualifier
                self.following.append(self.FOLLOW_type_qualifier_in_synpred59842)
                self.type_qualifier()
                self.following.pop()
                if self.failed:
                    return 


            else:
                if cnt86 >= 1:
                    break #loop86

                if self.backtracking > 0:
                    self.failed = True
                    return 

                eee = EarlyExitException(86, self.input)
                raise eee

            cnt86 += 1


        # C.g:212:24: ( pointer )?
        alt87 = 2
        LA87_0 = self.input.LA(1)

        if (LA87_0 == 55) :
            alt87 = 1
        if alt87 == 1:
            # C.g:0:0: pointer
            self.following.append(self.FOLLOW_pointer_in_synpred59845)
            self.pointer()
            self.following.pop()
            if self.failed:
                return 





    # $ANTLR end synpred59



    # $ANTLR start synpred60
    def synpred60_fragment(self, ):
        # C.g:213:4: ( '*' pointer )
        # C.g:213:4: '*' pointer
        self.match(self.input, 55, self.FOLLOW_55_in_synpred60851)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_pointer_in_synpred60853)
        self.pointer()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred60



    # $ANTLR start synpred63
    def synpred63_fragment(self, ):
        # C.g:226:28: ( declarator )
        # C.g:226:28: declarator
        self.following.append(self.FOLLOW_declarator_in_synpred63910)
        self.declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred63



    # $ANTLR start synpred64
    def synpred64_fragment(self, ):
        # C.g:226:39: ( abstract_declarator )
        # C.g:226:39: abstract_declarator
        self.following.append(self.FOLLOW_abstract_declarator_in_synpred64912)
        self.abstract_declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred64



    # $ANTLR start synpred67
    def synpred67_fragment(self, ):
        # C.g:235:4: ( specifier_qualifier_list ( abstract_declarator )? )
        # C.g:235:4: specifier_qualifier_list ( abstract_declarator )?
        self.following.append(self.FOLLOW_specifier_qualifier_list_in_synpred67951)
        self.specifier_qualifier_list()
        self.following.pop()
        if self.failed:
            return 
        # C.g:235:29: ( abstract_declarator )?
        alt88 = 2
        LA88_0 = self.input.LA(1)

        if (LA88_0 == 51 or LA88_0 == 53 or LA88_0 == 55) :
            alt88 = 1
        if alt88 == 1:
            # C.g:0:0: abstract_declarator
            self.following.append(self.FOLLOW_abstract_declarator_in_synpred67953)
            self.abstract_declarator()
            self.following.pop()
            if self.failed:
                return 





    # $ANTLR end synpred67



    # $ANTLR start synpred68
    def synpred68_fragment(self, ):
        # C.g:240:12: ( direct_abstract_declarator )
        # C.g:240:12: direct_abstract_declarator
        self.following.append(self.FOLLOW_direct_abstract_declarator_in_synpred68972)
        self.direct_abstract_declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred68



    # $ANTLR start synpred71
    def synpred71_fragment(self, ):
        # C.g:245:65: ( abstract_declarator_suffix )
        # C.g:245:65: abstract_declarator_suffix
        self.following.append(self.FOLLOW_abstract_declarator_suffix_in_synpred711003)
        self.abstract_declarator_suffix()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred71



    # $ANTLR start synpred84
    def synpred84_fragment(self, ):
        # C.g:280:4: ( '(' type_name ')' cast_expression )
        # C.g:280:4: '(' type_name ')' cast_expression
        self.match(self.input, 51, self.FOLLOW_51_in_synpred841177)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_type_name_in_synpred841179)
        self.type_name()
        self.following.pop()
        if self.failed:
            return 
        self.match(self.input, 52, self.FOLLOW_52_in_synpred841181)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_cast_expression_in_synpred841183)
        self.cast_expression()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred84



    # $ANTLR start synpred89
    def synpred89_fragment(self, ):
        # C.g:289:4: ( 'sizeof' unary_expression )
        # C.g:289:4: 'sizeof' unary_expression
        self.match(self.input, 63, self.FOLLOW_63_in_synpred891225)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_unary_expression_in_synpred891227)
        self.unary_expression()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred89



    # $ANTLR start synpred94
    def synpred94_fragment(self, ):
        # C.g:299:13: ( '*' IDENTIFIER )
        # C.g:299:13: '*' IDENTIFIER
        self.match(self.input, 55, self.FOLLOW_55_in_synpred941333)
        if self.failed:
            return 
        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_synpred941335)
        if self.failed:
            return 


    # $ANTLR end synpred94



    # $ANTLR start synpred111
    def synpred111_fragment(self, ):
        # C.g:341:4: ( lvalue assignment_operator assignment_expression )
        # C.g:341:4: lvalue assignment_operator assignment_expression
        self.following.append(self.FOLLOW_lvalue_in_synpred1111558)
        self.lvalue()
        self.following.pop()
        if self.failed:
            return 
        self.following.append(self.FOLLOW_assignment_operator_in_synpred1111560)
        self.assignment_operator()
        self.following.pop()
        if self.failed:
            return 
        self.following.append(self.FOLLOW_assignment_expression_in_synpred1111562)
        self.assignment_expression()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred111



    # $ANTLR start synpred138
    def synpred138_fragment(self, ):
        # C.g:403:4: ( expression_statement )
        # C.g:403:4: expression_statement
        self.following.append(self.FOLLOW_expression_statement_in_synpred1381844)
        self.expression_statement()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred138



    # $ANTLR start synpred143
    def synpred143_fragment(self, ):
        # C.g:411:33: ( declaration )
        # C.g:411:33: declaration
        self.following.append(self.FOLLOW_declaration_in_synpred1431884)
        self.declaration()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred143



    # $ANTLR start synpred147
    def synpred147_fragment(self, ):
        # C.g:425:8: ( declaration )
        # C.g:425:8: declaration
        self.following.append(self.FOLLOW_declaration_in_synpred1471952)
        self.declaration()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred147



    def synpred143(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred143_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred37(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred37_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred84(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred84_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred68(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred68_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred49(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred49_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred4(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred4_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred31(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred31_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred9(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred9_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred56(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred56_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred111(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred111_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred63(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred63_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred59(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred59_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred2(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred2_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred50(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred50_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred94(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred94_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred58(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred58_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred147(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred147_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred64(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred64_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred89(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred89_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred57(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred57_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred52(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred52_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred67(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred67_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred5(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred5_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred6(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred6_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred60(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred60_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred138(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred138_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred13(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred13_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred71(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred71_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred55(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred55_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success



 

    FOLLOW_external_declaration_in_translation_unit76 = frozenset([1, 4, 24, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50, 51, 55])
    FOLLOW_function_definition_in_external_declaration115 = frozenset([1])
    FOLLOW_declaration_in_external_declaration120 = frozenset([1])
    FOLLOW_macro_statement_in_external_declaration125 = frozenset([1])
    FOLLOW_declaration_specifiers_in_function_definition153 = frozenset([4, 51, 55])
    FOLLOW_declarator_in_function_definition156 = frozenset([4, 24, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_declaration_in_function_definition162 = frozenset([4, 24, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_compound_statement_in_function_definition165 = frozenset([1])
    FOLLOW_compound_statement_in_function_definition172 = frozenset([1])
    FOLLOW_24_in_declaration204 = frozenset([4, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50, 51, 55])
    FOLLOW_declaration_specifiers_in_declaration206 = frozenset([4, 51, 55])
    FOLLOW_init_declarator_list_in_declaration213 = frozenset([25])
    FOLLOW_25_in_declaration215 = frozenset([1])
    FOLLOW_declaration_specifiers_in_declaration221 = frozenset([4, 25, 51, 55])
    FOLLOW_init_declarator_list_in_declaration223 = frozenset([25])
    FOLLOW_25_in_declaration226 = frozenset([1])
    FOLLOW_storage_class_specifier_in_declaration_specifiers245 = frozenset([1, 4, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_type_specifier_in_declaration_specifiers253 = frozenset([1, 4, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_type_qualifier_in_declaration_specifiers267 = frozenset([1, 4, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_init_declarator_in_init_declarator_list289 = frozenset([1, 26])
    FOLLOW_26_in_init_declarator_list292 = frozenset([4, 51, 55])
    FOLLOW_init_declarator_in_init_declarator_list294 = frozenset([1, 26])
    FOLLOW_declarator_in_init_declarator307 = frozenset([1, 27])
    FOLLOW_27_in_init_declarator310 = frozenset([4, 5, 6, 7, 8, 9, 10, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_initializer_in_init_declarator312 = frozenset([1])
    FOLLOW_set_in_storage_class_specifier0 = frozenset([1])
    FOLLOW_32_in_type_specifier361 = frozenset([1])
    FOLLOW_33_in_type_specifier366 = frozenset([1])
    FOLLOW_34_in_type_specifier371 = frozenset([1])
    FOLLOW_35_in_type_specifier376 = frozenset([1])
    FOLLOW_36_in_type_specifier381 = frozenset([1])
    FOLLOW_37_in_type_specifier386 = frozenset([1])
    FOLLOW_38_in_type_specifier391 = frozenset([1])
    FOLLOW_39_in_type_specifier396 = frozenset([1])
    FOLLOW_40_in_type_specifier401 = frozenset([1])
    FOLLOW_struct_or_union_specifier_in_type_specifier406 = frozenset([1])
    FOLLOW_enum_specifier_in_type_specifier411 = frozenset([1])
    FOLLOW_type_id_in_type_specifier423 = frozenset([1])
    FOLLOW_IDENTIFIER_in_type_id439 = frozenset([1])
    FOLLOW_struct_or_union_in_struct_or_union_specifier478 = frozenset([4, 41])
    FOLLOW_IDENTIFIER_in_struct_or_union_specifier480 = frozenset([41])
    FOLLOW_41_in_struct_or_union_specifier483 = frozenset([4, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_struct_declaration_list_in_struct_or_union_specifier485 = frozenset([42])
    FOLLOW_42_in_struct_or_union_specifier487 = frozenset([1])
    FOLLOW_struct_or_union_in_struct_or_union_specifier492 = frozenset([4])
    FOLLOW_IDENTIFIER_in_struct_or_union_specifier494 = frozenset([1])
    FOLLOW_set_in_struct_or_union0 = frozenset([1])
    FOLLOW_struct_declaration_in_struct_declaration_list521 = frozenset([1, 4, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_specifier_qualifier_list_in_struct_declaration533 = frozenset([4, 45, 51, 55])
    FOLLOW_struct_declarator_list_in_struct_declaration535 = frozenset([25])
    FOLLOW_25_in_struct_declaration537 = frozenset([1])
    FOLLOW_type_qualifier_in_specifier_qualifier_list550 = frozenset([1, 4, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_type_specifier_in_specifier_qualifier_list554 = frozenset([1, 4, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_struct_declarator_in_struct_declarator_list568 = frozenset([1, 26])
    FOLLOW_26_in_struct_declarator_list571 = frozenset([4, 45, 51, 55])
    FOLLOW_struct_declarator_in_struct_declarator_list573 = frozenset([1, 26])
    FOLLOW_declarator_in_struct_declarator586 = frozenset([1, 45])
    FOLLOW_45_in_struct_declarator589 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_constant_expression_in_struct_declarator591 = frozenset([1])
    FOLLOW_45_in_struct_declarator598 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_constant_expression_in_struct_declarator600 = frozenset([1])
    FOLLOW_46_in_enum_specifier618 = frozenset([41])
    FOLLOW_41_in_enum_specifier620 = frozenset([4])
    FOLLOW_enumerator_list_in_enum_specifier622 = frozenset([42])
    FOLLOW_42_in_enum_specifier624 = frozenset([1])
    FOLLOW_46_in_enum_specifier629 = frozenset([4])
    FOLLOW_IDENTIFIER_in_enum_specifier631 = frozenset([41])
    FOLLOW_41_in_enum_specifier633 = frozenset([4])
    FOLLOW_enumerator_list_in_enum_specifier635 = frozenset([42])
    FOLLOW_42_in_enum_specifier637 = frozenset([1])
    FOLLOW_46_in_enum_specifier642 = frozenset([4])
    FOLLOW_IDENTIFIER_in_enum_specifier644 = frozenset([1])
    FOLLOW_enumerator_in_enumerator_list655 = frozenset([1, 26])
    FOLLOW_26_in_enumerator_list658 = frozenset([4])
    FOLLOW_enumerator_in_enumerator_list660 = frozenset([1, 26])
    FOLLOW_IDENTIFIER_in_enumerator673 = frozenset([1, 27])
    FOLLOW_27_in_enumerator676 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_constant_expression_in_enumerator678 = frozenset([1])
    FOLLOW_set_in_type_qualifier0 = frozenset([1])
    FOLLOW_pointer_in_declarator717 = frozenset([4, 51])
    FOLLOW_direct_declarator_in_declarator720 = frozenset([1])
    FOLLOW_pointer_in_declarator725 = frozenset([1])
    FOLLOW_IDENTIFIER_in_direct_declarator741 = frozenset([1, 51, 53])
    FOLLOW_declarator_suffix_in_direct_declarator743 = frozenset([1, 51, 53])
    FOLLOW_51_in_direct_declarator753 = frozenset([4, 51, 55])
    FOLLOW_declarator_in_direct_declarator755 = frozenset([52])
    FOLLOW_52_in_direct_declarator757 = frozenset([51, 53])
    FOLLOW_declarator_suffix_in_direct_declarator759 = frozenset([1, 51, 53])
    FOLLOW_53_in_declarator_suffix773 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_constant_expression_in_declarator_suffix775 = frozenset([54])
    FOLLOW_54_in_declarator_suffix777 = frozenset([1])
    FOLLOW_53_in_declarator_suffix787 = frozenset([54])
    FOLLOW_54_in_declarator_suffix789 = frozenset([1])
    FOLLOW_51_in_declarator_suffix799 = frozenset([4, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_parameter_type_list_in_declarator_suffix801 = frozenset([52])
    FOLLOW_52_in_declarator_suffix803 = frozenset([1])
    FOLLOW_51_in_declarator_suffix813 = frozenset([4])
    FOLLOW_identifier_list_in_declarator_suffix815 = frozenset([52])
    FOLLOW_52_in_declarator_suffix817 = frozenset([1])
    FOLLOW_51_in_declarator_suffix827 = frozenset([52])
    FOLLOW_52_in_declarator_suffix829 = frozenset([1])
    FOLLOW_55_in_pointer840 = frozenset([47, 48, 49, 50])
    FOLLOW_type_qualifier_in_pointer842 = frozenset([1, 47, 48, 49, 50, 55])
    FOLLOW_pointer_in_pointer845 = frozenset([1])
    FOLLOW_55_in_pointer851 = frozenset([55])
    FOLLOW_pointer_in_pointer853 = frozenset([1])
    FOLLOW_55_in_pointer860 = frozenset([1])
    FOLLOW_parameter_list_in_parameter_type_list871 = frozenset([1, 26])
    FOLLOW_26_in_parameter_type_list874 = frozenset([56])
    FOLLOW_56_in_parameter_type_list876 = frozenset([1])
    FOLLOW_parameter_declaration_in_parameter_list889 = frozenset([1, 26])
    FOLLOW_26_in_parameter_list892 = frozenset([4, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_parameter_declaration_in_parameter_list894 = frozenset([1, 26])
    FOLLOW_declaration_specifiers_in_parameter_declaration907 = frozenset([4, 51, 53, 55])
    FOLLOW_declarator_in_parameter_declaration910 = frozenset([1, 4, 51, 53, 55])
    FOLLOW_abstract_declarator_in_parameter_declaration912 = frozenset([1, 4, 51, 53, 55])
    FOLLOW_IDENTIFIER_in_identifier_list927 = frozenset([1, 26])
    FOLLOW_26_in_identifier_list932 = frozenset([4])
    FOLLOW_IDENTIFIER_in_identifier_list936 = frozenset([1, 26])
    FOLLOW_specifier_qualifier_list_in_type_name951 = frozenset([1, 51, 53, 55])
    FOLLOW_abstract_declarator_in_type_name953 = frozenset([1])
    FOLLOW_type_id_in_type_name959 = frozenset([1])
    FOLLOW_pointer_in_abstract_declarator970 = frozenset([1, 51, 53])
    FOLLOW_direct_abstract_declarator_in_abstract_declarator972 = frozenset([1])
    FOLLOW_direct_abstract_declarator_in_abstract_declarator978 = frozenset([1])
    FOLLOW_51_in_direct_abstract_declarator991 = frozenset([51, 53, 55])
    FOLLOW_abstract_declarator_in_direct_abstract_declarator993 = frozenset([52])
    FOLLOW_52_in_direct_abstract_declarator995 = frozenset([1, 51, 53])
    FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator999 = frozenset([1, 51, 53])
    FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator1003 = frozenset([1, 51, 53])
    FOLLOW_53_in_abstract_declarator_suffix1015 = frozenset([54])
    FOLLOW_54_in_abstract_declarator_suffix1017 = frozenset([1])
    FOLLOW_53_in_abstract_declarator_suffix1022 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_constant_expression_in_abstract_declarator_suffix1024 = frozenset([54])
    FOLLOW_54_in_abstract_declarator_suffix1026 = frozenset([1])
    FOLLOW_51_in_abstract_declarator_suffix1031 = frozenset([52])
    FOLLOW_52_in_abstract_declarator_suffix1033 = frozenset([1])
    FOLLOW_51_in_abstract_declarator_suffix1038 = frozenset([4, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_parameter_type_list_in_abstract_declarator_suffix1040 = frozenset([52])
    FOLLOW_52_in_abstract_declarator_suffix1042 = frozenset([1])
    FOLLOW_assignment_expression_in_initializer1055 = frozenset([1])
    FOLLOW_41_in_initializer1060 = frozenset([4, 5, 6, 7, 8, 9, 10, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_initializer_list_in_initializer1062 = frozenset([26, 42])
    FOLLOW_26_in_initializer1064 = frozenset([42])
    FOLLOW_42_in_initializer1067 = frozenset([1])
    FOLLOW_initializer_in_initializer_list1078 = frozenset([1, 26])
    FOLLOW_26_in_initializer_list1081 = frozenset([4, 5, 6, 7, 8, 9, 10, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_initializer_in_initializer_list1083 = frozenset([1, 26])
    FOLLOW_assignment_expression_in_argument_expression_list1101 = frozenset([1, 26])
    FOLLOW_26_in_argument_expression_list1104 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_assignment_expression_in_argument_expression_list1106 = frozenset([1, 26])
    FOLLOW_multiplicative_expression_in_additive_expression1120 = frozenset([1, 57, 58])
    FOLLOW_57_in_additive_expression1124 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_multiplicative_expression_in_additive_expression1126 = frozenset([1, 57, 58])
    FOLLOW_58_in_additive_expression1130 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_multiplicative_expression_in_additive_expression1132 = frozenset([1, 57, 58])
    FOLLOW_cast_expression_in_multiplicative_expression1146 = frozenset([1, 55, 59, 60])
    FOLLOW_55_in_multiplicative_expression1150 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_cast_expression_in_multiplicative_expression1152 = frozenset([1, 55, 59, 60])
    FOLLOW_59_in_multiplicative_expression1156 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_cast_expression_in_multiplicative_expression1158 = frozenset([1, 55, 59, 60])
    FOLLOW_60_in_multiplicative_expression1162 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_cast_expression_in_multiplicative_expression1164 = frozenset([1, 55, 59, 60])
    FOLLOW_51_in_cast_expression1177 = frozenset([4, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_type_name_in_cast_expression1179 = frozenset([52])
    FOLLOW_52_in_cast_expression1181 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_cast_expression_in_cast_expression1183 = frozenset([1])
    FOLLOW_unary_expression_in_cast_expression1188 = frozenset([1])
    FOLLOW_postfix_expression_in_unary_expression1199 = frozenset([1])
    FOLLOW_61_in_unary_expression1204 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_unary_expression_in_unary_expression1206 = frozenset([1])
    FOLLOW_62_in_unary_expression1211 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_unary_expression_in_unary_expression1213 = frozenset([1])
    FOLLOW_unary_operator_in_unary_expression1218 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_cast_expression_in_unary_expression1220 = frozenset([1])
    FOLLOW_63_in_unary_expression1225 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_unary_expression_in_unary_expression1227 = frozenset([1])
    FOLLOW_63_in_unary_expression1232 = frozenset([51])
    FOLLOW_51_in_unary_expression1234 = frozenset([4, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_type_name_in_unary_expression1236 = frozenset([52])
    FOLLOW_52_in_unary_expression1238 = frozenset([1])
    FOLLOW_primary_expression_in_postfix_expression1251 = frozenset([1, 51, 53, 55, 61, 62, 64, 65])
    FOLLOW_53_in_postfix_expression1265 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_in_postfix_expression1267 = frozenset([54])
    FOLLOW_54_in_postfix_expression1269 = frozenset([1, 51, 53, 55, 61, 62, 64, 65])
    FOLLOW_51_in_postfix_expression1283 = frozenset([52])
    FOLLOW_52_in_postfix_expression1285 = frozenset([1, 51, 53, 55, 61, 62, 64, 65])
    FOLLOW_51_in_postfix_expression1299 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_argument_expression_list_in_postfix_expression1301 = frozenset([52])
    FOLLOW_52_in_postfix_expression1303 = frozenset([1, 51, 53, 55, 61, 62, 64, 65])
    FOLLOW_64_in_postfix_expression1317 = frozenset([4])
    FOLLOW_IDENTIFIER_in_postfix_expression1319 = frozenset([1, 51, 53, 55, 61, 62, 64, 65])
    FOLLOW_55_in_postfix_expression1333 = frozenset([4])
    FOLLOW_IDENTIFIER_in_postfix_expression1335 = frozenset([1, 51, 53, 55, 61, 62, 64, 65])
    FOLLOW_65_in_postfix_expression1349 = frozenset([4])
    FOLLOW_IDENTIFIER_in_postfix_expression1351 = frozenset([1, 51, 53, 55, 61, 62, 64, 65])
    FOLLOW_61_in_postfix_expression1365 = frozenset([1, 51, 53, 55, 61, 62, 64, 65])
    FOLLOW_62_in_postfix_expression1379 = frozenset([1, 51, 53, 55, 61, 62, 64, 65])
    FOLLOW_set_in_unary_operator0 = frozenset([1])
    FOLLOW_IDENTIFIER_in_primary_expression1437 = frozenset([1])
    FOLLOW_constant_in_primary_expression1442 = frozenset([1])
    FOLLOW_51_in_primary_expression1447 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_in_primary_expression1449 = frozenset([52])
    FOLLOW_52_in_primary_expression1451 = frozenset([1])
    FOLLOW_set_in_constant0 = frozenset([1])
    FOLLOW_assignment_expression_in_expression1529 = frozenset([1, 26])
    FOLLOW_26_in_expression1532 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_assignment_expression_in_expression1534 = frozenset([1, 26])
    FOLLOW_conditional_expression_in_constant_expression1547 = frozenset([1])
    FOLLOW_lvalue_in_assignment_expression1558 = frozenset([27, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78])
    FOLLOW_assignment_operator_in_assignment_expression1560 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_assignment_expression_in_assignment_expression1562 = frozenset([1])
    FOLLOW_conditional_expression_in_assignment_expression1567 = frozenset([1])
    FOLLOW_unary_expression_in_lvalue1579 = frozenset([1])
    FOLLOW_set_in_assignment_operator0 = frozenset([1])
    FOLLOW_logical_or_expression_in_conditional_expression1651 = frozenset([1, 79])
    FOLLOW_79_in_conditional_expression1654 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_in_conditional_expression1656 = frozenset([45])
    FOLLOW_45_in_conditional_expression1658 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_conditional_expression_in_conditional_expression1660 = frozenset([1])
    FOLLOW_logical_and_expression_in_logical_or_expression1673 = frozenset([1, 80])
    FOLLOW_80_in_logical_or_expression1676 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_logical_and_expression_in_logical_or_expression1678 = frozenset([1, 80])
    FOLLOW_inclusive_or_expression_in_logical_and_expression1691 = frozenset([1, 81])
    FOLLOW_81_in_logical_and_expression1694 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_inclusive_or_expression_in_logical_and_expression1696 = frozenset([1, 81])
    FOLLOW_exclusive_or_expression_in_inclusive_or_expression1709 = frozenset([1, 82])
    FOLLOW_82_in_inclusive_or_expression1712 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_exclusive_or_expression_in_inclusive_or_expression1714 = frozenset([1, 82])
    FOLLOW_and_expression_in_exclusive_or_expression1727 = frozenset([1, 83])
    FOLLOW_83_in_exclusive_or_expression1730 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_and_expression_in_exclusive_or_expression1732 = frozenset([1, 83])
    FOLLOW_equality_expression_in_and_expression1745 = frozenset([1, 66])
    FOLLOW_66_in_and_expression1748 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_equality_expression_in_and_expression1750 = frozenset([1, 66])
    FOLLOW_relational_expression_in_equality_expression1762 = frozenset([1, 84, 85])
    FOLLOW_set_in_equality_expression1765 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_relational_expression_in_equality_expression1771 = frozenset([1, 84, 85])
    FOLLOW_shift_expression_in_relational_expression1784 = frozenset([1, 86, 87, 88, 89])
    FOLLOW_set_in_relational_expression1787 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_shift_expression_in_relational_expression1797 = frozenset([1, 86, 87, 88, 89])
    FOLLOW_additive_expression_in_shift_expression1810 = frozenset([1, 90, 91])
    FOLLOW_set_in_shift_expression1813 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_additive_expression_in_shift_expression1819 = frozenset([1, 90, 91])
    FOLLOW_labeled_statement_in_statement1834 = frozenset([1])
    FOLLOW_compound_statement_in_statement1839 = frozenset([1])
    FOLLOW_expression_statement_in_statement1844 = frozenset([1])
    FOLLOW_selection_statement_in_statement1849 = frozenset([1])
    FOLLOW_iteration_statement_in_statement1854 = frozenset([1])
    FOLLOW_jump_statement_in_statement1859 = frozenset([1])
    FOLLOW_macro_statement_in_statement1864 = frozenset([1])
    FOLLOW_IDENTIFIER_in_macro_statement1875 = frozenset([51])
    FOLLOW_51_in_macro_statement1877 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 46, 47, 48, 49, 50, 51, 52, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_IDENTIFIER_in_macro_statement1880 = frozenset([52])
    FOLLOW_declaration_in_macro_statement1884 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 46, 47, 48, 49, 50, 51, 52, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_list_in_macro_statement1888 = frozenset([52])
    FOLLOW_52_in_macro_statement1892 = frozenset([1])
    FOLLOW_IDENTIFIER_in_labeled_statement1904 = frozenset([45])
    FOLLOW_45_in_labeled_statement1906 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_in_labeled_statement1908 = frozenset([1])
    FOLLOW_92_in_labeled_statement1913 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_constant_expression_in_labeled_statement1915 = frozenset([45])
    FOLLOW_45_in_labeled_statement1917 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_in_labeled_statement1919 = frozenset([1])
    FOLLOW_93_in_labeled_statement1924 = frozenset([45])
    FOLLOW_45_in_labeled_statement1926 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_in_labeled_statement1928 = frozenset([1])
    FOLLOW_41_in_compound_statement1950 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_declaration_in_compound_statement1952 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_list_in_compound_statement1955 = frozenset([42])
    FOLLOW_42_in_compound_statement1958 = frozenset([1])
    FOLLOW_statement_in_statement_list1969 = frozenset([1, 4, 5, 6, 7, 8, 9, 10, 25, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_25_in_expression_statement1981 = frozenset([1])
    FOLLOW_expression_in_expression_statement1986 = frozenset([25])
    FOLLOW_25_in_expression_statement1988 = frozenset([1])
    FOLLOW_94_in_selection_statement1999 = frozenset([51])
    FOLLOW_51_in_selection_statement2001 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_in_selection_statement2003 = frozenset([52])
    FOLLOW_52_in_selection_statement2005 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_in_selection_statement2007 = frozenset([1, 95])
    FOLLOW_95_in_selection_statement2022 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_in_selection_statement2024 = frozenset([1])
    FOLLOW_96_in_selection_statement2031 = frozenset([51])
    FOLLOW_51_in_selection_statement2033 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_in_selection_statement2035 = frozenset([52])
    FOLLOW_52_in_selection_statement2037 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_in_selection_statement2039 = frozenset([1])
    FOLLOW_97_in_iteration_statement2050 = frozenset([51])
    FOLLOW_51_in_iteration_statement2052 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_in_iteration_statement2054 = frozenset([52])
    FOLLOW_52_in_iteration_statement2056 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_in_iteration_statement2058 = frozenset([1])
    FOLLOW_98_in_iteration_statement2063 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_in_iteration_statement2065 = frozenset([97])
    FOLLOW_97_in_iteration_statement2067 = frozenset([51])
    FOLLOW_51_in_iteration_statement2069 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_in_iteration_statement2071 = frozenset([52])
    FOLLOW_52_in_iteration_statement2073 = frozenset([25])
    FOLLOW_25_in_iteration_statement2075 = frozenset([1])
    FOLLOW_99_in_iteration_statement2080 = frozenset([51])
    FOLLOW_51_in_iteration_statement2082 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_statement_in_iteration_statement2084 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_statement_in_iteration_statement2086 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 52, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_in_iteration_statement2088 = frozenset([52])
    FOLLOW_52_in_iteration_statement2091 = frozenset([4, 5, 6, 7, 8, 9, 10, 25, 41, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103])
    FOLLOW_statement_in_iteration_statement2093 = frozenset([1])
    FOLLOW_100_in_jump_statement2104 = frozenset([4])
    FOLLOW_IDENTIFIER_in_jump_statement2106 = frozenset([25])
    FOLLOW_25_in_jump_statement2108 = frozenset([1])
    FOLLOW_101_in_jump_statement2113 = frozenset([25])
    FOLLOW_25_in_jump_statement2115 = frozenset([1])
    FOLLOW_102_in_jump_statement2120 = frozenset([25])
    FOLLOW_25_in_jump_statement2122 = frozenset([1])
    FOLLOW_103_in_jump_statement2127 = frozenset([25])
    FOLLOW_25_in_jump_statement2129 = frozenset([1])
    FOLLOW_103_in_jump_statement2134 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_expression_in_jump_statement2136 = frozenset([25])
    FOLLOW_25_in_jump_statement2138 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred2102 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred4102 = frozenset([4, 51, 55])
    FOLLOW_declarator_in_synpred4105 = frozenset([4, 24, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_declaration_in_synpred4107 = frozenset([4, 24, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_41_in_synpred4110 = frozenset([1])
    FOLLOW_declaration_in_synpred5120 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred6153 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred9206 = frozenset([1])
    FOLLOW_type_specifier_in_synpred13253 = frozenset([1])
    FOLLOW_IDENTIFIER_in_synpred31417 = frozenset([4, 51, 55])
    FOLLOW_declarator_in_synpred31419 = frozenset([1])
    FOLLOW_type_specifier_in_synpred37554 = frozenset([1])
    FOLLOW_pointer_in_synpred49717 = frozenset([4, 51])
    FOLLOW_direct_declarator_in_synpred49720 = frozenset([1])
    FOLLOW_declarator_suffix_in_synpred50743 = frozenset([1])
    FOLLOW_declarator_suffix_in_synpred52759 = frozenset([1])
    FOLLOW_51_in_synpred55799 = frozenset([4, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_parameter_type_list_in_synpred55801 = frozenset([52])
    FOLLOW_52_in_synpred55803 = frozenset([1])
    FOLLOW_51_in_synpred56813 = frozenset([4])
    FOLLOW_identifier_list_in_synpred56815 = frozenset([52])
    FOLLOW_52_in_synpred56817 = frozenset([1])
    FOLLOW_type_qualifier_in_synpred57842 = frozenset([1])
    FOLLOW_pointer_in_synpred58845 = frozenset([1])
    FOLLOW_55_in_synpred59840 = frozenset([47, 48, 49, 50])
    FOLLOW_type_qualifier_in_synpred59842 = frozenset([1, 47, 48, 49, 50, 55])
    FOLLOW_pointer_in_synpred59845 = frozenset([1])
    FOLLOW_55_in_synpred60851 = frozenset([55])
    FOLLOW_pointer_in_synpred60853 = frozenset([1])
    FOLLOW_declarator_in_synpred63910 = frozenset([1])
    FOLLOW_abstract_declarator_in_synpred64912 = frozenset([1])
    FOLLOW_specifier_qualifier_list_in_synpred67951 = frozenset([1, 51, 53, 55])
    FOLLOW_abstract_declarator_in_synpred67953 = frozenset([1])
    FOLLOW_direct_abstract_declarator_in_synpred68972 = frozenset([1])
    FOLLOW_abstract_declarator_suffix_in_synpred711003 = frozenset([1])
    FOLLOW_51_in_synpred841177 = frozenset([4, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50])
    FOLLOW_type_name_in_synpred841179 = frozenset([52])
    FOLLOW_52_in_synpred841181 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_cast_expression_in_synpred841183 = frozenset([1])
    FOLLOW_63_in_synpred891225 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_unary_expression_in_synpred891227 = frozenset([1])
    FOLLOW_55_in_synpred941333 = frozenset([4])
    FOLLOW_IDENTIFIER_in_synpred941335 = frozenset([1])
    FOLLOW_lvalue_in_synpred1111558 = frozenset([27, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78])
    FOLLOW_assignment_operator_in_synpred1111560 = frozenset([4, 5, 6, 7, 8, 9, 10, 51, 55, 57, 58, 61, 62, 63, 66, 67, 68])
    FOLLOW_assignment_expression_in_synpred1111562 = frozenset([1])
    FOLLOW_expression_statement_in_synpred1381844 = frozenset([1])
    FOLLOW_declaration_in_synpred1431884 = frozenset([1])
    FOLLOW_declaration_in_synpred1471952 = frozenset([1])


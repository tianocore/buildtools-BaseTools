# $ANTLR 3.0.1 C.g 2007-11-26 17:02:18

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
HexDigit=13
WS=19
LINE_COMMAND=22
COMMENT=20
LINE_COMMENT=21
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
    "UnicodeEscape", "WS", "COMMENT", "LINE_COMMENT", "LINE_COMMAND", "'typedef'", 
    "';'", "','", "'='", "'extern'", "'static'", "'auto'", "'register'", 
    "'void'", "'char'", "'short'", "'int'", "'long'", "'float'", "'double'", 
    "'signed'", "'unsigned'", "'{'", "'}'", "'struct'", "'union'", "':'", 
    "'enum'", "'const'", "'volatile'", "'IN'", "'OUT'", "'('", "')'", "'['", 
    "']'", "'*'", "'...'", "'+'", "'-'", "'/'", "'%'", "'++'", "'--'", "'sizeof'", 
    "'.'", "'->'", "'&'", "'~'", "'!'", "'*='", "'/='", "'%='", "'+='", 
    "'-='", "'<<='", "'>>='", "'&='", "'^='", "'|='", "'?'", "'||'", "'&&'", 
    "'|'", "'^'", "'=='", "'!='", "'<'", "'>'", "'<='", "'>='", "'<<'", 
    "'>>'", "'case'", "'default'", "'if'", "'else'", "'switch'", "'while'", 
    "'do'", "'for'", "'goto'", "'continue'", "'break'", "'return'"
]

class Symbols_scope(object):
    def __init__(self):
        self.types = None


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
    



    # $ANTLR start translation_unit
    # C.g:55:1: translation_unit : ( external_declaration )+ ;
    def translation_unit(self, ):
        self.Symbols_stack.append(Symbols_scope())

        translation_unit_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 1):
                    return 

                # C.g:60:2: ( ( external_declaration )+ )
                # C.g:60:4: ( external_declaration )+
                # C.g:60:4: ( external_declaration )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == IDENTIFIER or LA1_0 == 23 or (27 <= LA1_0 <= 39) or (42 <= LA1_0 <= 43) or (45 <= LA1_0 <= 50) or LA1_0 == 54) :
                        alt1 = 1


                    if alt1 == 1:
                        # C.g:0:0: external_declaration
                        self.following.append(self.FOLLOW_external_declaration_in_translation_unit77)
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
    # C.g:63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );
    def external_declaration(self, ):

        external_declaration_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 2):
                    return 

                # C.g:89:2: ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement )
                alt2 = 3
                LA2_0 = self.input.LA(1)

                if ((27 <= LA2_0 <= 30)) :
                    LA2_1 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 1, self.input)

                        raise nvae

                elif (LA2_0 == 31) :
                    LA2_2 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 2, self.input)

                        raise nvae

                elif (LA2_0 == 32) :
                    LA2_3 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 3, self.input)

                        raise nvae

                elif (LA2_0 == 33) :
                    LA2_4 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 4, self.input)

                        raise nvae

                elif (LA2_0 == 34) :
                    LA2_5 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 5, self.input)

                        raise nvae

                elif (LA2_0 == 35) :
                    LA2_6 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 6, self.input)

                        raise nvae

                elif (LA2_0 == 36) :
                    LA2_7 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 7, self.input)

                        raise nvae

                elif (LA2_0 == 37) :
                    LA2_8 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 8, self.input)

                        raise nvae

                elif (LA2_0 == 38) :
                    LA2_9 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 9, self.input)

                        raise nvae

                elif (LA2_0 == 39) :
                    LA2_10 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 10, self.input)

                        raise nvae

                elif ((42 <= LA2_0 <= 43)) :
                    LA2_11 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 11, self.input)

                        raise nvae

                elif (LA2_0 == 45) :
                    LA2_12 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 12, self.input)

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

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 13, self.input)

                        raise nvae

                elif ((46 <= LA2_0 <= 49)) :
                    LA2_14 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (self.synpred5()) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 14, self.input)

                        raise nvae

                elif (LA2_0 == 54) and (self.synpred4()):
                    alt2 = 1
                elif (LA2_0 == 50) and (self.synpred4()):
                    alt2 = 1
                elif (LA2_0 == 23) :
                    alt2 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration | macro_statement );", 2, 0, self.input)

                    raise nvae

                if alt2 == 1:
                    # C.g:89:4: ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition
                    self.following.append(self.FOLLOW_function_definition_in_external_declaration117)
                    self.function_definition()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt2 == 2:
                    # C.g:90:4: declaration
                    self.following.append(self.FOLLOW_declaration_in_external_declaration122)
                    self.declaration()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt2 == 3:
                    # C.g:91:4: macro_statement
                    self.following.append(self.FOLLOW_macro_statement_in_external_declaration127)
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


    # $ANTLR start function_definition
    # C.g:97:1: function_definition : ( declaration_specifiers )? declarator ( ( declaration )+ compound_statement | compound_statement ) ;
    def function_definition(self, ):
        self.Symbols_stack.append(Symbols_scope())

        function_definition_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 3):
                    return 

                # C.g:102:2: ( ( declaration_specifiers )? declarator ( ( declaration )+ compound_statement | compound_statement ) )
                # C.g:102:4: ( declaration_specifiers )? declarator ( ( declaration )+ compound_statement | compound_statement )
                # C.g:102:4: ( declaration_specifiers )?
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if ((27 <= LA3_0 <= 39) or (42 <= LA3_0 <= 43) or (45 <= LA3_0 <= 49)) :
                    alt3 = 1
                elif (LA3_0 == IDENTIFIER) :
                    LA3 = self.input.LA(2)
                    if LA3 == 54:
                        alt3 = 1
                    elif LA3 == IDENTIFIER:
                        LA3_18 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 50:
                        LA3_19 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 27 or LA3 == 28 or LA3 == 29 or LA3 == 30:
                        LA3_20 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 31:
                        LA3_21 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 32:
                        LA3_22 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 33:
                        LA3_23 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 34:
                        LA3_24 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 35:
                        LA3_25 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 36:
                        LA3_26 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 37:
                        LA3_27 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 38:
                        LA3_28 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 39:
                        LA3_29 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 42 or LA3 == 43:
                        LA3_30 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 45:
                        LA3_31 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                    elif LA3 == 46 or LA3 == 47 or LA3 == 48 or LA3 == 49:
                        LA3_32 = self.input.LA(3)

                        if (self.synpred6()) :
                            alt3 = 1
                if alt3 == 1:
                    # C.g:0:0: declaration_specifiers
                    self.following.append(self.FOLLOW_declaration_specifiers_in_function_definition153)
                    self.declaration_specifiers()
                    self.following.pop()
                    if self.failed:
                        return 



                self.following.append(self.FOLLOW_declarator_in_function_definition156)
                self.declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:103:3: ( ( declaration )+ compound_statement | compound_statement )
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == IDENTIFIER or LA5_0 == 23 or (27 <= LA5_0 <= 39) or (42 <= LA5_0 <= 43) or (45 <= LA5_0 <= 49)) :
                    alt5 = 1
                elif (LA5_0 == 40) :
                    alt5 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("103:3: ( ( declaration )+ compound_statement | compound_statement )", 5, 0, self.input)

                    raise nvae

                if alt5 == 1:
                    # C.g:103:5: ( declaration )+ compound_statement
                    # C.g:103:5: ( declaration )+
                    cnt4 = 0
                    while True: #loop4
                        alt4 = 2
                        LA4_0 = self.input.LA(1)

                        if (LA4_0 == IDENTIFIER or LA4_0 == 23 or (27 <= LA4_0 <= 39) or (42 <= LA4_0 <= 43) or (45 <= LA4_0 <= 49)) :
                            alt4 = 1


                        if alt4 == 1:
                            # C.g:0:0: declaration
                            self.following.append(self.FOLLOW_declaration_in_function_definition162)
                            self.declaration()
                            self.following.pop()
                            if self.failed:
                                return 


                        else:
                            if cnt4 >= 1:
                                break #loop4

                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            eee = EarlyExitException(4, self.input)
                            raise eee

                        cnt4 += 1


                    self.following.append(self.FOLLOW_compound_statement_in_function_definition165)
                    self.compound_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt5 == 2:
                    # C.g:104:5: compound_statement
                    self.following.append(self.FOLLOW_compound_statement_in_function_definition172)
                    self.compound_statement()
                    self.following.pop()
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 3, function_definition_StartIndex)

            self.Symbols_stack.pop()

            pass

        return 

    # $ANTLR end function_definition


    # $ANTLR start declaration
    # C.g:108:1: declaration : ( 'typedef' ( declaration_specifiers )? init_declarator_list ';' | declaration_specifiers ( init_declarator_list )? ';' );
    def declaration(self, ):
        self.declaration_stack.append(declaration_scope())
        declaration_StartIndex = self.input.index()
               
        self.declaration_stack[-1].isTypedef =  False

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 4):
                    return 

                # C.g:115:2: ( 'typedef' ( declaration_specifiers )? init_declarator_list ';' | declaration_specifiers ( init_declarator_list )? ';' )
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if (LA8_0 == 23) :
                    alt8 = 1
                elif (LA8_0 == IDENTIFIER or (27 <= LA8_0 <= 39) or (42 <= LA8_0 <= 43) or (45 <= LA8_0 <= 49)) :
                    alt8 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("108:1: declaration : ( 'typedef' ( declaration_specifiers )? init_declarator_list ';' | declaration_specifiers ( init_declarator_list )? ';' );", 8, 0, self.input)

                    raise nvae

                if alt8 == 1:
                    # C.g:115:4: 'typedef' ( declaration_specifiers )? init_declarator_list ';'
                    self.match(self.input, 23, self.FOLLOW_23_in_declaration200)
                    if self.failed:
                        return 
                    # C.g:115:14: ( declaration_specifiers )?
                    alt6 = 2
                    LA6_0 = self.input.LA(1)

                    if ((27 <= LA6_0 <= 39) or (42 <= LA6_0 <= 43) or (45 <= LA6_0 <= 49)) :
                        alt6 = 1
                    elif (LA6_0 == IDENTIFIER) :
                        LA6_13 = self.input.LA(2)

                        if (LA6_13 == IDENTIFIER or (27 <= LA6_13 <= 39) or (42 <= LA6_13 <= 43) or (45 <= LA6_13 <= 49) or LA6_13 == 54) :
                            alt6 = 1
                        elif (LA6_13 == 50) :
                            LA6_19 = self.input.LA(3)

                            if (self.synpred9()) :
                                alt6 = 1
                    if alt6 == 1:
                        # C.g:0:0: declaration_specifiers
                        self.following.append(self.FOLLOW_declaration_specifiers_in_declaration202)
                        self.declaration_specifiers()
                        self.following.pop()
                        if self.failed:
                            return 



                    if self.backtracking == 0:
                        self.declaration_stack[-1].isTypedef=True

                    self.following.append(self.FOLLOW_init_declarator_list_in_declaration210)
                    self.init_declarator_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_declaration212)
                    if self.failed:
                        return 


                elif alt8 == 2:
                    # C.g:117:4: declaration_specifiers ( init_declarator_list )? ';'
                    self.following.append(self.FOLLOW_declaration_specifiers_in_declaration218)
                    self.declaration_specifiers()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:117:27: ( init_declarator_list )?
                    alt7 = 2
                    LA7_0 = self.input.LA(1)

                    if (LA7_0 == IDENTIFIER or LA7_0 == 50 or LA7_0 == 54) :
                        alt7 = 1
                    if alt7 == 1:
                        # C.g:0:0: init_declarator_list
                        self.following.append(self.FOLLOW_init_declarator_list_in_declaration220)
                        self.init_declarator_list()
                        self.following.pop()
                        if self.failed:
                            return 



                    self.match(self.input, 24, self.FOLLOW_24_in_declaration223)
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
    # C.g:121:1: declaration_specifiers : ( storage_class_specifier | type_specifier | type_qualifier )+ ;
    def declaration_specifiers(self, ):

        declaration_specifiers_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 5):
                    return 

                # C.g:122:2: ( ( storage_class_specifier | type_specifier | type_qualifier )+ )
                # C.g:122:6: ( storage_class_specifier | type_specifier | type_qualifier )+
                # C.g:122:6: ( storage_class_specifier | type_specifier | type_qualifier )+
                cnt9 = 0
                while True: #loop9
                    alt9 = 4
                    LA9 = self.input.LA(1)
                    if LA9 == IDENTIFIER:
                        LA9_2 = self.input.LA(2)

                        if (self.synpred13()) :
                            alt9 = 2


                    elif LA9 == 27 or LA9 == 28 or LA9 == 29 or LA9 == 30:
                        alt9 = 1
                    elif LA9 == 31 or LA9 == 32 or LA9 == 33 or LA9 == 34 or LA9 == 35 or LA9 == 36 or LA9 == 37 or LA9 == 38 or LA9 == 39 or LA9 == 42 or LA9 == 43 or LA9 == 45:
                        alt9 = 2
                    elif LA9 == 46 or LA9 == 47 or LA9 == 48 or LA9 == 49:
                        alt9 = 3

                    if alt9 == 1:
                        # C.g:122:10: storage_class_specifier
                        self.following.append(self.FOLLOW_storage_class_specifier_in_declaration_specifiers242)
                        self.storage_class_specifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt9 == 2:
                        # C.g:123:7: type_specifier
                        self.following.append(self.FOLLOW_type_specifier_in_declaration_specifiers250)
                        self.type_specifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt9 == 3:
                        # C.g:124:13: type_qualifier
                        self.following.append(self.FOLLOW_type_qualifier_in_declaration_specifiers264)
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
    # C.g:128:1: init_declarator_list : init_declarator ( ',' init_declarator )* ;
    def init_declarator_list(self, ):

        init_declarator_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 6):
                    return 

                # C.g:129:2: ( init_declarator ( ',' init_declarator )* )
                # C.g:129:4: init_declarator ( ',' init_declarator )*
                self.following.append(self.FOLLOW_init_declarator_in_init_declarator_list286)
                self.init_declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:129:20: ( ',' init_declarator )*
                while True: #loop10
                    alt10 = 2
                    LA10_0 = self.input.LA(1)

                    if (LA10_0 == 25) :
                        alt10 = 1


                    if alt10 == 1:
                        # C.g:129:21: ',' init_declarator
                        self.match(self.input, 25, self.FOLLOW_25_in_init_declarator_list289)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_init_declarator_in_init_declarator_list291)
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
    # C.g:132:1: init_declarator : declarator ( '=' initializer )? ;
    def init_declarator(self, ):

        init_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 7):
                    return 

                # C.g:133:2: ( declarator ( '=' initializer )? )
                # C.g:133:4: declarator ( '=' initializer )?
                self.following.append(self.FOLLOW_declarator_in_init_declarator304)
                self.declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:133:15: ( '=' initializer )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 26) :
                    alt11 = 1
                if alt11 == 1:
                    # C.g:133:16: '=' initializer
                    self.match(self.input, 26, self.FOLLOW_26_in_init_declarator307)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_initializer_in_init_declarator309)
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
    # C.g:136:1: storage_class_specifier : ( 'extern' | 'static' | 'auto' | 'register' );
    def storage_class_specifier(self, ):

        storage_class_specifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 8):
                    return 

                # C.g:137:2: ( 'extern' | 'static' | 'auto' | 'register' )
                # C.g:
                if (27 <= self.input.LA(1) <= 30):
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
    # C.g:143:1: type_specifier options {k=3; } : ( 'void' | 'char' | 'short' | 'int' | 'long' | 'float' | 'double' | 'signed' | 'unsigned' | struct_or_union_specifier | enum_specifier | ( IDENTIFIER declarator )=> type_id );
    def type_specifier(self, ):

        type_specifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 9):
                    return 

                # C.g:145:2: ( 'void' | 'char' | 'short' | 'int' | 'long' | 'float' | 'double' | 'signed' | 'unsigned' | struct_or_union_specifier | enum_specifier | ( IDENTIFIER declarator )=> type_id )
                alt12 = 12
                LA12_0 = self.input.LA(1)

                if (LA12_0 == 31) :
                    alt12 = 1
                elif (LA12_0 == 32) :
                    alt12 = 2
                elif (LA12_0 == 33) :
                    alt12 = 3
                elif (LA12_0 == 34) :
                    alt12 = 4
                elif (LA12_0 == 35) :
                    alt12 = 5
                elif (LA12_0 == 36) :
                    alt12 = 6
                elif (LA12_0 == 37) :
                    alt12 = 7
                elif (LA12_0 == 38) :
                    alt12 = 8
                elif (LA12_0 == 39) :
                    alt12 = 9
                elif ((42 <= LA12_0 <= 43)) :
                    alt12 = 10
                elif (LA12_0 == 45) :
                    alt12 = 11
                elif (LA12_0 == IDENTIFIER) and (self.synpred31()):
                    alt12 = 12
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("143:1: type_specifier options {k=3; } : ( 'void' | 'char' | 'short' | 'int' | 'long' | 'float' | 'double' | 'signed' | 'unsigned' | struct_or_union_specifier | enum_specifier | ( IDENTIFIER declarator )=> type_id );", 12, 0, self.input)

                    raise nvae

                if alt12 == 1:
                    # C.g:145:4: 'void'
                    self.match(self.input, 31, self.FOLLOW_31_in_type_specifier355)
                    if self.failed:
                        return 


                elif alt12 == 2:
                    # C.g:146:4: 'char'
                    self.match(self.input, 32, self.FOLLOW_32_in_type_specifier360)
                    if self.failed:
                        return 


                elif alt12 == 3:
                    # C.g:147:4: 'short'
                    self.match(self.input, 33, self.FOLLOW_33_in_type_specifier365)
                    if self.failed:
                        return 


                elif alt12 == 4:
                    # C.g:148:4: 'int'
                    self.match(self.input, 34, self.FOLLOW_34_in_type_specifier370)
                    if self.failed:
                        return 


                elif alt12 == 5:
                    # C.g:149:4: 'long'
                    self.match(self.input, 35, self.FOLLOW_35_in_type_specifier375)
                    if self.failed:
                        return 


                elif alt12 == 6:
                    # C.g:150:4: 'float'
                    self.match(self.input, 36, self.FOLLOW_36_in_type_specifier380)
                    if self.failed:
                        return 


                elif alt12 == 7:
                    # C.g:151:4: 'double'
                    self.match(self.input, 37, self.FOLLOW_37_in_type_specifier385)
                    if self.failed:
                        return 


                elif alt12 == 8:
                    # C.g:152:4: 'signed'
                    self.match(self.input, 38, self.FOLLOW_38_in_type_specifier390)
                    if self.failed:
                        return 


                elif alt12 == 9:
                    # C.g:153:4: 'unsigned'
                    self.match(self.input, 39, self.FOLLOW_39_in_type_specifier395)
                    if self.failed:
                        return 


                elif alt12 == 10:
                    # C.g:154:4: struct_or_union_specifier
                    self.following.append(self.FOLLOW_struct_or_union_specifier_in_type_specifier400)
                    self.struct_or_union_specifier()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt12 == 11:
                    # C.g:155:4: enum_specifier
                    self.following.append(self.FOLLOW_enum_specifier_in_type_specifier405)
                    self.enum_specifier()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt12 == 12:
                    # C.g:156:4: ( IDENTIFIER declarator )=> type_id
                    self.following.append(self.FOLLOW_type_id_in_type_specifier417)
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
    # C.g:159:1: type_id : IDENTIFIER ;
    def type_id(self, ):

        type_id_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 10):
                    return 

                # C.g:160:5: ( IDENTIFIER )
                # C.g:160:9: IDENTIFIER
                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_type_id433)
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
    # C.g:164:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );
    def struct_or_union_specifier(self, ):
        self.Symbols_stack.append(Symbols_scope())

        struct_or_union_specifier_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 11):
                    return 

                # C.g:170:2: ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER )
                alt14 = 2
                LA14_0 = self.input.LA(1)

                if ((42 <= LA14_0 <= 43)) :
                    LA14_1 = self.input.LA(2)

                    if (LA14_1 == IDENTIFIER) :
                        LA14_2 = self.input.LA(3)

                        if (LA14_2 == 40) :
                            alt14 = 1
                        elif (LA14_2 == EOF or LA14_2 == IDENTIFIER or LA14_2 == 24 or (27 <= LA14_2 <= 39) or (42 <= LA14_2 <= 52) or LA14_2 == 54) :
                            alt14 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("164:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );", 14, 2, self.input)

                            raise nvae

                    elif (LA14_1 == 40) :
                        alt14 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("164:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );", 14, 1, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("164:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );", 14, 0, self.input)

                    raise nvae

                if alt14 == 1:
                    # C.g:170:4: struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}'
                    self.following.append(self.FOLLOW_struct_or_union_in_struct_or_union_specifier472)
                    self.struct_or_union()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:170:20: ( IDENTIFIER )?
                    alt13 = 2
                    LA13_0 = self.input.LA(1)

                    if (LA13_0 == IDENTIFIER) :
                        alt13 = 1
                    if alt13 == 1:
                        # C.g:0:0: IDENTIFIER
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_struct_or_union_specifier474)
                        if self.failed:
                            return 



                    self.match(self.input, 40, self.FOLLOW_40_in_struct_or_union_specifier477)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_struct_declaration_list_in_struct_or_union_specifier479)
                    self.struct_declaration_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 41, self.FOLLOW_41_in_struct_or_union_specifier481)
                    if self.failed:
                        return 


                elif alt14 == 2:
                    # C.g:171:4: struct_or_union IDENTIFIER
                    self.following.append(self.FOLLOW_struct_or_union_in_struct_or_union_specifier486)
                    self.struct_or_union()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_struct_or_union_specifier488)
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
    # C.g:174:1: struct_or_union : ( 'struct' | 'union' );
    def struct_or_union(self, ):

        struct_or_union_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 12):
                    return 

                # C.g:175:2: ( 'struct' | 'union' )
                # C.g:
                if (42 <= self.input.LA(1) <= 43):
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
    # C.g:179:1: struct_declaration_list : ( struct_declaration )+ ;
    def struct_declaration_list(self, ):

        struct_declaration_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 13):
                    return 

                # C.g:180:2: ( ( struct_declaration )+ )
                # C.g:180:4: ( struct_declaration )+
                # C.g:180:4: ( struct_declaration )+
                cnt15 = 0
                while True: #loop15
                    alt15 = 2
                    LA15_0 = self.input.LA(1)

                    if (LA15_0 == IDENTIFIER or (31 <= LA15_0 <= 39) or (42 <= LA15_0 <= 43) or (45 <= LA15_0 <= 49)) :
                        alt15 = 1


                    if alt15 == 1:
                        # C.g:0:0: struct_declaration
                        self.following.append(self.FOLLOW_struct_declaration_in_struct_declaration_list515)
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
    # C.g:183:1: struct_declaration : specifier_qualifier_list struct_declarator_list ';' ;
    def struct_declaration(self, ):

        struct_declaration_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 14):
                    return 

                # C.g:184:2: ( specifier_qualifier_list struct_declarator_list ';' )
                # C.g:184:4: specifier_qualifier_list struct_declarator_list ';'
                self.following.append(self.FOLLOW_specifier_qualifier_list_in_struct_declaration527)
                self.specifier_qualifier_list()
                self.following.pop()
                if self.failed:
                    return 
                self.following.append(self.FOLLOW_struct_declarator_list_in_struct_declaration529)
                self.struct_declarator_list()
                self.following.pop()
                if self.failed:
                    return 
                self.match(self.input, 24, self.FOLLOW_24_in_struct_declaration531)
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
    # C.g:187:1: specifier_qualifier_list : ( type_qualifier | type_specifier )+ ;
    def specifier_qualifier_list(self, ):

        specifier_qualifier_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 15):
                    return 

                # C.g:188:2: ( ( type_qualifier | type_specifier )+ )
                # C.g:188:4: ( type_qualifier | type_specifier )+
                # C.g:188:4: ( type_qualifier | type_specifier )+
                cnt16 = 0
                while True: #loop16
                    alt16 = 3
                    LA16 = self.input.LA(1)
                    if LA16 == IDENTIFIER:
                        LA16 = self.input.LA(2)
                        if LA16 == EOF or LA16 == IDENTIFIER or LA16 == 31 or LA16 == 32 or LA16 == 33 or LA16 == 34 or LA16 == 35 or LA16 == 36 or LA16 == 37 or LA16 == 38 or LA16 == 39 or LA16 == 42 or LA16 == 43 or LA16 == 45 or LA16 == 46 or LA16 == 47 or LA16 == 48 or LA16 == 49 or LA16 == 51 or LA16 == 54:
                            alt16 = 2
                        elif LA16 == 50:
                            LA16_22 = self.input.LA(3)

                            if (self.synpred37()) :
                                alt16 = 2


                        elif LA16 == 44:
                            LA16_23 = self.input.LA(3)

                            if (self.synpred37()) :
                                alt16 = 2


                        elif LA16 == 52:
                            LA16_24 = self.input.LA(3)

                            if (self.synpred37()) :
                                alt16 = 2



                    elif LA16 == 46 or LA16 == 47 or LA16 == 48 or LA16 == 49:
                        alt16 = 1
                    elif LA16 == 31 or LA16 == 32 or LA16 == 33 or LA16 == 34 or LA16 == 35 or LA16 == 36 or LA16 == 37 or LA16 == 38 or LA16 == 39 or LA16 == 42 or LA16 == 43 or LA16 == 45:
                        alt16 = 2

                    if alt16 == 1:
                        # C.g:188:6: type_qualifier
                        self.following.append(self.FOLLOW_type_qualifier_in_specifier_qualifier_list544)
                        self.type_qualifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt16 == 2:
                        # C.g:188:23: type_specifier
                        self.following.append(self.FOLLOW_type_specifier_in_specifier_qualifier_list548)
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
    # C.g:191:1: struct_declarator_list : struct_declarator ( ',' struct_declarator )* ;
    def struct_declarator_list(self, ):

        struct_declarator_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 16):
                    return 

                # C.g:192:2: ( struct_declarator ( ',' struct_declarator )* )
                # C.g:192:4: struct_declarator ( ',' struct_declarator )*
                self.following.append(self.FOLLOW_struct_declarator_in_struct_declarator_list562)
                self.struct_declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:192:22: ( ',' struct_declarator )*
                while True: #loop17
                    alt17 = 2
                    LA17_0 = self.input.LA(1)

                    if (LA17_0 == 25) :
                        alt17 = 1


                    if alt17 == 1:
                        # C.g:192:23: ',' struct_declarator
                        self.match(self.input, 25, self.FOLLOW_25_in_struct_declarator_list565)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_struct_declarator_in_struct_declarator_list567)
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
    # C.g:195:1: struct_declarator : ( declarator ( ':' constant_expression )? | ':' constant_expression );
    def struct_declarator(self, ):

        struct_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 17):
                    return 

                # C.g:196:2: ( declarator ( ':' constant_expression )? | ':' constant_expression )
                alt19 = 2
                LA19_0 = self.input.LA(1)

                if (LA19_0 == IDENTIFIER or LA19_0 == 50 or LA19_0 == 54) :
                    alt19 = 1
                elif (LA19_0 == 44) :
                    alt19 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("195:1: struct_declarator : ( declarator ( ':' constant_expression )? | ':' constant_expression );", 19, 0, self.input)

                    raise nvae

                if alt19 == 1:
                    # C.g:196:4: declarator ( ':' constant_expression )?
                    self.following.append(self.FOLLOW_declarator_in_struct_declarator580)
                    self.declarator()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:196:15: ( ':' constant_expression )?
                    alt18 = 2
                    LA18_0 = self.input.LA(1)

                    if (LA18_0 == 44) :
                        alt18 = 1
                    if alt18 == 1:
                        # C.g:196:16: ':' constant_expression
                        self.match(self.input, 44, self.FOLLOW_44_in_struct_declarator583)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_constant_expression_in_struct_declarator585)
                        self.constant_expression()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt19 == 2:
                    # C.g:197:4: ':' constant_expression
                    self.match(self.input, 44, self.FOLLOW_44_in_struct_declarator592)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_struct_declarator594)
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
    # C.g:200:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );
    def enum_specifier(self, ):

        enum_specifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 18):
                    return 

                # C.g:202:2: ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER )
                alt20 = 3
                LA20_0 = self.input.LA(1)

                if (LA20_0 == 45) :
                    LA20_1 = self.input.LA(2)

                    if (LA20_1 == 40) :
                        alt20 = 1
                    elif (LA20_1 == IDENTIFIER) :
                        LA20_3 = self.input.LA(3)

                        if (LA20_3 == 40) :
                            alt20 = 2
                        elif (LA20_3 == EOF or LA20_3 == IDENTIFIER or LA20_3 == 24 or (27 <= LA20_3 <= 39) or (42 <= LA20_3 <= 52) or LA20_3 == 54) :
                            alt20 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("200:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );", 20, 3, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("200:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );", 20, 1, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("200:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );", 20, 0, self.input)

                    raise nvae

                if alt20 == 1:
                    # C.g:202:4: 'enum' '{' enumerator_list '}'
                    self.match(self.input, 45, self.FOLLOW_45_in_enum_specifier612)
                    if self.failed:
                        return 
                    self.match(self.input, 40, self.FOLLOW_40_in_enum_specifier614)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_enumerator_list_in_enum_specifier616)
                    self.enumerator_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 41, self.FOLLOW_41_in_enum_specifier618)
                    if self.failed:
                        return 


                elif alt20 == 2:
                    # C.g:203:4: 'enum' IDENTIFIER '{' enumerator_list '}'
                    self.match(self.input, 45, self.FOLLOW_45_in_enum_specifier623)
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_enum_specifier625)
                    if self.failed:
                        return 
                    self.match(self.input, 40, self.FOLLOW_40_in_enum_specifier627)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_enumerator_list_in_enum_specifier629)
                    self.enumerator_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 41, self.FOLLOW_41_in_enum_specifier631)
                    if self.failed:
                        return 


                elif alt20 == 3:
                    # C.g:204:4: 'enum' IDENTIFIER
                    self.match(self.input, 45, self.FOLLOW_45_in_enum_specifier636)
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_enum_specifier638)
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
    # C.g:207:1: enumerator_list : enumerator ( ',' enumerator )* ;
    def enumerator_list(self, ):

        enumerator_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 19):
                    return 

                # C.g:208:2: ( enumerator ( ',' enumerator )* )
                # C.g:208:4: enumerator ( ',' enumerator )*
                self.following.append(self.FOLLOW_enumerator_in_enumerator_list649)
                self.enumerator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:208:15: ( ',' enumerator )*
                while True: #loop21
                    alt21 = 2
                    LA21_0 = self.input.LA(1)

                    if (LA21_0 == 25) :
                        alt21 = 1


                    if alt21 == 1:
                        # C.g:208:16: ',' enumerator
                        self.match(self.input, 25, self.FOLLOW_25_in_enumerator_list652)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_enumerator_in_enumerator_list654)
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
    # C.g:211:1: enumerator : IDENTIFIER ( '=' constant_expression )? ;
    def enumerator(self, ):

        enumerator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 20):
                    return 

                # C.g:212:2: ( IDENTIFIER ( '=' constant_expression )? )
                # C.g:212:4: IDENTIFIER ( '=' constant_expression )?
                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_enumerator667)
                if self.failed:
                    return 
                # C.g:212:15: ( '=' constant_expression )?
                alt22 = 2
                LA22_0 = self.input.LA(1)

                if (LA22_0 == 26) :
                    alt22 = 1
                if alt22 == 1:
                    # C.g:212:16: '=' constant_expression
                    self.match(self.input, 26, self.FOLLOW_26_in_enumerator670)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_enumerator672)
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
    # C.g:215:1: type_qualifier : ( 'const' | 'volatile' | 'IN' | 'OUT' );
    def type_qualifier(self, ):

        type_qualifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 21):
                    return 

                # C.g:216:2: ( 'const' | 'volatile' | 'IN' | 'OUT' )
                # C.g:
                if (46 <= self.input.LA(1) <= 49):
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


    # $ANTLR start declarator
    # C.g:222:1: declarator : ( ( pointer )? direct_declarator | pointer );
    def declarator(self, ):

        declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 22):
                    return 

                # C.g:223:2: ( ( pointer )? direct_declarator | pointer )
                alt24 = 2
                LA24_0 = self.input.LA(1)

                if (LA24_0 == 54) :
                    LA24_1 = self.input.LA(2)

                    if (self.synpred49()) :
                        alt24 = 1
                    elif (True) :
                        alt24 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("222:1: declarator : ( ( pointer )? direct_declarator | pointer );", 24, 1, self.input)

                        raise nvae

                elif (LA24_0 == IDENTIFIER or LA24_0 == 50) :
                    alt24 = 1
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("222:1: declarator : ( ( pointer )? direct_declarator | pointer );", 24, 0, self.input)

                    raise nvae

                if alt24 == 1:
                    # C.g:223:4: ( pointer )? direct_declarator
                    # C.g:223:4: ( pointer )?
                    alt23 = 2
                    LA23_0 = self.input.LA(1)

                    if (LA23_0 == 54) :
                        alt23 = 1
                    if alt23 == 1:
                        # C.g:0:0: pointer
                        self.following.append(self.FOLLOW_pointer_in_declarator711)
                        self.pointer()
                        self.following.pop()
                        if self.failed:
                            return 



                    self.following.append(self.FOLLOW_direct_declarator_in_declarator714)
                    self.direct_declarator()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt24 == 2:
                    # C.g:224:4: pointer
                    self.following.append(self.FOLLOW_pointer_in_declarator719)
                    self.pointer()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 22, declarator_StartIndex)

            pass

        return 

    # $ANTLR end declarator


    # $ANTLR start direct_declarator
    # C.g:227:1: direct_declarator : ( IDENTIFIER ( declarator_suffix )* | '(' declarator ')' ( declarator_suffix )+ );
    def direct_declarator(self, ):

        direct_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 23):
                    return 

                # C.g:228:2: ( IDENTIFIER ( declarator_suffix )* | '(' declarator ')' ( declarator_suffix )+ )
                alt27 = 2
                LA27_0 = self.input.LA(1)

                if (LA27_0 == IDENTIFIER) :
                    alt27 = 1
                elif (LA27_0 == 50) :
                    alt27 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("227:1: direct_declarator : ( IDENTIFIER ( declarator_suffix )* | '(' declarator ')' ( declarator_suffix )+ );", 27, 0, self.input)

                    raise nvae

                if alt27 == 1:
                    # C.g:228:6: IDENTIFIER ( declarator_suffix )*
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_direct_declarator732)
                    if self.failed:
                        return 
                    # C.g:228:17: ( declarator_suffix )*
                    while True: #loop25
                        alt25 = 2
                        LA25_0 = self.input.LA(1)

                        if (LA25_0 == 50) :
                            LA25 = self.input.LA(2)
                            if LA25 == 51:
                                LA25_26 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 27 or LA25 == 28 or LA25 == 29 or LA25 == 30:
                                LA25_27 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 31:
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


                            elif LA25 == 42 or LA25 == 43:
                                LA25_37 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 45:
                                LA25_38 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == IDENTIFIER:
                                LA25_39 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 46 or LA25 == 47 or LA25 == 48 or LA25 == 49:
                                LA25_40 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1



                        elif (LA25_0 == 52) :
                            LA25 = self.input.LA(2)
                            if LA25 == 53:
                                LA25_44 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 50:
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


                            elif LA25 == 60:
                                LA25_48 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 61:
                                LA25_49 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 54 or LA25 == 56 or LA25 == 57 or LA25 == 65 or LA25 == 66 or LA25 == 67:
                                LA25_50 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1


                            elif LA25 == 62:
                                LA25_51 = self.input.LA(3)

                                if (self.synpred50()) :
                                    alt25 = 1





                        if alt25 == 1:
                            # C.g:0:0: declarator_suffix
                            self.following.append(self.FOLLOW_declarator_suffix_in_direct_declarator734)
                            self.declarator_suffix()
                            self.following.pop()
                            if self.failed:
                                return 


                        else:
                            break #loop25




                elif alt27 == 2:
                    # C.g:230:5: '(' declarator ')' ( declarator_suffix )+
                    self.match(self.input, 50, self.FOLLOW_50_in_direct_declarator745)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_declarator_in_direct_declarator747)
                    self.declarator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_direct_declarator749)
                    if self.failed:
                        return 
                    # C.g:230:24: ( declarator_suffix )+
                    cnt26 = 0
                    while True: #loop26
                        alt26 = 2
                        LA26_0 = self.input.LA(1)

                        if (LA26_0 == 50) :
                            LA26 = self.input.LA(2)
                            if LA26 == 51:
                                LA26_26 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 27 or LA26 == 28 or LA26 == 29 or LA26 == 30:
                                LA26_27 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 31:
                                LA26_28 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 32:
                                LA26_29 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 33:
                                LA26_30 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 34:
                                LA26_31 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 35:
                                LA26_32 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 36:
                                LA26_33 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 37:
                                LA26_34 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 38:
                                LA26_35 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 39:
                                LA26_36 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 42 or LA26 == 43:
                                LA26_37 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 45:
                                LA26_38 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == IDENTIFIER:
                                LA26_39 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 46 or LA26 == 47 or LA26 == 48 or LA26 == 49:
                                LA26_40 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1



                        elif (LA26_0 == 52) :
                            LA26 = self.input.LA(2)
                            if LA26 == 53:
                                LA26_44 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 50:
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


                            elif LA26 == 60:
                                LA26_48 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 61:
                                LA26_49 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 54 or LA26 == 56 or LA26 == 57 or LA26 == 65 or LA26 == 66 or LA26 == 67:
                                LA26_50 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1


                            elif LA26 == 62:
                                LA26_51 = self.input.LA(3)

                                if (self.synpred52()) :
                                    alt26 = 1





                        if alt26 == 1:
                            # C.g:0:0: declarator_suffix
                            self.following.append(self.FOLLOW_declarator_suffix_in_direct_declarator751)
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

            pass

        return 

    # $ANTLR end direct_declarator


    # $ANTLR start declarator_suffix
    # C.g:233:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );
    def declarator_suffix(self, ):

        declarator_suffix_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 24):
                    return 

                # C.g:234:2: ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' )
                alt28 = 5
                LA28_0 = self.input.LA(1)

                if (LA28_0 == 52) :
                    LA28_1 = self.input.LA(2)

                    if (LA28_1 == 53) :
                        alt28 = 2
                    elif ((IDENTIFIER <= LA28_1 <= FLOATING_POINT_LITERAL) or LA28_1 == 50 or LA28_1 == 54 or (56 <= LA28_1 <= 57) or (60 <= LA28_1 <= 62) or (65 <= LA28_1 <= 67)) :
                        alt28 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("233:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 28, 1, self.input)

                        raise nvae

                elif (LA28_0 == 50) :
                    LA28 = self.input.LA(2)
                    if LA28 == 51:
                        alt28 = 5
                    elif LA28 == 27 or LA28 == 28 or LA28 == 29 or LA28 == 30 or LA28 == 31 or LA28 == 32 or LA28 == 33 or LA28 == 34 or LA28 == 35 or LA28 == 36 or LA28 == 37 or LA28 == 38 or LA28 == 39 or LA28 == 42 or LA28 == 43 or LA28 == 45 or LA28 == 46 or LA28 == 47 or LA28 == 48 or LA28 == 49:
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

                            nvae = NoViableAltException("233:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 28, 24, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("233:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 28, 2, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("233:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 28, 0, self.input)

                    raise nvae

                if alt28 == 1:
                    # C.g:234:6: '[' constant_expression ']'
                    self.match(self.input, 52, self.FOLLOW_52_in_declarator_suffix765)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_declarator_suffix767)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 53, self.FOLLOW_53_in_declarator_suffix769)
                    if self.failed:
                        return 


                elif alt28 == 2:
                    # C.g:235:9: '[' ']'
                    self.match(self.input, 52, self.FOLLOW_52_in_declarator_suffix779)
                    if self.failed:
                        return 
                    self.match(self.input, 53, self.FOLLOW_53_in_declarator_suffix781)
                    if self.failed:
                        return 


                elif alt28 == 3:
                    # C.g:236:9: '(' parameter_type_list ')'
                    self.match(self.input, 50, self.FOLLOW_50_in_declarator_suffix791)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_parameter_type_list_in_declarator_suffix793)
                    self.parameter_type_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_declarator_suffix795)
                    if self.failed:
                        return 


                elif alt28 == 4:
                    # C.g:237:9: '(' identifier_list ')'
                    self.match(self.input, 50, self.FOLLOW_50_in_declarator_suffix805)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_identifier_list_in_declarator_suffix807)
                    self.identifier_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_declarator_suffix809)
                    if self.failed:
                        return 


                elif alt28 == 5:
                    # C.g:238:9: '(' ')'
                    self.match(self.input, 50, self.FOLLOW_50_in_declarator_suffix819)
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_declarator_suffix821)
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
    # C.g:241:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' );
    def pointer(self, ):

        pointer_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 25):
                    return 

                # C.g:242:2: ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' )
                alt31 = 3
                LA31_0 = self.input.LA(1)

                if (LA31_0 == 54) :
                    LA31 = self.input.LA(2)
                    if LA31 == EOF or LA31 == IDENTIFIER or LA31 == 23 or LA31 == 24 or LA31 == 25 or LA31 == 26 or LA31 == 27 or LA31 == 28 or LA31 == 29 or LA31 == 30 or LA31 == 31 or LA31 == 32 or LA31 == 33 or LA31 == 34 or LA31 == 35 or LA31 == 36 or LA31 == 37 or LA31 == 38 or LA31 == 39 or LA31 == 40 or LA31 == 42 or LA31 == 43 or LA31 == 44 or LA31 == 45 or LA31 == 50 or LA31 == 51 or LA31 == 52:
                        alt31 = 3
                    elif LA31 == 46 or LA31 == 47 or LA31 == 48 or LA31 == 49:
                        LA31_17 = self.input.LA(3)

                        if (self.synpred59()) :
                            alt31 = 1
                        elif (True) :
                            alt31 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("241:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' );", 31, 17, self.input)

                            raise nvae

                    elif LA31 == 54:
                        LA31_25 = self.input.LA(3)

                        if (self.synpred60()) :
                            alt31 = 2
                        elif (True) :
                            alt31 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("241:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' );", 31, 25, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("241:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' );", 31, 1, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("241:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' );", 31, 0, self.input)

                    raise nvae

                if alt31 == 1:
                    # C.g:242:4: '*' ( type_qualifier )+ ( pointer )?
                    self.match(self.input, 54, self.FOLLOW_54_in_pointer832)
                    if self.failed:
                        return 
                    # C.g:242:8: ( type_qualifier )+
                    cnt29 = 0
                    while True: #loop29
                        alt29 = 2
                        LA29_0 = self.input.LA(1)

                        if ((46 <= LA29_0 <= 49)) :
                            LA29_17 = self.input.LA(2)

                            if (self.synpred57()) :
                                alt29 = 1




                        if alt29 == 1:
                            # C.g:0:0: type_qualifier
                            self.following.append(self.FOLLOW_type_qualifier_in_pointer834)
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


                    # C.g:242:24: ( pointer )?
                    alt30 = 2
                    LA30_0 = self.input.LA(1)

                    if (LA30_0 == 54) :
                        LA30_1 = self.input.LA(2)

                        if (self.synpred58()) :
                            alt30 = 1
                    if alt30 == 1:
                        # C.g:0:0: pointer
                        self.following.append(self.FOLLOW_pointer_in_pointer837)
                        self.pointer()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt31 == 2:
                    # C.g:243:4: '*' pointer
                    self.match(self.input, 54, self.FOLLOW_54_in_pointer843)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_pointer_in_pointer845)
                    self.pointer()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt31 == 3:
                    # C.g:244:4: '*'
                    self.match(self.input, 54, self.FOLLOW_54_in_pointer850)
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
    # C.g:247:1: parameter_type_list : parameter_list ( ',' '...' )? ;
    def parameter_type_list(self, ):

        parameter_type_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 26):
                    return 

                # C.g:248:2: ( parameter_list ( ',' '...' )? )
                # C.g:248:4: parameter_list ( ',' '...' )?
                self.following.append(self.FOLLOW_parameter_list_in_parameter_type_list861)
                self.parameter_list()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:248:19: ( ',' '...' )?
                alt32 = 2
                LA32_0 = self.input.LA(1)

                if (LA32_0 == 25) :
                    alt32 = 1
                if alt32 == 1:
                    # C.g:248:20: ',' '...'
                    self.match(self.input, 25, self.FOLLOW_25_in_parameter_type_list864)
                    if self.failed:
                        return 
                    self.match(self.input, 55, self.FOLLOW_55_in_parameter_type_list866)
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
    # C.g:251:1: parameter_list : parameter_declaration ( ',' parameter_declaration )* ;
    def parameter_list(self, ):

        parameter_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 27):
                    return 

                # C.g:252:2: ( parameter_declaration ( ',' parameter_declaration )* )
                # C.g:252:4: parameter_declaration ( ',' parameter_declaration )*
                self.following.append(self.FOLLOW_parameter_declaration_in_parameter_list879)
                self.parameter_declaration()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:252:26: ( ',' parameter_declaration )*
                while True: #loop33
                    alt33 = 2
                    LA33_0 = self.input.LA(1)

                    if (LA33_0 == 25) :
                        LA33_1 = self.input.LA(2)

                        if (LA33_1 == IDENTIFIER or (27 <= LA33_1 <= 39) or (42 <= LA33_1 <= 43) or (45 <= LA33_1 <= 49)) :
                            alt33 = 1




                    if alt33 == 1:
                        # C.g:252:27: ',' parameter_declaration
                        self.match(self.input, 25, self.FOLLOW_25_in_parameter_list882)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_parameter_declaration_in_parameter_list884)
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
    # C.g:255:1: parameter_declaration : declaration_specifiers ( declarator | abstract_declarator )+ ;
    def parameter_declaration(self, ):

        parameter_declaration_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 28):
                    return 

                # C.g:256:2: ( declaration_specifiers ( declarator | abstract_declarator )+ )
                # C.g:256:4: declaration_specifiers ( declarator | abstract_declarator )+
                self.following.append(self.FOLLOW_declaration_specifiers_in_parameter_declaration897)
                self.declaration_specifiers()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:256:27: ( declarator | abstract_declarator )+
                cnt34 = 0
                while True: #loop34
                    alt34 = 3
                    LA34 = self.input.LA(1)
                    if LA34 == 54:
                        LA34_4 = self.input.LA(2)

                        if (self.synpred63()) :
                            alt34 = 1
                        elif (self.synpred64()) :
                            alt34 = 2


                    elif LA34 == IDENTIFIER:
                        alt34 = 1
                    elif LA34 == 50:
                        LA34 = self.input.LA(2)
                        if LA34 == 27 or LA34 == 28 or LA34 == 29 or LA34 == 30 or LA34 == 31 or LA34 == 32 or LA34 == 33 or LA34 == 34 or LA34 == 35 or LA34 == 36 or LA34 == 37 or LA34 == 38 or LA34 == 39 or LA34 == 42 or LA34 == 43 or LA34 == 45 or LA34 == 46 or LA34 == 47 or LA34 == 48 or LA34 == 49 or LA34 == 51 or LA34 == 52:
                            alt34 = 2
                        elif LA34 == 54:
                            LA34_17 = self.input.LA(3)

                            if (self.synpred63()) :
                                alt34 = 1
                            elif (self.synpred64()) :
                                alt34 = 2


                        elif LA34 == IDENTIFIER:
                            LA34_18 = self.input.LA(3)

                            if (self.synpred63()) :
                                alt34 = 1
                            elif (self.synpred64()) :
                                alt34 = 2


                        elif LA34 == 50:
                            LA34_19 = self.input.LA(3)

                            if (self.synpred63()) :
                                alt34 = 1
                            elif (self.synpred64()) :
                                alt34 = 2



                    elif LA34 == 52:
                        alt34 = 2

                    if alt34 == 1:
                        # C.g:256:28: declarator
                        self.following.append(self.FOLLOW_declarator_in_parameter_declaration900)
                        self.declarator()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt34 == 2:
                        # C.g:256:39: abstract_declarator
                        self.following.append(self.FOLLOW_abstract_declarator_in_parameter_declaration902)
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
    # C.g:259:1: identifier_list : i= IDENTIFIER ( ',' d= IDENTIFIER )* ;
    def identifier_list(self, ):

        identifier_list_StartIndex = self.input.index()
        i = None
        d = None

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 29):
                    return 

                # C.g:260:2: (i= IDENTIFIER ( ',' d= IDENTIFIER )* )
                # C.g:260:4: i= IDENTIFIER ( ',' d= IDENTIFIER )*
                i = self.input.LT(1)
                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_identifier_list917)
                if self.failed:
                    return 
                # C.g:261:2: ( ',' d= IDENTIFIER )*
                while True: #loop35
                    alt35 = 2
                    LA35_0 = self.input.LA(1)

                    if (LA35_0 == 25) :
                        alt35 = 1


                    if alt35 == 1:
                        # C.g:261:3: ',' d= IDENTIFIER
                        self.match(self.input, 25, self.FOLLOW_25_in_identifier_list922)
                        if self.failed:
                            return 
                        d = self.input.LT(1)
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_identifier_list926)
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
    # C.g:264:1: type_name : ( specifier_qualifier_list ( abstract_declarator )? | type_id );
    def type_name(self, ):

        type_name_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 30):
                    return 

                # C.g:265:2: ( specifier_qualifier_list ( abstract_declarator )? | type_id )
                alt37 = 2
                LA37_0 = self.input.LA(1)

                if ((31 <= LA37_0 <= 39) or (42 <= LA37_0 <= 43) or (45 <= LA37_0 <= 49)) :
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

                        nvae = NoViableAltException("264:1: type_name : ( specifier_qualifier_list ( abstract_declarator )? | type_id );", 37, 13, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("264:1: type_name : ( specifier_qualifier_list ( abstract_declarator )? | type_id );", 37, 0, self.input)

                    raise nvae

                if alt37 == 1:
                    # C.g:265:4: specifier_qualifier_list ( abstract_declarator )?
                    self.following.append(self.FOLLOW_specifier_qualifier_list_in_type_name941)
                    self.specifier_qualifier_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:265:29: ( abstract_declarator )?
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 50 or LA36_0 == 52 or LA36_0 == 54) :
                        alt36 = 1
                    if alt36 == 1:
                        # C.g:0:0: abstract_declarator
                        self.following.append(self.FOLLOW_abstract_declarator_in_type_name943)
                        self.abstract_declarator()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt37 == 2:
                    # C.g:266:4: type_id
                    self.following.append(self.FOLLOW_type_id_in_type_name949)
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
    # C.g:269:1: abstract_declarator : ( pointer ( direct_abstract_declarator )? | direct_abstract_declarator );
    def abstract_declarator(self, ):

        abstract_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 31):
                    return 

                # C.g:270:2: ( pointer ( direct_abstract_declarator )? | direct_abstract_declarator )
                alt39 = 2
                LA39_0 = self.input.LA(1)

                if (LA39_0 == 54) :
                    alt39 = 1
                elif (LA39_0 == 50 or LA39_0 == 52) :
                    alt39 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("269:1: abstract_declarator : ( pointer ( direct_abstract_declarator )? | direct_abstract_declarator );", 39, 0, self.input)

                    raise nvae

                if alt39 == 1:
                    # C.g:270:4: pointer ( direct_abstract_declarator )?
                    self.following.append(self.FOLLOW_pointer_in_abstract_declarator960)
                    self.pointer()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:270:12: ( direct_abstract_declarator )?
                    alt38 = 2
                    LA38_0 = self.input.LA(1)

                    if (LA38_0 == 50) :
                        LA38 = self.input.LA(2)
                        if LA38 == 51:
                            LA38_8 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 27 or LA38 == 28 or LA38 == 29 or LA38 == 30:
                            LA38_9 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 31:
                            LA38_10 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 32:
                            LA38_11 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 33:
                            LA38_12 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 34:
                            LA38_13 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 35:
                            LA38_14 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 36:
                            LA38_15 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 37:
                            LA38_16 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 38:
                            LA38_17 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 39:
                            LA38_18 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 42 or LA38 == 43:
                            LA38_19 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 45:
                            LA38_20 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == IDENTIFIER:
                            LA38_21 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 46 or LA38 == 47 or LA38 == 48 or LA38 == 49:
                            LA38_22 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 54:
                            LA38_23 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 50:
                            LA38_24 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 52:
                            LA38_25 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                    elif (LA38_0 == 52) :
                        LA38 = self.input.LA(2)
                        if LA38 == 53:
                            LA38_26 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 50:
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
                        elif LA38 == 60:
                            LA38_30 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 61:
                            LA38_31 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 54 or LA38 == 56 or LA38 == 57 or LA38 == 65 or LA38 == 66 or LA38 == 67:
                            LA38_32 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                        elif LA38 == 62:
                            LA38_33 = self.input.LA(3)

                            if (self.synpred68()) :
                                alt38 = 1
                    if alt38 == 1:
                        # C.g:0:0: direct_abstract_declarator
                        self.following.append(self.FOLLOW_direct_abstract_declarator_in_abstract_declarator962)
                        self.direct_abstract_declarator()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt39 == 2:
                    # C.g:271:4: direct_abstract_declarator
                    self.following.append(self.FOLLOW_direct_abstract_declarator_in_abstract_declarator968)
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
    # C.g:274:1: direct_abstract_declarator : ( '(' abstract_declarator ')' | abstract_declarator_suffix ) ( abstract_declarator_suffix )* ;
    def direct_abstract_declarator(self, ):

        direct_abstract_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 32):
                    return 

                # C.g:275:2: ( ( '(' abstract_declarator ')' | abstract_declarator_suffix ) ( abstract_declarator_suffix )* )
                # C.g:275:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix ) ( abstract_declarator_suffix )*
                # C.g:275:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix )
                alt40 = 2
                LA40_0 = self.input.LA(1)

                if (LA40_0 == 50) :
                    LA40_1 = self.input.LA(2)

                    if (LA40_1 == IDENTIFIER or (27 <= LA40_1 <= 39) or (42 <= LA40_1 <= 43) or (45 <= LA40_1 <= 49) or LA40_1 == 51) :
                        alt40 = 2
                    elif (LA40_1 == 50 or LA40_1 == 52 or LA40_1 == 54) :
                        alt40 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("275:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix )", 40, 1, self.input)

                        raise nvae

                elif (LA40_0 == 52) :
                    alt40 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("275:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix )", 40, 0, self.input)

                    raise nvae

                if alt40 == 1:
                    # C.g:275:6: '(' abstract_declarator ')'
                    self.match(self.input, 50, self.FOLLOW_50_in_direct_abstract_declarator981)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_abstract_declarator_in_direct_abstract_declarator983)
                    self.abstract_declarator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_direct_abstract_declarator985)
                    if self.failed:
                        return 


                elif alt40 == 2:
                    # C.g:275:36: abstract_declarator_suffix
                    self.following.append(self.FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator989)
                    self.abstract_declarator_suffix()
                    self.following.pop()
                    if self.failed:
                        return 



                # C.g:275:65: ( abstract_declarator_suffix )*
                while True: #loop41
                    alt41 = 2
                    LA41_0 = self.input.LA(1)

                    if (LA41_0 == 50) :
                        LA41 = self.input.LA(2)
                        if LA41 == 51:
                            LA41_8 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 27 or LA41 == 28 or LA41 == 29 or LA41 == 30:
                            LA41_9 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 31:
                            LA41_10 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 32:
                            LA41_11 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 33:
                            LA41_12 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 34:
                            LA41_13 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 35:
                            LA41_14 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 36:
                            LA41_15 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 37:
                            LA41_16 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 38:
                            LA41_17 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 39:
                            LA41_18 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 42 or LA41 == 43:
                            LA41_19 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 45:
                            LA41_20 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == IDENTIFIER:
                            LA41_21 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 46 or LA41 == 47 or LA41 == 48 or LA41 == 49:
                            LA41_22 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1



                    elif (LA41_0 == 52) :
                        LA41 = self.input.LA(2)
                        if LA41 == 53:
                            LA41_26 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 50:
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


                        elif LA41 == 60:
                            LA41_30 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 61:
                            LA41_31 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 54 or LA41 == 56 or LA41 == 57 or LA41 == 65 or LA41 == 66 or LA41 == 67:
                            LA41_32 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1


                        elif LA41 == 62:
                            LA41_33 = self.input.LA(3)

                            if (self.synpred71()) :
                                alt41 = 1





                    if alt41 == 1:
                        # C.g:0:0: abstract_declarator_suffix
                        self.following.append(self.FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator993)
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
    # C.g:278:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );
    def abstract_declarator_suffix(self, ):

        abstract_declarator_suffix_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 33):
                    return 

                # C.g:279:2: ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' )
                alt42 = 4
                LA42_0 = self.input.LA(1)

                if (LA42_0 == 52) :
                    LA42_1 = self.input.LA(2)

                    if (LA42_1 == 53) :
                        alt42 = 1
                    elif ((IDENTIFIER <= LA42_1 <= FLOATING_POINT_LITERAL) or LA42_1 == 50 or LA42_1 == 54 or (56 <= LA42_1 <= 57) or (60 <= LA42_1 <= 62) or (65 <= LA42_1 <= 67)) :
                        alt42 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("278:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );", 42, 1, self.input)

                        raise nvae

                elif (LA42_0 == 50) :
                    LA42_2 = self.input.LA(2)

                    if (LA42_2 == 51) :
                        alt42 = 3
                    elif (LA42_2 == IDENTIFIER or (27 <= LA42_2 <= 39) or (42 <= LA42_2 <= 43) or (45 <= LA42_2 <= 49)) :
                        alt42 = 4
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("278:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );", 42, 2, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("278:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );", 42, 0, self.input)

                    raise nvae

                if alt42 == 1:
                    # C.g:279:4: '[' ']'
                    self.match(self.input, 52, self.FOLLOW_52_in_abstract_declarator_suffix1005)
                    if self.failed:
                        return 
                    self.match(self.input, 53, self.FOLLOW_53_in_abstract_declarator_suffix1007)
                    if self.failed:
                        return 


                elif alt42 == 2:
                    # C.g:280:4: '[' constant_expression ']'
                    self.match(self.input, 52, self.FOLLOW_52_in_abstract_declarator_suffix1012)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_abstract_declarator_suffix1014)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 53, self.FOLLOW_53_in_abstract_declarator_suffix1016)
                    if self.failed:
                        return 


                elif alt42 == 3:
                    # C.g:281:4: '(' ')'
                    self.match(self.input, 50, self.FOLLOW_50_in_abstract_declarator_suffix1021)
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_abstract_declarator_suffix1023)
                    if self.failed:
                        return 


                elif alt42 == 4:
                    # C.g:282:4: '(' parameter_type_list ')'
                    self.match(self.input, 50, self.FOLLOW_50_in_abstract_declarator_suffix1028)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_parameter_type_list_in_abstract_declarator_suffix1030)
                    self.parameter_type_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_abstract_declarator_suffix1032)
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
    # C.g:285:1: initializer : ( assignment_expression | '{' initializer_list ( ',' )? '}' );
    def initializer(self, ):

        initializer_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 34):
                    return 

                # C.g:287:2: ( assignment_expression | '{' initializer_list ( ',' )? '}' )
                alt44 = 2
                LA44_0 = self.input.LA(1)

                if ((IDENTIFIER <= LA44_0 <= FLOATING_POINT_LITERAL) or LA44_0 == 50 or LA44_0 == 54 or (56 <= LA44_0 <= 57) or (60 <= LA44_0 <= 62) or (65 <= LA44_0 <= 67)) :
                    alt44 = 1
                elif (LA44_0 == 40) :
                    alt44 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("285:1: initializer : ( assignment_expression | '{' initializer_list ( ',' )? '}' );", 44, 0, self.input)

                    raise nvae

                if alt44 == 1:
                    # C.g:287:4: assignment_expression
                    self.following.append(self.FOLLOW_assignment_expression_in_initializer1045)
                    self.assignment_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt44 == 2:
                    # C.g:288:4: '{' initializer_list ( ',' )? '}'
                    self.match(self.input, 40, self.FOLLOW_40_in_initializer1050)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_initializer_list_in_initializer1052)
                    self.initializer_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:288:25: ( ',' )?
                    alt43 = 2
                    LA43_0 = self.input.LA(1)

                    if (LA43_0 == 25) :
                        alt43 = 1
                    if alt43 == 1:
                        # C.g:0:0: ','
                        self.match(self.input, 25, self.FOLLOW_25_in_initializer1054)
                        if self.failed:
                            return 



                    self.match(self.input, 41, self.FOLLOW_41_in_initializer1057)
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
    # C.g:291:1: initializer_list : initializer ( ',' initializer )* ;
    def initializer_list(self, ):

        initializer_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 35):
                    return 

                # C.g:292:2: ( initializer ( ',' initializer )* )
                # C.g:292:4: initializer ( ',' initializer )*
                self.following.append(self.FOLLOW_initializer_in_initializer_list1068)
                self.initializer()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:292:16: ( ',' initializer )*
                while True: #loop45
                    alt45 = 2
                    LA45_0 = self.input.LA(1)

                    if (LA45_0 == 25) :
                        LA45_1 = self.input.LA(2)

                        if ((IDENTIFIER <= LA45_1 <= FLOATING_POINT_LITERAL) or LA45_1 == 40 or LA45_1 == 50 or LA45_1 == 54 or (56 <= LA45_1 <= 57) or (60 <= LA45_1 <= 62) or (65 <= LA45_1 <= 67)) :
                            alt45 = 1




                    if alt45 == 1:
                        # C.g:292:17: ',' initializer
                        self.match(self.input, 25, self.FOLLOW_25_in_initializer_list1071)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_initializer_in_initializer_list1073)
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
    # C.g:297:1: argument_expression_list : assignment_expression ( ',' assignment_expression )* ;
    def argument_expression_list(self, ):

        argument_expression_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 36):
                    return 

                # C.g:298:2: ( assignment_expression ( ',' assignment_expression )* )
                # C.g:298:6: assignment_expression ( ',' assignment_expression )*
                self.following.append(self.FOLLOW_assignment_expression_in_argument_expression_list1090)
                self.assignment_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:298:28: ( ',' assignment_expression )*
                while True: #loop46
                    alt46 = 2
                    LA46_0 = self.input.LA(1)

                    if (LA46_0 == 25) :
                        alt46 = 1


                    if alt46 == 1:
                        # C.g:298:29: ',' assignment_expression
                        self.match(self.input, 25, self.FOLLOW_25_in_argument_expression_list1093)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_assignment_expression_in_argument_expression_list1095)
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
    # C.g:301:1: additive_expression : ( multiplicative_expression ) ( '+' multiplicative_expression | '-' multiplicative_expression )* ;
    def additive_expression(self, ):

        additive_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 37):
                    return 

                # C.g:302:2: ( ( multiplicative_expression ) ( '+' multiplicative_expression | '-' multiplicative_expression )* )
                # C.g:302:4: ( multiplicative_expression ) ( '+' multiplicative_expression | '-' multiplicative_expression )*
                # C.g:302:4: ( multiplicative_expression )
                # C.g:302:5: multiplicative_expression
                self.following.append(self.FOLLOW_multiplicative_expression_in_additive_expression1109)
                self.multiplicative_expression()
                self.following.pop()
                if self.failed:
                    return 



                # C.g:302:32: ( '+' multiplicative_expression | '-' multiplicative_expression )*
                while True: #loop47
                    alt47 = 3
                    LA47_0 = self.input.LA(1)

                    if (LA47_0 == 56) :
                        alt47 = 1
                    elif (LA47_0 == 57) :
                        alt47 = 2


                    if alt47 == 1:
                        # C.g:302:33: '+' multiplicative_expression
                        self.match(self.input, 56, self.FOLLOW_56_in_additive_expression1113)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_multiplicative_expression_in_additive_expression1115)
                        self.multiplicative_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt47 == 2:
                        # C.g:302:65: '-' multiplicative_expression
                        self.match(self.input, 57, self.FOLLOW_57_in_additive_expression1119)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_multiplicative_expression_in_additive_expression1121)
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
    # C.g:305:1: multiplicative_expression : ( cast_expression ) ( '*' cast_expression | '/' cast_expression | '%' cast_expression )* ;
    def multiplicative_expression(self, ):

        multiplicative_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 38):
                    return 

                # C.g:306:2: ( ( cast_expression ) ( '*' cast_expression | '/' cast_expression | '%' cast_expression )* )
                # C.g:306:4: ( cast_expression ) ( '*' cast_expression | '/' cast_expression | '%' cast_expression )*
                # C.g:306:4: ( cast_expression )
                # C.g:306:5: cast_expression
                self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1135)
                self.cast_expression()
                self.following.pop()
                if self.failed:
                    return 



                # C.g:306:22: ( '*' cast_expression | '/' cast_expression | '%' cast_expression )*
                while True: #loop48
                    alt48 = 4
                    LA48 = self.input.LA(1)
                    if LA48 == 54:
                        alt48 = 1
                    elif LA48 == 58:
                        alt48 = 2
                    elif LA48 == 59:
                        alt48 = 3

                    if alt48 == 1:
                        # C.g:306:23: '*' cast_expression
                        self.match(self.input, 54, self.FOLLOW_54_in_multiplicative_expression1139)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1141)
                        self.cast_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt48 == 2:
                        # C.g:306:45: '/' cast_expression
                        self.match(self.input, 58, self.FOLLOW_58_in_multiplicative_expression1145)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1147)
                        self.cast_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt48 == 3:
                        # C.g:306:67: '%' cast_expression
                        self.match(self.input, 59, self.FOLLOW_59_in_multiplicative_expression1151)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1153)
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
    # C.g:309:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );
    def cast_expression(self, ):

        cast_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 39):
                    return 

                # C.g:310:2: ( '(' type_name ')' cast_expression | unary_expression )
                alt49 = 2
                LA49_0 = self.input.LA(1)

                if (LA49_0 == 50) :
                    LA49 = self.input.LA(2)
                    if LA49 == 31 or LA49 == 32 or LA49 == 33 or LA49 == 34 or LA49 == 35 or LA49 == 36 or LA49 == 37 or LA49 == 38 or LA49 == 39 or LA49 == 42 or LA49 == 43 or LA49 == 45 or LA49 == 46 or LA49 == 47 or LA49 == 48 or LA49 == 49:
                        alt49 = 1
                    elif LA49 == IDENTIFIER:
                        LA49_20 = self.input.LA(3)

                        if (self.synpred84()) :
                            alt49 = 1
                        elif (True) :
                            alt49 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("309:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );", 49, 20, self.input)

                            raise nvae

                    elif LA49 == HEX_LITERAL or LA49 == OCTAL_LITERAL or LA49 == DECIMAL_LITERAL or LA49 == CHARACTER_LITERAL or LA49 == STRING_LITERAL or LA49 == FLOATING_POINT_LITERAL or LA49 == 50 or LA49 == 54 or LA49 == 56 or LA49 == 57 or LA49 == 60 or LA49 == 61 or LA49 == 62 or LA49 == 65 or LA49 == 66 or LA49 == 67:
                        alt49 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("309:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );", 49, 1, self.input)

                        raise nvae

                elif ((IDENTIFIER <= LA49_0 <= FLOATING_POINT_LITERAL) or LA49_0 == 54 or (56 <= LA49_0 <= 57) or (60 <= LA49_0 <= 62) or (65 <= LA49_0 <= 67)) :
                    alt49 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("309:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );", 49, 0, self.input)

                    raise nvae

                if alt49 == 1:
                    # C.g:310:4: '(' type_name ')' cast_expression
                    self.match(self.input, 50, self.FOLLOW_50_in_cast_expression1166)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_type_name_in_cast_expression1168)
                    self.type_name()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_cast_expression1170)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_cast_expression_in_cast_expression1172)
                    self.cast_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt49 == 2:
                    # C.g:311:4: unary_expression
                    self.following.append(self.FOLLOW_unary_expression_in_cast_expression1177)
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
    # C.g:314:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );
    def unary_expression(self, ):

        unary_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 40):
                    return 

                # C.g:315:2: ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' )
                alt50 = 6
                LA50 = self.input.LA(1)
                if LA50 == IDENTIFIER or LA50 == HEX_LITERAL or LA50 == OCTAL_LITERAL or LA50 == DECIMAL_LITERAL or LA50 == CHARACTER_LITERAL or LA50 == STRING_LITERAL or LA50 == FLOATING_POINT_LITERAL or LA50 == 50:
                    alt50 = 1
                elif LA50 == 60:
                    alt50 = 2
                elif LA50 == 61:
                    alt50 = 3
                elif LA50 == 54 or LA50 == 56 or LA50 == 57 or LA50 == 65 or LA50 == 66 or LA50 == 67:
                    alt50 = 4
                elif LA50 == 62:
                    LA50_7 = self.input.LA(2)

                    if (LA50_7 == 50) :
                        LA50_8 = self.input.LA(3)

                        if (self.synpred89()) :
                            alt50 = 5
                        elif (True) :
                            alt50 = 6
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("314:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );", 50, 8, self.input)

                            raise nvae

                    elif ((IDENTIFIER <= LA50_7 <= FLOATING_POINT_LITERAL) or LA50_7 == 54 or (56 <= LA50_7 <= 57) or (60 <= LA50_7 <= 62) or (65 <= LA50_7 <= 67)) :
                        alt50 = 5
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("314:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );", 50, 7, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("314:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );", 50, 0, self.input)

                    raise nvae

                if alt50 == 1:
                    # C.g:315:4: postfix_expression
                    self.following.append(self.FOLLOW_postfix_expression_in_unary_expression1188)
                    self.postfix_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 2:
                    # C.g:316:4: '++' unary_expression
                    self.match(self.input, 60, self.FOLLOW_60_in_unary_expression1193)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_unary_expression_in_unary_expression1195)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 3:
                    # C.g:317:4: '--' unary_expression
                    self.match(self.input, 61, self.FOLLOW_61_in_unary_expression1200)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_unary_expression_in_unary_expression1202)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 4:
                    # C.g:318:4: unary_operator cast_expression
                    self.following.append(self.FOLLOW_unary_operator_in_unary_expression1207)
                    self.unary_operator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_cast_expression_in_unary_expression1209)
                    self.cast_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 5:
                    # C.g:319:4: 'sizeof' unary_expression
                    self.match(self.input, 62, self.FOLLOW_62_in_unary_expression1214)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_unary_expression_in_unary_expression1216)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 6:
                    # C.g:320:4: 'sizeof' '(' type_name ')'
                    self.match(self.input, 62, self.FOLLOW_62_in_unary_expression1221)
                    if self.failed:
                        return 
                    self.match(self.input, 50, self.FOLLOW_50_in_unary_expression1223)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_type_name_in_unary_expression1225)
                    self.type_name()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_unary_expression1227)
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
    # C.g:323:1: postfix_expression : primary_expression ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )* ;
    def postfix_expression(self, ):

        postfix_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 41):
                    return 

                # C.g:324:2: ( primary_expression ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )* )
                # C.g:324:6: primary_expression ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )*
                self.following.append(self.FOLLOW_primary_expression_in_postfix_expression1240)
                self.primary_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:325:9: ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )*
                while True: #loop51
                    alt51 = 9
                    LA51 = self.input.LA(1)
                    if LA51 == 54:
                        LA51_1 = self.input.LA(2)

                        if (LA51_1 == IDENTIFIER) :
                            LA51_29 = self.input.LA(3)

                            if (self.synpred94()) :
                                alt51 = 5




                    elif LA51 == 52:
                        alt51 = 1
                    elif LA51 == 50:
                        LA51_24 = self.input.LA(2)

                        if (LA51_24 == 51) :
                            alt51 = 2
                        elif ((IDENTIFIER <= LA51_24 <= FLOATING_POINT_LITERAL) or LA51_24 == 50 or LA51_24 == 54 or (56 <= LA51_24 <= 57) or (60 <= LA51_24 <= 62) or (65 <= LA51_24 <= 67)) :
                            alt51 = 3


                    elif LA51 == 63:
                        alt51 = 4
                    elif LA51 == 64:
                        alt51 = 6
                    elif LA51 == 60:
                        alt51 = 7
                    elif LA51 == 61:
                        alt51 = 8

                    if alt51 == 1:
                        # C.g:325:13: '[' expression ']'
                        self.match(self.input, 52, self.FOLLOW_52_in_postfix_expression1254)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_expression_in_postfix_expression1256)
                        self.expression()
                        self.following.pop()
                        if self.failed:
                            return 
                        self.match(self.input, 53, self.FOLLOW_53_in_postfix_expression1258)
                        if self.failed:
                            return 


                    elif alt51 == 2:
                        # C.g:326:13: '(' ')'
                        self.match(self.input, 50, self.FOLLOW_50_in_postfix_expression1272)
                        if self.failed:
                            return 
                        self.match(self.input, 51, self.FOLLOW_51_in_postfix_expression1274)
                        if self.failed:
                            return 


                    elif alt51 == 3:
                        # C.g:327:13: '(' argument_expression_list ')'
                        self.match(self.input, 50, self.FOLLOW_50_in_postfix_expression1288)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_argument_expression_list_in_postfix_expression1290)
                        self.argument_expression_list()
                        self.following.pop()
                        if self.failed:
                            return 
                        self.match(self.input, 51, self.FOLLOW_51_in_postfix_expression1292)
                        if self.failed:
                            return 


                    elif alt51 == 4:
                        # C.g:328:13: '.' IDENTIFIER
                        self.match(self.input, 63, self.FOLLOW_63_in_postfix_expression1306)
                        if self.failed:
                            return 
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_postfix_expression1308)
                        if self.failed:
                            return 


                    elif alt51 == 5:
                        # C.g:329:13: '*' IDENTIFIER
                        self.match(self.input, 54, self.FOLLOW_54_in_postfix_expression1322)
                        if self.failed:
                            return 
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_postfix_expression1324)
                        if self.failed:
                            return 


                    elif alt51 == 6:
                        # C.g:330:13: '->' IDENTIFIER
                        self.match(self.input, 64, self.FOLLOW_64_in_postfix_expression1338)
                        if self.failed:
                            return 
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_postfix_expression1340)
                        if self.failed:
                            return 


                    elif alt51 == 7:
                        # C.g:331:13: '++'
                        self.match(self.input, 60, self.FOLLOW_60_in_postfix_expression1354)
                        if self.failed:
                            return 


                    elif alt51 == 8:
                        # C.g:332:13: '--'
                        self.match(self.input, 61, self.FOLLOW_61_in_postfix_expression1368)
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
    # C.g:336:1: unary_operator : ( '&' | '*' | '+' | '-' | '~' | '!' );
    def unary_operator(self, ):

        unary_operator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 42):
                    return 

                # C.g:337:2: ( '&' | '*' | '+' | '-' | '~' | '!' )
                # C.g:
                if self.input.LA(1) == 54 or (56 <= self.input.LA(1) <= 57) or (65 <= self.input.LA(1) <= 67):
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
    # C.g:345:1: primary_expression : ( IDENTIFIER | constant | '(' expression ')' );
    def primary_expression(self, ):

        primary_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 43):
                    return 

                # C.g:346:2: ( IDENTIFIER | constant | '(' expression ')' )
                alt52 = 3
                LA52 = self.input.LA(1)
                if LA52 == IDENTIFIER:
                    alt52 = 1
                elif LA52 == HEX_LITERAL or LA52 == OCTAL_LITERAL or LA52 == DECIMAL_LITERAL or LA52 == CHARACTER_LITERAL or LA52 == STRING_LITERAL or LA52 == FLOATING_POINT_LITERAL:
                    alt52 = 2
                elif LA52 == 50:
                    alt52 = 3
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("345:1: primary_expression : ( IDENTIFIER | constant | '(' expression ')' );", 52, 0, self.input)

                    raise nvae

                if alt52 == 1:
                    # C.g:346:4: IDENTIFIER
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_primary_expression1426)
                    if self.failed:
                        return 


                elif alt52 == 2:
                    # C.g:347:4: constant
                    self.following.append(self.FOLLOW_constant_in_primary_expression1431)
                    self.constant()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt52 == 3:
                    # C.g:348:4: '(' expression ')'
                    self.match(self.input, 50, self.FOLLOW_50_in_primary_expression1436)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_primary_expression1438)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_primary_expression1440)
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
    # C.g:351:1: constant : ( HEX_LITERAL | OCTAL_LITERAL | DECIMAL_LITERAL | CHARACTER_LITERAL | STRING_LITERAL | FLOATING_POINT_LITERAL );
    def constant(self, ):

        constant_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 44):
                    return 

                # C.g:352:5: ( HEX_LITERAL | OCTAL_LITERAL | DECIMAL_LITERAL | CHARACTER_LITERAL | STRING_LITERAL | FLOATING_POINT_LITERAL )
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
    # C.g:362:1: expression : assignment_expression ( ',' assignment_expression )* ;
    def expression(self, ):

        expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 45):
                    return 

                # C.g:363:2: ( assignment_expression ( ',' assignment_expression )* )
                # C.g:363:4: assignment_expression ( ',' assignment_expression )*
                self.following.append(self.FOLLOW_assignment_expression_in_expression1518)
                self.assignment_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:363:26: ( ',' assignment_expression )*
                while True: #loop53
                    alt53 = 2
                    LA53_0 = self.input.LA(1)

                    if (LA53_0 == 25) :
                        alt53 = 1


                    if alt53 == 1:
                        # C.g:363:27: ',' assignment_expression
                        self.match(self.input, 25, self.FOLLOW_25_in_expression1521)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_assignment_expression_in_expression1523)
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
    # C.g:366:1: constant_expression : conditional_expression ;
    def constant_expression(self, ):

        constant_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 46):
                    return 

                # C.g:367:2: ( conditional_expression )
                # C.g:367:4: conditional_expression
                self.following.append(self.FOLLOW_conditional_expression_in_constant_expression1536)
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
    # C.g:370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );
    def assignment_expression(self, ):

        assignment_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 47):
                    return 

                # C.g:371:2: ( lvalue assignment_operator assignment_expression | conditional_expression )
                alt54 = 2
                LA54 = self.input.LA(1)
                if LA54 == IDENTIFIER:
                    LA54 = self.input.LA(2)
                    if LA54 == 52:
                        LA54_8 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 8, self.input)

                            raise nvae

                    elif LA54 == 50:
                        LA54_9 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 9, self.input)

                            raise nvae

                    elif LA54 == 63:
                        LA54_10 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 10, self.input)

                            raise nvae

                    elif LA54 == 54:
                        LA54_11 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 11, self.input)

                            raise nvae

                    elif LA54 == 64:
                        LA54_12 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 12, self.input)

                            raise nvae

                    elif LA54 == 60:
                        LA54_13 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 13, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_14 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 14, self.input)

                            raise nvae

                    elif LA54 == 26 or LA54 == 68 or LA54 == 69 or LA54 == 70 or LA54 == 71 or LA54 == 72 or LA54 == 73 or LA54 == 74 or LA54 == 75 or LA54 == 76 or LA54 == 77:
                        alt54 = 1
                    elif LA54 == EOF or LA54 == 24 or LA54 == 25 or LA54 == 41 or LA54 == 44 or LA54 == 51 or LA54 == 53 or LA54 == 56 or LA54 == 57 or LA54 == 58 or LA54 == 59 or LA54 == 65 or LA54 == 78 or LA54 == 79 or LA54 == 80 or LA54 == 81 or LA54 == 82 or LA54 == 83 or LA54 == 84 or LA54 == 85 or LA54 == 86 or LA54 == 87 or LA54 == 88 or LA54 == 89 or LA54 == 90:
                        alt54 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 1, self.input)

                        raise nvae

                elif LA54 == HEX_LITERAL or LA54 == OCTAL_LITERAL or LA54 == DECIMAL_LITERAL or LA54 == CHARACTER_LITERAL or LA54 == STRING_LITERAL or LA54 == FLOATING_POINT_LITERAL:
                    LA54 = self.input.LA(2)
                    if LA54 == 52:
                        LA54_36 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 36, self.input)

                            raise nvae

                    elif LA54 == 50:
                        LA54_37 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 37, self.input)

                            raise nvae

                    elif LA54 == 63:
                        LA54_38 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 38, self.input)

                            raise nvae

                    elif LA54 == 54:
                        LA54_39 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 39, self.input)

                            raise nvae

                    elif LA54 == 64:
                        LA54_40 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 40, self.input)

                            raise nvae

                    elif LA54 == 60:
                        LA54_41 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 41, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_42 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 42, self.input)

                            raise nvae

                    elif LA54 == 26 or LA54 == 68 or LA54 == 69 or LA54 == 70 or LA54 == 71 or LA54 == 72 or LA54 == 73 or LA54 == 74 or LA54 == 75 or LA54 == 76 or LA54 == 77:
                        alt54 = 1
                    elif LA54 == EOF or LA54 == 24 or LA54 == 25 or LA54 == 41 or LA54 == 44 or LA54 == 51 or LA54 == 53 or LA54 == 56 or LA54 == 57 or LA54 == 58 or LA54 == 59 or LA54 == 65 or LA54 == 78 or LA54 == 79 or LA54 == 80 or LA54 == 81 or LA54 == 82 or LA54 == 83 or LA54 == 84 or LA54 == 85 or LA54 == 86 or LA54 == 87 or LA54 == 88 or LA54 == 89 or LA54 == 90:
                        alt54 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 2, self.input)

                        raise nvae

                elif LA54 == 50:
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

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 64, self.input)

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

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 65, self.input)

                            raise nvae

                    elif LA54 == 50:
                        LA54_66 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 66, self.input)

                            raise nvae

                    elif LA54 == 60:
                        LA54_67 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 67, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_68 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 68, self.input)

                            raise nvae

                    elif LA54 == 54 or LA54 == 56 or LA54 == 57 or LA54 == 65 or LA54 == 66 or LA54 == 67:
                        LA54_69 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 69, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_70 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 70, self.input)

                            raise nvae

                    elif LA54 == 31 or LA54 == 32 or LA54 == 33 or LA54 == 34 or LA54 == 35 or LA54 == 36 or LA54 == 37 or LA54 == 38 or LA54 == 39 or LA54 == 42 or LA54 == 43 or LA54 == 45 or LA54 == 46 or LA54 == 47 or LA54 == 48 or LA54 == 49:
                        alt54 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 3, self.input)

                        raise nvae

                elif LA54 == 60:
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

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 83, self.input)

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

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 84, self.input)

                            raise nvae

                    elif LA54 == 50:
                        LA54_85 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 85, self.input)

                            raise nvae

                    elif LA54 == 60:
                        LA54_86 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 86, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_87 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 87, self.input)

                            raise nvae

                    elif LA54 == 54 or LA54 == 56 or LA54 == 57 or LA54 == 65 or LA54 == 66 or LA54 == 67:
                        LA54_88 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 88, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_89 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 89, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 4, self.input)

                        raise nvae

                elif LA54 == 61:
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

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 90, self.input)

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

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 91, self.input)

                            raise nvae

                    elif LA54 == 50:
                        LA54_92 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 92, self.input)

                            raise nvae

                    elif LA54 == 60:
                        LA54_93 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 93, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_94 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 94, self.input)

                            raise nvae

                    elif LA54 == 54 or LA54 == 56 or LA54 == 57 or LA54 == 65 or LA54 == 66 or LA54 == 67:
                        LA54_95 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 95, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_96 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 96, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 5, self.input)

                        raise nvae

                elif LA54 == 54 or LA54 == 56 or LA54 == 57 or LA54 == 65 or LA54 == 66 or LA54 == 67:
                    LA54 = self.input.LA(2)
                    if LA54 == 50:
                        LA54_97 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 97, self.input)

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

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 98, self.input)

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

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 99, self.input)

                            raise nvae

                    elif LA54 == 60:
                        LA54_100 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 100, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_101 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 101, self.input)

                            raise nvae

                    elif LA54 == 54 or LA54 == 56 or LA54 == 57 or LA54 == 65 or LA54 == 66 or LA54 == 67:
                        LA54_102 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 102, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_103 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 103, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 6, self.input)

                        raise nvae

                elif LA54 == 62:
                    LA54 = self.input.LA(2)
                    if LA54 == 50:
                        LA54_104 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 104, self.input)

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

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 105, self.input)

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

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 106, self.input)

                            raise nvae

                    elif LA54 == 60:
                        LA54_107 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 107, self.input)

                            raise nvae

                    elif LA54 == 61:
                        LA54_108 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 108, self.input)

                            raise nvae

                    elif LA54 == 54 or LA54 == 56 or LA54 == 57 or LA54 == 65 or LA54 == 66 or LA54 == 67:
                        LA54_109 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 109, self.input)

                            raise nvae

                    elif LA54 == 62:
                        LA54_110 = self.input.LA(3)

                        if (self.synpred111()) :
                            alt54 = 1
                        elif (True) :
                            alt54 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 110, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 7, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("370:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 54, 0, self.input)

                    raise nvae

                if alt54 == 1:
                    # C.g:371:4: lvalue assignment_operator assignment_expression
                    self.following.append(self.FOLLOW_lvalue_in_assignment_expression1547)
                    self.lvalue()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_assignment_operator_in_assignment_expression1549)
                    self.assignment_operator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_assignment_expression_in_assignment_expression1551)
                    self.assignment_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt54 == 2:
                    # C.g:372:4: conditional_expression
                    self.following.append(self.FOLLOW_conditional_expression_in_assignment_expression1556)
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
    # C.g:375:1: lvalue : unary_expression ;
    def lvalue(self, ):

        lvalue_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 48):
                    return 

                # C.g:376:2: ( unary_expression )
                # C.g:376:4: unary_expression
                self.following.append(self.FOLLOW_unary_expression_in_lvalue1568)
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
    # C.g:379:1: assignment_operator : ( '=' | '*=' | '/=' | '%=' | '+=' | '-=' | '<<=' | '>>=' | '&=' | '^=' | '|=' );
    def assignment_operator(self, ):

        assignment_operator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 49):
                    return 

                # C.g:380:2: ( '=' | '*=' | '/=' | '%=' | '+=' | '-=' | '<<=' | '>>=' | '&=' | '^=' | '|=' )
                # C.g:
                if self.input.LA(1) == 26 or (68 <= self.input.LA(1) <= 77):
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
    # C.g:393:1: conditional_expression : logical_or_expression ( '?' expression ':' conditional_expression )? ;
    def conditional_expression(self, ):

        conditional_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 50):
                    return 

                # C.g:394:2: ( logical_or_expression ( '?' expression ':' conditional_expression )? )
                # C.g:394:4: logical_or_expression ( '?' expression ':' conditional_expression )?
                self.following.append(self.FOLLOW_logical_or_expression_in_conditional_expression1640)
                self.logical_or_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:394:26: ( '?' expression ':' conditional_expression )?
                alt55 = 2
                LA55_0 = self.input.LA(1)

                if (LA55_0 == 78) :
                    alt55 = 1
                if alt55 == 1:
                    # C.g:394:27: '?' expression ':' conditional_expression
                    self.match(self.input, 78, self.FOLLOW_78_in_conditional_expression1643)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_conditional_expression1645)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 44, self.FOLLOW_44_in_conditional_expression1647)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_conditional_expression_in_conditional_expression1649)
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
    # C.g:397:1: logical_or_expression : logical_and_expression ( '||' logical_and_expression )* ;
    def logical_or_expression(self, ):

        logical_or_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 51):
                    return 

                # C.g:398:2: ( logical_and_expression ( '||' logical_and_expression )* )
                # C.g:398:4: logical_and_expression ( '||' logical_and_expression )*
                self.following.append(self.FOLLOW_logical_and_expression_in_logical_or_expression1662)
                self.logical_and_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:398:27: ( '||' logical_and_expression )*
                while True: #loop56
                    alt56 = 2
                    LA56_0 = self.input.LA(1)

                    if (LA56_0 == 79) :
                        alt56 = 1


                    if alt56 == 1:
                        # C.g:398:28: '||' logical_and_expression
                        self.match(self.input, 79, self.FOLLOW_79_in_logical_or_expression1665)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_logical_and_expression_in_logical_or_expression1667)
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
    # C.g:401:1: logical_and_expression : inclusive_or_expression ( '&&' inclusive_or_expression )* ;
    def logical_and_expression(self, ):

        logical_and_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 52):
                    return 

                # C.g:402:2: ( inclusive_or_expression ( '&&' inclusive_or_expression )* )
                # C.g:402:4: inclusive_or_expression ( '&&' inclusive_or_expression )*
                self.following.append(self.FOLLOW_inclusive_or_expression_in_logical_and_expression1680)
                self.inclusive_or_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:402:28: ( '&&' inclusive_or_expression )*
                while True: #loop57
                    alt57 = 2
                    LA57_0 = self.input.LA(1)

                    if (LA57_0 == 80) :
                        alt57 = 1


                    if alt57 == 1:
                        # C.g:402:29: '&&' inclusive_or_expression
                        self.match(self.input, 80, self.FOLLOW_80_in_logical_and_expression1683)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_inclusive_or_expression_in_logical_and_expression1685)
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
    # C.g:405:1: inclusive_or_expression : exclusive_or_expression ( '|' exclusive_or_expression )* ;
    def inclusive_or_expression(self, ):

        inclusive_or_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 53):
                    return 

                # C.g:406:2: ( exclusive_or_expression ( '|' exclusive_or_expression )* )
                # C.g:406:4: exclusive_or_expression ( '|' exclusive_or_expression )*
                self.following.append(self.FOLLOW_exclusive_or_expression_in_inclusive_or_expression1698)
                self.exclusive_or_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:406:28: ( '|' exclusive_or_expression )*
                while True: #loop58
                    alt58 = 2
                    LA58_0 = self.input.LA(1)

                    if (LA58_0 == 81) :
                        alt58 = 1


                    if alt58 == 1:
                        # C.g:406:29: '|' exclusive_or_expression
                        self.match(self.input, 81, self.FOLLOW_81_in_inclusive_or_expression1701)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_exclusive_or_expression_in_inclusive_or_expression1703)
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
    # C.g:409:1: exclusive_or_expression : and_expression ( '^' and_expression )* ;
    def exclusive_or_expression(self, ):

        exclusive_or_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 54):
                    return 

                # C.g:410:2: ( and_expression ( '^' and_expression )* )
                # C.g:410:4: and_expression ( '^' and_expression )*
                self.following.append(self.FOLLOW_and_expression_in_exclusive_or_expression1716)
                self.and_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:410:19: ( '^' and_expression )*
                while True: #loop59
                    alt59 = 2
                    LA59_0 = self.input.LA(1)

                    if (LA59_0 == 82) :
                        alt59 = 1


                    if alt59 == 1:
                        # C.g:410:20: '^' and_expression
                        self.match(self.input, 82, self.FOLLOW_82_in_exclusive_or_expression1719)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_and_expression_in_exclusive_or_expression1721)
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
    # C.g:413:1: and_expression : equality_expression ( '&' equality_expression )* ;
    def and_expression(self, ):

        and_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 55):
                    return 

                # C.g:414:2: ( equality_expression ( '&' equality_expression )* )
                # C.g:414:4: equality_expression ( '&' equality_expression )*
                self.following.append(self.FOLLOW_equality_expression_in_and_expression1734)
                self.equality_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:414:24: ( '&' equality_expression )*
                while True: #loop60
                    alt60 = 2
                    LA60_0 = self.input.LA(1)

                    if (LA60_0 == 65) :
                        alt60 = 1


                    if alt60 == 1:
                        # C.g:414:25: '&' equality_expression
                        self.match(self.input, 65, self.FOLLOW_65_in_and_expression1737)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_equality_expression_in_and_expression1739)
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
    # C.g:416:1: equality_expression : relational_expression ( ( '==' | '!=' ) relational_expression )* ;
    def equality_expression(self, ):

        equality_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 56):
                    return 

                # C.g:417:2: ( relational_expression ( ( '==' | '!=' ) relational_expression )* )
                # C.g:417:4: relational_expression ( ( '==' | '!=' ) relational_expression )*
                self.following.append(self.FOLLOW_relational_expression_in_equality_expression1751)
                self.relational_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:417:26: ( ( '==' | '!=' ) relational_expression )*
                while True: #loop61
                    alt61 = 2
                    LA61_0 = self.input.LA(1)

                    if ((83 <= LA61_0 <= 84)) :
                        alt61 = 1


                    if alt61 == 1:
                        # C.g:417:27: ( '==' | '!=' ) relational_expression
                        if (83 <= self.input.LA(1) <= 84):
                            self.input.consume();
                            self.errorRecovery = False
                            self.failed = False

                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            mse = MismatchedSetException(None, self.input)
                            self.recoverFromMismatchedSet(
                                self.input, mse, self.FOLLOW_set_in_equality_expression1754
                                )
                            raise mse


                        self.following.append(self.FOLLOW_relational_expression_in_equality_expression1760)
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
    # C.g:420:1: relational_expression : shift_expression ( ( '<' | '>' | '<=' | '>=' ) shift_expression )* ;
    def relational_expression(self, ):

        relational_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 57):
                    return 

                # C.g:421:2: ( shift_expression ( ( '<' | '>' | '<=' | '>=' ) shift_expression )* )
                # C.g:421:4: shift_expression ( ( '<' | '>' | '<=' | '>=' ) shift_expression )*
                self.following.append(self.FOLLOW_shift_expression_in_relational_expression1773)
                self.shift_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:421:21: ( ( '<' | '>' | '<=' | '>=' ) shift_expression )*
                while True: #loop62
                    alt62 = 2
                    LA62_0 = self.input.LA(1)

                    if ((85 <= LA62_0 <= 88)) :
                        alt62 = 1


                    if alt62 == 1:
                        # C.g:421:22: ( '<' | '>' | '<=' | '>=' ) shift_expression
                        if (85 <= self.input.LA(1) <= 88):
                            self.input.consume();
                            self.errorRecovery = False
                            self.failed = False

                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            mse = MismatchedSetException(None, self.input)
                            self.recoverFromMismatchedSet(
                                self.input, mse, self.FOLLOW_set_in_relational_expression1776
                                )
                            raise mse


                        self.following.append(self.FOLLOW_shift_expression_in_relational_expression1786)
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
    # C.g:424:1: shift_expression : additive_expression ( ( '<<' | '>>' ) additive_expression )* ;
    def shift_expression(self, ):

        shift_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 58):
                    return 

                # C.g:425:2: ( additive_expression ( ( '<<' | '>>' ) additive_expression )* )
                # C.g:425:4: additive_expression ( ( '<<' | '>>' ) additive_expression )*
                self.following.append(self.FOLLOW_additive_expression_in_shift_expression1799)
                self.additive_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:425:24: ( ( '<<' | '>>' ) additive_expression )*
                while True: #loop63
                    alt63 = 2
                    LA63_0 = self.input.LA(1)

                    if ((89 <= LA63_0 <= 90)) :
                        alt63 = 1


                    if alt63 == 1:
                        # C.g:425:25: ( '<<' | '>>' ) additive_expression
                        if (89 <= self.input.LA(1) <= 90):
                            self.input.consume();
                            self.errorRecovery = False
                            self.failed = False

                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            mse = MismatchedSetException(None, self.input)
                            self.recoverFromMismatchedSet(
                                self.input, mse, self.FOLLOW_set_in_shift_expression1802
                                )
                            raise mse


                        self.following.append(self.FOLLOW_additive_expression_in_shift_expression1808)
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
    # C.g:430:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | macro_statement );
    def statement(self, ):

        statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 59):
                    return 

                # C.g:431:2: ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | macro_statement )
                alt64 = 7
                LA64 = self.input.LA(1)
                if LA64 == IDENTIFIER:
                    LA64 = self.input.LA(2)
                    if LA64 == 50:
                        LA64_21 = self.input.LA(3)

                        if (self.synpred138()) :
                            alt64 = 3
                        elif (True) :
                            alt64 = 7
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("430:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | macro_statement );", 64, 21, self.input)

                            raise nvae

                    elif LA64 == 44:
                        alt64 = 1
                    elif LA64 == 24 or LA64 == 25 or LA64 == 26 or LA64 == 52 or LA64 == 54 or LA64 == 56 or LA64 == 57 or LA64 == 58 or LA64 == 59 or LA64 == 60 or LA64 == 61 or LA64 == 63 or LA64 == 64 or LA64 == 65 or LA64 == 68 or LA64 == 69 or LA64 == 70 or LA64 == 71 or LA64 == 72 or LA64 == 73 or LA64 == 74 or LA64 == 75 or LA64 == 76 or LA64 == 77 or LA64 == 78 or LA64 == 79 or LA64 == 80 or LA64 == 81 or LA64 == 82 or LA64 == 83 or LA64 == 84 or LA64 == 85 or LA64 == 86 or LA64 == 87 or LA64 == 88 or LA64 == 89 or LA64 == 90:
                        alt64 = 3
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("430:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | macro_statement );", 64, 1, self.input)

                        raise nvae

                elif LA64 == 91 or LA64 == 92:
                    alt64 = 1
                elif LA64 == 40:
                    alt64 = 2
                elif LA64 == HEX_LITERAL or LA64 == OCTAL_LITERAL or LA64 == DECIMAL_LITERAL or LA64 == CHARACTER_LITERAL or LA64 == STRING_LITERAL or LA64 == FLOATING_POINT_LITERAL or LA64 == 24 or LA64 == 50 or LA64 == 54 or LA64 == 56 or LA64 == 57 or LA64 == 60 or LA64 == 61 or LA64 == 62 or LA64 == 65 or LA64 == 66 or LA64 == 67:
                    alt64 = 3
                elif LA64 == 93 or LA64 == 95:
                    alt64 = 4
                elif LA64 == 96 or LA64 == 97 or LA64 == 98:
                    alt64 = 5
                elif LA64 == 99 or LA64 == 100 or LA64 == 101 or LA64 == 102:
                    alt64 = 6
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("430:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | macro_statement );", 64, 0, self.input)

                    raise nvae

                if alt64 == 1:
                    # C.g:431:4: labeled_statement
                    self.following.append(self.FOLLOW_labeled_statement_in_statement1823)
                    self.labeled_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 2:
                    # C.g:432:4: compound_statement
                    self.following.append(self.FOLLOW_compound_statement_in_statement1828)
                    self.compound_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 3:
                    # C.g:433:4: expression_statement
                    self.following.append(self.FOLLOW_expression_statement_in_statement1833)
                    self.expression_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 4:
                    # C.g:434:4: selection_statement
                    self.following.append(self.FOLLOW_selection_statement_in_statement1838)
                    self.selection_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 5:
                    # C.g:435:4: iteration_statement
                    self.following.append(self.FOLLOW_iteration_statement_in_statement1843)
                    self.iteration_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 6:
                    # C.g:436:4: jump_statement
                    self.following.append(self.FOLLOW_jump_statement_in_statement1848)
                    self.jump_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt64 == 7:
                    # C.g:437:4: macro_statement
                    self.following.append(self.FOLLOW_macro_statement_in_statement1853)
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
    # C.g:440:1: macro_statement : IDENTIFIER '(' ( IDENTIFIER | statement_list | declaration ) ')' ;
    def macro_statement(self, ):

        macro_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 60):
                    return 

                # C.g:441:2: ( IDENTIFIER '(' ( IDENTIFIER | statement_list | declaration ) ')' )
                # C.g:441:4: IDENTIFIER '(' ( IDENTIFIER | statement_list | declaration ) ')'
                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_macro_statement1864)
                if self.failed:
                    return 
                self.match(self.input, 50, self.FOLLOW_50_in_macro_statement1866)
                if self.failed:
                    return 
                # C.g:441:19: ( IDENTIFIER | statement_list | declaration )
                alt65 = 3
                LA65 = self.input.LA(1)
                if LA65 == IDENTIFIER:
                    LA65 = self.input.LA(2)
                    if LA65 == 50:
                        LA65_35 = self.input.LA(3)

                        if (self.synpred143()) :
                            alt65 = 2
                        elif (True) :
                            alt65 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("441:19: ( IDENTIFIER | statement_list | declaration )", 65, 35, self.input)

                            raise nvae

                    elif LA65 == 25 or LA65 == 26 or LA65 == 44 or LA65 == 52 or LA65 == 56 or LA65 == 57 or LA65 == 58 or LA65 == 59 or LA65 == 60 or LA65 == 61 or LA65 == 63 or LA65 == 64 or LA65 == 65 or LA65 == 68 or LA65 == 69 or LA65 == 70 or LA65 == 71 or LA65 == 72 or LA65 == 73 or LA65 == 74 or LA65 == 75 or LA65 == 76 or LA65 == 77 or LA65 == 78 or LA65 == 79 or LA65 == 80 or LA65 == 81 or LA65 == 82 or LA65 == 83 or LA65 == 84 or LA65 == 85 or LA65 == 86 or LA65 == 87 or LA65 == 88 or LA65 == 89 or LA65 == 90:
                        alt65 = 2
                    elif LA65 == 54:
                        LA65_37 = self.input.LA(3)

                        if (self.synpred143()) :
                            alt65 = 2
                        elif (True) :
                            alt65 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("441:19: ( IDENTIFIER | statement_list | declaration )", 65, 37, self.input)

                            raise nvae

                    elif LA65 == IDENTIFIER or LA65 == 27 or LA65 == 28 or LA65 == 29 or LA65 == 30 or LA65 == 31 or LA65 == 32 or LA65 == 33 or LA65 == 34 or LA65 == 35 or LA65 == 36 or LA65 == 37 or LA65 == 38 or LA65 == 39 or LA65 == 42 or LA65 == 43 or LA65 == 45 or LA65 == 46 or LA65 == 47 or LA65 == 48 or LA65 == 49:
                        alt65 = 3
                    elif LA65 == 24:
                        LA65_39 = self.input.LA(3)

                        if (self.synpred143()) :
                            alt65 = 2
                        elif (True) :
                            alt65 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("441:19: ( IDENTIFIER | statement_list | declaration )", 65, 39, self.input)

                            raise nvae

                    elif LA65 == 51:
                        alt65 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("441:19: ( IDENTIFIER | statement_list | declaration )", 65, 1, self.input)

                        raise nvae

                elif LA65 == HEX_LITERAL or LA65 == OCTAL_LITERAL or LA65 == DECIMAL_LITERAL or LA65 == CHARACTER_LITERAL or LA65 == STRING_LITERAL or LA65 == FLOATING_POINT_LITERAL or LA65 == 24 or LA65 == 40 or LA65 == 50 or LA65 == 54 or LA65 == 56 or LA65 == 57 or LA65 == 60 or LA65 == 61 or LA65 == 62 or LA65 == 65 or LA65 == 66 or LA65 == 67 or LA65 == 91 or LA65 == 92 or LA65 == 93 or LA65 == 95 or LA65 == 96 or LA65 == 97 or LA65 == 98 or LA65 == 99 or LA65 == 100 or LA65 == 101 or LA65 == 102:
                    alt65 = 2
                elif LA65 == 23 or LA65 == 27 or LA65 == 28 or LA65 == 29 or LA65 == 30 or LA65 == 31 or LA65 == 32 or LA65 == 33 or LA65 == 34 or LA65 == 35 or LA65 == 36 or LA65 == 37 or LA65 == 38 or LA65 == 39 or LA65 == 42 or LA65 == 43 or LA65 == 45 or LA65 == 46 or LA65 == 47 or LA65 == 48 or LA65 == 49:
                    alt65 = 3
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("441:19: ( IDENTIFIER | statement_list | declaration )", 65, 0, self.input)

                    raise nvae

                if alt65 == 1:
                    # C.g:441:20: IDENTIFIER
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_macro_statement1869)
                    if self.failed:
                        return 


                elif alt65 == 2:
                    # C.g:441:33: statement_list
                    self.following.append(self.FOLLOW_statement_list_in_macro_statement1873)
                    self.statement_list()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt65 == 3:
                    # C.g:441:50: declaration
                    self.following.append(self.FOLLOW_declaration_in_macro_statement1877)
                    self.declaration()
                    self.following.pop()
                    if self.failed:
                        return 



                self.match(self.input, 51, self.FOLLOW_51_in_macro_statement1880)
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
    # C.g:444:1: labeled_statement : ( IDENTIFIER ':' statement | 'case' constant_expression ':' statement | 'default' ':' statement );
    def labeled_statement(self, ):

        labeled_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 61):
                    return 

                # C.g:445:2: ( IDENTIFIER ':' statement | 'case' constant_expression ':' statement | 'default' ':' statement )
                alt66 = 3
                LA66 = self.input.LA(1)
                if LA66 == IDENTIFIER:
                    alt66 = 1
                elif LA66 == 91:
                    alt66 = 2
                elif LA66 == 92:
                    alt66 = 3
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("444:1: labeled_statement : ( IDENTIFIER ':' statement | 'case' constant_expression ':' statement | 'default' ':' statement );", 66, 0, self.input)

                    raise nvae

                if alt66 == 1:
                    # C.g:445:4: IDENTIFIER ':' statement
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_labeled_statement1892)
                    if self.failed:
                        return 
                    self.match(self.input, 44, self.FOLLOW_44_in_labeled_statement1894)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_labeled_statement1896)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt66 == 2:
                    # C.g:446:4: 'case' constant_expression ':' statement
                    self.match(self.input, 91, self.FOLLOW_91_in_labeled_statement1901)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_labeled_statement1903)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 44, self.FOLLOW_44_in_labeled_statement1905)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_labeled_statement1907)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt66 == 3:
                    # C.g:447:4: 'default' ':' statement
                    self.match(self.input, 92, self.FOLLOW_92_in_labeled_statement1912)
                    if self.failed:
                        return 
                    self.match(self.input, 44, self.FOLLOW_44_in_labeled_statement1914)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_labeled_statement1916)
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
    # C.g:450:1: compound_statement : '{' ( declaration )* ( statement_list )? '}' ;
    def compound_statement(self, ):
        self.Symbols_stack.append(Symbols_scope())

        compound_statement_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 62):
                    return 

                # C.g:455:2: ( '{' ( declaration )* ( statement_list )? '}' )
                # C.g:455:4: '{' ( declaration )* ( statement_list )? '}'
                self.match(self.input, 40, self.FOLLOW_40_in_compound_statement1938)
                if self.failed:
                    return 
                # C.g:455:8: ( declaration )*
                while True: #loop67
                    alt67 = 2
                    LA67_0 = self.input.LA(1)

                    if (LA67_0 == IDENTIFIER) :
                        LA67 = self.input.LA(2)
                        if LA67 == 50:
                            LA67_37 = self.input.LA(3)

                            if (self.synpred146()) :
                                alt67 = 1


                        elif LA67 == 54:
                            LA67_40 = self.input.LA(3)

                            if (self.synpred146()) :
                                alt67 = 1


                        elif LA67 == 24:
                            LA67_59 = self.input.LA(3)

                            if (self.synpred146()) :
                                alt67 = 1


                        elif LA67 == IDENTIFIER or LA67 == 27 or LA67 == 28 or LA67 == 29 or LA67 == 30 or LA67 == 31 or LA67 == 32 or LA67 == 33 or LA67 == 34 or LA67 == 35 or LA67 == 36 or LA67 == 37 or LA67 == 38 or LA67 == 39 or LA67 == 42 or LA67 == 43 or LA67 == 45 or LA67 == 46 or LA67 == 47 or LA67 == 48 or LA67 == 49:
                            alt67 = 1

                    elif (LA67_0 == 23 or (27 <= LA67_0 <= 39) or (42 <= LA67_0 <= 43) or (45 <= LA67_0 <= 49)) :
                        alt67 = 1


                    if alt67 == 1:
                        # C.g:0:0: declaration
                        self.following.append(self.FOLLOW_declaration_in_compound_statement1940)
                        self.declaration()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop67


                # C.g:455:21: ( statement_list )?
                alt68 = 2
                LA68_0 = self.input.LA(1)

                if ((IDENTIFIER <= LA68_0 <= FLOATING_POINT_LITERAL) or LA68_0 == 24 or LA68_0 == 40 or LA68_0 == 50 or LA68_0 == 54 or (56 <= LA68_0 <= 57) or (60 <= LA68_0 <= 62) or (65 <= LA68_0 <= 67) or (91 <= LA68_0 <= 93) or (95 <= LA68_0 <= 102)) :
                    alt68 = 1
                if alt68 == 1:
                    # C.g:0:0: statement_list
                    self.following.append(self.FOLLOW_statement_list_in_compound_statement1943)
                    self.statement_list()
                    self.following.pop()
                    if self.failed:
                        return 



                self.match(self.input, 41, self.FOLLOW_41_in_compound_statement1946)
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
    # C.g:458:1: statement_list : ( statement )+ ;
    def statement_list(self, ):

        statement_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 63):
                    return 

                # C.g:459:2: ( ( statement )+ )
                # C.g:459:4: ( statement )+
                # C.g:459:4: ( statement )+
                cnt69 = 0
                while True: #loop69
                    alt69 = 2
                    LA69_0 = self.input.LA(1)

                    if ((IDENTIFIER <= LA69_0 <= FLOATING_POINT_LITERAL) or LA69_0 == 24 or LA69_0 == 40 or LA69_0 == 50 or LA69_0 == 54 or (56 <= LA69_0 <= 57) or (60 <= LA69_0 <= 62) or (65 <= LA69_0 <= 67) or (91 <= LA69_0 <= 93) or (95 <= LA69_0 <= 102)) :
                        alt69 = 1


                    if alt69 == 1:
                        # C.g:0:0: statement
                        self.following.append(self.FOLLOW_statement_in_statement_list1957)
                        self.statement()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt69 >= 1:
                            break #loop69

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(69, self.input)
                        raise eee

                    cnt69 += 1






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
    # C.g:462:1: expression_statement : ( ';' | expression ';' );
    def expression_statement(self, ):

        expression_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 64):
                    return 

                # C.g:463:2: ( ';' | expression ';' )
                alt70 = 2
                LA70_0 = self.input.LA(1)

                if (LA70_0 == 24) :
                    alt70 = 1
                elif ((IDENTIFIER <= LA70_0 <= FLOATING_POINT_LITERAL) or LA70_0 == 50 or LA70_0 == 54 or (56 <= LA70_0 <= 57) or (60 <= LA70_0 <= 62) or (65 <= LA70_0 <= 67)) :
                    alt70 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("462:1: expression_statement : ( ';' | expression ';' );", 70, 0, self.input)

                    raise nvae

                if alt70 == 1:
                    # C.g:463:4: ';'
                    self.match(self.input, 24, self.FOLLOW_24_in_expression_statement1969)
                    if self.failed:
                        return 


                elif alt70 == 2:
                    # C.g:464:4: expression ';'
                    self.following.append(self.FOLLOW_expression_in_expression_statement1974)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_expression_statement1976)
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
    # C.g:467:1: selection_statement : ( 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )? | 'switch' '(' expression ')' statement );
    def selection_statement(self, ):

        selection_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 65):
                    return 

                # C.g:468:2: ( 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )? | 'switch' '(' expression ')' statement )
                alt72 = 2
                LA72_0 = self.input.LA(1)

                if (LA72_0 == 93) :
                    alt72 = 1
                elif (LA72_0 == 95) :
                    alt72 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("467:1: selection_statement : ( 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )? | 'switch' '(' expression ')' statement );", 72, 0, self.input)

                    raise nvae

                if alt72 == 1:
                    # C.g:468:4: 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )?
                    self.match(self.input, 93, self.FOLLOW_93_in_selection_statement1987)
                    if self.failed:
                        return 
                    self.match(self.input, 50, self.FOLLOW_50_in_selection_statement1989)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_selection_statement1991)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_selection_statement1993)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_selection_statement1995)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:468:38: ( options {k=1; backtrack=false; } : 'else' statement )?
                    alt71 = 2
                    LA71_0 = self.input.LA(1)

                    if (LA71_0 == 94) :
                        alt71 = 1
                    if alt71 == 1:
                        # C.g:468:71: 'else' statement
                        self.match(self.input, 94, self.FOLLOW_94_in_selection_statement2010)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_statement_in_selection_statement2012)
                        self.statement()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt72 == 2:
                    # C.g:469:4: 'switch' '(' expression ')' statement
                    self.match(self.input, 95, self.FOLLOW_95_in_selection_statement2019)
                    if self.failed:
                        return 
                    self.match(self.input, 50, self.FOLLOW_50_in_selection_statement2021)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_selection_statement2023)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_selection_statement2025)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_selection_statement2027)
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
    # C.g:472:1: iteration_statement : ( 'while' '(' expression ')' statement | 'do' statement 'while' '(' expression ')' ';' | 'for' '(' expression_statement expression_statement ( expression )? ')' statement );
    def iteration_statement(self, ):

        iteration_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 66):
                    return 

                # C.g:473:2: ( 'while' '(' expression ')' statement | 'do' statement 'while' '(' expression ')' ';' | 'for' '(' expression_statement expression_statement ( expression )? ')' statement )
                alt74 = 3
                LA74 = self.input.LA(1)
                if LA74 == 96:
                    alt74 = 1
                elif LA74 == 97:
                    alt74 = 2
                elif LA74 == 98:
                    alt74 = 3
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("472:1: iteration_statement : ( 'while' '(' expression ')' statement | 'do' statement 'while' '(' expression ')' ';' | 'for' '(' expression_statement expression_statement ( expression )? ')' statement );", 74, 0, self.input)

                    raise nvae

                if alt74 == 1:
                    # C.g:473:4: 'while' '(' expression ')' statement
                    self.match(self.input, 96, self.FOLLOW_96_in_iteration_statement2038)
                    if self.failed:
                        return 
                    self.match(self.input, 50, self.FOLLOW_50_in_iteration_statement2040)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_iteration_statement2042)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_iteration_statement2044)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_iteration_statement2046)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt74 == 2:
                    # C.g:474:4: 'do' statement 'while' '(' expression ')' ';'
                    self.match(self.input, 97, self.FOLLOW_97_in_iteration_statement2051)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_iteration_statement2053)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 96, self.FOLLOW_96_in_iteration_statement2055)
                    if self.failed:
                        return 
                    self.match(self.input, 50, self.FOLLOW_50_in_iteration_statement2057)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_iteration_statement2059)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_iteration_statement2061)
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_iteration_statement2063)
                    if self.failed:
                        return 


                elif alt74 == 3:
                    # C.g:475:4: 'for' '(' expression_statement expression_statement ( expression )? ')' statement
                    self.match(self.input, 98, self.FOLLOW_98_in_iteration_statement2068)
                    if self.failed:
                        return 
                    self.match(self.input, 50, self.FOLLOW_50_in_iteration_statement2070)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_statement_in_iteration_statement2072)
                    self.expression_statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_statement_in_iteration_statement2074)
                    self.expression_statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:475:56: ( expression )?
                    alt73 = 2
                    LA73_0 = self.input.LA(1)

                    if ((IDENTIFIER <= LA73_0 <= FLOATING_POINT_LITERAL) or LA73_0 == 50 or LA73_0 == 54 or (56 <= LA73_0 <= 57) or (60 <= LA73_0 <= 62) or (65 <= LA73_0 <= 67)) :
                        alt73 = 1
                    if alt73 == 1:
                        # C.g:0:0: expression
                        self.following.append(self.FOLLOW_expression_in_iteration_statement2076)
                        self.expression()
                        self.following.pop()
                        if self.failed:
                            return 



                    self.match(self.input, 51, self.FOLLOW_51_in_iteration_statement2079)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_iteration_statement2081)
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
    # C.g:478:1: jump_statement : ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' );
    def jump_statement(self, ):

        jump_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 67):
                    return 

                # C.g:479:2: ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' )
                alt75 = 5
                LA75 = self.input.LA(1)
                if LA75 == 99:
                    alt75 = 1
                elif LA75 == 100:
                    alt75 = 2
                elif LA75 == 101:
                    alt75 = 3
                elif LA75 == 102:
                    LA75_4 = self.input.LA(2)

                    if (LA75_4 == 24) :
                        alt75 = 4
                    elif ((IDENTIFIER <= LA75_4 <= FLOATING_POINT_LITERAL) or LA75_4 == 50 or LA75_4 == 54 or (56 <= LA75_4 <= 57) or (60 <= LA75_4 <= 62) or (65 <= LA75_4 <= 67)) :
                        alt75 = 5
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("478:1: jump_statement : ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' );", 75, 4, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("478:1: jump_statement : ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' );", 75, 0, self.input)

                    raise nvae

                if alt75 == 1:
                    # C.g:479:4: 'goto' IDENTIFIER ';'
                    self.match(self.input, 99, self.FOLLOW_99_in_jump_statement2092)
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_jump_statement2094)
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_jump_statement2096)
                    if self.failed:
                        return 


                elif alt75 == 2:
                    # C.g:480:4: 'continue' ';'
                    self.match(self.input, 100, self.FOLLOW_100_in_jump_statement2101)
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_jump_statement2103)
                    if self.failed:
                        return 


                elif alt75 == 3:
                    # C.g:481:4: 'break' ';'
                    self.match(self.input, 101, self.FOLLOW_101_in_jump_statement2108)
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_jump_statement2110)
                    if self.failed:
                        return 


                elif alt75 == 4:
                    # C.g:482:4: 'return' ';'
                    self.match(self.input, 102, self.FOLLOW_102_in_jump_statement2115)
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_jump_statement2117)
                    if self.failed:
                        return 


                elif alt75 == 5:
                    # C.g:483:4: 'return' expression ';'
                    self.match(self.input, 102, self.FOLLOW_102_in_jump_statement2122)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_jump_statement2124)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_jump_statement2126)
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
        # C.g:89:6: ( declaration_specifiers )
        # C.g:89:6: declaration_specifiers
        self.following.append(self.FOLLOW_declaration_specifiers_in_synpred2104)
        self.declaration_specifiers()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred2



    # $ANTLR start synpred4
    def synpred4_fragment(self, ):
        # C.g:89:4: ( ( declaration_specifiers )? declarator ( declaration )* '{' )
        # C.g:89:6: ( declaration_specifiers )? declarator ( declaration )* '{'
        # C.g:89:6: ( declaration_specifiers )?
        alt76 = 2
        LA76_0 = self.input.LA(1)

        if ((27 <= LA76_0 <= 39) or (42 <= LA76_0 <= 43) or (45 <= LA76_0 <= 49)) :
            alt76 = 1
        elif (LA76_0 == IDENTIFIER) :
            LA76 = self.input.LA(2)
            if LA76 == 54:
                alt76 = 1
            elif LA76 == IDENTIFIER:
                LA76_18 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 50:
                LA76_19 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 27 or LA76 == 28 or LA76 == 29 or LA76 == 30:
                LA76_20 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 31:
                LA76_21 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 32:
                LA76_22 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 33:
                LA76_23 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 34:
                LA76_24 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 35:
                LA76_25 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 36:
                LA76_26 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 37:
                LA76_27 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 38:
                LA76_28 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 39:
                LA76_29 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 42 or LA76 == 43:
                LA76_30 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 45:
                LA76_31 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
            elif LA76 == 46 or LA76 == 47 or LA76 == 48 or LA76 == 49:
                LA76_32 = self.input.LA(3)

                if (self.synpred2()) :
                    alt76 = 1
        if alt76 == 1:
            # C.g:0:0: declaration_specifiers
            self.following.append(self.FOLLOW_declaration_specifiers_in_synpred4104)
            self.declaration_specifiers()
            self.following.pop()
            if self.failed:
                return 



        self.following.append(self.FOLLOW_declarator_in_synpred4107)
        self.declarator()
        self.following.pop()
        if self.failed:
            return 
        # C.g:89:41: ( declaration )*
        while True: #loop77
            alt77 = 2
            LA77_0 = self.input.LA(1)

            if (LA77_0 == IDENTIFIER or LA77_0 == 23 or (27 <= LA77_0 <= 39) or (42 <= LA77_0 <= 43) or (45 <= LA77_0 <= 49)) :
                alt77 = 1


            if alt77 == 1:
                # C.g:0:0: declaration
                self.following.append(self.FOLLOW_declaration_in_synpred4109)
                self.declaration()
                self.following.pop()
                if self.failed:
                    return 


            else:
                break #loop77


        self.match(self.input, 40, self.FOLLOW_40_in_synpred4112)
        if self.failed:
            return 


    # $ANTLR end synpred4



    # $ANTLR start synpred5
    def synpred5_fragment(self, ):
        # C.g:90:4: ( declaration )
        # C.g:90:4: declaration
        self.following.append(self.FOLLOW_declaration_in_synpred5122)
        self.declaration()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred5



    # $ANTLR start synpred6
    def synpred6_fragment(self, ):
        # C.g:102:4: ( declaration_specifiers )
        # C.g:102:4: declaration_specifiers
        self.following.append(self.FOLLOW_declaration_specifiers_in_synpred6153)
        self.declaration_specifiers()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred6



    # $ANTLR start synpred9
    def synpred9_fragment(self, ):
        # C.g:115:14: ( declaration_specifiers )
        # C.g:115:14: declaration_specifiers
        self.following.append(self.FOLLOW_declaration_specifiers_in_synpred9202)
        self.declaration_specifiers()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred9



    # $ANTLR start synpred13
    def synpred13_fragment(self, ):
        # C.g:123:7: ( type_specifier )
        # C.g:123:7: type_specifier
        self.following.append(self.FOLLOW_type_specifier_in_synpred13250)
        self.type_specifier()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred13



    # $ANTLR start synpred31
    def synpred31_fragment(self, ):
        # C.g:156:4: ( IDENTIFIER declarator )
        # C.g:156:5: IDENTIFIER declarator
        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_synpred31411)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_declarator_in_synpred31413)
        self.declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred31



    # $ANTLR start synpred37
    def synpred37_fragment(self, ):
        # C.g:188:23: ( type_specifier )
        # C.g:188:23: type_specifier
        self.following.append(self.FOLLOW_type_specifier_in_synpred37548)
        self.type_specifier()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred37



    # $ANTLR start synpred49
    def synpred49_fragment(self, ):
        # C.g:223:4: ( ( pointer )? direct_declarator )
        # C.g:223:4: ( pointer )? direct_declarator
        # C.g:223:4: ( pointer )?
        alt82 = 2
        LA82_0 = self.input.LA(1)

        if (LA82_0 == 54) :
            alt82 = 1
        if alt82 == 1:
            # C.g:0:0: pointer
            self.following.append(self.FOLLOW_pointer_in_synpred49711)
            self.pointer()
            self.following.pop()
            if self.failed:
                return 



        self.following.append(self.FOLLOW_direct_declarator_in_synpred49714)
        self.direct_declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred49



    # $ANTLR start synpred50
    def synpred50_fragment(self, ):
        # C.g:228:17: ( declarator_suffix )
        # C.g:228:17: declarator_suffix
        self.following.append(self.FOLLOW_declarator_suffix_in_synpred50734)
        self.declarator_suffix()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred50



    # $ANTLR start synpred52
    def synpred52_fragment(self, ):
        # C.g:230:24: ( declarator_suffix )
        # C.g:230:24: declarator_suffix
        self.following.append(self.FOLLOW_declarator_suffix_in_synpred52751)
        self.declarator_suffix()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred52



    # $ANTLR start synpred55
    def synpred55_fragment(self, ):
        # C.g:236:9: ( '(' parameter_type_list ')' )
        # C.g:236:9: '(' parameter_type_list ')'
        self.match(self.input, 50, self.FOLLOW_50_in_synpred55791)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_parameter_type_list_in_synpred55793)
        self.parameter_type_list()
        self.following.pop()
        if self.failed:
            return 
        self.match(self.input, 51, self.FOLLOW_51_in_synpred55795)
        if self.failed:
            return 


    # $ANTLR end synpred55



    # $ANTLR start synpred56
    def synpred56_fragment(self, ):
        # C.g:237:9: ( '(' identifier_list ')' )
        # C.g:237:9: '(' identifier_list ')'
        self.match(self.input, 50, self.FOLLOW_50_in_synpred56805)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_identifier_list_in_synpred56807)
        self.identifier_list()
        self.following.pop()
        if self.failed:
            return 
        self.match(self.input, 51, self.FOLLOW_51_in_synpred56809)
        if self.failed:
            return 


    # $ANTLR end synpred56



    # $ANTLR start synpred57
    def synpred57_fragment(self, ):
        # C.g:242:8: ( type_qualifier )
        # C.g:242:8: type_qualifier
        self.following.append(self.FOLLOW_type_qualifier_in_synpred57834)
        self.type_qualifier()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred57



    # $ANTLR start synpred58
    def synpred58_fragment(self, ):
        # C.g:242:24: ( pointer )
        # C.g:242:24: pointer
        self.following.append(self.FOLLOW_pointer_in_synpred58837)
        self.pointer()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred58



    # $ANTLR start synpred59
    def synpred59_fragment(self, ):
        # C.g:242:4: ( '*' ( type_qualifier )+ ( pointer )? )
        # C.g:242:4: '*' ( type_qualifier )+ ( pointer )?
        self.match(self.input, 54, self.FOLLOW_54_in_synpred59832)
        if self.failed:
            return 
        # C.g:242:8: ( type_qualifier )+
        cnt84 = 0
        while True: #loop84
            alt84 = 2
            LA84_0 = self.input.LA(1)

            if ((46 <= LA84_0 <= 49)) :
                alt84 = 1


            if alt84 == 1:
                # C.g:0:0: type_qualifier
                self.following.append(self.FOLLOW_type_qualifier_in_synpred59834)
                self.type_qualifier()
                self.following.pop()
                if self.failed:
                    return 


            else:
                if cnt84 >= 1:
                    break #loop84

                if self.backtracking > 0:
                    self.failed = True
                    return 

                eee = EarlyExitException(84, self.input)
                raise eee

            cnt84 += 1


        # C.g:242:24: ( pointer )?
        alt85 = 2
        LA85_0 = self.input.LA(1)

        if (LA85_0 == 54) :
            alt85 = 1
        if alt85 == 1:
            # C.g:0:0: pointer
            self.following.append(self.FOLLOW_pointer_in_synpred59837)
            self.pointer()
            self.following.pop()
            if self.failed:
                return 





    # $ANTLR end synpred59



    # $ANTLR start synpred60
    def synpred60_fragment(self, ):
        # C.g:243:4: ( '*' pointer )
        # C.g:243:4: '*' pointer
        self.match(self.input, 54, self.FOLLOW_54_in_synpred60843)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_pointer_in_synpred60845)
        self.pointer()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred60



    # $ANTLR start synpred63
    def synpred63_fragment(self, ):
        # C.g:256:28: ( declarator )
        # C.g:256:28: declarator
        self.following.append(self.FOLLOW_declarator_in_synpred63900)
        self.declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred63



    # $ANTLR start synpred64
    def synpred64_fragment(self, ):
        # C.g:256:39: ( abstract_declarator )
        # C.g:256:39: abstract_declarator
        self.following.append(self.FOLLOW_abstract_declarator_in_synpred64902)
        self.abstract_declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred64



    # $ANTLR start synpred67
    def synpred67_fragment(self, ):
        # C.g:265:4: ( specifier_qualifier_list ( abstract_declarator )? )
        # C.g:265:4: specifier_qualifier_list ( abstract_declarator )?
        self.following.append(self.FOLLOW_specifier_qualifier_list_in_synpred67941)
        self.specifier_qualifier_list()
        self.following.pop()
        if self.failed:
            return 
        # C.g:265:29: ( abstract_declarator )?
        alt86 = 2
        LA86_0 = self.input.LA(1)

        if (LA86_0 == 50 or LA86_0 == 52 or LA86_0 == 54) :
            alt86 = 1
        if alt86 == 1:
            # C.g:0:0: abstract_declarator
            self.following.append(self.FOLLOW_abstract_declarator_in_synpred67943)
            self.abstract_declarator()
            self.following.pop()
            if self.failed:
                return 





    # $ANTLR end synpred67



    # $ANTLR start synpred68
    def synpred68_fragment(self, ):
        # C.g:270:12: ( direct_abstract_declarator )
        # C.g:270:12: direct_abstract_declarator
        self.following.append(self.FOLLOW_direct_abstract_declarator_in_synpred68962)
        self.direct_abstract_declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred68



    # $ANTLR start synpred71
    def synpred71_fragment(self, ):
        # C.g:275:65: ( abstract_declarator_suffix )
        # C.g:275:65: abstract_declarator_suffix
        self.following.append(self.FOLLOW_abstract_declarator_suffix_in_synpred71993)
        self.abstract_declarator_suffix()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred71



    # $ANTLR start synpred84
    def synpred84_fragment(self, ):
        # C.g:310:4: ( '(' type_name ')' cast_expression )
        # C.g:310:4: '(' type_name ')' cast_expression
        self.match(self.input, 50, self.FOLLOW_50_in_synpred841166)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_type_name_in_synpred841168)
        self.type_name()
        self.following.pop()
        if self.failed:
            return 
        self.match(self.input, 51, self.FOLLOW_51_in_synpred841170)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_cast_expression_in_synpred841172)
        self.cast_expression()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred84



    # $ANTLR start synpred89
    def synpred89_fragment(self, ):
        # C.g:319:4: ( 'sizeof' unary_expression )
        # C.g:319:4: 'sizeof' unary_expression
        self.match(self.input, 62, self.FOLLOW_62_in_synpred891214)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_unary_expression_in_synpred891216)
        self.unary_expression()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred89



    # $ANTLR start synpred94
    def synpred94_fragment(self, ):
        # C.g:329:13: ( '*' IDENTIFIER )
        # C.g:329:13: '*' IDENTIFIER
        self.match(self.input, 54, self.FOLLOW_54_in_synpred941322)
        if self.failed:
            return 
        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_synpred941324)
        if self.failed:
            return 


    # $ANTLR end synpred94



    # $ANTLR start synpred111
    def synpred111_fragment(self, ):
        # C.g:371:4: ( lvalue assignment_operator assignment_expression )
        # C.g:371:4: lvalue assignment_operator assignment_expression
        self.following.append(self.FOLLOW_lvalue_in_synpred1111547)
        self.lvalue()
        self.following.pop()
        if self.failed:
            return 
        self.following.append(self.FOLLOW_assignment_operator_in_synpred1111549)
        self.assignment_operator()
        self.following.pop()
        if self.failed:
            return 
        self.following.append(self.FOLLOW_assignment_expression_in_synpred1111551)
        self.assignment_expression()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred111



    # $ANTLR start synpred138
    def synpred138_fragment(self, ):
        # C.g:433:4: ( expression_statement )
        # C.g:433:4: expression_statement
        self.following.append(self.FOLLOW_expression_statement_in_synpred1381833)
        self.expression_statement()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred138



    # $ANTLR start synpred143
    def synpred143_fragment(self, ):
        # C.g:441:33: ( statement_list )
        # C.g:441:33: statement_list
        self.following.append(self.FOLLOW_statement_list_in_synpred1431873)
        self.statement_list()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred143



    # $ANTLR start synpred146
    def synpred146_fragment(self, ):
        # C.g:455:8: ( declaration )
        # C.g:455:8: declaration
        self.following.append(self.FOLLOW_declaration_in_synpred1461940)
        self.declaration()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred146



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

    def synpred146(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred146_fragment()
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



 

    FOLLOW_external_declaration_in_translation_unit77 = frozenset([1, 4, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49, 50, 54])
    FOLLOW_function_definition_in_external_declaration117 = frozenset([1])
    FOLLOW_declaration_in_external_declaration122 = frozenset([1])
    FOLLOW_macro_statement_in_external_declaration127 = frozenset([1])
    FOLLOW_declaration_specifiers_in_function_definition153 = frozenset([4, 50, 54])
    FOLLOW_declarator_in_function_definition156 = frozenset([4, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_declaration_in_function_definition162 = frozenset([4, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_compound_statement_in_function_definition165 = frozenset([1])
    FOLLOW_compound_statement_in_function_definition172 = frozenset([1])
    FOLLOW_23_in_declaration200 = frozenset([4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49, 50, 54])
    FOLLOW_declaration_specifiers_in_declaration202 = frozenset([4, 50, 54])
    FOLLOW_init_declarator_list_in_declaration210 = frozenset([24])
    FOLLOW_24_in_declaration212 = frozenset([1])
    FOLLOW_declaration_specifiers_in_declaration218 = frozenset([4, 24, 50, 54])
    FOLLOW_init_declarator_list_in_declaration220 = frozenset([24])
    FOLLOW_24_in_declaration223 = frozenset([1])
    FOLLOW_storage_class_specifier_in_declaration_specifiers242 = frozenset([1, 4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_type_specifier_in_declaration_specifiers250 = frozenset([1, 4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_type_qualifier_in_declaration_specifiers264 = frozenset([1, 4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_init_declarator_in_init_declarator_list286 = frozenset([1, 25])
    FOLLOW_25_in_init_declarator_list289 = frozenset([4, 50, 54])
    FOLLOW_init_declarator_in_init_declarator_list291 = frozenset([1, 25])
    FOLLOW_declarator_in_init_declarator304 = frozenset([1, 26])
    FOLLOW_26_in_init_declarator307 = frozenset([4, 5, 6, 7, 8, 9, 10, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_initializer_in_init_declarator309 = frozenset([1])
    FOLLOW_set_in_storage_class_specifier0 = frozenset([1])
    FOLLOW_31_in_type_specifier355 = frozenset([1])
    FOLLOW_32_in_type_specifier360 = frozenset([1])
    FOLLOW_33_in_type_specifier365 = frozenset([1])
    FOLLOW_34_in_type_specifier370 = frozenset([1])
    FOLLOW_35_in_type_specifier375 = frozenset([1])
    FOLLOW_36_in_type_specifier380 = frozenset([1])
    FOLLOW_37_in_type_specifier385 = frozenset([1])
    FOLLOW_38_in_type_specifier390 = frozenset([1])
    FOLLOW_39_in_type_specifier395 = frozenset([1])
    FOLLOW_struct_or_union_specifier_in_type_specifier400 = frozenset([1])
    FOLLOW_enum_specifier_in_type_specifier405 = frozenset([1])
    FOLLOW_type_id_in_type_specifier417 = frozenset([1])
    FOLLOW_IDENTIFIER_in_type_id433 = frozenset([1])
    FOLLOW_struct_or_union_in_struct_or_union_specifier472 = frozenset([4, 40])
    FOLLOW_IDENTIFIER_in_struct_or_union_specifier474 = frozenset([40])
    FOLLOW_40_in_struct_or_union_specifier477 = frozenset([4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_struct_declaration_list_in_struct_or_union_specifier479 = frozenset([41])
    FOLLOW_41_in_struct_or_union_specifier481 = frozenset([1])
    FOLLOW_struct_or_union_in_struct_or_union_specifier486 = frozenset([4])
    FOLLOW_IDENTIFIER_in_struct_or_union_specifier488 = frozenset([1])
    FOLLOW_set_in_struct_or_union0 = frozenset([1])
    FOLLOW_struct_declaration_in_struct_declaration_list515 = frozenset([1, 4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_specifier_qualifier_list_in_struct_declaration527 = frozenset([4, 44, 50, 54])
    FOLLOW_struct_declarator_list_in_struct_declaration529 = frozenset([24])
    FOLLOW_24_in_struct_declaration531 = frozenset([1])
    FOLLOW_type_qualifier_in_specifier_qualifier_list544 = frozenset([1, 4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_type_specifier_in_specifier_qualifier_list548 = frozenset([1, 4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_struct_declarator_in_struct_declarator_list562 = frozenset([1, 25])
    FOLLOW_25_in_struct_declarator_list565 = frozenset([4, 44, 50, 54])
    FOLLOW_struct_declarator_in_struct_declarator_list567 = frozenset([1, 25])
    FOLLOW_declarator_in_struct_declarator580 = frozenset([1, 44])
    FOLLOW_44_in_struct_declarator583 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_constant_expression_in_struct_declarator585 = frozenset([1])
    FOLLOW_44_in_struct_declarator592 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_constant_expression_in_struct_declarator594 = frozenset([1])
    FOLLOW_45_in_enum_specifier612 = frozenset([40])
    FOLLOW_40_in_enum_specifier614 = frozenset([4])
    FOLLOW_enumerator_list_in_enum_specifier616 = frozenset([41])
    FOLLOW_41_in_enum_specifier618 = frozenset([1])
    FOLLOW_45_in_enum_specifier623 = frozenset([4])
    FOLLOW_IDENTIFIER_in_enum_specifier625 = frozenset([40])
    FOLLOW_40_in_enum_specifier627 = frozenset([4])
    FOLLOW_enumerator_list_in_enum_specifier629 = frozenset([41])
    FOLLOW_41_in_enum_specifier631 = frozenset([1])
    FOLLOW_45_in_enum_specifier636 = frozenset([4])
    FOLLOW_IDENTIFIER_in_enum_specifier638 = frozenset([1])
    FOLLOW_enumerator_in_enumerator_list649 = frozenset([1, 25])
    FOLLOW_25_in_enumerator_list652 = frozenset([4])
    FOLLOW_enumerator_in_enumerator_list654 = frozenset([1, 25])
    FOLLOW_IDENTIFIER_in_enumerator667 = frozenset([1, 26])
    FOLLOW_26_in_enumerator670 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_constant_expression_in_enumerator672 = frozenset([1])
    FOLLOW_set_in_type_qualifier0 = frozenset([1])
    FOLLOW_pointer_in_declarator711 = frozenset([4, 50])
    FOLLOW_direct_declarator_in_declarator714 = frozenset([1])
    FOLLOW_pointer_in_declarator719 = frozenset([1])
    FOLLOW_IDENTIFIER_in_direct_declarator732 = frozenset([1, 50, 52])
    FOLLOW_declarator_suffix_in_direct_declarator734 = frozenset([1, 50, 52])
    FOLLOW_50_in_direct_declarator745 = frozenset([4, 50, 54])
    FOLLOW_declarator_in_direct_declarator747 = frozenset([51])
    FOLLOW_51_in_direct_declarator749 = frozenset([50, 52])
    FOLLOW_declarator_suffix_in_direct_declarator751 = frozenset([1, 50, 52])
    FOLLOW_52_in_declarator_suffix765 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_constant_expression_in_declarator_suffix767 = frozenset([53])
    FOLLOW_53_in_declarator_suffix769 = frozenset([1])
    FOLLOW_52_in_declarator_suffix779 = frozenset([53])
    FOLLOW_53_in_declarator_suffix781 = frozenset([1])
    FOLLOW_50_in_declarator_suffix791 = frozenset([4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_parameter_type_list_in_declarator_suffix793 = frozenset([51])
    FOLLOW_51_in_declarator_suffix795 = frozenset([1])
    FOLLOW_50_in_declarator_suffix805 = frozenset([4])
    FOLLOW_identifier_list_in_declarator_suffix807 = frozenset([51])
    FOLLOW_51_in_declarator_suffix809 = frozenset([1])
    FOLLOW_50_in_declarator_suffix819 = frozenset([51])
    FOLLOW_51_in_declarator_suffix821 = frozenset([1])
    FOLLOW_54_in_pointer832 = frozenset([46, 47, 48, 49])
    FOLLOW_type_qualifier_in_pointer834 = frozenset([1, 46, 47, 48, 49, 54])
    FOLLOW_pointer_in_pointer837 = frozenset([1])
    FOLLOW_54_in_pointer843 = frozenset([54])
    FOLLOW_pointer_in_pointer845 = frozenset([1])
    FOLLOW_54_in_pointer850 = frozenset([1])
    FOLLOW_parameter_list_in_parameter_type_list861 = frozenset([1, 25])
    FOLLOW_25_in_parameter_type_list864 = frozenset([55])
    FOLLOW_55_in_parameter_type_list866 = frozenset([1])
    FOLLOW_parameter_declaration_in_parameter_list879 = frozenset([1, 25])
    FOLLOW_25_in_parameter_list882 = frozenset([4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_parameter_declaration_in_parameter_list884 = frozenset([1, 25])
    FOLLOW_declaration_specifiers_in_parameter_declaration897 = frozenset([4, 50, 52, 54])
    FOLLOW_declarator_in_parameter_declaration900 = frozenset([1, 4, 50, 52, 54])
    FOLLOW_abstract_declarator_in_parameter_declaration902 = frozenset([1, 4, 50, 52, 54])
    FOLLOW_IDENTIFIER_in_identifier_list917 = frozenset([1, 25])
    FOLLOW_25_in_identifier_list922 = frozenset([4])
    FOLLOW_IDENTIFIER_in_identifier_list926 = frozenset([1, 25])
    FOLLOW_specifier_qualifier_list_in_type_name941 = frozenset([1, 50, 52, 54])
    FOLLOW_abstract_declarator_in_type_name943 = frozenset([1])
    FOLLOW_type_id_in_type_name949 = frozenset([1])
    FOLLOW_pointer_in_abstract_declarator960 = frozenset([1, 50, 52])
    FOLLOW_direct_abstract_declarator_in_abstract_declarator962 = frozenset([1])
    FOLLOW_direct_abstract_declarator_in_abstract_declarator968 = frozenset([1])
    FOLLOW_50_in_direct_abstract_declarator981 = frozenset([50, 52, 54])
    FOLLOW_abstract_declarator_in_direct_abstract_declarator983 = frozenset([51])
    FOLLOW_51_in_direct_abstract_declarator985 = frozenset([1, 50, 52])
    FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator989 = frozenset([1, 50, 52])
    FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator993 = frozenset([1, 50, 52])
    FOLLOW_52_in_abstract_declarator_suffix1005 = frozenset([53])
    FOLLOW_53_in_abstract_declarator_suffix1007 = frozenset([1])
    FOLLOW_52_in_abstract_declarator_suffix1012 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_constant_expression_in_abstract_declarator_suffix1014 = frozenset([53])
    FOLLOW_53_in_abstract_declarator_suffix1016 = frozenset([1])
    FOLLOW_50_in_abstract_declarator_suffix1021 = frozenset([51])
    FOLLOW_51_in_abstract_declarator_suffix1023 = frozenset([1])
    FOLLOW_50_in_abstract_declarator_suffix1028 = frozenset([4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_parameter_type_list_in_abstract_declarator_suffix1030 = frozenset([51])
    FOLLOW_51_in_abstract_declarator_suffix1032 = frozenset([1])
    FOLLOW_assignment_expression_in_initializer1045 = frozenset([1])
    FOLLOW_40_in_initializer1050 = frozenset([4, 5, 6, 7, 8, 9, 10, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_initializer_list_in_initializer1052 = frozenset([25, 41])
    FOLLOW_25_in_initializer1054 = frozenset([41])
    FOLLOW_41_in_initializer1057 = frozenset([1])
    FOLLOW_initializer_in_initializer_list1068 = frozenset([1, 25])
    FOLLOW_25_in_initializer_list1071 = frozenset([4, 5, 6, 7, 8, 9, 10, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_initializer_in_initializer_list1073 = frozenset([1, 25])
    FOLLOW_assignment_expression_in_argument_expression_list1090 = frozenset([1, 25])
    FOLLOW_25_in_argument_expression_list1093 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_assignment_expression_in_argument_expression_list1095 = frozenset([1, 25])
    FOLLOW_multiplicative_expression_in_additive_expression1109 = frozenset([1, 56, 57])
    FOLLOW_56_in_additive_expression1113 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_multiplicative_expression_in_additive_expression1115 = frozenset([1, 56, 57])
    FOLLOW_57_in_additive_expression1119 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_multiplicative_expression_in_additive_expression1121 = frozenset([1, 56, 57])
    FOLLOW_cast_expression_in_multiplicative_expression1135 = frozenset([1, 54, 58, 59])
    FOLLOW_54_in_multiplicative_expression1139 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_cast_expression_in_multiplicative_expression1141 = frozenset([1, 54, 58, 59])
    FOLLOW_58_in_multiplicative_expression1145 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_cast_expression_in_multiplicative_expression1147 = frozenset([1, 54, 58, 59])
    FOLLOW_59_in_multiplicative_expression1151 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_cast_expression_in_multiplicative_expression1153 = frozenset([1, 54, 58, 59])
    FOLLOW_50_in_cast_expression1166 = frozenset([4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_type_name_in_cast_expression1168 = frozenset([51])
    FOLLOW_51_in_cast_expression1170 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_cast_expression_in_cast_expression1172 = frozenset([1])
    FOLLOW_unary_expression_in_cast_expression1177 = frozenset([1])
    FOLLOW_postfix_expression_in_unary_expression1188 = frozenset([1])
    FOLLOW_60_in_unary_expression1193 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_unary_expression_in_unary_expression1195 = frozenset([1])
    FOLLOW_61_in_unary_expression1200 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_unary_expression_in_unary_expression1202 = frozenset([1])
    FOLLOW_unary_operator_in_unary_expression1207 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_cast_expression_in_unary_expression1209 = frozenset([1])
    FOLLOW_62_in_unary_expression1214 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_unary_expression_in_unary_expression1216 = frozenset([1])
    FOLLOW_62_in_unary_expression1221 = frozenset([50])
    FOLLOW_50_in_unary_expression1223 = frozenset([4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_type_name_in_unary_expression1225 = frozenset([51])
    FOLLOW_51_in_unary_expression1227 = frozenset([1])
    FOLLOW_primary_expression_in_postfix_expression1240 = frozenset([1, 50, 52, 54, 60, 61, 63, 64])
    FOLLOW_52_in_postfix_expression1254 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_in_postfix_expression1256 = frozenset([53])
    FOLLOW_53_in_postfix_expression1258 = frozenset([1, 50, 52, 54, 60, 61, 63, 64])
    FOLLOW_50_in_postfix_expression1272 = frozenset([51])
    FOLLOW_51_in_postfix_expression1274 = frozenset([1, 50, 52, 54, 60, 61, 63, 64])
    FOLLOW_50_in_postfix_expression1288 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_argument_expression_list_in_postfix_expression1290 = frozenset([51])
    FOLLOW_51_in_postfix_expression1292 = frozenset([1, 50, 52, 54, 60, 61, 63, 64])
    FOLLOW_63_in_postfix_expression1306 = frozenset([4])
    FOLLOW_IDENTIFIER_in_postfix_expression1308 = frozenset([1, 50, 52, 54, 60, 61, 63, 64])
    FOLLOW_54_in_postfix_expression1322 = frozenset([4])
    FOLLOW_IDENTIFIER_in_postfix_expression1324 = frozenset([1, 50, 52, 54, 60, 61, 63, 64])
    FOLLOW_64_in_postfix_expression1338 = frozenset([4])
    FOLLOW_IDENTIFIER_in_postfix_expression1340 = frozenset([1, 50, 52, 54, 60, 61, 63, 64])
    FOLLOW_60_in_postfix_expression1354 = frozenset([1, 50, 52, 54, 60, 61, 63, 64])
    FOLLOW_61_in_postfix_expression1368 = frozenset([1, 50, 52, 54, 60, 61, 63, 64])
    FOLLOW_set_in_unary_operator0 = frozenset([1])
    FOLLOW_IDENTIFIER_in_primary_expression1426 = frozenset([1])
    FOLLOW_constant_in_primary_expression1431 = frozenset([1])
    FOLLOW_50_in_primary_expression1436 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_in_primary_expression1438 = frozenset([51])
    FOLLOW_51_in_primary_expression1440 = frozenset([1])
    FOLLOW_set_in_constant0 = frozenset([1])
    FOLLOW_assignment_expression_in_expression1518 = frozenset([1, 25])
    FOLLOW_25_in_expression1521 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_assignment_expression_in_expression1523 = frozenset([1, 25])
    FOLLOW_conditional_expression_in_constant_expression1536 = frozenset([1])
    FOLLOW_lvalue_in_assignment_expression1547 = frozenset([26, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77])
    FOLLOW_assignment_operator_in_assignment_expression1549 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_assignment_expression_in_assignment_expression1551 = frozenset([1])
    FOLLOW_conditional_expression_in_assignment_expression1556 = frozenset([1])
    FOLLOW_unary_expression_in_lvalue1568 = frozenset([1])
    FOLLOW_set_in_assignment_operator0 = frozenset([1])
    FOLLOW_logical_or_expression_in_conditional_expression1640 = frozenset([1, 78])
    FOLLOW_78_in_conditional_expression1643 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_in_conditional_expression1645 = frozenset([44])
    FOLLOW_44_in_conditional_expression1647 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_conditional_expression_in_conditional_expression1649 = frozenset([1])
    FOLLOW_logical_and_expression_in_logical_or_expression1662 = frozenset([1, 79])
    FOLLOW_79_in_logical_or_expression1665 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_logical_and_expression_in_logical_or_expression1667 = frozenset([1, 79])
    FOLLOW_inclusive_or_expression_in_logical_and_expression1680 = frozenset([1, 80])
    FOLLOW_80_in_logical_and_expression1683 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_inclusive_or_expression_in_logical_and_expression1685 = frozenset([1, 80])
    FOLLOW_exclusive_or_expression_in_inclusive_or_expression1698 = frozenset([1, 81])
    FOLLOW_81_in_inclusive_or_expression1701 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_exclusive_or_expression_in_inclusive_or_expression1703 = frozenset([1, 81])
    FOLLOW_and_expression_in_exclusive_or_expression1716 = frozenset([1, 82])
    FOLLOW_82_in_exclusive_or_expression1719 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_and_expression_in_exclusive_or_expression1721 = frozenset([1, 82])
    FOLLOW_equality_expression_in_and_expression1734 = frozenset([1, 65])
    FOLLOW_65_in_and_expression1737 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_equality_expression_in_and_expression1739 = frozenset([1, 65])
    FOLLOW_relational_expression_in_equality_expression1751 = frozenset([1, 83, 84])
    FOLLOW_set_in_equality_expression1754 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_relational_expression_in_equality_expression1760 = frozenset([1, 83, 84])
    FOLLOW_shift_expression_in_relational_expression1773 = frozenset([1, 85, 86, 87, 88])
    FOLLOW_set_in_relational_expression1776 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_shift_expression_in_relational_expression1786 = frozenset([1, 85, 86, 87, 88])
    FOLLOW_additive_expression_in_shift_expression1799 = frozenset([1, 89, 90])
    FOLLOW_set_in_shift_expression1802 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_additive_expression_in_shift_expression1808 = frozenset([1, 89, 90])
    FOLLOW_labeled_statement_in_statement1823 = frozenset([1])
    FOLLOW_compound_statement_in_statement1828 = frozenset([1])
    FOLLOW_expression_statement_in_statement1833 = frozenset([1])
    FOLLOW_selection_statement_in_statement1838 = frozenset([1])
    FOLLOW_iteration_statement_in_statement1843 = frozenset([1])
    FOLLOW_jump_statement_in_statement1848 = frozenset([1])
    FOLLOW_macro_statement_in_statement1853 = frozenset([1])
    FOLLOW_IDENTIFIER_in_macro_statement1864 = frozenset([50])
    FOLLOW_50_in_macro_statement1866 = frozenset([4, 5, 6, 7, 8, 9, 10, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 48, 49, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_IDENTIFIER_in_macro_statement1869 = frozenset([51])
    FOLLOW_statement_list_in_macro_statement1873 = frozenset([51])
    FOLLOW_declaration_in_macro_statement1877 = frozenset([51])
    FOLLOW_51_in_macro_statement1880 = frozenset([1])
    FOLLOW_IDENTIFIER_in_labeled_statement1892 = frozenset([44])
    FOLLOW_44_in_labeled_statement1894 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_statement_in_labeled_statement1896 = frozenset([1])
    FOLLOW_91_in_labeled_statement1901 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_constant_expression_in_labeled_statement1903 = frozenset([44])
    FOLLOW_44_in_labeled_statement1905 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_statement_in_labeled_statement1907 = frozenset([1])
    FOLLOW_92_in_labeled_statement1912 = frozenset([44])
    FOLLOW_44_in_labeled_statement1914 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_statement_in_labeled_statement1916 = frozenset([1])
    FOLLOW_40_in_compound_statement1938 = frozenset([4, 5, 6, 7, 8, 9, 10, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_declaration_in_compound_statement1940 = frozenset([4, 5, 6, 7, 8, 9, 10, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_statement_list_in_compound_statement1943 = frozenset([41])
    FOLLOW_41_in_compound_statement1946 = frozenset([1])
    FOLLOW_statement_in_statement_list1957 = frozenset([1, 4, 5, 6, 7, 8, 9, 10, 24, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_24_in_expression_statement1969 = frozenset([1])
    FOLLOW_expression_in_expression_statement1974 = frozenset([24])
    FOLLOW_24_in_expression_statement1976 = frozenset([1])
    FOLLOW_93_in_selection_statement1987 = frozenset([50])
    FOLLOW_50_in_selection_statement1989 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_in_selection_statement1991 = frozenset([51])
    FOLLOW_51_in_selection_statement1993 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_statement_in_selection_statement1995 = frozenset([1, 94])
    FOLLOW_94_in_selection_statement2010 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_statement_in_selection_statement2012 = frozenset([1])
    FOLLOW_95_in_selection_statement2019 = frozenset([50])
    FOLLOW_50_in_selection_statement2021 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_in_selection_statement2023 = frozenset([51])
    FOLLOW_51_in_selection_statement2025 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_statement_in_selection_statement2027 = frozenset([1])
    FOLLOW_96_in_iteration_statement2038 = frozenset([50])
    FOLLOW_50_in_iteration_statement2040 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_in_iteration_statement2042 = frozenset([51])
    FOLLOW_51_in_iteration_statement2044 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_statement_in_iteration_statement2046 = frozenset([1])
    FOLLOW_97_in_iteration_statement2051 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_statement_in_iteration_statement2053 = frozenset([96])
    FOLLOW_96_in_iteration_statement2055 = frozenset([50])
    FOLLOW_50_in_iteration_statement2057 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_in_iteration_statement2059 = frozenset([51])
    FOLLOW_51_in_iteration_statement2061 = frozenset([24])
    FOLLOW_24_in_iteration_statement2063 = frozenset([1])
    FOLLOW_98_in_iteration_statement2068 = frozenset([50])
    FOLLOW_50_in_iteration_statement2070 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_statement_in_iteration_statement2072 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_statement_in_iteration_statement2074 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 51, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_in_iteration_statement2076 = frozenset([51])
    FOLLOW_51_in_iteration_statement2079 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102])
    FOLLOW_statement_in_iteration_statement2081 = frozenset([1])
    FOLLOW_99_in_jump_statement2092 = frozenset([4])
    FOLLOW_IDENTIFIER_in_jump_statement2094 = frozenset([24])
    FOLLOW_24_in_jump_statement2096 = frozenset([1])
    FOLLOW_100_in_jump_statement2101 = frozenset([24])
    FOLLOW_24_in_jump_statement2103 = frozenset([1])
    FOLLOW_101_in_jump_statement2108 = frozenset([24])
    FOLLOW_24_in_jump_statement2110 = frozenset([1])
    FOLLOW_102_in_jump_statement2115 = frozenset([24])
    FOLLOW_24_in_jump_statement2117 = frozenset([1])
    FOLLOW_102_in_jump_statement2122 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_expression_in_jump_statement2124 = frozenset([24])
    FOLLOW_24_in_jump_statement2126 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred2104 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred4104 = frozenset([4, 50, 54])
    FOLLOW_declarator_in_synpred4107 = frozenset([4, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_declaration_in_synpred4109 = frozenset([4, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_40_in_synpred4112 = frozenset([1])
    FOLLOW_declaration_in_synpred5122 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred6153 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred9202 = frozenset([1])
    FOLLOW_type_specifier_in_synpred13250 = frozenset([1])
    FOLLOW_IDENTIFIER_in_synpred31411 = frozenset([4, 50, 54])
    FOLLOW_declarator_in_synpred31413 = frozenset([1])
    FOLLOW_type_specifier_in_synpred37548 = frozenset([1])
    FOLLOW_pointer_in_synpred49711 = frozenset([4, 50])
    FOLLOW_direct_declarator_in_synpred49714 = frozenset([1])
    FOLLOW_declarator_suffix_in_synpred50734 = frozenset([1])
    FOLLOW_declarator_suffix_in_synpred52751 = frozenset([1])
    FOLLOW_50_in_synpred55791 = frozenset([4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_parameter_type_list_in_synpred55793 = frozenset([51])
    FOLLOW_51_in_synpred55795 = frozenset([1])
    FOLLOW_50_in_synpred56805 = frozenset([4])
    FOLLOW_identifier_list_in_synpred56807 = frozenset([51])
    FOLLOW_51_in_synpred56809 = frozenset([1])
    FOLLOW_type_qualifier_in_synpred57834 = frozenset([1])
    FOLLOW_pointer_in_synpred58837 = frozenset([1])
    FOLLOW_54_in_synpred59832 = frozenset([46, 47, 48, 49])
    FOLLOW_type_qualifier_in_synpred59834 = frozenset([1, 46, 47, 48, 49, 54])
    FOLLOW_pointer_in_synpred59837 = frozenset([1])
    FOLLOW_54_in_synpred60843 = frozenset([54])
    FOLLOW_pointer_in_synpred60845 = frozenset([1])
    FOLLOW_declarator_in_synpred63900 = frozenset([1])
    FOLLOW_abstract_declarator_in_synpred64902 = frozenset([1])
    FOLLOW_specifier_qualifier_list_in_synpred67941 = frozenset([1, 50, 52, 54])
    FOLLOW_abstract_declarator_in_synpred67943 = frozenset([1])
    FOLLOW_direct_abstract_declarator_in_synpred68962 = frozenset([1])
    FOLLOW_abstract_declarator_suffix_in_synpred71993 = frozenset([1])
    FOLLOW_50_in_synpred841166 = frozenset([4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 49])
    FOLLOW_type_name_in_synpred841168 = frozenset([51])
    FOLLOW_51_in_synpred841170 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_cast_expression_in_synpred841172 = frozenset([1])
    FOLLOW_62_in_synpred891214 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_unary_expression_in_synpred891216 = frozenset([1])
    FOLLOW_54_in_synpred941322 = frozenset([4])
    FOLLOW_IDENTIFIER_in_synpred941324 = frozenset([1])
    FOLLOW_lvalue_in_synpred1111547 = frozenset([26, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77])
    FOLLOW_assignment_operator_in_synpred1111549 = frozenset([4, 5, 6, 7, 8, 9, 10, 50, 54, 56, 57, 60, 61, 62, 65, 66, 67])
    FOLLOW_assignment_expression_in_synpred1111551 = frozenset([1])
    FOLLOW_expression_statement_in_synpred1381833 = frozenset([1])
    FOLLOW_statement_list_in_synpred1431873 = frozenset([1])
    FOLLOW_declaration_in_synpred1461940 = frozenset([1])


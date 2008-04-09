# $ANTLR 3.0.1 H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g 2008-04-09 15:15:35

from antlr3 import *
from antlr3.compat import set, frozenset
         
from Common.BuildToolError import *
from Common import EdkLogger as EdkLogger



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
OpCode=6
Letter=10
GuidName=4
AlphaNumeric=11
WS=9
EOF=-1
Hex=5
Whitespace=8
COMMENT=7

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "GuidName", "Hex", "OpCode", "COMMENT", "Whitespace", "WS", "Letter", 
    "AlphaNumeric", "'DEPENDENCY_START'", "'END'", "'DEPENDENCY_END'", "'BEFORE'", 
    "'AFTER'", "'SOR'", "'AND'", "'OR'", "'TRUE'", "'FALSE'", "'NOT'", "'('", 
    "')'", "'{'", "','", "'}'"
]



class DepexParser(Parser):
    grammarFileName = "H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g"
    tokenNames = tokenNames

    def __init__(self, input):
        Parser.__init__(self, input)


               
        self._DepexFile = ''
        self._ExclusiveOpcode = ["BEFORE", "AFTER"]
        self._AboveAllOpcode = ["SOR", "BEFORE", "AFTER"]
        self._ExpressionType = -1
        self._Parentheses = 0
        self.PostfixNotation = []
        self.TokenList = [t.text for t in self.input.tokens]
        self.OpcodeList = []
        self._DepexString = ' '.join(self.TokenList)


                


              
    EXPRESSION_BEFORE = 0
    EXPRESSION_AFTER = 1
    EXPRESSION_SOR = 2
    EXPRESSION_BOOL = 3



    # $ANTLR start start
    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:41:1: start[FilePath] : depex_expression ;
    def start(self, FilePath):

        self._DepexFile=FilePath
        try:
            try:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:43:5: ( depex_expression )
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:43:7: depex_expression
                self.following.append(self.FOLLOW_depex_expression_in_start64)
                self.depex_expression()
                self.following.pop()

                #action start
                 
                # there should be no more tokens left
                if self.input.LT(1).text != None:
                    raise RecognitionException("Ending error")
                if self.PostfixNotation[-1] != 'END':
                    self.PostfixNotation.append('END')

                #action end




            except RecognitionException, e:
                                                 
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
                    Msg = "Unnecessary expression after [%s]" % LastToken
                elif NextToken in ['SOR', 'BEFORE', 'AFTER']:
                    Msg = "[%s] is not expected." % NextToken
                elif NextToken in ['AND', 'OR']:
                    Msg = "Missing operand near [%s]" % NextToken
                elif NextToken in [')', '(']:
                    Msg = "Parentheses mismatched"
                else:
                    Msg = "Missing opcode or operand between [%s] and [%s]" % (LastToken, NextToken)
                EdkLogger.error("GenDepex", PARAMETER_INVALID, Msg, ExtraData=self._DepexString, File=self._DepexFile)


            except :
                          
                raise


        finally:

            pass

        return 

    # $ANTLR end start


    # $ANTLR start depex_expression
    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:79:1: depex_expression : ( 'DEPENDENCY_START' )? ( before_expression | after_expression | sor_expression | bool_expression ) ( 'END' )? ( 'DEPENDENCY_END' )? ;
    def depex_expression(self, ):

        try:
            try:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:80:5: ( ( 'DEPENDENCY_START' )? ( before_expression | after_expression | sor_expression | bool_expression ) ( 'END' )? ( 'DEPENDENCY_END' )? )
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:80:9: ( 'DEPENDENCY_START' )? ( before_expression | after_expression | sor_expression | bool_expression ) ( 'END' )? ( 'DEPENDENCY_END' )?
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:80:9: ( 'DEPENDENCY_START' )?
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if (LA1_0 == 12) :
                    alt1 = 1
                if alt1 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:80:9: 'DEPENDENCY_START'
                    self.match(self.input, 12, self.FOLLOW_12_in_depex_expression97)




                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:81:6: ( before_expression | after_expression | sor_expression | bool_expression )
                alt2 = 4
                LA2 = self.input.LA(1)
                if LA2 == 15:
                    alt2 = 1
                elif LA2 == 16:
                    alt2 = 2
                elif LA2 == 17:
                    alt2 = 3
                elif LA2 == GuidName or LA2 == 20 or LA2 == 21 or LA2 == 22 or LA2 == 23 or LA2 == 25:
                    alt2 = 4
                else:
                    nvae = NoViableAltException("81:6: ( before_expression | after_expression | sor_expression | bool_expression )", 2, 0, self.input)

                    raise nvae

                if alt2 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:81:7: before_expression
                    self.following.append(self.FOLLOW_before_expression_in_depex_expression106)
                    self.before_expression()
                    self.following.pop()



                elif alt2 == 2:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:81:25: after_expression
                    self.following.append(self.FOLLOW_after_expression_in_depex_expression108)
                    self.after_expression()
                    self.following.pop()



                elif alt2 == 3:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:81:42: sor_expression
                    self.following.append(self.FOLLOW_sor_expression_in_depex_expression110)
                    self.sor_expression()
                    self.following.pop()



                elif alt2 == 4:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:81:57: bool_expression
                    self.following.append(self.FOLLOW_bool_expression_in_depex_expression112)
                    self.bool_expression()
                    self.following.pop()




                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:82:6: ( 'END' )?
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if (LA3_0 == 13) :
                    alt3 = 1
                if alt3 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:82:6: 'END'
                    self.match(self.input, 13, self.FOLLOW_13_in_depex_expression120)




                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:83:6: ( 'DEPENDENCY_END' )?
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if (LA4_0 == 14) :
                    alt4 = 1
                if alt4 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:83:6: 'DEPENDENCY_END'
                    self.match(self.input, 14, self.FOLLOW_14_in_depex_expression128)








                        
            except BaseException,e:
                raise
        finally:

            pass

        return 

    # $ANTLR end depex_expression


    # $ANTLR start before_expression
    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:86:1: before_expression : Op= 'BEFORE' V= guid ;
    def before_expression(self, ):

        Op = None
        V = None


        try:
            try:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:87:5: (Op= 'BEFORE' V= guid )
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:87:10: Op= 'BEFORE' V= guid
                Op = self.input.LT(1)
                self.match(self.input, 15, self.FOLLOW_15_in_before_expression151)

                self.following.append(self.FOLLOW_guid_in_before_expression155)
                V = self.guid()
                self.following.pop()

                #action start
                                             
                self.PostfixNotation.append(Op.text)
                self.PostfixNotation.append(V)
                self.OpcodeList.append(Op.text)
                self._ExpressionType = self.EXPRESSION_BEFORE

                #action end




                        
            except BaseException,e:
                raise
        finally:

            pass

        return 

    # $ANTLR end before_expression


    # $ANTLR start after_expression
    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:95:1: after_expression : Op= 'AFTER' V= guid ;
    def after_expression(self, ):

        Op = None
        V = None


        try:
            try:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:96:5: (Op= 'AFTER' V= guid )
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:96:10: Op= 'AFTER' V= guid
                Op = self.input.LT(1)
                self.match(self.input, 16, self.FOLLOW_16_in_after_expression179)

                self.following.append(self.FOLLOW_guid_in_after_expression183)
                V = self.guid()
                self.following.pop()

                #action start
                 
                self.PostfixNotation.append(Op.text)
                self.PostfixNotation.append(V)
                self.OpcodeList.append(Op.text)
                self._ExpressionType = self.EXPRESSION_AFTER

                #action end




                        
            except BaseException,e:
                raise
        finally:

            pass

        return 

    # $ANTLR end after_expression


    # $ANTLR start sor_expression
    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:105:1: sor_expression : Op= 'SOR' Expr= bool_statement ;
    def sor_expression(self, ):

        Op = None
        Expr = None


        try:
            try:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:106:5: (Op= 'SOR' Expr= bool_statement )
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:106:10: Op= 'SOR' Expr= bool_statement
                Op = self.input.LT(1)
                self.match(self.input, 17, self.FOLLOW_17_in_sor_expression207)

                self.following.append(self.FOLLOW_bool_statement_in_sor_expression211)
                Expr = self.bool_statement()
                self.following.pop()

                #action start
                 
                self.PostfixNotation.append(Op.text)
                self.PostfixNotation.extend(Expr)
                self.OpcodeList.append(Op.text)
                self._ExpressionType = self.EXPRESSION_SOR

                #action end




                        
            except BaseException,e:
                raise
        finally:

            pass

        return 

    # $ANTLR end sor_expression


    # $ANTLR start bool_expression
    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:115:1: bool_expression : Expr= bool_statement ;
    def bool_expression(self, ):

        Expr = None


        try:
            try:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:116:5: (Expr= bool_statement )
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:116:10: Expr= bool_statement
                self.following.append(self.FOLLOW_bool_statement_in_bool_expression239)
                Expr = self.bool_statement()
                self.following.pop()

                #action start
                 
                self.PostfixNotation.extend(Expr)
                self._ExpressionType = self.EXPRESSION_BOOL

                #action end




                        
            except BaseException,e:
                raise
        finally:

            pass

        return 

    # $ANTLR end bool_expression


    # $ANTLR start bool_statement
    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:123:1: bool_statement returns [ExpressionList] : SubExpr= bool_factor ( 'AND' SubExpr= bool_statement | 'OR' SubExpr= bool_statement )* ;
    def bool_statement(self, ):

        ExpressionList = None

        SubExpr = None


               
        ExpressionList=[]

        try:
            try:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:126:3: (SubExpr= bool_factor ( 'AND' SubExpr= bool_statement | 'OR' SubExpr= bool_statement )* )
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:127:5: SubExpr= bool_factor ( 'AND' SubExpr= bool_statement | 'OR' SubExpr= bool_statement )*
                self.following.append(self.FOLLOW_bool_factor_in_bool_statement269)
                SubExpr = self.bool_factor()
                self.following.pop()

                #action start
                ExpressionList.extend(SubExpr)
                #action end
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:128:5: ( 'AND' SubExpr= bool_statement | 'OR' SubExpr= bool_statement )*
                while True: #loop5
                    alt5 = 3
                    LA5_0 = self.input.LA(1)

                    if (LA5_0 == 18) :
                        alt5 = 1
                    elif (LA5_0 == 19) :
                        alt5 = 2


                    if alt5 == 1:
                        # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:128:10: 'AND' SubExpr= bool_statement
                        self.match(self.input, 18, self.FOLLOW_18_in_bool_statement282)

                        self.following.append(self.FOLLOW_bool_statement_in_bool_statement286)
                        SubExpr = self.bool_statement()
                        self.following.pop()

                        #action start
                        ExpressionList.extend(SubExpr);ExpressionList.append('AND');self.OpcodeList.append('AND')
                        #action end


                    elif alt5 == 2:
                        # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:129:10: 'OR' SubExpr= bool_statement
                        self.match(self.input, 19, self.FOLLOW_19_in_bool_statement299)

                        self.following.append(self.FOLLOW_bool_statement_in_bool_statement303)
                        SubExpr = self.bool_statement()
                        self.following.pop()

                        #action start
                        ExpressionList.extend(SubExpr);ExpressionList.append('OR');self.OpcodeList.append('OR')
                        #action end


                    else:
                        break #loop5






                        
            except BaseException,e:
                raise
        finally:

            pass

        return ExpressionList

    # $ANTLR end bool_statement


    # $ANTLR start bool_factor
    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:133:1: bool_factor returns [ExpressionList] : (Bl= 'TRUE' | Bl= 'FALSE' | Op= 'NOT' Be= bool_statement | ( '(' ) Be= bool_statement ( ')' ) | V= guid );
    def bool_factor(self, ):

        ExpressionList = None

        Bl = None
        Op = None
        Be = None

        V = None


               
        ExpressionList=[]

        try:
            try:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:136:3: (Bl= 'TRUE' | Bl= 'FALSE' | Op= 'NOT' Be= bool_statement | ( '(' ) Be= bool_statement ( ')' ) | V= guid )
                alt6 = 5
                LA6 = self.input.LA(1)
                if LA6 == 20:
                    alt6 = 1
                elif LA6 == 21:
                    alt6 = 2
                elif LA6 == 22:
                    alt6 = 3
                elif LA6 == 23:
                    alt6 = 4
                elif LA6 == GuidName or LA6 == 25:
                    alt6 = 5
                else:
                    nvae = NoViableAltException("133:1: bool_factor returns [ExpressionList] : (Bl= 'TRUE' | Bl= 'FALSE' | Op= 'NOT' Be= bool_statement | ( '(' ) Be= bool_statement ( ')' ) | V= guid );", 6, 0, self.input)

                    raise nvae

                if alt6 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:137:9: Bl= 'TRUE'
                    Bl = self.input.LT(1)
                    self.match(self.input, 20, self.FOLLOW_20_in_bool_factor340)

                    #action start
                    ExpressionList.append(Bl.text)
                    #action end


                elif alt6 == 2:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:138:10: Bl= 'FALSE'
                    Bl = self.input.LT(1)
                    self.match(self.input, 21, self.FOLLOW_21_in_bool_factor355)

                    #action start
                    ExpressionList.append(Bl.text)
                    #action end


                elif alt6 == 3:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:139:10: Op= 'NOT' Be= bool_statement
                    Op = self.input.LT(1)
                    self.match(self.input, 22, self.FOLLOW_22_in_bool_factor370)

                    self.following.append(self.FOLLOW_bool_statement_in_bool_factor374)
                    Be = self.bool_statement()
                    self.following.pop()

                    #action start
                    ExpressionList.extend(Be);ExpressionList.append(Op.text)
                    #action end


                elif alt6 == 4:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:140:10: ( '(' ) Be= bool_statement ( ')' )
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:140:10: ( '(' )
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:140:12: '('
                    self.match(self.input, 23, self.FOLLOW_23_in_bool_factor389)

                    #action start
                    self._Parentheses+=1
                    #action end



                    self.following.append(self.FOLLOW_bool_statement_in_bool_factor397)
                    Be = self.bool_statement()
                    self.following.pop()

                    #action start
                    ExpressionList.extend(Be)
                    #action end
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:140:87: ( ')' )
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:140:89: ')'
                    self.match(self.input, 24, self.FOLLOW_24_in_bool_factor403)

                    #action start
                    self._Parentheses-=1
                    #action end





                elif alt6 == 5:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:141:10: V= guid
                    self.following.append(self.FOLLOW_guid_in_bool_factor420)
                    V = self.guid()
                    self.following.pop()

                    #action start
                    ExpressionList.append('PUSH');ExpressionList.append(V)
                    #action end



                        
            except BaseException,e:
                raise
        finally:

            pass

        return ExpressionList

    # $ANTLR end bool_factor


    # $ANTLR start guid
    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:144:1: guid returns [GuidValue] : ( GuidName | guid_value );
    def guid(self, ):

        GuidValue = None

        GuidName1 = None
        guid_value2 = None


               
        GuidValue = None

        try:
            try:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:147:3: ( GuidName | guid_value )
                alt7 = 2
                LA7_0 = self.input.LA(1)

                if (LA7_0 == GuidName) :
                    alt7 = 1
                elif (LA7_0 == 25) :
                    alt7 = 2
                else:
                    nvae = NoViableAltException("144:1: guid returns [GuidValue] : ( GuidName | guid_value );", 7, 0, self.input)

                    raise nvae

                if alt7 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:148:5: GuidName
                    GuidName1 = self.input.LT(1)
                    self.match(self.input, GuidName, self.FOLLOW_GuidName_in_guid452)

                    #action start
                     
                    EdkLogger.error("GenDepex", RESOURCE_NOT_AVAILABLE, "Value of GUID [%s] is not available" % GuidName1.text, ExtraData=self._DepexString, File=self._DepexFile)

                    #action end


                elif alt7 == 2:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:152:10: guid_value
                    self.following.append(self.FOLLOW_guid_value_in_guid465)
                    guid_value2 = self.guid_value()
                    self.following.pop()

                    #action start
                     
                    GuidValue=self.input.toString(guid_value2.start,guid_value2.stop)

                    #action end



                        
            except BaseException,e:
                raise
        finally:

            pass

        return GuidValue

    # $ANTLR end guid

    class guid_value_return(object):
        def __init__(self):
            self.start = None
            self.stop = None



    # $ANTLR start guid_value
    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:158:1: guid_value : '{' Hex ',' Hex ',' Hex ',' ( '{' )? Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ( '}' )? '}' ;
    def guid_value(self, ):

        retval = self.guid_value_return()
        retval.start = self.input.LT(1)

        try:
            try:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:159:5: ( '{' Hex ',' Hex ',' Hex ',' ( '{' )? Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ( '}' )? '}' )
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:159:10: '{' Hex ',' Hex ',' Hex ',' ( '{' )? Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ',' Hex ( '}' )? '}'
                self.match(self.input, 25, self.FOLLOW_25_in_guid_value487)

                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value489)

                self.match(self.input, 26, self.FOLLOW_26_in_guid_value491)

                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value493)

                self.match(self.input, 26, self.FOLLOW_26_in_guid_value495)

                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value497)

                self.match(self.input, 26, self.FOLLOW_26_in_guid_value499)

                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:159:38: ( '{' )?
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if (LA8_0 == 25) :
                    alt8 = 1
                if alt8 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:159:38: '{'
                    self.match(self.input, 25, self.FOLLOW_25_in_guid_value501)




                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value504)

                self.match(self.input, 26, self.FOLLOW_26_in_guid_value506)

                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value508)

                self.match(self.input, 26, self.FOLLOW_26_in_guid_value510)

                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value512)

                self.match(self.input, 26, self.FOLLOW_26_in_guid_value514)

                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value516)

                self.match(self.input, 26, self.FOLLOW_26_in_guid_value518)

                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value520)

                self.match(self.input, 26, self.FOLLOW_26_in_guid_value522)

                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value524)

                self.match(self.input, 26, self.FOLLOW_26_in_guid_value526)

                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value528)

                self.match(self.input, 26, self.FOLLOW_26_in_guid_value530)

                self.match(self.input, Hex, self.FOLLOW_Hex_in_guid_value532)

                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:159:103: ( '}' )?
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if (LA9_0 == 27) :
                    LA9_1 = self.input.LA(2)

                    if (LA9_1 == 27) :
                        alt9 = 1
                if alt9 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:159:103: '}'
                    self.match(self.input, 27, self.FOLLOW_27_in_guid_value534)




                self.match(self.input, 27, self.FOLLOW_27_in_guid_value537)




                retval.stop = self.input.LT(-1)


                        
            except BaseException,e:
                raise
        finally:

            pass

        return retval

    # $ANTLR end guid_value


 

    FOLLOW_depex_expression_in_start64 = frozenset([1])
    FOLLOW_12_in_depex_expression97 = frozenset([4, 15, 16, 17, 20, 21, 22, 23, 25])
    FOLLOW_before_expression_in_depex_expression106 = frozenset([1, 13, 14])
    FOLLOW_after_expression_in_depex_expression108 = frozenset([1, 13, 14])
    FOLLOW_sor_expression_in_depex_expression110 = frozenset([1, 13, 14])
    FOLLOW_bool_expression_in_depex_expression112 = frozenset([1, 13, 14])
    FOLLOW_13_in_depex_expression120 = frozenset([1, 14])
    FOLLOW_14_in_depex_expression128 = frozenset([1])
    FOLLOW_15_in_before_expression151 = frozenset([4, 25])
    FOLLOW_guid_in_before_expression155 = frozenset([1])
    FOLLOW_16_in_after_expression179 = frozenset([4, 25])
    FOLLOW_guid_in_after_expression183 = frozenset([1])
    FOLLOW_17_in_sor_expression207 = frozenset([4, 20, 21, 22, 23, 25])
    FOLLOW_bool_statement_in_sor_expression211 = frozenset([1])
    FOLLOW_bool_statement_in_bool_expression239 = frozenset([1])
    FOLLOW_bool_factor_in_bool_statement269 = frozenset([1, 18, 19])
    FOLLOW_18_in_bool_statement282 = frozenset([4, 20, 21, 22, 23, 25])
    FOLLOW_bool_statement_in_bool_statement286 = frozenset([1, 18, 19])
    FOLLOW_19_in_bool_statement299 = frozenset([4, 20, 21, 22, 23, 25])
    FOLLOW_bool_statement_in_bool_statement303 = frozenset([1, 18, 19])
    FOLLOW_20_in_bool_factor340 = frozenset([1])
    FOLLOW_21_in_bool_factor355 = frozenset([1])
    FOLLOW_22_in_bool_factor370 = frozenset([4, 20, 21, 22, 23, 25])
    FOLLOW_bool_statement_in_bool_factor374 = frozenset([1])
    FOLLOW_23_in_bool_factor389 = frozenset([4, 20, 21, 22, 23, 25])
    FOLLOW_bool_statement_in_bool_factor397 = frozenset([24])
    FOLLOW_24_in_bool_factor403 = frozenset([1])
    FOLLOW_guid_in_bool_factor420 = frozenset([1])
    FOLLOW_GuidName_in_guid452 = frozenset([1])
    FOLLOW_guid_value_in_guid465 = frozenset([1])
    FOLLOW_25_in_guid_value487 = frozenset([5])
    FOLLOW_Hex_in_guid_value489 = frozenset([26])
    FOLLOW_26_in_guid_value491 = frozenset([5])
    FOLLOW_Hex_in_guid_value493 = frozenset([26])
    FOLLOW_26_in_guid_value495 = frozenset([5])
    FOLLOW_Hex_in_guid_value497 = frozenset([26])
    FOLLOW_26_in_guid_value499 = frozenset([5, 25])
    FOLLOW_25_in_guid_value501 = frozenset([5])
    FOLLOW_Hex_in_guid_value504 = frozenset([26])
    FOLLOW_26_in_guid_value506 = frozenset([5])
    FOLLOW_Hex_in_guid_value508 = frozenset([26])
    FOLLOW_26_in_guid_value510 = frozenset([5])
    FOLLOW_Hex_in_guid_value512 = frozenset([26])
    FOLLOW_26_in_guid_value514 = frozenset([5])
    FOLLOW_Hex_in_guid_value516 = frozenset([26])
    FOLLOW_26_in_guid_value518 = frozenset([5])
    FOLLOW_Hex_in_guid_value520 = frozenset([26])
    FOLLOW_26_in_guid_value522 = frozenset([5])
    FOLLOW_Hex_in_guid_value524 = frozenset([26])
    FOLLOW_26_in_guid_value526 = frozenset([5])
    FOLLOW_Hex_in_guid_value528 = frozenset([26])
    FOLLOW_26_in_guid_value530 = frozenset([5])
    FOLLOW_Hex_in_guid_value532 = frozenset([27])
    FOLLOW_27_in_guid_value534 = frozenset([27])
    FOLLOW_27_in_guid_value537 = frozenset([1])


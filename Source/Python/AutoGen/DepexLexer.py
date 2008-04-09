# $ANTLR 3.0.1 H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g 2008-04-09 15:15:36

from antlr3 import *
from antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
T21=21
T14=14
GuidName=4
T22=22
AlphaNumeric=11
WS=9
Hex=5
T12=12
T23=23
COMMENT=7
T13=13
T20=20
OpCode=6
T25=25
Letter=10
T18=18
T26=26
T15=15
EOF=-1
Whitespace=8
T17=17
Tokens=28
T16=16
T27=27
T24=24
T19=19

class DepexLexer(Lexer):

    grammarFileName = "H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g"

    def __init__(self, input=None):
        Lexer.__init__(self, input)





    # $ANTLR start T12
    def mT12(self, ):

        try:
            self.type = T12

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:7:5: ( 'DEPENDENCY_START' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:7:7: 'DEPENDENCY_START'
            self.match("DEPENDENCY_START")






        finally:

            pass

    # $ANTLR end T12



    # $ANTLR start T13
    def mT13(self, ):

        try:
            self.type = T13

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:8:5: ( 'END' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:8:7: 'END'
            self.match("END")






        finally:

            pass

    # $ANTLR end T13



    # $ANTLR start T14
    def mT14(self, ):

        try:
            self.type = T14

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:9:5: ( 'DEPENDENCY_END' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:9:7: 'DEPENDENCY_END'
            self.match("DEPENDENCY_END")






        finally:

            pass

    # $ANTLR end T14



    # $ANTLR start T15
    def mT15(self, ):

        try:
            self.type = T15

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:10:5: ( 'BEFORE' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:10:7: 'BEFORE'
            self.match("BEFORE")






        finally:

            pass

    # $ANTLR end T15



    # $ANTLR start T16
    def mT16(self, ):

        try:
            self.type = T16

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:11:5: ( 'AFTER' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:11:7: 'AFTER'
            self.match("AFTER")






        finally:

            pass

    # $ANTLR end T16



    # $ANTLR start T17
    def mT17(self, ):

        try:
            self.type = T17

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:12:5: ( 'SOR' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:12:7: 'SOR'
            self.match("SOR")






        finally:

            pass

    # $ANTLR end T17



    # $ANTLR start T18
    def mT18(self, ):

        try:
            self.type = T18

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:13:5: ( 'AND' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:13:7: 'AND'
            self.match("AND")






        finally:

            pass

    # $ANTLR end T18



    # $ANTLR start T19
    def mT19(self, ):

        try:
            self.type = T19

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:14:5: ( 'OR' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:14:7: 'OR'
            self.match("OR")






        finally:

            pass

    # $ANTLR end T19



    # $ANTLR start T20
    def mT20(self, ):

        try:
            self.type = T20

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:15:5: ( 'TRUE' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:15:7: 'TRUE'
            self.match("TRUE")






        finally:

            pass

    # $ANTLR end T20



    # $ANTLR start T21
    def mT21(self, ):

        try:
            self.type = T21

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:16:5: ( 'FALSE' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:16:7: 'FALSE'
            self.match("FALSE")






        finally:

            pass

    # $ANTLR end T21



    # $ANTLR start T22
    def mT22(self, ):

        try:
            self.type = T22

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:17:5: ( 'NOT' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:17:7: 'NOT'
            self.match("NOT")






        finally:

            pass

    # $ANTLR end T22



    # $ANTLR start T23
    def mT23(self, ):

        try:
            self.type = T23

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:18:5: ( '(' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:18:7: '('
            self.match(u'(')





        finally:

            pass

    # $ANTLR end T23



    # $ANTLR start T24
    def mT24(self, ):

        try:
            self.type = T24

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:19:5: ( ')' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:19:7: ')'
            self.match(u')')





        finally:

            pass

    # $ANTLR end T24



    # $ANTLR start T25
    def mT25(self, ):

        try:
            self.type = T25

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:20:5: ( '{' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:20:7: '{'
            self.match(u'{')





        finally:

            pass

    # $ANTLR end T25



    # $ANTLR start T26
    def mT26(self, ):

        try:
            self.type = T26

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:21:5: ( ',' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:21:7: ','
            self.match(u',')





        finally:

            pass

    # $ANTLR end T26



    # $ANTLR start T27
    def mT27(self, ):

        try:
            self.type = T27

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:22:5: ( '}' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:22:7: '}'
            self.match(u'}')





        finally:

            pass

    # $ANTLR end T27



    # $ANTLR start OpCode
    def mOpCode(self, ):

        try:
            self.type = OpCode

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:165:5: ( 'BEFORE' | 'AFTER' | 'SOR' | 'TRUE' | 'FALSE' | 'AND' | 'OR' | 'NOT' | 'PUSH' | 'END' )
            alt1 = 10
            LA1 = self.input.LA(1)
            if LA1 == u'B':
                alt1 = 1
            elif LA1 == u'A':
                LA1_2 = self.input.LA(2)

                if (LA1_2 == u'F') :
                    alt1 = 2
                elif (LA1_2 == u'N') :
                    alt1 = 6
                else:
                    nvae = NoViableAltException("164:1: OpCode : ( 'BEFORE' | 'AFTER' | 'SOR' | 'TRUE' | 'FALSE' | 'AND' | 'OR' | 'NOT' | 'PUSH' | 'END' );", 1, 2, self.input)

                    raise nvae

            elif LA1 == u'S':
                alt1 = 3
            elif LA1 == u'T':
                alt1 = 4
            elif LA1 == u'F':
                alt1 = 5
            elif LA1 == u'O':
                alt1 = 7
            elif LA1 == u'N':
                alt1 = 8
            elif LA1 == u'P':
                alt1 = 9
            elif LA1 == u'E':
                alt1 = 10
            else:
                nvae = NoViableAltException("164:1: OpCode : ( 'BEFORE' | 'AFTER' | 'SOR' | 'TRUE' | 'FALSE' | 'AND' | 'OR' | 'NOT' | 'PUSH' | 'END' );", 1, 0, self.input)

                raise nvae

            if alt1 == 1:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:165:10: 'BEFORE'
                self.match("BEFORE")




            elif alt1 == 2:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:166:10: 'AFTER'
                self.match("AFTER")




            elif alt1 == 3:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:167:10: 'SOR'
                self.match("SOR")




            elif alt1 == 4:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:168:10: 'TRUE'
                self.match("TRUE")




            elif alt1 == 5:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:169:10: 'FALSE'
                self.match("FALSE")




            elif alt1 == 6:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:170:10: 'AND'
                self.match("AND")




            elif alt1 == 7:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:171:10: 'OR'
                self.match("OR")




            elif alt1 == 8:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:172:10: 'NOT'
                self.match("NOT")




            elif alt1 == 9:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:173:10: 'PUSH'
                self.match("PUSH")




            elif alt1 == 10:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:174:10: 'END'
                self.match("END")





        finally:

            pass

    # $ANTLR end OpCode



    # $ANTLR start COMMENT
    def mCOMMENT(self, ):

        try:
            self.type = COMMENT

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:178:5: ( '#' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:178:10: '#' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
            self.match(u'#')

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:178:14: (~ ( '\\n' | '\\r' ) )*
            while True: #loop2
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if ((u'\u0000' <= LA2_0 <= u'\t') or (u'\u000B' <= LA2_0 <= u'\f') or (u'\u000E' <= LA2_0 <= u'\uFFFE')) :
                    alt2 = 1


                if alt2 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:178:14: ~ ( '\\n' | '\\r' )
                    if (u'\u0000' <= self.input.LA(1) <= u'\t') or (u'\u000B' <= self.input.LA(1) <= u'\f') or (u'\u000E' <= self.input.LA(1) <= u'\uFFFE'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop2


            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:178:28: ( '\\r' )?
            alt3 = 2
            LA3_0 = self.input.LA(1)

            if (LA3_0 == u'\r') :
                alt3 = 1
            if alt3 == 1:
                # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:178:28: '\\r'
                self.match(u'\r')




            self.match(u'\n')

            #action start
            self.skip()
            #action end




        finally:

            pass

    # $ANTLR end COMMENT



    # $ANTLR start WS
    def mWS(self, ):

        try:
            self.type = WS

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:180:7: ( Whitespace )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:180:12: Whitespace
            self.mWhitespace()

            #action start
            self.skip()
            #action end




        finally:

            pass

    # $ANTLR end WS



    # $ANTLR start GuidName
    def mGuidName(self, ):

        try:
            self.type = GuidName

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:183:5: ( ( Letter | '_' ) ( AlphaNumeric | '_' )* )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:183:10: ( Letter | '_' ) ( AlphaNumeric | '_' )*
            if (u'A' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'_' or (u'a' <= self.input.LA(1) <= u'z'):
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse


            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:183:23: ( AlphaNumeric | '_' )*
            while True: #loop4
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if ((u'0' <= LA4_0 <= u'9') or (u'A' <= LA4_0 <= u'Z') or LA4_0 == u'_' or (u'a' <= LA4_0 <= u'z')) :
                    alt4 = 1


                if alt4 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:
                    if (u'0' <= self.input.LA(1) <= u'9') or (u'A' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'_' or (u'a' <= self.input.LA(1) <= u'z'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop4






        finally:

            pass

    # $ANTLR end GuidName



    # $ANTLR start Hex
    def mHex(self, ):

        try:
            self.type = Hex

            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:186:4: ( '0' ( 'x' | 'X' ) ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' )+ )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:186:9: '0' ( 'x' | 'X' ) ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' )+
            self.match(u'0')

            if self.input.LA(1) == u'X' or self.input.LA(1) == u'x':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse


            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:186:23: ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' )+
            cnt5 = 0
            while True: #loop5
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if ((u'0' <= LA5_0 <= u'9') or (u'A' <= LA5_0 <= u'F') or (u'a' <= LA5_0 <= u'f')) :
                    alt5 = 1


                if alt5 == 1:
                    # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:
                    if (u'0' <= self.input.LA(1) <= u'9') or (u'A' <= self.input.LA(1) <= u'F') or (u'a' <= self.input.LA(1) <= u'f'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    if cnt5 >= 1:
                        break #loop5

                    eee = EarlyExitException(5, self.input)
                    raise eee

                cnt5 += 1






        finally:

            pass

    # $ANTLR end Hex



    # $ANTLR start AlphaNumeric
    def mAlphaNumeric(self, ):

        try:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:190:5: ( ( Letter | '0' .. '9' ) )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:190:10: ( Letter | '0' .. '9' )
            if (u'0' <= self.input.LA(1) <= u'9') or (u'A' <= self.input.LA(1) <= u'Z') or (u'a' <= self.input.LA(1) <= u'z'):
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end AlphaNumeric



    # $ANTLR start Letter
    def mLetter(self, ):

        try:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:195:5: ( 'A' .. 'Z' | 'a' .. 'z' )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:
            if (u'A' <= self.input.LA(1) <= u'Z') or (u'a' <= self.input.LA(1) <= u'z'):
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end Letter



    # $ANTLR start Whitespace
    def mWhitespace(self, ):

        try:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:201:5: ( ( ' ' | '\\t' | '\\r' | '\\n' ) )
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:201:10: ( ' ' | '\\t' | '\\r' | '\\n' )
            if (u'\t' <= self.input.LA(1) <= u'\n') or self.input.LA(1) == u'\r' or self.input.LA(1) == u' ':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end Whitespace



    def mTokens(self):
        # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:8: ( T12 | T13 | T14 | T15 | T16 | T17 | T18 | T19 | T20 | T21 | T22 | T23 | T24 | T25 | T26 | T27 | OpCode | COMMENT | WS | GuidName | Hex )
        alt6 = 21
        LA6 = self.input.LA(1)
        if LA6 == u'D':
            LA6_1 = self.input.LA(2)

            if (LA6_1 == u'E') :
                LA6_20 = self.input.LA(3)

                if (LA6_20 == u'P') :
                    LA6_31 = self.input.LA(4)

                    if (LA6_31 == u'E') :
                        LA6_42 = self.input.LA(5)

                        if (LA6_42 == u'N') :
                            LA6_52 = self.input.LA(6)

                            if (LA6_52 == u'D') :
                                LA6_58 = self.input.LA(7)

                                if (LA6_58 == u'E') :
                                    LA6_62 = self.input.LA(8)

                                    if (LA6_62 == u'N') :
                                        LA6_64 = self.input.LA(9)

                                        if (LA6_64 == u'C') :
                                            LA6_65 = self.input.LA(10)

                                            if (LA6_65 == u'Y') :
                                                LA6_66 = self.input.LA(11)

                                                if (LA6_66 == u'_') :
                                                    LA6 = self.input.LA(12)
                                                    if LA6 == u'S':
                                                        LA6_68 = self.input.LA(13)

                                                        if (LA6_68 == u'T') :
                                                            LA6_70 = self.input.LA(14)

                                                            if (LA6_70 == u'A') :
                                                                LA6_72 = self.input.LA(15)

                                                                if (LA6_72 == u'R') :
                                                                    LA6_74 = self.input.LA(16)

                                                                    if (LA6_74 == u'T') :
                                                                        LA6_76 = self.input.LA(17)

                                                                        if ((u'0' <= LA6_76 <= u'9') or (u'A' <= LA6_76 <= u'Z') or LA6_76 == u'_' or (u'a' <= LA6_76 <= u'z')) :
                                                                            alt6 = 20
                                                                        else:
                                                                            alt6 = 1
                                                                    else:
                                                                        alt6 = 20
                                                                else:
                                                                    alt6 = 20
                                                            else:
                                                                alt6 = 20
                                                        else:
                                                            alt6 = 20
                                                    elif LA6 == u'E':
                                                        LA6_69 = self.input.LA(13)

                                                        if (LA6_69 == u'N') :
                                                            LA6_71 = self.input.LA(14)

                                                            if (LA6_71 == u'D') :
                                                                LA6_73 = self.input.LA(15)

                                                                if ((u'0' <= LA6_73 <= u'9') or (u'A' <= LA6_73 <= u'Z') or LA6_73 == u'_' or (u'a' <= LA6_73 <= u'z')) :
                                                                    alt6 = 20
                                                                else:
                                                                    alt6 = 3
                                                            else:
                                                                alt6 = 20
                                                        else:
                                                            alt6 = 20
                                                    else:
                                                        alt6 = 20
                                                else:
                                                    alt6 = 20
                                            else:
                                                alt6 = 20
                                        else:
                                            alt6 = 20
                                    else:
                                        alt6 = 20
                                else:
                                    alt6 = 20
                            else:
                                alt6 = 20
                        else:
                            alt6 = 20
                    else:
                        alt6 = 20
                else:
                    alt6 = 20
            else:
                alt6 = 20
        elif LA6 == u'E':
            LA6_2 = self.input.LA(2)

            if (LA6_2 == u'N') :
                LA6_21 = self.input.LA(3)

                if (LA6_21 == u'D') :
                    LA6_32 = self.input.LA(4)

                    if ((u'0' <= LA6_32 <= u'9') or (u'A' <= LA6_32 <= u'Z') or LA6_32 == u'_' or (u'a' <= LA6_32 <= u'z')) :
                        alt6 = 20
                    else:
                        alt6 = 2
                else:
                    alt6 = 20
            else:
                alt6 = 20
        elif LA6 == u'B':
            LA6_3 = self.input.LA(2)

            if (LA6_3 == u'E') :
                LA6_22 = self.input.LA(3)

                if (LA6_22 == u'F') :
                    LA6_33 = self.input.LA(4)

                    if (LA6_33 == u'O') :
                        LA6_44 = self.input.LA(5)

                        if (LA6_44 == u'R') :
                            LA6_53 = self.input.LA(6)

                            if (LA6_53 == u'E') :
                                LA6_59 = self.input.LA(7)

                                if ((u'0' <= LA6_59 <= u'9') or (u'A' <= LA6_59 <= u'Z') or LA6_59 == u'_' or (u'a' <= LA6_59 <= u'z')) :
                                    alt6 = 20
                                else:
                                    alt6 = 4
                            else:
                                alt6 = 20
                        else:
                            alt6 = 20
                    else:
                        alt6 = 20
                else:
                    alt6 = 20
            else:
                alt6 = 20
        elif LA6 == u'A':
            LA6 = self.input.LA(2)
            if LA6 == u'F':
                LA6_23 = self.input.LA(3)

                if (LA6_23 == u'T') :
                    LA6_34 = self.input.LA(4)

                    if (LA6_34 == u'E') :
                        LA6_45 = self.input.LA(5)

                        if (LA6_45 == u'R') :
                            LA6_54 = self.input.LA(6)

                            if ((u'0' <= LA6_54 <= u'9') or (u'A' <= LA6_54 <= u'Z') or LA6_54 == u'_' or (u'a' <= LA6_54 <= u'z')) :
                                alt6 = 20
                            else:
                                alt6 = 5
                        else:
                            alt6 = 20
                    else:
                        alt6 = 20
                else:
                    alt6 = 20
            elif LA6 == u'N':
                LA6_24 = self.input.LA(3)

                if (LA6_24 == u'D') :
                    LA6_35 = self.input.LA(4)

                    if ((u'0' <= LA6_35 <= u'9') or (u'A' <= LA6_35 <= u'Z') or LA6_35 == u'_' or (u'a' <= LA6_35 <= u'z')) :
                        alt6 = 20
                    else:
                        alt6 = 7
                else:
                    alt6 = 20
            else:
                alt6 = 20
        elif LA6 == u'S':
            LA6_5 = self.input.LA(2)

            if (LA6_5 == u'O') :
                LA6_25 = self.input.LA(3)

                if (LA6_25 == u'R') :
                    LA6_36 = self.input.LA(4)

                    if ((u'0' <= LA6_36 <= u'9') or (u'A' <= LA6_36 <= u'Z') or LA6_36 == u'_' or (u'a' <= LA6_36 <= u'z')) :
                        alt6 = 20
                    else:
                        alt6 = 6
                else:
                    alt6 = 20
            else:
                alt6 = 20
        elif LA6 == u'O':
            LA6_6 = self.input.LA(2)

            if (LA6_6 == u'R') :
                LA6_26 = self.input.LA(3)

                if ((u'0' <= LA6_26 <= u'9') or (u'A' <= LA6_26 <= u'Z') or LA6_26 == u'_' or (u'a' <= LA6_26 <= u'z')) :
                    alt6 = 20
                else:
                    alt6 = 8
            else:
                alt6 = 20
        elif LA6 == u'T':
            LA6_7 = self.input.LA(2)

            if (LA6_7 == u'R') :
                LA6_27 = self.input.LA(3)

                if (LA6_27 == u'U') :
                    LA6_38 = self.input.LA(4)

                    if (LA6_38 == u'E') :
                        LA6_48 = self.input.LA(5)

                        if ((u'0' <= LA6_48 <= u'9') or (u'A' <= LA6_48 <= u'Z') or LA6_48 == u'_' or (u'a' <= LA6_48 <= u'z')) :
                            alt6 = 20
                        else:
                            alt6 = 9
                    else:
                        alt6 = 20
                else:
                    alt6 = 20
            else:
                alt6 = 20
        elif LA6 == u'F':
            LA6_8 = self.input.LA(2)

            if (LA6_8 == u'A') :
                LA6_28 = self.input.LA(3)

                if (LA6_28 == u'L') :
                    LA6_39 = self.input.LA(4)

                    if (LA6_39 == u'S') :
                        LA6_49 = self.input.LA(5)

                        if (LA6_49 == u'E') :
                            LA6_56 = self.input.LA(6)

                            if ((u'0' <= LA6_56 <= u'9') or (u'A' <= LA6_56 <= u'Z') or LA6_56 == u'_' or (u'a' <= LA6_56 <= u'z')) :
                                alt6 = 20
                            else:
                                alt6 = 10
                        else:
                            alt6 = 20
                    else:
                        alt6 = 20
                else:
                    alt6 = 20
            else:
                alt6 = 20
        elif LA6 == u'N':
            LA6_9 = self.input.LA(2)

            if (LA6_9 == u'O') :
                LA6_29 = self.input.LA(3)

                if (LA6_29 == u'T') :
                    LA6_40 = self.input.LA(4)

                    if ((u'0' <= LA6_40 <= u'9') or (u'A' <= LA6_40 <= u'Z') or LA6_40 == u'_' or (u'a' <= LA6_40 <= u'z')) :
                        alt6 = 20
                    else:
                        alt6 = 11
                else:
                    alt6 = 20
            else:
                alt6 = 20
        elif LA6 == u'(':
            alt6 = 12
        elif LA6 == u')':
            alt6 = 13
        elif LA6 == u'{':
            alt6 = 14
        elif LA6 == u',':
            alt6 = 15
        elif LA6 == u'}':
            alt6 = 16
        elif LA6 == u'P':
            LA6_15 = self.input.LA(2)

            if (LA6_15 == u'U') :
                LA6_30 = self.input.LA(3)

                if (LA6_30 == u'S') :
                    LA6_41 = self.input.LA(4)

                    if (LA6_41 == u'H') :
                        LA6_51 = self.input.LA(5)

                        if ((u'0' <= LA6_51 <= u'9') or (u'A' <= LA6_51 <= u'Z') or LA6_51 == u'_' or (u'a' <= LA6_51 <= u'z')) :
                            alt6 = 20
                        else:
                            alt6 = 17
                    else:
                        alt6 = 20
                else:
                    alt6 = 20
            else:
                alt6 = 20
        elif LA6 == u'#':
            alt6 = 18
        elif LA6 == u'\t' or LA6 == u'\n' or LA6 == u'\r' or LA6 == u' ':
            alt6 = 19
        elif LA6 == u'C' or LA6 == u'G' or LA6 == u'H' or LA6 == u'I' or LA6 == u'J' or LA6 == u'K' or LA6 == u'L' or LA6 == u'M' or LA6 == u'Q' or LA6 == u'R' or LA6 == u'U' or LA6 == u'V' or LA6 == u'W' or LA6 == u'X' or LA6 == u'Y' or LA6 == u'Z' or LA6 == u'_' or LA6 == u'a' or LA6 == u'b' or LA6 == u'c' or LA6 == u'd' or LA6 == u'e' or LA6 == u'f' or LA6 == u'g' or LA6 == u'h' or LA6 == u'i' or LA6 == u'j' or LA6 == u'k' or LA6 == u'l' or LA6 == u'm' or LA6 == u'n' or LA6 == u'o' or LA6 == u'p' or LA6 == u'q' or LA6 == u'r' or LA6 == u's' or LA6 == u't' or LA6 == u'u' or LA6 == u'v' or LA6 == u'w' or LA6 == u'x' or LA6 == u'y' or LA6 == u'z':
            alt6 = 20
        elif LA6 == u'0':
            alt6 = 21
        else:
            nvae = NoViableAltException("1:1: Tokens : ( T12 | T13 | T14 | T15 | T16 | T17 | T18 | T19 | T20 | T21 | T22 | T23 | T24 | T25 | T26 | T27 | OpCode | COMMENT | WS | GuidName | Hex );", 6, 0, self.input)

            raise nvae

        if alt6 == 1:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:10: T12
            self.mT12()



        elif alt6 == 2:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:14: T13
            self.mT13()



        elif alt6 == 3:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:18: T14
            self.mT14()



        elif alt6 == 4:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:22: T15
            self.mT15()



        elif alt6 == 5:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:26: T16
            self.mT16()



        elif alt6 == 6:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:30: T17
            self.mT17()



        elif alt6 == 7:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:34: T18
            self.mT18()



        elif alt6 == 8:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:38: T19
            self.mT19()



        elif alt6 == 9:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:42: T20
            self.mT20()



        elif alt6 == 10:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:46: T21
            self.mT21()



        elif alt6 == 11:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:50: T22
            self.mT22()



        elif alt6 == 12:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:54: T23
            self.mT23()



        elif alt6 == 13:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:58: T24
            self.mT24()



        elif alt6 == 14:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:62: T25
            self.mT25()



        elif alt6 == 15:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:66: T26
            self.mT26()



        elif alt6 == 16:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:70: T27
            self.mT27()



        elif alt6 == 17:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:74: OpCode
            self.mOpCode()



        elif alt6 == 18:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:81: COMMENT
            self.mCOMMENT()



        elif alt6 == 19:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:89: WS
            self.mWS()



        elif alt6 == 20:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:92: GuidName
            self.mGuidName()



        elif alt6 == 21:
            # H:\\dev\\BugFix\\Source\\Python\\AutoGen\\Depex.g:1:101: Hex
            self.mHex()








 


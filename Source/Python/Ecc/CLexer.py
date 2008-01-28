# $ANTLR 3.0.1 C.g 2008-01-25 19:33:36

from antlr3 import *
from antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
T29=29
HexDigit=13
T70=70
T74=74
T85=85
T102=102
T103=103
STRING_LITERAL=9
T32=32
T81=81
T41=41
FloatTypeSuffix=16
T62=62
DECIMAL_LITERAL=7
IntegerTypeSuffix=14
T68=68
T73=73
T84=84
T33=33
UnicodeVocabulary=21
T78=78
WS=19
LINE_COMMAND=24
T42=42
T96=96
T71=71
LINE_COMMENT=23
T72=72
T94=94
FLOATING_POINT_LITERAL=10
T76=76
UnicodeEscape=18
T75=75
T89=89
T67=67
T31=31
T60=60
T82=82
T100=100
T49=49
IDENTIFIER=4
T30=30
CHARACTER_LITERAL=8
T79=79
T36=36
T58=58
T93=93
T35=35
T107=107
OCTAL_LITERAL=6
T83=83
T61=61
HEX_LITERAL=5
T45=45
T34=34
T101=101
T64=64
T25=25
T91=91
T105=105
T37=37
T86=86
EscapeSequence=12
T26=26
T51=51
T46=46
T77=77
T38=38
T106=106
T69=69
T39=39
T44=44
T55=55
LETTER=11
Exponent=15
T95=95
T50=50
BS=20
T92=92
T43=43
T28=28
T40=40
T66=66
COMMENT=22
T88=88
T63=63
T57=57
T65=65
T98=98
T56=56
T87=87
T80=80
T59=59
T97=97
T48=48
T54=54
EOF=-1
T104=104
T47=47
Tokens=108
T53=53
OctalEscape=17
T99=99
T27=27
T52=52
T90=90

class CLexer(Lexer):

    grammarFileName = "C.g"

    def __init__(self, input=None):
        Lexer.__init__(self, input)
        self.dfa28 = self.DFA28(
            self, 28,
            eot = self.DFA28_eot,
            eof = self.DFA28_eof,
            min = self.DFA28_min,
            max = self.DFA28_max,
            accept = self.DFA28_accept,
            special = self.DFA28_special,
            transition = self.DFA28_transition
            )
        self.dfa38 = self.DFA38(
            self, 38,
            eot = self.DFA38_eot,
            eof = self.DFA38_eof,
            min = self.DFA38_min,
            max = self.DFA38_max,
            accept = self.DFA38_accept,
            special = self.DFA38_special,
            transition = self.DFA38_transition
            )






    # $ANTLR start T25
    def mT25(self, ):

        try:
            self.type = T25

            # C.g:7:5: ( ';' )
            # C.g:7:7: ';'
            self.match(u';')





        finally:

            pass

    # $ANTLR end T25



    # $ANTLR start T26
    def mT26(self, ):

        try:
            self.type = T26

            # C.g:8:5: ( 'typedef' )
            # C.g:8:7: 'typedef'
            self.match("typedef")






        finally:

            pass

    # $ANTLR end T26



    # $ANTLR start T27
    def mT27(self, ):

        try:
            self.type = T27

            # C.g:9:5: ( ',' )
            # C.g:9:7: ','
            self.match(u',')





        finally:

            pass

    # $ANTLR end T27



    # $ANTLR start T28
    def mT28(self, ):

        try:
            self.type = T28

            # C.g:10:5: ( '=' )
            # C.g:10:7: '='
            self.match(u'=')





        finally:

            pass

    # $ANTLR end T28



    # $ANTLR start T29
    def mT29(self, ):

        try:
            self.type = T29

            # C.g:11:5: ( 'extern' )
            # C.g:11:7: 'extern'
            self.match("extern")






        finally:

            pass

    # $ANTLR end T29



    # $ANTLR start T30
    def mT30(self, ):

        try:
            self.type = T30

            # C.g:12:5: ( 'static' )
            # C.g:12:7: 'static'
            self.match("static")






        finally:

            pass

    # $ANTLR end T30



    # $ANTLR start T31
    def mT31(self, ):

        try:
            self.type = T31

            # C.g:13:5: ( 'auto' )
            # C.g:13:7: 'auto'
            self.match("auto")






        finally:

            pass

    # $ANTLR end T31



    # $ANTLR start T32
    def mT32(self, ):

        try:
            self.type = T32

            # C.g:14:5: ( 'register' )
            # C.g:14:7: 'register'
            self.match("register")






        finally:

            pass

    # $ANTLR end T32



    # $ANTLR start T33
    def mT33(self, ):

        try:
            self.type = T33

            # C.g:15:5: ( 'STATIC' )
            # C.g:15:7: 'STATIC'
            self.match("STATIC")






        finally:

            pass

    # $ANTLR end T33



    # $ANTLR start T34
    def mT34(self, ):

        try:
            self.type = T34

            # C.g:16:5: ( 'void' )
            # C.g:16:7: 'void'
            self.match("void")






        finally:

            pass

    # $ANTLR end T34



    # $ANTLR start T35
    def mT35(self, ):

        try:
            self.type = T35

            # C.g:17:5: ( 'char' )
            # C.g:17:7: 'char'
            self.match("char")






        finally:

            pass

    # $ANTLR end T35



    # $ANTLR start T36
    def mT36(self, ):

        try:
            self.type = T36

            # C.g:18:5: ( 'short' )
            # C.g:18:7: 'short'
            self.match("short")






        finally:

            pass

    # $ANTLR end T36



    # $ANTLR start T37
    def mT37(self, ):

        try:
            self.type = T37

            # C.g:19:5: ( 'int' )
            # C.g:19:7: 'int'
            self.match("int")






        finally:

            pass

    # $ANTLR end T37



    # $ANTLR start T38
    def mT38(self, ):

        try:
            self.type = T38

            # C.g:20:5: ( 'long' )
            # C.g:20:7: 'long'
            self.match("long")






        finally:

            pass

    # $ANTLR end T38



    # $ANTLR start T39
    def mT39(self, ):

        try:
            self.type = T39

            # C.g:21:5: ( 'float' )
            # C.g:21:7: 'float'
            self.match("float")






        finally:

            pass

    # $ANTLR end T39



    # $ANTLR start T40
    def mT40(self, ):

        try:
            self.type = T40

            # C.g:22:5: ( 'double' )
            # C.g:22:7: 'double'
            self.match("double")






        finally:

            pass

    # $ANTLR end T40



    # $ANTLR start T41
    def mT41(self, ):

        try:
            self.type = T41

            # C.g:23:5: ( 'signed' )
            # C.g:23:7: 'signed'
            self.match("signed")






        finally:

            pass

    # $ANTLR end T41



    # $ANTLR start T42
    def mT42(self, ):

        try:
            self.type = T42

            # C.g:24:5: ( 'unsigned' )
            # C.g:24:7: 'unsigned'
            self.match("unsigned")






        finally:

            pass

    # $ANTLR end T42



    # $ANTLR start T43
    def mT43(self, ):

        try:
            self.type = T43

            # C.g:25:5: ( '{' )
            # C.g:25:7: '{'
            self.match(u'{')





        finally:

            pass

    # $ANTLR end T43



    # $ANTLR start T44
    def mT44(self, ):

        try:
            self.type = T44

            # C.g:26:5: ( '}' )
            # C.g:26:7: '}'
            self.match(u'}')





        finally:

            pass

    # $ANTLR end T44



    # $ANTLR start T45
    def mT45(self, ):

        try:
            self.type = T45

            # C.g:27:5: ( 'struct' )
            # C.g:27:7: 'struct'
            self.match("struct")






        finally:

            pass

    # $ANTLR end T45



    # $ANTLR start T46
    def mT46(self, ):

        try:
            self.type = T46

            # C.g:28:5: ( 'union' )
            # C.g:28:7: 'union'
            self.match("union")






        finally:

            pass

    # $ANTLR end T46



    # $ANTLR start T47
    def mT47(self, ):

        try:
            self.type = T47

            # C.g:29:5: ( ':' )
            # C.g:29:7: ':'
            self.match(u':')





        finally:

            pass

    # $ANTLR end T47



    # $ANTLR start T48
    def mT48(self, ):

        try:
            self.type = T48

            # C.g:30:5: ( 'enum' )
            # C.g:30:7: 'enum'
            self.match("enum")






        finally:

            pass

    # $ANTLR end T48



    # $ANTLR start T49
    def mT49(self, ):

        try:
            self.type = T49

            # C.g:31:5: ( 'const' )
            # C.g:31:7: 'const'
            self.match("const")






        finally:

            pass

    # $ANTLR end T49



    # $ANTLR start T50
    def mT50(self, ):

        try:
            self.type = T50

            # C.g:32:5: ( 'volatile' )
            # C.g:32:7: 'volatile'
            self.match("volatile")






        finally:

            pass

    # $ANTLR end T50



    # $ANTLR start T51
    def mT51(self, ):

        try:
            self.type = T51

            # C.g:33:5: ( 'IN' )
            # C.g:33:7: 'IN'
            self.match("IN")






        finally:

            pass

    # $ANTLR end T51



    # $ANTLR start T52
    def mT52(self, ):

        try:
            self.type = T52

            # C.g:34:5: ( 'OUT' )
            # C.g:34:7: 'OUT'
            self.match("OUT")






        finally:

            pass

    # $ANTLR end T52



    # $ANTLR start T53
    def mT53(self, ):

        try:
            self.type = T53

            # C.g:35:5: ( 'OPTIONAL' )
            # C.g:35:7: 'OPTIONAL'
            self.match("OPTIONAL")






        finally:

            pass

    # $ANTLR end T53



    # $ANTLR start T54
    def mT54(self, ):

        try:
            self.type = T54

            # C.g:36:5: ( 'EFIAPI' )
            # C.g:36:7: 'EFIAPI'
            self.match("EFIAPI")






        finally:

            pass

    # $ANTLR end T54



    # $ANTLR start T55
    def mT55(self, ):

        try:
            self.type = T55

            # C.g:37:5: ( '(' )
            # C.g:37:7: '('
            self.match(u'(')





        finally:

            pass

    # $ANTLR end T55



    # $ANTLR start T56
    def mT56(self, ):

        try:
            self.type = T56

            # C.g:38:5: ( ')' )
            # C.g:38:7: ')'
            self.match(u')')





        finally:

            pass

    # $ANTLR end T56



    # $ANTLR start T57
    def mT57(self, ):

        try:
            self.type = T57

            # C.g:39:5: ( '[' )
            # C.g:39:7: '['
            self.match(u'[')





        finally:

            pass

    # $ANTLR end T57



    # $ANTLR start T58
    def mT58(self, ):

        try:
            self.type = T58

            # C.g:40:5: ( ']' )
            # C.g:40:7: ']'
            self.match(u']')





        finally:

            pass

    # $ANTLR end T58



    # $ANTLR start T59
    def mT59(self, ):

        try:
            self.type = T59

            # C.g:41:5: ( '*' )
            # C.g:41:7: '*'
            self.match(u'*')





        finally:

            pass

    # $ANTLR end T59



    # $ANTLR start T60
    def mT60(self, ):

        try:
            self.type = T60

            # C.g:42:5: ( '...' )
            # C.g:42:7: '...'
            self.match("...")






        finally:

            pass

    # $ANTLR end T60



    # $ANTLR start T61
    def mT61(self, ):

        try:
            self.type = T61

            # C.g:43:5: ( '+' )
            # C.g:43:7: '+'
            self.match(u'+')





        finally:

            pass

    # $ANTLR end T61



    # $ANTLR start T62
    def mT62(self, ):

        try:
            self.type = T62

            # C.g:44:5: ( '-' )
            # C.g:44:7: '-'
            self.match(u'-')





        finally:

            pass

    # $ANTLR end T62



    # $ANTLR start T63
    def mT63(self, ):

        try:
            self.type = T63

            # C.g:45:5: ( '/' )
            # C.g:45:7: '/'
            self.match(u'/')





        finally:

            pass

    # $ANTLR end T63



    # $ANTLR start T64
    def mT64(self, ):

        try:
            self.type = T64

            # C.g:46:5: ( '%' )
            # C.g:46:7: '%'
            self.match(u'%')





        finally:

            pass

    # $ANTLR end T64



    # $ANTLR start T65
    def mT65(self, ):

        try:
            self.type = T65

            # C.g:47:5: ( '++' )
            # C.g:47:7: '++'
            self.match("++")






        finally:

            pass

    # $ANTLR end T65



    # $ANTLR start T66
    def mT66(self, ):

        try:
            self.type = T66

            # C.g:48:5: ( '--' )
            # C.g:48:7: '--'
            self.match("--")






        finally:

            pass

    # $ANTLR end T66



    # $ANTLR start T67
    def mT67(self, ):

        try:
            self.type = T67

            # C.g:49:5: ( 'sizeof' )
            # C.g:49:7: 'sizeof'
            self.match("sizeof")






        finally:

            pass

    # $ANTLR end T67



    # $ANTLR start T68
    def mT68(self, ):

        try:
            self.type = T68

            # C.g:50:5: ( '.' )
            # C.g:50:7: '.'
            self.match(u'.')





        finally:

            pass

    # $ANTLR end T68



    # $ANTLR start T69
    def mT69(self, ):

        try:
            self.type = T69

            # C.g:51:5: ( '->' )
            # C.g:51:7: '->'
            self.match("->")






        finally:

            pass

    # $ANTLR end T69



    # $ANTLR start T70
    def mT70(self, ):

        try:
            self.type = T70

            # C.g:52:5: ( '&' )
            # C.g:52:7: '&'
            self.match(u'&')





        finally:

            pass

    # $ANTLR end T70



    # $ANTLR start T71
    def mT71(self, ):

        try:
            self.type = T71

            # C.g:53:5: ( '~' )
            # C.g:53:7: '~'
            self.match(u'~')





        finally:

            pass

    # $ANTLR end T71



    # $ANTLR start T72
    def mT72(self, ):

        try:
            self.type = T72

            # C.g:54:5: ( '!' )
            # C.g:54:7: '!'
            self.match(u'!')





        finally:

            pass

    # $ANTLR end T72



    # $ANTLR start T73
    def mT73(self, ):

        try:
            self.type = T73

            # C.g:55:5: ( '*=' )
            # C.g:55:7: '*='
            self.match("*=")






        finally:

            pass

    # $ANTLR end T73



    # $ANTLR start T74
    def mT74(self, ):

        try:
            self.type = T74

            # C.g:56:5: ( '/=' )
            # C.g:56:7: '/='
            self.match("/=")






        finally:

            pass

    # $ANTLR end T74



    # $ANTLR start T75
    def mT75(self, ):

        try:
            self.type = T75

            # C.g:57:5: ( '%=' )
            # C.g:57:7: '%='
            self.match("%=")






        finally:

            pass

    # $ANTLR end T75



    # $ANTLR start T76
    def mT76(self, ):

        try:
            self.type = T76

            # C.g:58:5: ( '+=' )
            # C.g:58:7: '+='
            self.match("+=")






        finally:

            pass

    # $ANTLR end T76



    # $ANTLR start T77
    def mT77(self, ):

        try:
            self.type = T77

            # C.g:59:5: ( '-=' )
            # C.g:59:7: '-='
            self.match("-=")






        finally:

            pass

    # $ANTLR end T77



    # $ANTLR start T78
    def mT78(self, ):

        try:
            self.type = T78

            # C.g:60:5: ( '<<=' )
            # C.g:60:7: '<<='
            self.match("<<=")






        finally:

            pass

    # $ANTLR end T78



    # $ANTLR start T79
    def mT79(self, ):

        try:
            self.type = T79

            # C.g:61:5: ( '>>=' )
            # C.g:61:7: '>>='
            self.match(">>=")






        finally:

            pass

    # $ANTLR end T79



    # $ANTLR start T80
    def mT80(self, ):

        try:
            self.type = T80

            # C.g:62:5: ( '&=' )
            # C.g:62:7: '&='
            self.match("&=")






        finally:

            pass

    # $ANTLR end T80



    # $ANTLR start T81
    def mT81(self, ):

        try:
            self.type = T81

            # C.g:63:5: ( '^=' )
            # C.g:63:7: '^='
            self.match("^=")






        finally:

            pass

    # $ANTLR end T81



    # $ANTLR start T82
    def mT82(self, ):

        try:
            self.type = T82

            # C.g:64:5: ( '|=' )
            # C.g:64:7: '|='
            self.match("|=")






        finally:

            pass

    # $ANTLR end T82



    # $ANTLR start T83
    def mT83(self, ):

        try:
            self.type = T83

            # C.g:65:5: ( '?' )
            # C.g:65:7: '?'
            self.match(u'?')





        finally:

            pass

    # $ANTLR end T83



    # $ANTLR start T84
    def mT84(self, ):

        try:
            self.type = T84

            # C.g:66:5: ( '||' )
            # C.g:66:7: '||'
            self.match("||")






        finally:

            pass

    # $ANTLR end T84



    # $ANTLR start T85
    def mT85(self, ):

        try:
            self.type = T85

            # C.g:67:5: ( '&&' )
            # C.g:67:7: '&&'
            self.match("&&")






        finally:

            pass

    # $ANTLR end T85



    # $ANTLR start T86
    def mT86(self, ):

        try:
            self.type = T86

            # C.g:68:5: ( '|' )
            # C.g:68:7: '|'
            self.match(u'|')





        finally:

            pass

    # $ANTLR end T86



    # $ANTLR start T87
    def mT87(self, ):

        try:
            self.type = T87

            # C.g:69:5: ( '^' )
            # C.g:69:7: '^'
            self.match(u'^')





        finally:

            pass

    # $ANTLR end T87



    # $ANTLR start T88
    def mT88(self, ):

        try:
            self.type = T88

            # C.g:70:5: ( '==' )
            # C.g:70:7: '=='
            self.match("==")






        finally:

            pass

    # $ANTLR end T88



    # $ANTLR start T89
    def mT89(self, ):

        try:
            self.type = T89

            # C.g:71:5: ( '!=' )
            # C.g:71:7: '!='
            self.match("!=")






        finally:

            pass

    # $ANTLR end T89



    # $ANTLR start T90
    def mT90(self, ):

        try:
            self.type = T90

            # C.g:72:5: ( '<' )
            # C.g:72:7: '<'
            self.match(u'<')





        finally:

            pass

    # $ANTLR end T90



    # $ANTLR start T91
    def mT91(self, ):

        try:
            self.type = T91

            # C.g:73:5: ( '>' )
            # C.g:73:7: '>'
            self.match(u'>')





        finally:

            pass

    # $ANTLR end T91



    # $ANTLR start T92
    def mT92(self, ):

        try:
            self.type = T92

            # C.g:74:5: ( '<=' )
            # C.g:74:7: '<='
            self.match("<=")






        finally:

            pass

    # $ANTLR end T92



    # $ANTLR start T93
    def mT93(self, ):

        try:
            self.type = T93

            # C.g:75:5: ( '>=' )
            # C.g:75:7: '>='
            self.match(">=")






        finally:

            pass

    # $ANTLR end T93



    # $ANTLR start T94
    def mT94(self, ):

        try:
            self.type = T94

            # C.g:76:5: ( '<<' )
            # C.g:76:7: '<<'
            self.match("<<")






        finally:

            pass

    # $ANTLR end T94



    # $ANTLR start T95
    def mT95(self, ):

        try:
            self.type = T95

            # C.g:77:5: ( '>>' )
            # C.g:77:7: '>>'
            self.match(">>")






        finally:

            pass

    # $ANTLR end T95



    # $ANTLR start T96
    def mT96(self, ):

        try:
            self.type = T96

            # C.g:78:5: ( 'case' )
            # C.g:78:7: 'case'
            self.match("case")






        finally:

            pass

    # $ANTLR end T96



    # $ANTLR start T97
    def mT97(self, ):

        try:
            self.type = T97

            # C.g:79:5: ( 'default' )
            # C.g:79:7: 'default'
            self.match("default")






        finally:

            pass

    # $ANTLR end T97



    # $ANTLR start T98
    def mT98(self, ):

        try:
            self.type = T98

            # C.g:80:5: ( 'if' )
            # C.g:80:7: 'if'
            self.match("if")






        finally:

            pass

    # $ANTLR end T98



    # $ANTLR start T99
    def mT99(self, ):

        try:
            self.type = T99

            # C.g:81:5: ( 'else' )
            # C.g:81:7: 'else'
            self.match("else")






        finally:

            pass

    # $ANTLR end T99



    # $ANTLR start T100
    def mT100(self, ):

        try:
            self.type = T100

            # C.g:82:6: ( 'switch' )
            # C.g:82:8: 'switch'
            self.match("switch")






        finally:

            pass

    # $ANTLR end T100



    # $ANTLR start T101
    def mT101(self, ):

        try:
            self.type = T101

            # C.g:83:6: ( 'while' )
            # C.g:83:8: 'while'
            self.match("while")






        finally:

            pass

    # $ANTLR end T101



    # $ANTLR start T102
    def mT102(self, ):

        try:
            self.type = T102

            # C.g:84:6: ( 'do' )
            # C.g:84:8: 'do'
            self.match("do")






        finally:

            pass

    # $ANTLR end T102



    # $ANTLR start T103
    def mT103(self, ):

        try:
            self.type = T103

            # C.g:85:6: ( 'for' )
            # C.g:85:8: 'for'
            self.match("for")






        finally:

            pass

    # $ANTLR end T103



    # $ANTLR start T104
    def mT104(self, ):

        try:
            self.type = T104

            # C.g:86:6: ( 'goto' )
            # C.g:86:8: 'goto'
            self.match("goto")






        finally:

            pass

    # $ANTLR end T104



    # $ANTLR start T105
    def mT105(self, ):

        try:
            self.type = T105

            # C.g:87:6: ( 'continue' )
            # C.g:87:8: 'continue'
            self.match("continue")






        finally:

            pass

    # $ANTLR end T105



    # $ANTLR start T106
    def mT106(self, ):

        try:
            self.type = T106

            # C.g:88:6: ( 'break' )
            # C.g:88:8: 'break'
            self.match("break")






        finally:

            pass

    # $ANTLR end T106



    # $ANTLR start T107
    def mT107(self, ):

        try:
            self.type = T107

            # C.g:89:6: ( 'return' )
            # C.g:89:8: 'return'
            self.match("return")






        finally:

            pass

    # $ANTLR end T107



    # $ANTLR start IDENTIFIER
    def mIDENTIFIER(self, ):

        try:
            self.type = IDENTIFIER

            # C.g:489:2: ( LETTER ( LETTER | '0' .. '9' )* )
            # C.g:489:4: LETTER ( LETTER | '0' .. '9' )*
            self.mLETTER()

            # C.g:489:11: ( LETTER | '0' .. '9' )*
            while True: #loop1
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if (LA1_0 == u'$' or (u'0' <= LA1_0 <= u'9') or (u'A' <= LA1_0 <= u'Z') or LA1_0 == u'_' or (u'a' <= LA1_0 <= u'z')) :
                    alt1 = 1


                if alt1 == 1:
                    # C.g:
                    if self.input.LA(1) == u'$' or (u'0' <= self.input.LA(1) <= u'9') or (u'A' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'_' or (u'a' <= self.input.LA(1) <= u'z'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop1






        finally:

            pass

    # $ANTLR end IDENTIFIER



    # $ANTLR start LETTER
    def mLETTER(self, ):

        try:
            # C.g:494:2: ( '$' | 'A' .. 'Z' | 'a' .. 'z' | '_' )
            # C.g:
            if self.input.LA(1) == u'$' or (u'A' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'_' or (u'a' <= self.input.LA(1) <= u'z'):
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end LETTER



    # $ANTLR start CHARACTER_LITERAL
    def mCHARACTER_LITERAL(self, ):

        try:
            self.type = CHARACTER_LITERAL

            # C.g:501:5: ( ( 'L' )? '\\'' ( EscapeSequence | ~ ( '\\'' | '\\\\' ) ) '\\'' )
            # C.g:501:9: ( 'L' )? '\\'' ( EscapeSequence | ~ ( '\\'' | '\\\\' ) ) '\\''
            # C.g:501:9: ( 'L' )?
            alt2 = 2
            LA2_0 = self.input.LA(1)

            if (LA2_0 == u'L') :
                alt2 = 1
            if alt2 == 1:
                # C.g:501:10: 'L'
                self.match(u'L')




            self.match(u'\'')

            # C.g:501:21: ( EscapeSequence | ~ ( '\\'' | '\\\\' ) )
            alt3 = 2
            LA3_0 = self.input.LA(1)

            if (LA3_0 == u'\\') :
                alt3 = 1
            elif ((u'\u0000' <= LA3_0 <= u'&') or (u'(' <= LA3_0 <= u'[') or (u']' <= LA3_0 <= u'\uFFFE')) :
                alt3 = 2
            else:
                nvae = NoViableAltException("501:21: ( EscapeSequence | ~ ( '\\'' | '\\\\' ) )", 3, 0, self.input)

                raise nvae

            if alt3 == 1:
                # C.g:501:23: EscapeSequence
                self.mEscapeSequence()



            elif alt3 == 2:
                # C.g:501:40: ~ ( '\\'' | '\\\\' )
                if (u'\u0000' <= self.input.LA(1) <= u'&') or (u'(' <= self.input.LA(1) <= u'[') or (u']' <= self.input.LA(1) <= u'\uFFFE'):
                    self.input.consume();

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse





            self.match(u'\'')





        finally:

            pass

    # $ANTLR end CHARACTER_LITERAL



    # $ANTLR start STRING_LITERAL
    def mSTRING_LITERAL(self, ):

        try:
            self.type = STRING_LITERAL

            # C.g:505:5: ( ( 'L' )? '\"' ( EscapeSequence | ~ ( '\\\\' | '\"' ) )* '\"' )
            # C.g:505:8: ( 'L' )? '\"' ( EscapeSequence | ~ ( '\\\\' | '\"' ) )* '\"'
            # C.g:505:8: ( 'L' )?
            alt4 = 2
            LA4_0 = self.input.LA(1)

            if (LA4_0 == u'L') :
                alt4 = 1
            if alt4 == 1:
                # C.g:505:9: 'L'
                self.match(u'L')




            self.match(u'"')

            # C.g:505:19: ( EscapeSequence | ~ ( '\\\\' | '\"' ) )*
            while True: #loop5
                alt5 = 3
                LA5_0 = self.input.LA(1)

                if (LA5_0 == u'\\') :
                    alt5 = 1
                elif ((u'\u0000' <= LA5_0 <= u'!') or (u'#' <= LA5_0 <= u'[') or (u']' <= LA5_0 <= u'\uFFFE')) :
                    alt5 = 2


                if alt5 == 1:
                    # C.g:505:21: EscapeSequence
                    self.mEscapeSequence()



                elif alt5 == 2:
                    # C.g:505:38: ~ ( '\\\\' | '\"' )
                    if (u'\u0000' <= self.input.LA(1) <= u'!') or (u'#' <= self.input.LA(1) <= u'[') or (u']' <= self.input.LA(1) <= u'\uFFFE'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop5


            self.match(u'"')





        finally:

            pass

    # $ANTLR end STRING_LITERAL



    # $ANTLR start HEX_LITERAL
    def mHEX_LITERAL(self, ):

        try:
            self.type = HEX_LITERAL

            # C.g:508:13: ( '0' ( 'x' | 'X' ) ( HexDigit )+ ( IntegerTypeSuffix )? )
            # C.g:508:15: '0' ( 'x' | 'X' ) ( HexDigit )+ ( IntegerTypeSuffix )?
            self.match(u'0')

            if self.input.LA(1) == u'X' or self.input.LA(1) == u'x':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse


            # C.g:508:29: ( HexDigit )+
            cnt6 = 0
            while True: #loop6
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if ((u'0' <= LA6_0 <= u'9') or (u'A' <= LA6_0 <= u'F') or (u'a' <= LA6_0 <= u'f')) :
                    alt6 = 1


                if alt6 == 1:
                    # C.g:508:29: HexDigit
                    self.mHexDigit()



                else:
                    if cnt6 >= 1:
                        break #loop6

                    eee = EarlyExitException(6, self.input)
                    raise eee

                cnt6 += 1


            # C.g:508:39: ( IntegerTypeSuffix )?
            alt7 = 2
            LA7_0 = self.input.LA(1)

            if (LA7_0 == u'L' or LA7_0 == u'U' or LA7_0 == u'l' or LA7_0 == u'u') :
                alt7 = 1
            if alt7 == 1:
                # C.g:508:39: IntegerTypeSuffix
                self.mIntegerTypeSuffix()








        finally:

            pass

    # $ANTLR end HEX_LITERAL



    # $ANTLR start DECIMAL_LITERAL
    def mDECIMAL_LITERAL(self, ):

        try:
            self.type = DECIMAL_LITERAL

            # C.g:510:17: ( ( '0' | '1' .. '9' ( '0' .. '9' )* ) ( IntegerTypeSuffix )? )
            # C.g:510:19: ( '0' | '1' .. '9' ( '0' .. '9' )* ) ( IntegerTypeSuffix )?
            # C.g:510:19: ( '0' | '1' .. '9' ( '0' .. '9' )* )
            alt9 = 2
            LA9_0 = self.input.LA(1)

            if (LA9_0 == u'0') :
                alt9 = 1
            elif ((u'1' <= LA9_0 <= u'9')) :
                alt9 = 2
            else:
                nvae = NoViableAltException("510:19: ( '0' | '1' .. '9' ( '0' .. '9' )* )", 9, 0, self.input)

                raise nvae

            if alt9 == 1:
                # C.g:510:20: '0'
                self.match(u'0')



            elif alt9 == 2:
                # C.g:510:26: '1' .. '9' ( '0' .. '9' )*
                self.matchRange(u'1', u'9')

                # C.g:510:35: ( '0' .. '9' )*
                while True: #loop8
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if ((u'0' <= LA8_0 <= u'9')) :
                        alt8 = 1


                    if alt8 == 1:
                        # C.g:510:35: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        break #loop8





            # C.g:510:46: ( IntegerTypeSuffix )?
            alt10 = 2
            LA10_0 = self.input.LA(1)

            if (LA10_0 == u'L' or LA10_0 == u'U' or LA10_0 == u'l' or LA10_0 == u'u') :
                alt10 = 1
            if alt10 == 1:
                # C.g:510:46: IntegerTypeSuffix
                self.mIntegerTypeSuffix()








        finally:

            pass

    # $ANTLR end DECIMAL_LITERAL



    # $ANTLR start OCTAL_LITERAL
    def mOCTAL_LITERAL(self, ):

        try:
            self.type = OCTAL_LITERAL

            # C.g:512:15: ( '0' ( '0' .. '7' )+ ( IntegerTypeSuffix )? )
            # C.g:512:17: '0' ( '0' .. '7' )+ ( IntegerTypeSuffix )?
            self.match(u'0')

            # C.g:512:21: ( '0' .. '7' )+
            cnt11 = 0
            while True: #loop11
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if ((u'0' <= LA11_0 <= u'7')) :
                    alt11 = 1


                if alt11 == 1:
                    # C.g:512:22: '0' .. '7'
                    self.matchRange(u'0', u'7')



                else:
                    if cnt11 >= 1:
                        break #loop11

                    eee = EarlyExitException(11, self.input)
                    raise eee

                cnt11 += 1


            # C.g:512:33: ( IntegerTypeSuffix )?
            alt12 = 2
            LA12_0 = self.input.LA(1)

            if (LA12_0 == u'L' or LA12_0 == u'U' or LA12_0 == u'l' or LA12_0 == u'u') :
                alt12 = 1
            if alt12 == 1:
                # C.g:512:33: IntegerTypeSuffix
                self.mIntegerTypeSuffix()








        finally:

            pass

    # $ANTLR end OCTAL_LITERAL



    # $ANTLR start HexDigit
    def mHexDigit(self, ):

        try:
            # C.g:515:10: ( ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' ) )
            # C.g:515:12: ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' )
            if (u'0' <= self.input.LA(1) <= u'9') or (u'A' <= self.input.LA(1) <= u'F') or (u'a' <= self.input.LA(1) <= u'f'):
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end HexDigit



    # $ANTLR start IntegerTypeSuffix
    def mIntegerTypeSuffix(self, ):

        try:
            # C.g:519:2: ( ( 'u' | 'U' )? ( 'l' | 'L' ) | ( 'u' | 'U' ) ( 'l' | 'L' )? ( 'l' | 'L' )? )
            alt16 = 2
            LA16_0 = self.input.LA(1)

            if (LA16_0 == u'U' or LA16_0 == u'u') :
                LA16_1 = self.input.LA(2)

                if (LA16_1 == u'L' or LA16_1 == u'l') :
                    alt16 = 1
                else:
                    alt16 = 2
            elif (LA16_0 == u'L' or LA16_0 == u'l') :
                alt16 = 1
            else:
                nvae = NoViableAltException("517:1: fragment IntegerTypeSuffix : ( ( 'u' | 'U' )? ( 'l' | 'L' ) | ( 'u' | 'U' ) ( 'l' | 'L' )? ( 'l' | 'L' )? );", 16, 0, self.input)

                raise nvae

            if alt16 == 1:
                # C.g:519:4: ( 'u' | 'U' )? ( 'l' | 'L' )
                # C.g:519:4: ( 'u' | 'U' )?
                alt13 = 2
                LA13_0 = self.input.LA(1)

                if (LA13_0 == u'U' or LA13_0 == u'u') :
                    alt13 = 1
                if alt13 == 1:
                    # C.g:
                    if self.input.LA(1) == u'U' or self.input.LA(1) == u'u':
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse





                if self.input.LA(1) == u'L' or self.input.LA(1) == u'l':
                    self.input.consume();

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse




            elif alt16 == 2:
                # C.g:520:4: ( 'u' | 'U' ) ( 'l' | 'L' )? ( 'l' | 'L' )?
                if self.input.LA(1) == u'U' or self.input.LA(1) == u'u':
                    self.input.consume();

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse


                # C.g:520:15: ( 'l' | 'L' )?
                alt14 = 2
                LA14_0 = self.input.LA(1)

                if (LA14_0 == u'L' or LA14_0 == u'l') :
                    alt14 = 1
                if alt14 == 1:
                    # C.g:
                    if self.input.LA(1) == u'L' or self.input.LA(1) == u'l':
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse





                # C.g:520:26: ( 'l' | 'L' )?
                alt15 = 2
                LA15_0 = self.input.LA(1)

                if (LA15_0 == u'L' or LA15_0 == u'l') :
                    alt15 = 1
                if alt15 == 1:
                    # C.g:
                    if self.input.LA(1) == u'L' or self.input.LA(1) == u'l':
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse








        finally:

            pass

    # $ANTLR end IntegerTypeSuffix



    # $ANTLR start FLOATING_POINT_LITERAL
    def mFLOATING_POINT_LITERAL(self, ):

        try:
            self.type = FLOATING_POINT_LITERAL

            # C.g:524:5: ( ( '0' .. '9' )+ '.' ( '0' .. '9' )* ( Exponent )? ( FloatTypeSuffix )? | '.' ( '0' .. '9' )+ ( Exponent )? ( FloatTypeSuffix )? | ( '0' .. '9' )+ Exponent ( FloatTypeSuffix )? | ( '0' .. '9' )+ ( Exponent )? FloatTypeSuffix )
            alt28 = 4
            alt28 = self.dfa28.predict(self.input)
            if alt28 == 1:
                # C.g:524:9: ( '0' .. '9' )+ '.' ( '0' .. '9' )* ( Exponent )? ( FloatTypeSuffix )?
                # C.g:524:9: ( '0' .. '9' )+
                cnt17 = 0
                while True: #loop17
                    alt17 = 2
                    LA17_0 = self.input.LA(1)

                    if ((u'0' <= LA17_0 <= u'9')) :
                        alt17 = 1


                    if alt17 == 1:
                        # C.g:524:10: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        if cnt17 >= 1:
                            break #loop17

                        eee = EarlyExitException(17, self.input)
                        raise eee

                    cnt17 += 1


                self.match(u'.')

                # C.g:524:25: ( '0' .. '9' )*
                while True: #loop18
                    alt18 = 2
                    LA18_0 = self.input.LA(1)

                    if ((u'0' <= LA18_0 <= u'9')) :
                        alt18 = 1


                    if alt18 == 1:
                        # C.g:524:26: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        break #loop18


                # C.g:524:37: ( Exponent )?
                alt19 = 2
                LA19_0 = self.input.LA(1)

                if (LA19_0 == u'E' or LA19_0 == u'e') :
                    alt19 = 1
                if alt19 == 1:
                    # C.g:524:37: Exponent
                    self.mExponent()




                # C.g:524:47: ( FloatTypeSuffix )?
                alt20 = 2
                LA20_0 = self.input.LA(1)

                if (LA20_0 == u'D' or LA20_0 == u'F' or LA20_0 == u'd' or LA20_0 == u'f') :
                    alt20 = 1
                if alt20 == 1:
                    # C.g:524:47: FloatTypeSuffix
                    self.mFloatTypeSuffix()






            elif alt28 == 2:
                # C.g:525:9: '.' ( '0' .. '9' )+ ( Exponent )? ( FloatTypeSuffix )?
                self.match(u'.')

                # C.g:525:13: ( '0' .. '9' )+
                cnt21 = 0
                while True: #loop21
                    alt21 = 2
                    LA21_0 = self.input.LA(1)

                    if ((u'0' <= LA21_0 <= u'9')) :
                        alt21 = 1


                    if alt21 == 1:
                        # C.g:525:14: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        if cnt21 >= 1:
                            break #loop21

                        eee = EarlyExitException(21, self.input)
                        raise eee

                    cnt21 += 1


                # C.g:525:25: ( Exponent )?
                alt22 = 2
                LA22_0 = self.input.LA(1)

                if (LA22_0 == u'E' or LA22_0 == u'e') :
                    alt22 = 1
                if alt22 == 1:
                    # C.g:525:25: Exponent
                    self.mExponent()




                # C.g:525:35: ( FloatTypeSuffix )?
                alt23 = 2
                LA23_0 = self.input.LA(1)

                if (LA23_0 == u'D' or LA23_0 == u'F' or LA23_0 == u'd' or LA23_0 == u'f') :
                    alt23 = 1
                if alt23 == 1:
                    # C.g:525:35: FloatTypeSuffix
                    self.mFloatTypeSuffix()






            elif alt28 == 3:
                # C.g:526:9: ( '0' .. '9' )+ Exponent ( FloatTypeSuffix )?
                # C.g:526:9: ( '0' .. '9' )+
                cnt24 = 0
                while True: #loop24
                    alt24 = 2
                    LA24_0 = self.input.LA(1)

                    if ((u'0' <= LA24_0 <= u'9')) :
                        alt24 = 1


                    if alt24 == 1:
                        # C.g:526:10: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        if cnt24 >= 1:
                            break #loop24

                        eee = EarlyExitException(24, self.input)
                        raise eee

                    cnt24 += 1


                self.mExponent()

                # C.g:526:30: ( FloatTypeSuffix )?
                alt25 = 2
                LA25_0 = self.input.LA(1)

                if (LA25_0 == u'D' or LA25_0 == u'F' or LA25_0 == u'd' or LA25_0 == u'f') :
                    alt25 = 1
                if alt25 == 1:
                    # C.g:526:30: FloatTypeSuffix
                    self.mFloatTypeSuffix()






            elif alt28 == 4:
                # C.g:527:9: ( '0' .. '9' )+ ( Exponent )? FloatTypeSuffix
                # C.g:527:9: ( '0' .. '9' )+
                cnt26 = 0
                while True: #loop26
                    alt26 = 2
                    LA26_0 = self.input.LA(1)

                    if ((u'0' <= LA26_0 <= u'9')) :
                        alt26 = 1


                    if alt26 == 1:
                        # C.g:527:10: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        if cnt26 >= 1:
                            break #loop26

                        eee = EarlyExitException(26, self.input)
                        raise eee

                    cnt26 += 1


                # C.g:527:21: ( Exponent )?
                alt27 = 2
                LA27_0 = self.input.LA(1)

                if (LA27_0 == u'E' or LA27_0 == u'e') :
                    alt27 = 1
                if alt27 == 1:
                    # C.g:527:21: Exponent
                    self.mExponent()




                self.mFloatTypeSuffix()




        finally:

            pass

    # $ANTLR end FLOATING_POINT_LITERAL



    # $ANTLR start Exponent
    def mExponent(self, ):

        try:
            # C.g:531:10: ( ( 'e' | 'E' ) ( '+' | '-' )? ( '0' .. '9' )+ )
            # C.g:531:12: ( 'e' | 'E' ) ( '+' | '-' )? ( '0' .. '9' )+
            if self.input.LA(1) == u'E' or self.input.LA(1) == u'e':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse


            # C.g:531:22: ( '+' | '-' )?
            alt29 = 2
            LA29_0 = self.input.LA(1)

            if (LA29_0 == u'+' or LA29_0 == u'-') :
                alt29 = 1
            if alt29 == 1:
                # C.g:
                if self.input.LA(1) == u'+' or self.input.LA(1) == u'-':
                    self.input.consume();

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse





            # C.g:531:33: ( '0' .. '9' )+
            cnt30 = 0
            while True: #loop30
                alt30 = 2
                LA30_0 = self.input.LA(1)

                if ((u'0' <= LA30_0 <= u'9')) :
                    alt30 = 1


                if alt30 == 1:
                    # C.g:531:34: '0' .. '9'
                    self.matchRange(u'0', u'9')



                else:
                    if cnt30 >= 1:
                        break #loop30

                    eee = EarlyExitException(30, self.input)
                    raise eee

                cnt30 += 1






        finally:

            pass

    # $ANTLR end Exponent



    # $ANTLR start FloatTypeSuffix
    def mFloatTypeSuffix(self, ):

        try:
            # C.g:534:17: ( ( 'f' | 'F' | 'd' | 'D' ) )
            # C.g:534:19: ( 'f' | 'F' | 'd' | 'D' )
            if self.input.LA(1) == u'D' or self.input.LA(1) == u'F' or self.input.LA(1) == u'd' or self.input.LA(1) == u'f':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse






        finally:

            pass

    # $ANTLR end FloatTypeSuffix



    # $ANTLR start EscapeSequence
    def mEscapeSequence(self, ):

        try:
            # C.g:538:5: ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) | OctalEscape )
            alt31 = 2
            LA31_0 = self.input.LA(1)

            if (LA31_0 == u'\\') :
                LA31_1 = self.input.LA(2)

                if (LA31_1 == u'"' or LA31_1 == u'\'' or LA31_1 == u'\\' or LA31_1 == u'b' or LA31_1 == u'f' or LA31_1 == u'n' or LA31_1 == u'r' or LA31_1 == u't') :
                    alt31 = 1
                elif ((u'0' <= LA31_1 <= u'7')) :
                    alt31 = 2
                else:
                    nvae = NoViableAltException("536:1: fragment EscapeSequence : ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) | OctalEscape );", 31, 1, self.input)

                    raise nvae

            else:
                nvae = NoViableAltException("536:1: fragment EscapeSequence : ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) | OctalEscape );", 31, 0, self.input)

                raise nvae

            if alt31 == 1:
                # C.g:538:8: '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' )
                self.match(u'\\')

                if self.input.LA(1) == u'"' or self.input.LA(1) == u'\'' or self.input.LA(1) == u'\\' or self.input.LA(1) == u'b' or self.input.LA(1) == u'f' or self.input.LA(1) == u'n' or self.input.LA(1) == u'r' or self.input.LA(1) == u't':
                    self.input.consume();

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse




            elif alt31 == 2:
                # C.g:539:9: OctalEscape
                self.mOctalEscape()




        finally:

            pass

    # $ANTLR end EscapeSequence



    # $ANTLR start OctalEscape
    def mOctalEscape(self, ):

        try:
            # C.g:544:5: ( '\\\\' ( '0' .. '3' ) ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) )
            alt32 = 3
            LA32_0 = self.input.LA(1)

            if (LA32_0 == u'\\') :
                LA32_1 = self.input.LA(2)

                if ((u'0' <= LA32_1 <= u'3')) :
                    LA32_2 = self.input.LA(3)

                    if ((u'0' <= LA32_2 <= u'7')) :
                        LA32_5 = self.input.LA(4)

                        if ((u'0' <= LA32_5 <= u'7')) :
                            alt32 = 1
                        else:
                            alt32 = 2
                    else:
                        alt32 = 3
                elif ((u'4' <= LA32_1 <= u'7')) :
                    LA32_3 = self.input.LA(3)

                    if ((u'0' <= LA32_3 <= u'7')) :
                        alt32 = 2
                    else:
                        alt32 = 3
                else:
                    nvae = NoViableAltException("542:1: fragment OctalEscape : ( '\\\\' ( '0' .. '3' ) ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) );", 32, 1, self.input)

                    raise nvae

            else:
                nvae = NoViableAltException("542:1: fragment OctalEscape : ( '\\\\' ( '0' .. '3' ) ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) );", 32, 0, self.input)

                raise nvae

            if alt32 == 1:
                # C.g:544:9: '\\\\' ( '0' .. '3' ) ( '0' .. '7' ) ( '0' .. '7' )
                self.match(u'\\')

                # C.g:544:14: ( '0' .. '3' )
                # C.g:544:15: '0' .. '3'
                self.matchRange(u'0', u'3')




                # C.g:544:25: ( '0' .. '7' )
                # C.g:544:26: '0' .. '7'
                self.matchRange(u'0', u'7')




                # C.g:544:36: ( '0' .. '7' )
                # C.g:544:37: '0' .. '7'
                self.matchRange(u'0', u'7')






            elif alt32 == 2:
                # C.g:545:9: '\\\\' ( '0' .. '7' ) ( '0' .. '7' )
                self.match(u'\\')

                # C.g:545:14: ( '0' .. '7' )
                # C.g:545:15: '0' .. '7'
                self.matchRange(u'0', u'7')




                # C.g:545:25: ( '0' .. '7' )
                # C.g:545:26: '0' .. '7'
                self.matchRange(u'0', u'7')






            elif alt32 == 3:
                # C.g:546:9: '\\\\' ( '0' .. '7' )
                self.match(u'\\')

                # C.g:546:14: ( '0' .. '7' )
                # C.g:546:15: '0' .. '7'
                self.matchRange(u'0', u'7')







        finally:

            pass

    # $ANTLR end OctalEscape



    # $ANTLR start UnicodeEscape
    def mUnicodeEscape(self, ):

        try:
            # C.g:551:5: ( '\\\\' 'u' HexDigit HexDigit HexDigit HexDigit )
            # C.g:551:9: '\\\\' 'u' HexDigit HexDigit HexDigit HexDigit
            self.match(u'\\')

            self.match(u'u')

            self.mHexDigit()

            self.mHexDigit()

            self.mHexDigit()

            self.mHexDigit()





        finally:

            pass

    # $ANTLR end UnicodeEscape



    # $ANTLR start WS
    def mWS(self, ):

        try:
            self.type = WS

            # C.g:554:5: ( ( ' ' | '\\r' | '\\t' | '\\u000C' | '\\n' ) )
            # C.g:554:8: ( ' ' | '\\r' | '\\t' | '\\u000C' | '\\n' )
            if (u'\t' <= self.input.LA(1) <= u'\n') or (u'\f' <= self.input.LA(1) <= u'\r') or self.input.LA(1) == u' ':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse


            #action start
            self.channel=HIDDEN;
            #action end




        finally:

            pass

    # $ANTLR end WS



    # $ANTLR start BS
    def mBS(self, ):

        try:
            self.type = BS

            # C.g:558:5: ( ( '\\\\' ) )
            # C.g:558:7: ( '\\\\' )
            # C.g:558:7: ( '\\\\' )
            # C.g:558:8: '\\\\'
            self.match(u'\\')




            #action start
            self.channel=HIDDEN;
            #action end




        finally:

            pass

    # $ANTLR end BS



    # $ANTLR start UnicodeVocabulary
    def mUnicodeVocabulary(self, ):

        try:
            self.type = UnicodeVocabulary

            # C.g:566:5: ( '\\u0003' .. '\\uFFFE' )
            # C.g:566:7: '\\u0003' .. '\\uFFFE'
            self.matchRange(u'\u0003', u'\uFFFE')





        finally:

            pass

    # $ANTLR end UnicodeVocabulary



    # $ANTLR start COMMENT
    def mCOMMENT(self, ):

        try:
            self.type = COMMENT

            # C.g:569:5: ( '/*' ( options {greedy=false; } : . )* '*/' )
            # C.g:569:9: '/*' ( options {greedy=false; } : . )* '*/'
            self.match("/*")


            # C.g:569:14: ( options {greedy=false; } : . )*
            while True: #loop33
                alt33 = 2
                LA33_0 = self.input.LA(1)

                if (LA33_0 == u'*') :
                    LA33_1 = self.input.LA(2)

                    if (LA33_1 == u'/') :
                        alt33 = 2
                    elif ((u'\u0000' <= LA33_1 <= u'.') or (u'0' <= LA33_1 <= u'\uFFFE')) :
                        alt33 = 1


                elif ((u'\u0000' <= LA33_0 <= u')') or (u'+' <= LA33_0 <= u'\uFFFE')) :
                    alt33 = 1


                if alt33 == 1:
                    # C.g:569:42: .
                    self.matchAny()



                else:
                    break #loop33


            self.match("*/")


            #action start
            self.channel=HIDDEN;
            #action end




        finally:

            pass

    # $ANTLR end COMMENT



    # $ANTLR start LINE_COMMENT
    def mLINE_COMMENT(self, ):

        try:
            self.type = LINE_COMMENT

            # C.g:574:5: ( '//' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' )
            # C.g:574:7: '//' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
            self.match("//")


            # C.g:574:12: (~ ( '\\n' | '\\r' ) )*
            while True: #loop34
                alt34 = 2
                LA34_0 = self.input.LA(1)

                if ((u'\u0000' <= LA34_0 <= u'\t') or (u'\u000B' <= LA34_0 <= u'\f') or (u'\u000E' <= LA34_0 <= u'\uFFFE')) :
                    alt34 = 1


                if alt34 == 1:
                    # C.g:574:12: ~ ( '\\n' | '\\r' )
                    if (u'\u0000' <= self.input.LA(1) <= u'\t') or (u'\u000B' <= self.input.LA(1) <= u'\f') or (u'\u000E' <= self.input.LA(1) <= u'\uFFFE'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop34


            # C.g:574:26: ( '\\r' )?
            alt35 = 2
            LA35_0 = self.input.LA(1)

            if (LA35_0 == u'\r') :
                alt35 = 1
            if alt35 == 1:
                # C.g:574:26: '\\r'
                self.match(u'\r')




            self.match(u'\n')

            #action start
            self.channel=HIDDEN;
            #action end




        finally:

            pass

    # $ANTLR end LINE_COMMENT



    # $ANTLR start LINE_COMMAND
    def mLINE_COMMAND(self, ):

        try:
            self.type = LINE_COMMAND

            # C.g:579:5: ( '#' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' )
            # C.g:579:7: '#' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
            self.match(u'#')

            # C.g:579:11: (~ ( '\\n' | '\\r' ) )*
            while True: #loop36
                alt36 = 2
                LA36_0 = self.input.LA(1)

                if ((u'\u0000' <= LA36_0 <= u'\t') or (u'\u000B' <= LA36_0 <= u'\f') or (u'\u000E' <= LA36_0 <= u'\uFFFE')) :
                    alt36 = 1


                if alt36 == 1:
                    # C.g:579:11: ~ ( '\\n' | '\\r' )
                    if (u'\u0000' <= self.input.LA(1) <= u'\t') or (u'\u000B' <= self.input.LA(1) <= u'\f') or (u'\u000E' <= self.input.LA(1) <= u'\uFFFE'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop36


            # C.g:579:25: ( '\\r' )?
            alt37 = 2
            LA37_0 = self.input.LA(1)

            if (LA37_0 == u'\r') :
                alt37 = 1
            if alt37 == 1:
                # C.g:579:25: '\\r'
                self.match(u'\r')




            self.match(u'\n')

            #action start
            self.channel=HIDDEN;
            #action end




        finally:

            pass

    # $ANTLR end LINE_COMMAND



    def mTokens(self):
        # C.g:1:8: ( T25 | T26 | T27 | T28 | T29 | T30 | T31 | T32 | T33 | T34 | T35 | T36 | T37 | T38 | T39 | T40 | T41 | T42 | T43 | T44 | T45 | T46 | T47 | T48 | T49 | T50 | T51 | T52 | T53 | T54 | T55 | T56 | T57 | T58 | T59 | T60 | T61 | T62 | T63 | T64 | T65 | T66 | T67 | T68 | T69 | T70 | T71 | T72 | T73 | T74 | T75 | T76 | T77 | T78 | T79 | T80 | T81 | T82 | T83 | T84 | T85 | T86 | T87 | T88 | T89 | T90 | T91 | T92 | T93 | T94 | T95 | T96 | T97 | T98 | T99 | T100 | T101 | T102 | T103 | T104 | T105 | T106 | T107 | IDENTIFIER | CHARACTER_LITERAL | STRING_LITERAL | HEX_LITERAL | DECIMAL_LITERAL | OCTAL_LITERAL | FLOATING_POINT_LITERAL | WS | BS | UnicodeVocabulary | COMMENT | LINE_COMMENT | LINE_COMMAND )
        alt38 = 96
        alt38 = self.dfa38.predict(self.input)
        if alt38 == 1:
            # C.g:1:10: T25
            self.mT25()



        elif alt38 == 2:
            # C.g:1:14: T26
            self.mT26()



        elif alt38 == 3:
            # C.g:1:18: T27
            self.mT27()



        elif alt38 == 4:
            # C.g:1:22: T28
            self.mT28()



        elif alt38 == 5:
            # C.g:1:26: T29
            self.mT29()



        elif alt38 == 6:
            # C.g:1:30: T30
            self.mT30()



        elif alt38 == 7:
            # C.g:1:34: T31
            self.mT31()



        elif alt38 == 8:
            # C.g:1:38: T32
            self.mT32()



        elif alt38 == 9:
            # C.g:1:42: T33
            self.mT33()



        elif alt38 == 10:
            # C.g:1:46: T34
            self.mT34()



        elif alt38 == 11:
            # C.g:1:50: T35
            self.mT35()



        elif alt38 == 12:
            # C.g:1:54: T36
            self.mT36()



        elif alt38 == 13:
            # C.g:1:58: T37
            self.mT37()



        elif alt38 == 14:
            # C.g:1:62: T38
            self.mT38()



        elif alt38 == 15:
            # C.g:1:66: T39
            self.mT39()



        elif alt38 == 16:
            # C.g:1:70: T40
            self.mT40()



        elif alt38 == 17:
            # C.g:1:74: T41
            self.mT41()



        elif alt38 == 18:
            # C.g:1:78: T42
            self.mT42()



        elif alt38 == 19:
            # C.g:1:82: T43
            self.mT43()



        elif alt38 == 20:
            # C.g:1:86: T44
            self.mT44()



        elif alt38 == 21:
            # C.g:1:90: T45
            self.mT45()



        elif alt38 == 22:
            # C.g:1:94: T46
            self.mT46()



        elif alt38 == 23:
            # C.g:1:98: T47
            self.mT47()



        elif alt38 == 24:
            # C.g:1:102: T48
            self.mT48()



        elif alt38 == 25:
            # C.g:1:106: T49
            self.mT49()



        elif alt38 == 26:
            # C.g:1:110: T50
            self.mT50()



        elif alt38 == 27:
            # C.g:1:114: T51
            self.mT51()



        elif alt38 == 28:
            # C.g:1:118: T52
            self.mT52()



        elif alt38 == 29:
            # C.g:1:122: T53
            self.mT53()



        elif alt38 == 30:
            # C.g:1:126: T54
            self.mT54()



        elif alt38 == 31:
            # C.g:1:130: T55
            self.mT55()



        elif alt38 == 32:
            # C.g:1:134: T56
            self.mT56()



        elif alt38 == 33:
            # C.g:1:138: T57
            self.mT57()



        elif alt38 == 34:
            # C.g:1:142: T58
            self.mT58()



        elif alt38 == 35:
            # C.g:1:146: T59
            self.mT59()



        elif alt38 == 36:
            # C.g:1:150: T60
            self.mT60()



        elif alt38 == 37:
            # C.g:1:154: T61
            self.mT61()



        elif alt38 == 38:
            # C.g:1:158: T62
            self.mT62()



        elif alt38 == 39:
            # C.g:1:162: T63
            self.mT63()



        elif alt38 == 40:
            # C.g:1:166: T64
            self.mT64()



        elif alt38 == 41:
            # C.g:1:170: T65
            self.mT65()



        elif alt38 == 42:
            # C.g:1:174: T66
            self.mT66()



        elif alt38 == 43:
            # C.g:1:178: T67
            self.mT67()



        elif alt38 == 44:
            # C.g:1:182: T68
            self.mT68()



        elif alt38 == 45:
            # C.g:1:186: T69
            self.mT69()



        elif alt38 == 46:
            # C.g:1:190: T70
            self.mT70()



        elif alt38 == 47:
            # C.g:1:194: T71
            self.mT71()



        elif alt38 == 48:
            # C.g:1:198: T72
            self.mT72()



        elif alt38 == 49:
            # C.g:1:202: T73
            self.mT73()



        elif alt38 == 50:
            # C.g:1:206: T74
            self.mT74()



        elif alt38 == 51:
            # C.g:1:210: T75
            self.mT75()



        elif alt38 == 52:
            # C.g:1:214: T76
            self.mT76()



        elif alt38 == 53:
            # C.g:1:218: T77
            self.mT77()



        elif alt38 == 54:
            # C.g:1:222: T78
            self.mT78()



        elif alt38 == 55:
            # C.g:1:226: T79
            self.mT79()



        elif alt38 == 56:
            # C.g:1:230: T80
            self.mT80()



        elif alt38 == 57:
            # C.g:1:234: T81
            self.mT81()



        elif alt38 == 58:
            # C.g:1:238: T82
            self.mT82()



        elif alt38 == 59:
            # C.g:1:242: T83
            self.mT83()



        elif alt38 == 60:
            # C.g:1:246: T84
            self.mT84()



        elif alt38 == 61:
            # C.g:1:250: T85
            self.mT85()



        elif alt38 == 62:
            # C.g:1:254: T86
            self.mT86()



        elif alt38 == 63:
            # C.g:1:258: T87
            self.mT87()



        elif alt38 == 64:
            # C.g:1:262: T88
            self.mT88()



        elif alt38 == 65:
            # C.g:1:266: T89
            self.mT89()



        elif alt38 == 66:
            # C.g:1:270: T90
            self.mT90()



        elif alt38 == 67:
            # C.g:1:274: T91
            self.mT91()



        elif alt38 == 68:
            # C.g:1:278: T92
            self.mT92()



        elif alt38 == 69:
            # C.g:1:282: T93
            self.mT93()



        elif alt38 == 70:
            # C.g:1:286: T94
            self.mT94()



        elif alt38 == 71:
            # C.g:1:290: T95
            self.mT95()



        elif alt38 == 72:
            # C.g:1:294: T96
            self.mT96()



        elif alt38 == 73:
            # C.g:1:298: T97
            self.mT97()



        elif alt38 == 74:
            # C.g:1:302: T98
            self.mT98()



        elif alt38 == 75:
            # C.g:1:306: T99
            self.mT99()



        elif alt38 == 76:
            # C.g:1:310: T100
            self.mT100()



        elif alt38 == 77:
            # C.g:1:315: T101
            self.mT101()



        elif alt38 == 78:
            # C.g:1:320: T102
            self.mT102()



        elif alt38 == 79:
            # C.g:1:325: T103
            self.mT103()



        elif alt38 == 80:
            # C.g:1:330: T104
            self.mT104()



        elif alt38 == 81:
            # C.g:1:335: T105
            self.mT105()



        elif alt38 == 82:
            # C.g:1:340: T106
            self.mT106()



        elif alt38 == 83:
            # C.g:1:345: T107
            self.mT107()



        elif alt38 == 84:
            # C.g:1:350: IDENTIFIER
            self.mIDENTIFIER()



        elif alt38 == 85:
            # C.g:1:361: CHARACTER_LITERAL
            self.mCHARACTER_LITERAL()



        elif alt38 == 86:
            # C.g:1:379: STRING_LITERAL
            self.mSTRING_LITERAL()



        elif alt38 == 87:
            # C.g:1:394: HEX_LITERAL
            self.mHEX_LITERAL()



        elif alt38 == 88:
            # C.g:1:406: DECIMAL_LITERAL
            self.mDECIMAL_LITERAL()



        elif alt38 == 89:
            # C.g:1:422: OCTAL_LITERAL
            self.mOCTAL_LITERAL()



        elif alt38 == 90:
            # C.g:1:436: FLOATING_POINT_LITERAL
            self.mFLOATING_POINT_LITERAL()



        elif alt38 == 91:
            # C.g:1:459: WS
            self.mWS()



        elif alt38 == 92:
            # C.g:1:462: BS
            self.mBS()



        elif alt38 == 93:
            # C.g:1:465: UnicodeVocabulary
            self.mUnicodeVocabulary()



        elif alt38 == 94:
            # C.g:1:483: COMMENT
            self.mCOMMENT()



        elif alt38 == 95:
            # C.g:1:491: LINE_COMMENT
            self.mLINE_COMMENT()



        elif alt38 == 96:
            # C.g:1:504: LINE_COMMAND
            self.mLINE_COMMAND()








    # lookup tables for DFA #28

    DFA28_eot = DFA.unpack(
        u"\7\uffff\1\10\2\uffff"
        )

    DFA28_eof = DFA.unpack(
        u"\12\uffff"
        )

    DFA28_min = DFA.unpack(
        u"\2\56\2\uffff\1\53\1\uffff\2\60\2\uffff"
        )

    DFA28_max = DFA.unpack(
        u"\1\71\1\146\2\uffff\1\71\1\uffff\1\71\1\146\2\uffff"
        )

    DFA28_accept = DFA.unpack(
        u"\2\uffff\1\2\1\1\1\uffff\1\4\2\uffff\2\3"
        )

    DFA28_special = DFA.unpack(
        u"\12\uffff"
        )

            
    DFA28_transition = [
        DFA.unpack(u"\1\2\1\uffff\12\1"),
        DFA.unpack(u"\1\3\1\uffff\12\1\12\uffff\1\5\1\4\1\5\35\uffff\1\5"
        u"\1\4\1\5"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\6\1\uffff\1\6\2\uffff\12\7"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\7"),
        DFA.unpack(u"\12\7\12\uffff\1\11\1\uffff\1\11\35\uffff\1\11\1\uffff"
        u"\1\11"),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #28

    DFA28 = DFA
    # lookup tables for DFA #38

    DFA38_eot = DFA.unpack(
        u"\2\uffff\1\70\1\uffff\1\73\14\70\3\uffff\3\70\4\uffff\1\136\1\141"
        u"\1\144\1\150\1\154\1\156\1\161\1\uffff\1\164\1\167\1\172\1\174"
        u"\1\177\1\uffff\4\70\1\uffff\2\65\2\u0087\2\uffff\1\65\2\uffff\1"
        u"\70\4\uffff\16\70\1\u00a0\4\70\1\u00a6\2\70\3\uffff\1\u00aa\3\70"
        u"\34\uffff\1\u00af\2\uffff\1\u00b1\10\uffff\3\70\4\uffff\1\u00b5"
        u"\1\u0087\3\uffff\23\70\1\uffff\1\u00ca\2\70\1\u00cd\1\70\1\uffff"
        u"\3\70\1\uffff\1\u00d2\2\70\4\uffff\3\70\1\uffff\1\70\1\u00d9\1"
        u"\70\1\u00db\6\70\1\u00e2\4\70\1\u00e7\1\u00e8\2\70\1\u00eb\1\uffff"
        u"\1\u00ec\1\70\1\uffff\4\70\1\uffff\3\70\1\u00f5\2\70\1\uffff\1"
        u"\70\1\uffff\2\70\1\u00fb\3\70\1\uffff\4\70\2\uffff\1\70\1\u0104"
        u"\2\uffff\1\u0105\2\70\1\u0108\3\70\1\u010c\1\uffff\1\u010d\1\70"
        u"\1\u010f\1\u0110\1\u0111\1\uffff\1\u0112\1\u0113\1\u0114\1\70\1"
        u"\u0116\1\u0117\2\70\2\uffff\1\u011a\1\70\1\uffff\2\70\1\u011e\2"
        u"\uffff\1\u011f\6\uffff\1\70\2\uffff\2\70\1\uffff\1\u0123\2\70\2"
        u"\uffff\1\u0126\1\u0127\1\u0128\1\uffff\1\u0129\1\u012a\5\uffff"
        )

    DFA38_eof = DFA.unpack(
        u"\u012b\uffff"
        )

    DFA38_min = DFA.unpack(
        u"\1\3\1\uffff\1\171\1\uffff\1\75\1\154\1\150\1\165\1\145\1\124\1"
        u"\157\1\141\1\146\1\157\1\154\1\145\1\156\3\uffff\1\116\1\120\1"
        u"\106\4\uffff\1\75\1\56\1\53\1\55\1\52\1\75\1\46\1\uffff\1\75\1"
        u"\74\3\75\1\uffff\1\150\1\157\1\162\1\42\1\uffff\2\0\2\56\2\uffff"
        u"\1\0\2\uffff\1\160\4\uffff\1\165\1\164\1\163\1\141\1\157\1\151"
        u"\1\147\1\164\1\147\1\101\1\151\1\163\1\156\1\141\1\44\1\164\1\156"
        u"\1\157\1\162\1\44\1\146\1\151\3\uffff\1\44\2\124\1\111\34\uffff"
        u"\1\75\2\uffff\1\75\10\uffff\1\151\1\164\1\145\4\uffff\2\56\3\uffff"
        u"\1\145\1\155\2\145\1\165\1\164\1\162\1\164\1\156\1\145\1\157\1"
        u"\151\1\165\1\124\1\141\1\144\1\145\1\163\1\162\1\uffff\1\44\1\147"
        u"\1\141\1\44\1\142\1\uffff\1\141\1\157\1\151\1\uffff\1\44\1\111"
        u"\1\101\4\uffff\1\154\1\157\1\141\1\uffff\1\144\1\44\1\162\1\44"
        u"\1\143\1\151\1\164\1\143\1\145\1\157\1\44\1\163\1\162\1\111\1\164"
        u"\2\44\1\151\1\164\1\44\1\uffff\1\44\1\164\1\uffff\1\154\1\165\1"
        u"\156\1\147\1\uffff\1\117\1\120\1\145\1\44\1\153\1\145\1\uffff\1"
        u"\156\1\uffff\1\164\1\143\1\44\1\150\1\144\1\146\1\uffff\1\164\1"
        u"\156\1\103\1\151\2\uffff\1\156\1\44\2\uffff\1\44\1\145\1\154\1"
        u"\44\1\156\1\116\1\111\1\44\1\uffff\1\44\1\146\3\44\1\uffff\3\44"
        u"\1\145\2\44\1\154\1\165\2\uffff\1\44\1\164\1\uffff\1\145\1\101"
        u"\1\44\2\uffff\1\44\6\uffff\1\162\2\uffff\2\145\1\uffff\1\44\1\144"
        u"\1\114\2\uffff\3\44\1\uffff\2\44\5\uffff"
        )

    DFA38_max = DFA.unpack(
        u"\1\ufffe\1\uffff\1\171\1\uffff\1\75\1\170\1\167\1\165\1\145\1\124"
        u"\2\157\1\156\3\157\1\156\3\uffff\1\116\1\125\1\106\4\uffff\1\75"
        u"\1\71\1\75\1\76\3\75\1\uffff\2\75\1\76\1\75\1\174\1\uffff\1\150"
        u"\1\157\1\162\1\47\1\uffff\2\ufffe\1\170\1\146\2\uffff\1\ufffe\2"
        u"\uffff\1\160\4\uffff\1\165\1\164\1\163\1\162\1\157\1\151\1\172"
        u"\2\164\1\101\1\154\1\163\1\156\1\141\1\172\1\164\1\156\1\157\1"
        u"\162\1\172\1\146\1\163\3\uffff\1\172\2\124\1\111\34\uffff\1\75"
        u"\2\uffff\1\75\10\uffff\1\151\1\164\1\145\4\uffff\2\146\3\uffff"
        u"\1\145\1\155\2\145\1\165\1\164\1\162\1\164\1\156\1\145\1\157\1"
        u"\151\1\165\1\124\1\141\1\144\1\145\1\164\1\162\1\uffff\1\172\1"
        u"\147\1\141\1\172\1\142\1\uffff\1\141\1\157\1\151\1\uffff\1\172"
        u"\1\111\1\101\4\uffff\1\154\1\157\1\141\1\uffff\1\144\1\172\1\162"
        u"\1\172\1\143\1\151\1\164\1\143\1\145\1\157\1\172\1\163\1\162\1"
        u"\111\1\164\2\172\1\151\1\164\1\172\1\uffff\1\172\1\164\1\uffff"
        u"\1\154\1\165\1\156\1\147\1\uffff\1\117\1\120\1\145\1\172\1\153"
        u"\1\145\1\uffff\1\156\1\uffff\1\164\1\143\1\172\1\150\1\144\1\146"
        u"\1\uffff\1\164\1\156\1\103\1\151\2\uffff\1\156\1\172\2\uffff\1"
        u"\172\1\145\1\154\1\172\1\156\1\116\1\111\1\172\1\uffff\1\172\1"
        u"\146\3\172\1\uffff\3\172\1\145\2\172\1\154\1\165\2\uffff\1\172"
        u"\1\164\1\uffff\1\145\1\101\1\172\2\uffff\1\172\6\uffff\1\162\2"
        u"\uffff\2\145\1\uffff\1\172\1\144\1\114\2\uffff\3\172\1\uffff\2"
        u"\172\5\uffff"
        )

    DFA38_accept = DFA.unpack(
        u"\1\uffff\1\1\1\uffff\1\3\15\uffff\1\23\1\24\1\27\3\uffff\1\37\1"
        u"\40\1\41\1\42\7\uffff\1\57\5\uffff\1\73\4\uffff\1\124\4\uffff\1"
        u"\133\1\134\1\uffff\1\135\1\1\1\uffff\1\124\1\3\1\100\1\4\26\uffff"
        u"\1\23\1\24\1\27\4\uffff\1\37\1\40\1\41\1\42\1\61\1\43\1\44\1\132"
        u"\1\54\1\64\1\51\1\45\1\52\1\65\1\55\1\46\1\136\1\62\1\137\1\47"
        u"\1\63\1\50\1\70\1\75\1\56\1\57\1\101\1\60\1\uffff\1\104\1\102\1"
        u"\uffff\1\105\1\103\1\71\1\77\1\74\1\72\1\76\1\73\3\uffff\1\125"
        u"\1\126\1\127\1\130\2\uffff\1\133\1\134\1\140\23\uffff\1\112\5\uffff"
        u"\1\116\3\uffff\1\33\3\uffff\1\66\1\106\1\67\1\107\3\uffff\1\131"
        u"\24\uffff\1\15\2\uffff\1\117\4\uffff\1\34\6\uffff\1\30\1\uffff"
        u"\1\113\6\uffff\1\7\4\uffff\1\12\1\110\2\uffff\1\13\1\16\10\uffff"
        u"\1\120\5\uffff\1\14\10\uffff\1\31\1\17\2\uffff\1\26\3\uffff\1\115"
        u"\1\122\1\uffff\1\5\1\25\1\6\1\114\1\21\1\53\1\uffff\1\123\1\11"
        u"\2\uffff\1\20\3\uffff\1\36\1\2\3\uffff\1\111\2\uffff\1\10\1\32"
        u"\1\121\1\22\1\35"
        )

    DFA38_special = DFA.unpack(
        u"\u012b\uffff"
        )

            
    DFA38_transition = [
        DFA.unpack(u"\6\65\2\62\1\65\2\62\22\65\1\62\1\43\1\57\1\64\1\55"
        u"\1\40\1\41\1\56\1\27\1\30\1\33\1\35\1\3\1\36\1\34\1\37\1\60\11"
        u"\61\1\23\1\1\1\44\1\4\1\45\1\50\1\65\4\55\1\26\3\55\1\24\2\55\1"
        u"\54\2\55\1\25\3\55\1\11\7\55\1\31\1\63\1\32\1\46\1\55\1\65\1\7"
        u"\1\53\1\13\1\17\1\5\1\16\1\52\1\55\1\14\2\55\1\15\5\55\1\10\1\6"
        u"\1\2\1\20\1\12\1\51\3\55\1\21\1\47\1\22\1\42\uff80\65"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\67"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72"),
        DFA.unpack(u"\1\76\1\uffff\1\74\11\uffff\1\75"),
        DFA.unpack(u"\1\100\1\102\12\uffff\1\77\2\uffff\1\101"),
        DFA.unpack(u"\1\103"),
        DFA.unpack(u"\1\104"),
        DFA.unpack(u"\1\105"),
        DFA.unpack(u"\1\106"),
        DFA.unpack(u"\1\107\6\uffff\1\111\6\uffff\1\110"),
        DFA.unpack(u"\1\112\7\uffff\1\113"),
        DFA.unpack(u"\1\114"),
        DFA.unpack(u"\1\115\2\uffff\1\116"),
        DFA.unpack(u"\1\120\11\uffff\1\117"),
        DFA.unpack(u"\1\121"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\125"),
        DFA.unpack(u"\1\127\4\uffff\1\126"),
        DFA.unpack(u"\1\130"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\135"),
        DFA.unpack(u"\1\137\1\uffff\12\140"),
        DFA.unpack(u"\1\143\21\uffff\1\142"),
        DFA.unpack(u"\1\145\17\uffff\1\146\1\147"),
        DFA.unpack(u"\1\151\4\uffff\1\153\15\uffff\1\152"),
        DFA.unpack(u"\1\155"),
        DFA.unpack(u"\1\160\26\uffff\1\157"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\163"),
        DFA.unpack(u"\1\165\1\166"),
        DFA.unpack(u"\1\171\1\170"),
        DFA.unpack(u"\1\173"),
        DFA.unpack(u"\1\176\76\uffff\1\175"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0081"),
        DFA.unpack(u"\1\u0082"),
        DFA.unpack(u"\1\u0083"),
        DFA.unpack(u"\1\u0085\4\uffff\1\u0084"),
        DFA.unpack(u""),
        DFA.unpack(u"\47\u0084\1\uffff\uffd7\u0084"),
        DFA.unpack(u"\uffff\u0085"),
        DFA.unpack(u"\1\140\1\uffff\10\u0088\2\140\12\uffff\3\140\21\uffff"
        u"\1\u0086\13\uffff\3\140\21\uffff\1\u0086"),
        DFA.unpack(u"\1\140\1\uffff\12\u0089\12\uffff\3\140\35\uffff\3\140"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\uffff\u008c"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u008d"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u008e"),
        DFA.unpack(u"\1\u008f"),
        DFA.unpack(u"\1\u0090"),
        DFA.unpack(u"\1\u0092\20\uffff\1\u0091"),
        DFA.unpack(u"\1\u0093"),
        DFA.unpack(u"\1\u0094"),
        DFA.unpack(u"\1\u0095\22\uffff\1\u0096"),
        DFA.unpack(u"\1\u0097"),
        DFA.unpack(u"\1\u0098\14\uffff\1\u0099"),
        DFA.unpack(u"\1\u009a"),
        DFA.unpack(u"\1\u009c\2\uffff\1\u009b"),
        DFA.unpack(u"\1\u009d"),
        DFA.unpack(u"\1\u009e"),
        DFA.unpack(u"\1\u009f"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00a1"),
        DFA.unpack(u"\1\u00a2"),
        DFA.unpack(u"\1\u00a3"),
        DFA.unpack(u"\1\u00a4"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\24\70\1\u00a5\5\70"),
        DFA.unpack(u"\1\u00a7"),
        DFA.unpack(u"\1\u00a8\11\uffff\1\u00a9"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00ab"),
        DFA.unpack(u"\1\u00ac"),
        DFA.unpack(u"\1\u00ad"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00ae"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00b0"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00b2"),
        DFA.unpack(u"\1\u00b3"),
        DFA.unpack(u"\1\u00b4"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\140\1\uffff\10\u0088\2\140\12\uffff\3\140\35\uffff"
        u"\3\140"),
        DFA.unpack(u"\1\140\1\uffff\12\u0089\12\uffff\3\140\35\uffff\3\140"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00b6"),
        DFA.unpack(u"\1\u00b7"),
        DFA.unpack(u"\1\u00b8"),
        DFA.unpack(u"\1\u00b9"),
        DFA.unpack(u"\1\u00ba"),
        DFA.unpack(u"\1\u00bb"),
        DFA.unpack(u"\1\u00bc"),
        DFA.unpack(u"\1\u00bd"),
        DFA.unpack(u"\1\u00be"),
        DFA.unpack(u"\1\u00bf"),
        DFA.unpack(u"\1\u00c0"),
        DFA.unpack(u"\1\u00c1"),
        DFA.unpack(u"\1\u00c2"),
        DFA.unpack(u"\1\u00c3"),
        DFA.unpack(u"\1\u00c4"),
        DFA.unpack(u"\1\u00c5"),
        DFA.unpack(u"\1\u00c6"),
        DFA.unpack(u"\1\u00c8\1\u00c7"),
        DFA.unpack(u"\1\u00c9"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00cb"),
        DFA.unpack(u"\1\u00cc"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00ce"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00cf"),
        DFA.unpack(u"\1\u00d0"),
        DFA.unpack(u"\1\u00d1"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00d3"),
        DFA.unpack(u"\1\u00d4"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00d5"),
        DFA.unpack(u"\1\u00d6"),
        DFA.unpack(u"\1\u00d7"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00d8"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00da"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00dc"),
        DFA.unpack(u"\1\u00dd"),
        DFA.unpack(u"\1\u00de"),
        DFA.unpack(u"\1\u00df"),
        DFA.unpack(u"\1\u00e0"),
        DFA.unpack(u"\1\u00e1"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00e3"),
        DFA.unpack(u"\1\u00e4"),
        DFA.unpack(u"\1\u00e5"),
        DFA.unpack(u"\1\u00e6"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00e9"),
        DFA.unpack(u"\1\u00ea"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00ed"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00ee"),
        DFA.unpack(u"\1\u00ef"),
        DFA.unpack(u"\1\u00f0"),
        DFA.unpack(u"\1\u00f1"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00f2"),
        DFA.unpack(u"\1\u00f3"),
        DFA.unpack(u"\1\u00f4"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00f6"),
        DFA.unpack(u"\1\u00f7"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00f8"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00f9"),
        DFA.unpack(u"\1\u00fa"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u00fc"),
        DFA.unpack(u"\1\u00fd"),
        DFA.unpack(u"\1\u00fe"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00ff"),
        DFA.unpack(u"\1\u0100"),
        DFA.unpack(u"\1\u0101"),
        DFA.unpack(u"\1\u0102"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0103"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u0106"),
        DFA.unpack(u"\1\u0107"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u0109"),
        DFA.unpack(u"\1\u010a"),
        DFA.unpack(u"\1\u010b"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u010e"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u0115"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u0118"),
        DFA.unpack(u"\1\u0119"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u011b"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u011c"),
        DFA.unpack(u"\1\u011d"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0120"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0121"),
        DFA.unpack(u"\1\u0122"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\u0124"),
        DFA.unpack(u"\1\u0125"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u"\1\70\13\uffff\12\70\7\uffff\32\70\4\uffff\1\70\1\uffff"
        u"\32\70"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #38

    DFA38 = DFA
 


# $ANTLR 3.0.1 C.g 2008-01-28 19:51:32

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
T109=109
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
T108=108
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
Tokens=110
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
        self.dfa27 = self.DFA27(
            self, 27,
            eot = self.DFA27_eot,
            eof = self.DFA27_eof,
            min = self.DFA27_min,
            max = self.DFA27_max,
            accept = self.DFA27_accept,
            special = self.DFA27_special,
            transition = self.DFA27_transition
            )
        self.dfa37 = self.DFA37(
            self, 37,
            eot = self.DFA37_eot,
            eof = self.DFA37_eof,
            min = self.DFA37_min,
            max = self.DFA37_max,
            accept = self.DFA37_accept,
            special = self.DFA37_special,
            transition = self.DFA37_transition
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

            # C.g:25:5: ( 'BOOLEAN' )
            # C.g:25:7: 'BOOLEAN'
            self.match("BOOLEAN")






        finally:

            pass

    # $ANTLR end T43



    # $ANTLR start T44
    def mT44(self, ):

        try:
            self.type = T44

            # C.g:26:5: ( '{' )
            # C.g:26:7: '{'
            self.match(u'{')





        finally:

            pass

    # $ANTLR end T44



    # $ANTLR start T45
    def mT45(self, ):

        try:
            self.type = T45

            # C.g:27:5: ( '}' )
            # C.g:27:7: '}'
            self.match(u'}')





        finally:

            pass

    # $ANTLR end T45



    # $ANTLR start T46
    def mT46(self, ):

        try:
            self.type = T46

            # C.g:28:5: ( 'struct' )
            # C.g:28:7: 'struct'
            self.match("struct")






        finally:

            pass

    # $ANTLR end T46



    # $ANTLR start T47
    def mT47(self, ):

        try:
            self.type = T47

            # C.g:29:5: ( 'union' )
            # C.g:29:7: 'union'
            self.match("union")






        finally:

            pass

    # $ANTLR end T47



    # $ANTLR start T48
    def mT48(self, ):

        try:
            self.type = T48

            # C.g:30:5: ( ':' )
            # C.g:30:7: ':'
            self.match(u':')





        finally:

            pass

    # $ANTLR end T48



    # $ANTLR start T49
    def mT49(self, ):

        try:
            self.type = T49

            # C.g:31:5: ( 'enum' )
            # C.g:31:7: 'enum'
            self.match("enum")






        finally:

            pass

    # $ANTLR end T49



    # $ANTLR start T50
    def mT50(self, ):

        try:
            self.type = T50

            # C.g:32:5: ( 'const' )
            # C.g:32:7: 'const'
            self.match("const")






        finally:

            pass

    # $ANTLR end T50



    # $ANTLR start T51
    def mT51(self, ):

        try:
            self.type = T51

            # C.g:33:5: ( 'volatile' )
            # C.g:33:7: 'volatile'
            self.match("volatile")






        finally:

            pass

    # $ANTLR end T51



    # $ANTLR start T52
    def mT52(self, ):

        try:
            self.type = T52

            # C.g:34:5: ( 'IN' )
            # C.g:34:7: 'IN'
            self.match("IN")






        finally:

            pass

    # $ANTLR end T52



    # $ANTLR start T53
    def mT53(self, ):

        try:
            self.type = T53

            # C.g:35:5: ( 'OUT' )
            # C.g:35:7: 'OUT'
            self.match("OUT")






        finally:

            pass

    # $ANTLR end T53



    # $ANTLR start T54
    def mT54(self, ):

        try:
            self.type = T54

            # C.g:36:5: ( 'OPTIONAL' )
            # C.g:36:7: 'OPTIONAL'
            self.match("OPTIONAL")






        finally:

            pass

    # $ANTLR end T54



    # $ANTLR start T55
    def mT55(self, ):

        try:
            self.type = T55

            # C.g:37:5: ( 'CONST' )
            # C.g:37:7: 'CONST'
            self.match("CONST")






        finally:

            pass

    # $ANTLR end T55



    # $ANTLR start T56
    def mT56(self, ):

        try:
            self.type = T56

            # C.g:38:5: ( 'EFIAPI' )
            # C.g:38:7: 'EFIAPI'
            self.match("EFIAPI")






        finally:

            pass

    # $ANTLR end T56



    # $ANTLR start T57
    def mT57(self, ):

        try:
            self.type = T57

            # C.g:39:5: ( '(' )
            # C.g:39:7: '('
            self.match(u'(')





        finally:

            pass

    # $ANTLR end T57



    # $ANTLR start T58
    def mT58(self, ):

        try:
            self.type = T58

            # C.g:40:5: ( ')' )
            # C.g:40:7: ')'
            self.match(u')')





        finally:

            pass

    # $ANTLR end T58



    # $ANTLR start T59
    def mT59(self, ):

        try:
            self.type = T59

            # C.g:41:5: ( '[' )
            # C.g:41:7: '['
            self.match(u'[')





        finally:

            pass

    # $ANTLR end T59



    # $ANTLR start T60
    def mT60(self, ):

        try:
            self.type = T60

            # C.g:42:5: ( ']' )
            # C.g:42:7: ']'
            self.match(u']')





        finally:

            pass

    # $ANTLR end T60



    # $ANTLR start T61
    def mT61(self, ):

        try:
            self.type = T61

            # C.g:43:5: ( '*' )
            # C.g:43:7: '*'
            self.match(u'*')





        finally:

            pass

    # $ANTLR end T61



    # $ANTLR start T62
    def mT62(self, ):

        try:
            self.type = T62

            # C.g:44:5: ( '...' )
            # C.g:44:7: '...'
            self.match("...")






        finally:

            pass

    # $ANTLR end T62



    # $ANTLR start T63
    def mT63(self, ):

        try:
            self.type = T63

            # C.g:45:5: ( '+' )
            # C.g:45:7: '+'
            self.match(u'+')





        finally:

            pass

    # $ANTLR end T63



    # $ANTLR start T64
    def mT64(self, ):

        try:
            self.type = T64

            # C.g:46:5: ( '-' )
            # C.g:46:7: '-'
            self.match(u'-')





        finally:

            pass

    # $ANTLR end T64



    # $ANTLR start T65
    def mT65(self, ):

        try:
            self.type = T65

            # C.g:47:5: ( '/' )
            # C.g:47:7: '/'
            self.match(u'/')





        finally:

            pass

    # $ANTLR end T65



    # $ANTLR start T66
    def mT66(self, ):

        try:
            self.type = T66

            # C.g:48:5: ( '%' )
            # C.g:48:7: '%'
            self.match(u'%')





        finally:

            pass

    # $ANTLR end T66



    # $ANTLR start T67
    def mT67(self, ):

        try:
            self.type = T67

            # C.g:49:5: ( '++' )
            # C.g:49:7: '++'
            self.match("++")






        finally:

            pass

    # $ANTLR end T67



    # $ANTLR start T68
    def mT68(self, ):

        try:
            self.type = T68

            # C.g:50:5: ( '--' )
            # C.g:50:7: '--'
            self.match("--")






        finally:

            pass

    # $ANTLR end T68



    # $ANTLR start T69
    def mT69(self, ):

        try:
            self.type = T69

            # C.g:51:5: ( 'sizeof' )
            # C.g:51:7: 'sizeof'
            self.match("sizeof")






        finally:

            pass

    # $ANTLR end T69



    # $ANTLR start T70
    def mT70(self, ):

        try:
            self.type = T70

            # C.g:52:5: ( '.' )
            # C.g:52:7: '.'
            self.match(u'.')





        finally:

            pass

    # $ANTLR end T70



    # $ANTLR start T71
    def mT71(self, ):

        try:
            self.type = T71

            # C.g:53:5: ( '->' )
            # C.g:53:7: '->'
            self.match("->")






        finally:

            pass

    # $ANTLR end T71



    # $ANTLR start T72
    def mT72(self, ):

        try:
            self.type = T72

            # C.g:54:5: ( '&' )
            # C.g:54:7: '&'
            self.match(u'&')





        finally:

            pass

    # $ANTLR end T72



    # $ANTLR start T73
    def mT73(self, ):

        try:
            self.type = T73

            # C.g:55:5: ( '~' )
            # C.g:55:7: '~'
            self.match(u'~')





        finally:

            pass

    # $ANTLR end T73



    # $ANTLR start T74
    def mT74(self, ):

        try:
            self.type = T74

            # C.g:56:5: ( '!' )
            # C.g:56:7: '!'
            self.match(u'!')





        finally:

            pass

    # $ANTLR end T74



    # $ANTLR start T75
    def mT75(self, ):

        try:
            self.type = T75

            # C.g:57:5: ( '*=' )
            # C.g:57:7: '*='
            self.match("*=")






        finally:

            pass

    # $ANTLR end T75



    # $ANTLR start T76
    def mT76(self, ):

        try:
            self.type = T76

            # C.g:58:5: ( '/=' )
            # C.g:58:7: '/='
            self.match("/=")






        finally:

            pass

    # $ANTLR end T76



    # $ANTLR start T77
    def mT77(self, ):

        try:
            self.type = T77

            # C.g:59:5: ( '%=' )
            # C.g:59:7: '%='
            self.match("%=")






        finally:

            pass

    # $ANTLR end T77



    # $ANTLR start T78
    def mT78(self, ):

        try:
            self.type = T78

            # C.g:60:5: ( '+=' )
            # C.g:60:7: '+='
            self.match("+=")






        finally:

            pass

    # $ANTLR end T78



    # $ANTLR start T79
    def mT79(self, ):

        try:
            self.type = T79

            # C.g:61:5: ( '-=' )
            # C.g:61:7: '-='
            self.match("-=")






        finally:

            pass

    # $ANTLR end T79



    # $ANTLR start T80
    def mT80(self, ):

        try:
            self.type = T80

            # C.g:62:5: ( '<<=' )
            # C.g:62:7: '<<='
            self.match("<<=")






        finally:

            pass

    # $ANTLR end T80



    # $ANTLR start T81
    def mT81(self, ):

        try:
            self.type = T81

            # C.g:63:5: ( '>>=' )
            # C.g:63:7: '>>='
            self.match(">>=")






        finally:

            pass

    # $ANTLR end T81



    # $ANTLR start T82
    def mT82(self, ):

        try:
            self.type = T82

            # C.g:64:5: ( '&=' )
            # C.g:64:7: '&='
            self.match("&=")






        finally:

            pass

    # $ANTLR end T82



    # $ANTLR start T83
    def mT83(self, ):

        try:
            self.type = T83

            # C.g:65:5: ( '^=' )
            # C.g:65:7: '^='
            self.match("^=")






        finally:

            pass

    # $ANTLR end T83



    # $ANTLR start T84
    def mT84(self, ):

        try:
            self.type = T84

            # C.g:66:5: ( '|=' )
            # C.g:66:7: '|='
            self.match("|=")






        finally:

            pass

    # $ANTLR end T84



    # $ANTLR start T85
    def mT85(self, ):

        try:
            self.type = T85

            # C.g:67:5: ( '?' )
            # C.g:67:7: '?'
            self.match(u'?')





        finally:

            pass

    # $ANTLR end T85



    # $ANTLR start T86
    def mT86(self, ):

        try:
            self.type = T86

            # C.g:68:5: ( '||' )
            # C.g:68:7: '||'
            self.match("||")






        finally:

            pass

    # $ANTLR end T86



    # $ANTLR start T87
    def mT87(self, ):

        try:
            self.type = T87

            # C.g:69:5: ( '&&' )
            # C.g:69:7: '&&'
            self.match("&&")






        finally:

            pass

    # $ANTLR end T87



    # $ANTLR start T88
    def mT88(self, ):

        try:
            self.type = T88

            # C.g:70:5: ( '|' )
            # C.g:70:7: '|'
            self.match(u'|')





        finally:

            pass

    # $ANTLR end T88



    # $ANTLR start T89
    def mT89(self, ):

        try:
            self.type = T89

            # C.g:71:5: ( '^' )
            # C.g:71:7: '^'
            self.match(u'^')





        finally:

            pass

    # $ANTLR end T89



    # $ANTLR start T90
    def mT90(self, ):

        try:
            self.type = T90

            # C.g:72:5: ( '==' )
            # C.g:72:7: '=='
            self.match("==")






        finally:

            pass

    # $ANTLR end T90



    # $ANTLR start T91
    def mT91(self, ):

        try:
            self.type = T91

            # C.g:73:5: ( '!=' )
            # C.g:73:7: '!='
            self.match("!=")






        finally:

            pass

    # $ANTLR end T91



    # $ANTLR start T92
    def mT92(self, ):

        try:
            self.type = T92

            # C.g:74:5: ( '<' )
            # C.g:74:7: '<'
            self.match(u'<')





        finally:

            pass

    # $ANTLR end T92



    # $ANTLR start T93
    def mT93(self, ):

        try:
            self.type = T93

            # C.g:75:5: ( '>' )
            # C.g:75:7: '>'
            self.match(u'>')





        finally:

            pass

    # $ANTLR end T93



    # $ANTLR start T94
    def mT94(self, ):

        try:
            self.type = T94

            # C.g:76:5: ( '<=' )
            # C.g:76:7: '<='
            self.match("<=")






        finally:

            pass

    # $ANTLR end T94



    # $ANTLR start T95
    def mT95(self, ):

        try:
            self.type = T95

            # C.g:77:5: ( '>=' )
            # C.g:77:7: '>='
            self.match(">=")






        finally:

            pass

    # $ANTLR end T95



    # $ANTLR start T96
    def mT96(self, ):

        try:
            self.type = T96

            # C.g:78:5: ( '<<' )
            # C.g:78:7: '<<'
            self.match("<<")






        finally:

            pass

    # $ANTLR end T96



    # $ANTLR start T97
    def mT97(self, ):

        try:
            self.type = T97

            # C.g:79:5: ( '>>' )
            # C.g:79:7: '>>'
            self.match(">>")






        finally:

            pass

    # $ANTLR end T97



    # $ANTLR start T98
    def mT98(self, ):

        try:
            self.type = T98

            # C.g:80:5: ( 'case' )
            # C.g:80:7: 'case'
            self.match("case")






        finally:

            pass

    # $ANTLR end T98



    # $ANTLR start T99
    def mT99(self, ):

        try:
            self.type = T99

            # C.g:81:5: ( 'default' )
            # C.g:81:7: 'default'
            self.match("default")






        finally:

            pass

    # $ANTLR end T99



    # $ANTLR start T100
    def mT100(self, ):

        try:
            self.type = T100

            # C.g:82:6: ( 'if' )
            # C.g:82:8: 'if'
            self.match("if")






        finally:

            pass

    # $ANTLR end T100



    # $ANTLR start T101
    def mT101(self, ):

        try:
            self.type = T101

            # C.g:83:6: ( 'else' )
            # C.g:83:8: 'else'
            self.match("else")






        finally:

            pass

    # $ANTLR end T101



    # $ANTLR start T102
    def mT102(self, ):

        try:
            self.type = T102

            # C.g:84:6: ( 'switch' )
            # C.g:84:8: 'switch'
            self.match("switch")






        finally:

            pass

    # $ANTLR end T102



    # $ANTLR start T103
    def mT103(self, ):

        try:
            self.type = T103

            # C.g:85:6: ( 'while' )
            # C.g:85:8: 'while'
            self.match("while")






        finally:

            pass

    # $ANTLR end T103



    # $ANTLR start T104
    def mT104(self, ):

        try:
            self.type = T104

            # C.g:86:6: ( 'do' )
            # C.g:86:8: 'do'
            self.match("do")






        finally:

            pass

    # $ANTLR end T104



    # $ANTLR start T105
    def mT105(self, ):

        try:
            self.type = T105

            # C.g:87:6: ( 'for' )
            # C.g:87:8: 'for'
            self.match("for")






        finally:

            pass

    # $ANTLR end T105



    # $ANTLR start T106
    def mT106(self, ):

        try:
            self.type = T106

            # C.g:88:6: ( 'goto' )
            # C.g:88:8: 'goto'
            self.match("goto")






        finally:

            pass

    # $ANTLR end T106



    # $ANTLR start T107
    def mT107(self, ):

        try:
            self.type = T107

            # C.g:89:6: ( 'continue' )
            # C.g:89:8: 'continue'
            self.match("continue")






        finally:

            pass

    # $ANTLR end T107



    # $ANTLR start T108
    def mT108(self, ):

        try:
            self.type = T108

            # C.g:90:6: ( 'break' )
            # C.g:90:8: 'break'
            self.match("break")






        finally:

            pass

    # $ANTLR end T108



    # $ANTLR start T109
    def mT109(self, ):

        try:
            self.type = T109

            # C.g:91:6: ( 'return' )
            # C.g:91:8: 'return'
            self.match("return")






        finally:

            pass

    # $ANTLR end T109



    # $ANTLR start IDENTIFIER
    def mIDENTIFIER(self, ):

        try:
            self.type = IDENTIFIER

            # C.g:493:2: ( LETTER ( LETTER | '0' .. '9' )* )
            # C.g:493:4: LETTER ( LETTER | '0' .. '9' )*
            self.mLETTER()

            # C.g:493:11: ( LETTER | '0' .. '9' )*
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
            # C.g:498:2: ( '$' | 'A' .. 'Z' | 'a' .. 'z' | '_' )
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

            # C.g:505:5: ( ( 'L' )? '\\'' ( EscapeSequence | ~ ( '\\'' | '\\\\' ) ) '\\'' )
            # C.g:505:9: ( 'L' )? '\\'' ( EscapeSequence | ~ ( '\\'' | '\\\\' ) ) '\\''
            # C.g:505:9: ( 'L' )?
            alt2 = 2
            LA2_0 = self.input.LA(1)

            if (LA2_0 == u'L') :
                alt2 = 1
            if alt2 == 1:
                # C.g:505:10: 'L'
                self.match(u'L')




            self.match(u'\'')

            # C.g:505:21: ( EscapeSequence | ~ ( '\\'' | '\\\\' ) )
            alt3 = 2
            LA3_0 = self.input.LA(1)

            if (LA3_0 == u'\\') :
                alt3 = 1
            elif ((u'\u0000' <= LA3_0 <= u'&') or (u'(' <= LA3_0 <= u'[') or (u']' <= LA3_0 <= u'\uFFFE')) :
                alt3 = 2
            else:
                nvae = NoViableAltException("505:21: ( EscapeSequence | ~ ( '\\'' | '\\\\' ) )", 3, 0, self.input)

                raise nvae

            if alt3 == 1:
                # C.g:505:23: EscapeSequence
                self.mEscapeSequence()



            elif alt3 == 2:
                # C.g:505:40: ~ ( '\\'' | '\\\\' )
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

            # C.g:509:5: ( ( 'L' )? '\"' ( EscapeSequence | ~ ( '\\\\' | '\"' ) )* '\"' )
            # C.g:509:8: ( 'L' )? '\"' ( EscapeSequence | ~ ( '\\\\' | '\"' ) )* '\"'
            # C.g:509:8: ( 'L' )?
            alt4 = 2
            LA4_0 = self.input.LA(1)

            if (LA4_0 == u'L') :
                alt4 = 1
            if alt4 == 1:
                # C.g:509:9: 'L'
                self.match(u'L')




            self.match(u'"')

            # C.g:509:19: ( EscapeSequence | ~ ( '\\\\' | '\"' ) )*
            while True: #loop5
                alt5 = 3
                LA5_0 = self.input.LA(1)

                if (LA5_0 == u'\\') :
                    alt5 = 1
                elif ((u'\u0000' <= LA5_0 <= u'!') or (u'#' <= LA5_0 <= u'[') or (u']' <= LA5_0 <= u'\uFFFE')) :
                    alt5 = 2


                if alt5 == 1:
                    # C.g:509:21: EscapeSequence
                    self.mEscapeSequence()



                elif alt5 == 2:
                    # C.g:509:38: ~ ( '\\\\' | '\"' )
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

            # C.g:512:13: ( '0' ( 'x' | 'X' ) ( HexDigit )+ ( IntegerTypeSuffix )? )
            # C.g:512:15: '0' ( 'x' | 'X' ) ( HexDigit )+ ( IntegerTypeSuffix )?
            self.match(u'0')

            if self.input.LA(1) == u'X' or self.input.LA(1) == u'x':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse


            # C.g:512:29: ( HexDigit )+
            cnt6 = 0
            while True: #loop6
                alt6 = 2
                LA6_0 = self.input.LA(1)

                if ((u'0' <= LA6_0 <= u'9') or (u'A' <= LA6_0 <= u'F') or (u'a' <= LA6_0 <= u'f')) :
                    alt6 = 1


                if alt6 == 1:
                    # C.g:512:29: HexDigit
                    self.mHexDigit()



                else:
                    if cnt6 >= 1:
                        break #loop6

                    eee = EarlyExitException(6, self.input)
                    raise eee

                cnt6 += 1


            # C.g:512:39: ( IntegerTypeSuffix )?
            alt7 = 2
            LA7_0 = self.input.LA(1)

            if (LA7_0 == u'L' or LA7_0 == u'U' or LA7_0 == u'l' or LA7_0 == u'u') :
                alt7 = 1
            if alt7 == 1:
                # C.g:512:39: IntegerTypeSuffix
                self.mIntegerTypeSuffix()








        finally:

            pass

    # $ANTLR end HEX_LITERAL



    # $ANTLR start DECIMAL_LITERAL
    def mDECIMAL_LITERAL(self, ):

        try:
            self.type = DECIMAL_LITERAL

            # C.g:514:17: ( ( '0' | '1' .. '9' ( '0' .. '9' )* ) ( IntegerTypeSuffix )? )
            # C.g:514:19: ( '0' | '1' .. '9' ( '0' .. '9' )* ) ( IntegerTypeSuffix )?
            # C.g:514:19: ( '0' | '1' .. '9' ( '0' .. '9' )* )
            alt9 = 2
            LA9_0 = self.input.LA(1)

            if (LA9_0 == u'0') :
                alt9 = 1
            elif ((u'1' <= LA9_0 <= u'9')) :
                alt9 = 2
            else:
                nvae = NoViableAltException("514:19: ( '0' | '1' .. '9' ( '0' .. '9' )* )", 9, 0, self.input)

                raise nvae

            if alt9 == 1:
                # C.g:514:20: '0'
                self.match(u'0')



            elif alt9 == 2:
                # C.g:514:26: '1' .. '9' ( '0' .. '9' )*
                self.matchRange(u'1', u'9')

                # C.g:514:35: ( '0' .. '9' )*
                while True: #loop8
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if ((u'0' <= LA8_0 <= u'9')) :
                        alt8 = 1


                    if alt8 == 1:
                        # C.g:514:35: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        break #loop8





            # C.g:514:46: ( IntegerTypeSuffix )?
            alt10 = 2
            LA10_0 = self.input.LA(1)

            if (LA10_0 == u'L' or LA10_0 == u'U' or LA10_0 == u'l' or LA10_0 == u'u') :
                alt10 = 1
            if alt10 == 1:
                # C.g:514:46: IntegerTypeSuffix
                self.mIntegerTypeSuffix()








        finally:

            pass

    # $ANTLR end DECIMAL_LITERAL



    # $ANTLR start OCTAL_LITERAL
    def mOCTAL_LITERAL(self, ):

        try:
            self.type = OCTAL_LITERAL

            # C.g:516:15: ( '0' ( '0' .. '7' )+ ( IntegerTypeSuffix )? )
            # C.g:516:17: '0' ( '0' .. '7' )+ ( IntegerTypeSuffix )?
            self.match(u'0')

            # C.g:516:21: ( '0' .. '7' )+
            cnt11 = 0
            while True: #loop11
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if ((u'0' <= LA11_0 <= u'7')) :
                    alt11 = 1


                if alt11 == 1:
                    # C.g:516:22: '0' .. '7'
                    self.matchRange(u'0', u'7')



                else:
                    if cnt11 >= 1:
                        break #loop11

                    eee = EarlyExitException(11, self.input)
                    raise eee

                cnt11 += 1


            # C.g:516:33: ( IntegerTypeSuffix )?
            alt12 = 2
            LA12_0 = self.input.LA(1)

            if (LA12_0 == u'L' or LA12_0 == u'U' or LA12_0 == u'l' or LA12_0 == u'u') :
                alt12 = 1
            if alt12 == 1:
                # C.g:516:33: IntegerTypeSuffix
                self.mIntegerTypeSuffix()








        finally:

            pass

    # $ANTLR end OCTAL_LITERAL



    # $ANTLR start HexDigit
    def mHexDigit(self, ):

        try:
            # C.g:519:10: ( ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' ) )
            # C.g:519:12: ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' )
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
            # C.g:523:2: ( ( 'u' | 'U' )? ( 'l' | 'L' ) | ( 'u' | 'U' ) ( 'l' | 'L' )? | 'ULL' )
            alt15 = 3
            LA15 = self.input.LA(1)
            if LA15 == u'U':
                LA15 = self.input.LA(2)
                if LA15 == u'L':
                    LA15_4 = self.input.LA(3)

                    if (LA15_4 == u'L') :
                        alt15 = 3
                    else:
                        alt15 = 1
                elif LA15 == u'l':
                    alt15 = 1
                else:
                    alt15 = 2
            elif LA15 == u'L' or LA15 == u'l':
                alt15 = 1
            elif LA15 == u'u':
                LA15_3 = self.input.LA(2)

                if (LA15_3 == u'L' or LA15_3 == u'l') :
                    alt15 = 1
                else:
                    alt15 = 2
            else:
                nvae = NoViableAltException("521:1: fragment IntegerTypeSuffix : ( ( 'u' | 'U' )? ( 'l' | 'L' ) | ( 'u' | 'U' ) ( 'l' | 'L' )? | 'ULL' );", 15, 0, self.input)

                raise nvae

            if alt15 == 1:
                # C.g:523:4: ( 'u' | 'U' )? ( 'l' | 'L' )
                # C.g:523:4: ( 'u' | 'U' )?
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




            elif alt15 == 2:
                # C.g:524:4: ( 'u' | 'U' ) ( 'l' | 'L' )?
                if self.input.LA(1) == u'U' or self.input.LA(1) == u'u':
                    self.input.consume();

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse


                # C.g:524:15: ( 'l' | 'L' )?
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







            elif alt15 == 3:
                # C.g:525:4: 'ULL'
                self.match("ULL")





        finally:

            pass

    # $ANTLR end IntegerTypeSuffix



    # $ANTLR start FLOATING_POINT_LITERAL
    def mFLOATING_POINT_LITERAL(self, ):

        try:
            self.type = FLOATING_POINT_LITERAL

            # C.g:529:5: ( ( '0' .. '9' )+ '.' ( '0' .. '9' )* ( Exponent )? ( FloatTypeSuffix )? | '.' ( '0' .. '9' )+ ( Exponent )? ( FloatTypeSuffix )? | ( '0' .. '9' )+ Exponent ( FloatTypeSuffix )? | ( '0' .. '9' )+ ( Exponent )? FloatTypeSuffix )
            alt27 = 4
            alt27 = self.dfa27.predict(self.input)
            if alt27 == 1:
                # C.g:529:9: ( '0' .. '9' )+ '.' ( '0' .. '9' )* ( Exponent )? ( FloatTypeSuffix )?
                # C.g:529:9: ( '0' .. '9' )+
                cnt16 = 0
                while True: #loop16
                    alt16 = 2
                    LA16_0 = self.input.LA(1)

                    if ((u'0' <= LA16_0 <= u'9')) :
                        alt16 = 1


                    if alt16 == 1:
                        # C.g:529:10: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        if cnt16 >= 1:
                            break #loop16

                        eee = EarlyExitException(16, self.input)
                        raise eee

                    cnt16 += 1


                self.match(u'.')

                # C.g:529:25: ( '0' .. '9' )*
                while True: #loop17
                    alt17 = 2
                    LA17_0 = self.input.LA(1)

                    if ((u'0' <= LA17_0 <= u'9')) :
                        alt17 = 1


                    if alt17 == 1:
                        # C.g:529:26: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        break #loop17


                # C.g:529:37: ( Exponent )?
                alt18 = 2
                LA18_0 = self.input.LA(1)

                if (LA18_0 == u'E' or LA18_0 == u'e') :
                    alt18 = 1
                if alt18 == 1:
                    # C.g:529:37: Exponent
                    self.mExponent()




                # C.g:529:47: ( FloatTypeSuffix )?
                alt19 = 2
                LA19_0 = self.input.LA(1)

                if (LA19_0 == u'D' or LA19_0 == u'F' or LA19_0 == u'd' or LA19_0 == u'f') :
                    alt19 = 1
                if alt19 == 1:
                    # C.g:529:47: FloatTypeSuffix
                    self.mFloatTypeSuffix()






            elif alt27 == 2:
                # C.g:530:9: '.' ( '0' .. '9' )+ ( Exponent )? ( FloatTypeSuffix )?
                self.match(u'.')

                # C.g:530:13: ( '0' .. '9' )+
                cnt20 = 0
                while True: #loop20
                    alt20 = 2
                    LA20_0 = self.input.LA(1)

                    if ((u'0' <= LA20_0 <= u'9')) :
                        alt20 = 1


                    if alt20 == 1:
                        # C.g:530:14: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        if cnt20 >= 1:
                            break #loop20

                        eee = EarlyExitException(20, self.input)
                        raise eee

                    cnt20 += 1


                # C.g:530:25: ( Exponent )?
                alt21 = 2
                LA21_0 = self.input.LA(1)

                if (LA21_0 == u'E' or LA21_0 == u'e') :
                    alt21 = 1
                if alt21 == 1:
                    # C.g:530:25: Exponent
                    self.mExponent()




                # C.g:530:35: ( FloatTypeSuffix )?
                alt22 = 2
                LA22_0 = self.input.LA(1)

                if (LA22_0 == u'D' or LA22_0 == u'F' or LA22_0 == u'd' or LA22_0 == u'f') :
                    alt22 = 1
                if alt22 == 1:
                    # C.g:530:35: FloatTypeSuffix
                    self.mFloatTypeSuffix()






            elif alt27 == 3:
                # C.g:531:9: ( '0' .. '9' )+ Exponent ( FloatTypeSuffix )?
                # C.g:531:9: ( '0' .. '9' )+
                cnt23 = 0
                while True: #loop23
                    alt23 = 2
                    LA23_0 = self.input.LA(1)

                    if ((u'0' <= LA23_0 <= u'9')) :
                        alt23 = 1


                    if alt23 == 1:
                        # C.g:531:10: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        if cnt23 >= 1:
                            break #loop23

                        eee = EarlyExitException(23, self.input)
                        raise eee

                    cnt23 += 1


                self.mExponent()

                # C.g:531:30: ( FloatTypeSuffix )?
                alt24 = 2
                LA24_0 = self.input.LA(1)

                if (LA24_0 == u'D' or LA24_0 == u'F' or LA24_0 == u'd' or LA24_0 == u'f') :
                    alt24 = 1
                if alt24 == 1:
                    # C.g:531:30: FloatTypeSuffix
                    self.mFloatTypeSuffix()






            elif alt27 == 4:
                # C.g:532:9: ( '0' .. '9' )+ ( Exponent )? FloatTypeSuffix
                # C.g:532:9: ( '0' .. '9' )+
                cnt25 = 0
                while True: #loop25
                    alt25 = 2
                    LA25_0 = self.input.LA(1)

                    if ((u'0' <= LA25_0 <= u'9')) :
                        alt25 = 1


                    if alt25 == 1:
                        # C.g:532:10: '0' .. '9'
                        self.matchRange(u'0', u'9')



                    else:
                        if cnt25 >= 1:
                            break #loop25

                        eee = EarlyExitException(25, self.input)
                        raise eee

                    cnt25 += 1


                # C.g:532:21: ( Exponent )?
                alt26 = 2
                LA26_0 = self.input.LA(1)

                if (LA26_0 == u'E' or LA26_0 == u'e') :
                    alt26 = 1
                if alt26 == 1:
                    # C.g:532:21: Exponent
                    self.mExponent()




                self.mFloatTypeSuffix()




        finally:

            pass

    # $ANTLR end FLOATING_POINT_LITERAL



    # $ANTLR start Exponent
    def mExponent(self, ):

        try:
            # C.g:536:10: ( ( 'e' | 'E' ) ( '+' | '-' )? ( '0' .. '9' )+ )
            # C.g:536:12: ( 'e' | 'E' ) ( '+' | '-' )? ( '0' .. '9' )+
            if self.input.LA(1) == u'E' or self.input.LA(1) == u'e':
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse


            # C.g:536:22: ( '+' | '-' )?
            alt28 = 2
            LA28_0 = self.input.LA(1)

            if (LA28_0 == u'+' or LA28_0 == u'-') :
                alt28 = 1
            if alt28 == 1:
                # C.g:
                if self.input.LA(1) == u'+' or self.input.LA(1) == u'-':
                    self.input.consume();

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse





            # C.g:536:33: ( '0' .. '9' )+
            cnt29 = 0
            while True: #loop29
                alt29 = 2
                LA29_0 = self.input.LA(1)

                if ((u'0' <= LA29_0 <= u'9')) :
                    alt29 = 1


                if alt29 == 1:
                    # C.g:536:34: '0' .. '9'
                    self.matchRange(u'0', u'9')



                else:
                    if cnt29 >= 1:
                        break #loop29

                    eee = EarlyExitException(29, self.input)
                    raise eee

                cnt29 += 1






        finally:

            pass

    # $ANTLR end Exponent



    # $ANTLR start FloatTypeSuffix
    def mFloatTypeSuffix(self, ):

        try:
            # C.g:539:17: ( ( 'f' | 'F' | 'd' | 'D' ) )
            # C.g:539:19: ( 'f' | 'F' | 'd' | 'D' )
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
            # C.g:543:5: ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) | OctalEscape )
            alt30 = 2
            LA30_0 = self.input.LA(1)

            if (LA30_0 == u'\\') :
                LA30_1 = self.input.LA(2)

                if (LA30_1 == u'"' or LA30_1 == u'\'' or LA30_1 == u'\\' or LA30_1 == u'b' or LA30_1 == u'f' or LA30_1 == u'n' or LA30_1 == u'r' or LA30_1 == u't') :
                    alt30 = 1
                elif ((u'0' <= LA30_1 <= u'7')) :
                    alt30 = 2
                else:
                    nvae = NoViableAltException("541:1: fragment EscapeSequence : ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) | OctalEscape );", 30, 1, self.input)

                    raise nvae

            else:
                nvae = NoViableAltException("541:1: fragment EscapeSequence : ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) | OctalEscape );", 30, 0, self.input)

                raise nvae

            if alt30 == 1:
                # C.g:543:8: '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' )
                self.match(u'\\')

                if self.input.LA(1) == u'"' or self.input.LA(1) == u'\'' or self.input.LA(1) == u'\\' or self.input.LA(1) == u'b' or self.input.LA(1) == u'f' or self.input.LA(1) == u'n' or self.input.LA(1) == u'r' or self.input.LA(1) == u't':
                    self.input.consume();

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse




            elif alt30 == 2:
                # C.g:544:9: OctalEscape
                self.mOctalEscape()




        finally:

            pass

    # $ANTLR end EscapeSequence



    # $ANTLR start OctalEscape
    def mOctalEscape(self, ):

        try:
            # C.g:549:5: ( '\\\\' ( '0' .. '3' ) ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) )
            alt31 = 3
            LA31_0 = self.input.LA(1)

            if (LA31_0 == u'\\') :
                LA31_1 = self.input.LA(2)

                if ((u'0' <= LA31_1 <= u'3')) :
                    LA31_2 = self.input.LA(3)

                    if ((u'0' <= LA31_2 <= u'7')) :
                        LA31_5 = self.input.LA(4)

                        if ((u'0' <= LA31_5 <= u'7')) :
                            alt31 = 1
                        else:
                            alt31 = 2
                    else:
                        alt31 = 3
                elif ((u'4' <= LA31_1 <= u'7')) :
                    LA31_3 = self.input.LA(3)

                    if ((u'0' <= LA31_3 <= u'7')) :
                        alt31 = 2
                    else:
                        alt31 = 3
                else:
                    nvae = NoViableAltException("547:1: fragment OctalEscape : ( '\\\\' ( '0' .. '3' ) ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) );", 31, 1, self.input)

                    raise nvae

            else:
                nvae = NoViableAltException("547:1: fragment OctalEscape : ( '\\\\' ( '0' .. '3' ) ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) );", 31, 0, self.input)

                raise nvae

            if alt31 == 1:
                # C.g:549:9: '\\\\' ( '0' .. '3' ) ( '0' .. '7' ) ( '0' .. '7' )
                self.match(u'\\')

                # C.g:549:14: ( '0' .. '3' )
                # C.g:549:15: '0' .. '3'
                self.matchRange(u'0', u'3')




                # C.g:549:25: ( '0' .. '7' )
                # C.g:549:26: '0' .. '7'
                self.matchRange(u'0', u'7')




                # C.g:549:36: ( '0' .. '7' )
                # C.g:549:37: '0' .. '7'
                self.matchRange(u'0', u'7')






            elif alt31 == 2:
                # C.g:550:9: '\\\\' ( '0' .. '7' ) ( '0' .. '7' )
                self.match(u'\\')

                # C.g:550:14: ( '0' .. '7' )
                # C.g:550:15: '0' .. '7'
                self.matchRange(u'0', u'7')




                # C.g:550:25: ( '0' .. '7' )
                # C.g:550:26: '0' .. '7'
                self.matchRange(u'0', u'7')






            elif alt31 == 3:
                # C.g:551:9: '\\\\' ( '0' .. '7' )
                self.match(u'\\')

                # C.g:551:14: ( '0' .. '7' )
                # C.g:551:15: '0' .. '7'
                self.matchRange(u'0', u'7')







        finally:

            pass

    # $ANTLR end OctalEscape



    # $ANTLR start UnicodeEscape
    def mUnicodeEscape(self, ):

        try:
            # C.g:556:5: ( '\\\\' 'u' HexDigit HexDigit HexDigit HexDigit )
            # C.g:556:9: '\\\\' 'u' HexDigit HexDigit HexDigit HexDigit
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

            # C.g:559:5: ( ( ' ' | '\\r' | '\\t' | '\\u000C' | '\\n' ) )
            # C.g:559:8: ( ' ' | '\\r' | '\\t' | '\\u000C' | '\\n' )
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

            # C.g:563:5: ( ( '\\\\' ) )
            # C.g:563:7: ( '\\\\' )
            # C.g:563:7: ( '\\\\' )
            # C.g:563:8: '\\\\'
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

            # C.g:571:5: ( '\\u0003' .. '\\uFFFE' )
            # C.g:571:7: '\\u0003' .. '\\uFFFE'
            self.matchRange(u'\u0003', u'\uFFFE')





        finally:

            pass

    # $ANTLR end UnicodeVocabulary



    # $ANTLR start COMMENT
    def mCOMMENT(self, ):

        try:
            self.type = COMMENT

            # C.g:574:5: ( '/*' ( options {greedy=false; } : . )* '*/' )
            # C.g:574:9: '/*' ( options {greedy=false; } : . )* '*/'
            self.match("/*")


            # C.g:574:14: ( options {greedy=false; } : . )*
            while True: #loop32
                alt32 = 2
                LA32_0 = self.input.LA(1)

                if (LA32_0 == u'*') :
                    LA32_1 = self.input.LA(2)

                    if (LA32_1 == u'/') :
                        alt32 = 2
                    elif ((u'\u0000' <= LA32_1 <= u'.') or (u'0' <= LA32_1 <= u'\uFFFE')) :
                        alt32 = 1


                elif ((u'\u0000' <= LA32_0 <= u')') or (u'+' <= LA32_0 <= u'\uFFFE')) :
                    alt32 = 1


                if alt32 == 1:
                    # C.g:574:42: .
                    self.matchAny()



                else:
                    break #loop32


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

            # C.g:579:5: ( '//' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' )
            # C.g:579:7: '//' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
            self.match("//")


            # C.g:579:12: (~ ( '\\n' | '\\r' ) )*
            while True: #loop33
                alt33 = 2
                LA33_0 = self.input.LA(1)

                if ((u'\u0000' <= LA33_0 <= u'\t') or (u'\u000B' <= LA33_0 <= u'\f') or (u'\u000E' <= LA33_0 <= u'\uFFFE')) :
                    alt33 = 1


                if alt33 == 1:
                    # C.g:579:12: ~ ( '\\n' | '\\r' )
                    if (u'\u0000' <= self.input.LA(1) <= u'\t') or (u'\u000B' <= self.input.LA(1) <= u'\f') or (u'\u000E' <= self.input.LA(1) <= u'\uFFFE'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop33


            # C.g:579:26: ( '\\r' )?
            alt34 = 2
            LA34_0 = self.input.LA(1)

            if (LA34_0 == u'\r') :
                alt34 = 1
            if alt34 == 1:
                # C.g:579:26: '\\r'
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

            # C.g:584:5: ( '#' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' )
            # C.g:584:7: '#' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
            self.match(u'#')

            # C.g:584:11: (~ ( '\\n' | '\\r' ) )*
            while True: #loop35
                alt35 = 2
                LA35_0 = self.input.LA(1)

                if ((u'\u0000' <= LA35_0 <= u'\t') or (u'\u000B' <= LA35_0 <= u'\f') or (u'\u000E' <= LA35_0 <= u'\uFFFE')) :
                    alt35 = 1


                if alt35 == 1:
                    # C.g:584:11: ~ ( '\\n' | '\\r' )
                    if (u'\u0000' <= self.input.LA(1) <= u'\t') or (u'\u000B' <= self.input.LA(1) <= u'\f') or (u'\u000E' <= self.input.LA(1) <= u'\uFFFE'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop35


            # C.g:584:25: ( '\\r' )?
            alt36 = 2
            LA36_0 = self.input.LA(1)

            if (LA36_0 == u'\r') :
                alt36 = 1
            if alt36 == 1:
                # C.g:584:25: '\\r'
                self.match(u'\r')




            self.match(u'\n')

            #action start
            self.channel=HIDDEN;
            #action end




        finally:

            pass

    # $ANTLR end LINE_COMMAND



    def mTokens(self):
        # C.g:1:8: ( T25 | T26 | T27 | T28 | T29 | T30 | T31 | T32 | T33 | T34 | T35 | T36 | T37 | T38 | T39 | T40 | T41 | T42 | T43 | T44 | T45 | T46 | T47 | T48 | T49 | T50 | T51 | T52 | T53 | T54 | T55 | T56 | T57 | T58 | T59 | T60 | T61 | T62 | T63 | T64 | T65 | T66 | T67 | T68 | T69 | T70 | T71 | T72 | T73 | T74 | T75 | T76 | T77 | T78 | T79 | T80 | T81 | T82 | T83 | T84 | T85 | T86 | T87 | T88 | T89 | T90 | T91 | T92 | T93 | T94 | T95 | T96 | T97 | T98 | T99 | T100 | T101 | T102 | T103 | T104 | T105 | T106 | T107 | T108 | T109 | IDENTIFIER | CHARACTER_LITERAL | STRING_LITERAL | HEX_LITERAL | DECIMAL_LITERAL | OCTAL_LITERAL | FLOATING_POINT_LITERAL | WS | BS | UnicodeVocabulary | COMMENT | LINE_COMMENT | LINE_COMMAND )
        alt37 = 98
        alt37 = self.dfa37.predict(self.input)
        if alt37 == 1:
            # C.g:1:10: T25
            self.mT25()



        elif alt37 == 2:
            # C.g:1:14: T26
            self.mT26()



        elif alt37 == 3:
            # C.g:1:18: T27
            self.mT27()



        elif alt37 == 4:
            # C.g:1:22: T28
            self.mT28()



        elif alt37 == 5:
            # C.g:1:26: T29
            self.mT29()



        elif alt37 == 6:
            # C.g:1:30: T30
            self.mT30()



        elif alt37 == 7:
            # C.g:1:34: T31
            self.mT31()



        elif alt37 == 8:
            # C.g:1:38: T32
            self.mT32()



        elif alt37 == 9:
            # C.g:1:42: T33
            self.mT33()



        elif alt37 == 10:
            # C.g:1:46: T34
            self.mT34()



        elif alt37 == 11:
            # C.g:1:50: T35
            self.mT35()



        elif alt37 == 12:
            # C.g:1:54: T36
            self.mT36()



        elif alt37 == 13:
            # C.g:1:58: T37
            self.mT37()



        elif alt37 == 14:
            # C.g:1:62: T38
            self.mT38()



        elif alt37 == 15:
            # C.g:1:66: T39
            self.mT39()



        elif alt37 == 16:
            # C.g:1:70: T40
            self.mT40()



        elif alt37 == 17:
            # C.g:1:74: T41
            self.mT41()



        elif alt37 == 18:
            # C.g:1:78: T42
            self.mT42()



        elif alt37 == 19:
            # C.g:1:82: T43
            self.mT43()



        elif alt37 == 20:
            # C.g:1:86: T44
            self.mT44()



        elif alt37 == 21:
            # C.g:1:90: T45
            self.mT45()



        elif alt37 == 22:
            # C.g:1:94: T46
            self.mT46()



        elif alt37 == 23:
            # C.g:1:98: T47
            self.mT47()



        elif alt37 == 24:
            # C.g:1:102: T48
            self.mT48()



        elif alt37 == 25:
            # C.g:1:106: T49
            self.mT49()



        elif alt37 == 26:
            # C.g:1:110: T50
            self.mT50()



        elif alt37 == 27:
            # C.g:1:114: T51
            self.mT51()



        elif alt37 == 28:
            # C.g:1:118: T52
            self.mT52()



        elif alt37 == 29:
            # C.g:1:122: T53
            self.mT53()



        elif alt37 == 30:
            # C.g:1:126: T54
            self.mT54()



        elif alt37 == 31:
            # C.g:1:130: T55
            self.mT55()



        elif alt37 == 32:
            # C.g:1:134: T56
            self.mT56()



        elif alt37 == 33:
            # C.g:1:138: T57
            self.mT57()



        elif alt37 == 34:
            # C.g:1:142: T58
            self.mT58()



        elif alt37 == 35:
            # C.g:1:146: T59
            self.mT59()



        elif alt37 == 36:
            # C.g:1:150: T60
            self.mT60()



        elif alt37 == 37:
            # C.g:1:154: T61
            self.mT61()



        elif alt37 == 38:
            # C.g:1:158: T62
            self.mT62()



        elif alt37 == 39:
            # C.g:1:162: T63
            self.mT63()



        elif alt37 == 40:
            # C.g:1:166: T64
            self.mT64()



        elif alt37 == 41:
            # C.g:1:170: T65
            self.mT65()



        elif alt37 == 42:
            # C.g:1:174: T66
            self.mT66()



        elif alt37 == 43:
            # C.g:1:178: T67
            self.mT67()



        elif alt37 == 44:
            # C.g:1:182: T68
            self.mT68()



        elif alt37 == 45:
            # C.g:1:186: T69
            self.mT69()



        elif alt37 == 46:
            # C.g:1:190: T70
            self.mT70()



        elif alt37 == 47:
            # C.g:1:194: T71
            self.mT71()



        elif alt37 == 48:
            # C.g:1:198: T72
            self.mT72()



        elif alt37 == 49:
            # C.g:1:202: T73
            self.mT73()



        elif alt37 == 50:
            # C.g:1:206: T74
            self.mT74()



        elif alt37 == 51:
            # C.g:1:210: T75
            self.mT75()



        elif alt37 == 52:
            # C.g:1:214: T76
            self.mT76()



        elif alt37 == 53:
            # C.g:1:218: T77
            self.mT77()



        elif alt37 == 54:
            # C.g:1:222: T78
            self.mT78()



        elif alt37 == 55:
            # C.g:1:226: T79
            self.mT79()



        elif alt37 == 56:
            # C.g:1:230: T80
            self.mT80()



        elif alt37 == 57:
            # C.g:1:234: T81
            self.mT81()



        elif alt37 == 58:
            # C.g:1:238: T82
            self.mT82()



        elif alt37 == 59:
            # C.g:1:242: T83
            self.mT83()



        elif alt37 == 60:
            # C.g:1:246: T84
            self.mT84()



        elif alt37 == 61:
            # C.g:1:250: T85
            self.mT85()



        elif alt37 == 62:
            # C.g:1:254: T86
            self.mT86()



        elif alt37 == 63:
            # C.g:1:258: T87
            self.mT87()



        elif alt37 == 64:
            # C.g:1:262: T88
            self.mT88()



        elif alt37 == 65:
            # C.g:1:266: T89
            self.mT89()



        elif alt37 == 66:
            # C.g:1:270: T90
            self.mT90()



        elif alt37 == 67:
            # C.g:1:274: T91
            self.mT91()



        elif alt37 == 68:
            # C.g:1:278: T92
            self.mT92()



        elif alt37 == 69:
            # C.g:1:282: T93
            self.mT93()



        elif alt37 == 70:
            # C.g:1:286: T94
            self.mT94()



        elif alt37 == 71:
            # C.g:1:290: T95
            self.mT95()



        elif alt37 == 72:
            # C.g:1:294: T96
            self.mT96()



        elif alt37 == 73:
            # C.g:1:298: T97
            self.mT97()



        elif alt37 == 74:
            # C.g:1:302: T98
            self.mT98()



        elif alt37 == 75:
            # C.g:1:306: T99
            self.mT99()



        elif alt37 == 76:
            # C.g:1:310: T100
            self.mT100()



        elif alt37 == 77:
            # C.g:1:315: T101
            self.mT101()



        elif alt37 == 78:
            # C.g:1:320: T102
            self.mT102()



        elif alt37 == 79:
            # C.g:1:325: T103
            self.mT103()



        elif alt37 == 80:
            # C.g:1:330: T104
            self.mT104()



        elif alt37 == 81:
            # C.g:1:335: T105
            self.mT105()



        elif alt37 == 82:
            # C.g:1:340: T106
            self.mT106()



        elif alt37 == 83:
            # C.g:1:345: T107
            self.mT107()



        elif alt37 == 84:
            # C.g:1:350: T108
            self.mT108()



        elif alt37 == 85:
            # C.g:1:355: T109
            self.mT109()



        elif alt37 == 86:
            # C.g:1:360: IDENTIFIER
            self.mIDENTIFIER()



        elif alt37 == 87:
            # C.g:1:371: CHARACTER_LITERAL
            self.mCHARACTER_LITERAL()



        elif alt37 == 88:
            # C.g:1:389: STRING_LITERAL
            self.mSTRING_LITERAL()



        elif alt37 == 89:
            # C.g:1:404: HEX_LITERAL
            self.mHEX_LITERAL()



        elif alt37 == 90:
            # C.g:1:416: DECIMAL_LITERAL
            self.mDECIMAL_LITERAL()



        elif alt37 == 91:
            # C.g:1:432: OCTAL_LITERAL
            self.mOCTAL_LITERAL()



        elif alt37 == 92:
            # C.g:1:446: FLOATING_POINT_LITERAL
            self.mFLOATING_POINT_LITERAL()



        elif alt37 == 93:
            # C.g:1:469: WS
            self.mWS()



        elif alt37 == 94:
            # C.g:1:472: BS
            self.mBS()



        elif alt37 == 95:
            # C.g:1:475: UnicodeVocabulary
            self.mUnicodeVocabulary()



        elif alt37 == 96:
            # C.g:1:493: COMMENT
            self.mCOMMENT()



        elif alt37 == 97:
            # C.g:1:501: LINE_COMMENT
            self.mLINE_COMMENT()



        elif alt37 == 98:
            # C.g:1:514: LINE_COMMAND
            self.mLINE_COMMAND()








    # lookup tables for DFA #27

    DFA27_eot = DFA.unpack(
        u"\7\uffff\1\10\2\uffff"
        )

    DFA27_eof = DFA.unpack(
        u"\12\uffff"
        )

    DFA27_min = DFA.unpack(
        u"\2\56\1\uffff\1\53\2\uffff\2\60\2\uffff"
        )

    DFA27_max = DFA.unpack(
        u"\1\71\1\146\1\uffff\1\71\2\uffff\1\71\1\146\2\uffff"
        )

    DFA27_accept = DFA.unpack(
        u"\2\uffff\1\2\1\uffff\1\4\1\1\2\uffff\2\3"
        )

    DFA27_special = DFA.unpack(
        u"\12\uffff"
        )

            
    DFA27_transition = [
        DFA.unpack(u"\1\2\1\uffff\12\1"),
        DFA.unpack(u"\1\5\1\uffff\12\1\12\uffff\1\4\1\3\1\4\35\uffff\1\4"
        u"\1\3\1\4"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\6\1\uffff\1\6\2\uffff\12\7"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\7"),
        DFA.unpack(u"\12\7\12\uffff\1\11\1\uffff\1\11\35\uffff\1\11\1\uffff"
        u"\1\11"),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #27

    DFA27 = DFA
    # lookup tables for DFA #37

    DFA37_eot = DFA.unpack(
        u"\2\uffff\1\72\1\uffff\1\75\15\72\3\uffff\4\72\4\uffff\1\142\1\145"
        u"\1\150\1\154\1\160\1\162\1\165\1\uffff\1\170\1\173\1\176\1\u0080"
        u"\1\u0083\1\uffff\4\72\1\uffff\2\67\2\u008c\2\uffff\1\67\2\uffff"
        u"\1\72\4\uffff\16\72\1\u00a4\4\72\1\u00aa\3\72\3\uffff\1\u00af\4"
        u"\72\34\uffff\1\u00b5\3\uffff\1\u00b7\7\uffff\3\72\3\uffff\1\u00bb"
        u"\1\uffff\1\u008c\3\uffff\23\72\1\uffff\1\u00d0\2\72\1\u00d3\1\72"
        u"\1\uffff\4\72\1\uffff\1\u00d9\3\72\4\uffff\3\72\1\uffff\1\72\1"
        u"\u00e1\1\u00e2\7\72\1\u00ea\4\72\1\u00ef\2\72\1\u00f2\1\u00f3\1"
        u"\uffff\1\u00f4\1\72\1\uffff\5\72\1\uffff\4\72\1\u00ff\2\72\2\uffff"
        u"\5\72\1\u0107\1\72\1\uffff\4\72\1\uffff\1\u010d\1\72\3\uffff\1"
        u"\u010f\2\72\1\u0112\3\72\1\u0116\1\72\1\u0118\1\uffff\1\u0119\1"
        u"\72\1\u011b\1\u011c\1\u011d\1\u011e\1\u011f\1\uffff\1\u0120\1\72"
        u"\1\u0122\1\u0123\1\72\1\uffff\1\72\1\uffff\1\u0126\1\72\1\uffff"
        u"\3\72\1\uffff\1\u012b\2\uffff\1\u012c\6\uffff\1\72\2\uffff\2\72"
        u"\1\uffff\1\u0130\1\72\1\u0132\1\72\2\uffff\1\u0134\1\u0135\1\u0136"
        u"\1\uffff\1\u0137\1\uffff\1\u0138\5\uffff"
        )

    DFA37_eof = DFA.unpack(
        u"\u0139\uffff"
        )

    DFA37_min = DFA.unpack(
        u"\1\3\1\uffff\1\171\1\uffff\1\75\1\154\1\150\1\165\1\145\1\124\1"
        u"\157\1\141\1\146\1\157\1\154\1\145\1\156\1\117\3\uffff\1\116\1"
        u"\120\1\117\1\106\4\uffff\1\75\1\56\1\53\1\55\1\52\1\75\1\46\1\uffff"
        u"\1\75\1\74\3\75\1\uffff\1\150\1\157\1\162\1\42\1\uffff\2\0\2\56"
        u"\2\uffff\1\0\2\uffff\1\160\4\uffff\1\165\1\163\1\164\1\141\1\147"
        u"\1\157\1\151\1\164\1\147\1\101\1\151\1\156\1\163\1\141\1\44\1\164"
        u"\1\156\1\157\1\162\1\44\1\146\1\151\1\117\3\uffff\1\44\2\124\1"
        u"\116\1\111\34\uffff\1\75\3\uffff\1\75\7\uffff\1\151\1\164\1\145"
        u"\3\uffff\1\56\1\uffff\1\56\3\uffff\1\145\1\155\2\145\1\164\1\165"
        u"\1\156\1\145\1\162\1\164\1\157\1\151\1\165\1\124\1\141\1\144\1"
        u"\163\1\145\1\162\1\uffff\1\44\1\147\1\141\1\44\1\142\1\uffff\1"
        u"\141\1\157\1\151\1\114\1\uffff\1\44\1\111\1\123\1\101\4\uffff\1"
        u"\154\1\157\1\141\1\uffff\1\144\2\44\1\162\1\151\1\143\1\145\1\157"
        u"\1\164\1\143\1\44\1\163\1\162\1\111\1\164\1\44\1\164\1\151\2\44"
        u"\1\uffff\1\44\1\164\1\uffff\1\154\1\165\1\156\1\147\1\105\1\uffff"
        u"\1\117\1\124\1\120\1\145\1\44\1\153\1\145\2\uffff\1\156\1\143\1"
        u"\164\1\144\1\146\1\44\1\150\1\uffff\1\164\1\156\1\103\1\151\1\uffff"
        u"\1\44\1\156\3\uffff\1\44\1\145\1\154\1\44\1\156\1\101\1\116\1\44"
        u"\1\111\1\44\1\uffff\1\44\1\146\5\44\1\uffff\1\44\1\145\2\44\1\154"
        u"\1\uffff\1\165\1\uffff\1\44\1\164\1\uffff\1\145\1\116\1\101\1\uffff"
        u"\1\44\2\uffff\1\44\6\uffff\1\162\2\uffff\2\145\1\uffff\1\44\1\144"
        u"\1\44\1\114\2\uffff\3\44\1\uffff\1\44\1\uffff\1\44\5\uffff"
        )

    DFA37_max = DFA.unpack(
        u"\1\ufffe\1\uffff\1\171\1\uffff\1\75\1\170\1\167\1\165\1\145\1\124"
        u"\2\157\1\156\3\157\1\156\1\117\3\uffff\1\116\1\125\1\117\1\106"
        u"\4\uffff\1\75\1\71\1\75\1\76\3\75\1\uffff\2\75\1\76\1\75\1\174"
        u"\1\uffff\1\150\1\157\1\162\1\47\1\uffff\2\ufffe\1\170\1\146\2\uffff"
        u"\1\ufffe\2\uffff\1\160\4\uffff\1\165\1\163\1\164\1\162\1\172\1"
        u"\157\1\151\2\164\1\101\1\154\1\156\1\163\1\141\1\172\1\164\1\156"
        u"\1\157\1\162\1\172\1\146\1\163\1\117\3\uffff\1\172\2\124\1\116"
        u"\1\111\34\uffff\1\75\3\uffff\1\75\7\uffff\1\151\1\164\1\145\3\uffff"
        u"\1\146\1\uffff\1\146\3\uffff\1\145\1\155\2\145\1\164\1\165\1\156"
        u"\1\145\1\162\1\164\1\157\1\151\1\165\1\124\1\141\1\144\1\164\1"
        u"\145\1\162\1\uffff\1\172\1\147\1\141\1\172\1\142\1\uffff\1\141"
        u"\1\157\1\151\1\114\1\uffff\1\172\1\111\1\123\1\101\4\uffff\1\154"
        u"\1\157\1\141\1\uffff\1\144\2\172\1\162\1\151\1\143\1\145\1\157"
        u"\1\164\1\143\1\172\1\163\1\162\1\111\1\164\1\172\1\164\1\151\2"
        u"\172\1\uffff\1\172\1\164\1\uffff\1\154\1\165\1\156\1\147\1\105"
        u"\1\uffff\1\117\1\124\1\120\1\145\1\172\1\153\1\145\2\uffff\1\156"
        u"\1\143\1\164\1\144\1\146\1\172\1\150\1\uffff\1\164\1\156\1\103"
        u"\1\151\1\uffff\1\172\1\156\3\uffff\1\172\1\145\1\154\1\172\1\156"
        u"\1\101\1\116\1\172\1\111\1\172\1\uffff\1\172\1\146\5\172\1\uffff"
        u"\1\172\1\145\2\172\1\154\1\uffff\1\165\1\uffff\1\172\1\164\1\uffff"
        u"\1\145\1\116\1\101\1\uffff\1\172\2\uffff\1\172\6\uffff\1\162\2"
        u"\uffff\2\145\1\uffff\1\172\1\144\1\172\1\114\2\uffff\3\172\1\uffff"
        u"\1\172\1\uffff\1\172\5\uffff"
        )

    DFA37_accept = DFA.unpack(
        u"\1\uffff\1\1\1\uffff\1\3\16\uffff\1\24\1\25\1\30\4\uffff\1\41\1"
        u"\42\1\43\1\44\7\uffff\1\61\5\uffff\1\75\4\uffff\1\126\4\uffff\1"
        u"\135\1\136\1\uffff\1\137\1\1\1\uffff\1\126\1\3\1\102\1\4\27\uffff"
        u"\1\24\1\25\1\30\5\uffff\1\41\1\42\1\43\1\44\1\63\1\45\1\46\1\134"
        u"\1\56\1\53\1\66\1\47\1\57\1\54\1\67\1\50\1\64\1\140\1\141\1\51"
        u"\1\65\1\52\1\77\1\72\1\60\1\61\1\103\1\62\1\uffff\1\106\1\104\1"
        u"\107\1\uffff\1\105\1\73\1\101\1\76\1\74\1\100\1\75\3\uffff\1\130"
        u"\1\127\1\131\1\uffff\1\132\1\uffff\1\135\1\136\1\142\23\uffff\1"
        u"\114\5\uffff\1\120\4\uffff\1\34\4\uffff\1\70\1\110\1\71\1\111\3"
        u"\uffff\1\133\24\uffff\1\15\2\uffff\1\121\5\uffff\1\35\7\uffff\1"
        u"\31\1\115\7\uffff\1\7\4\uffff\1\12\2\uffff\1\112\1\13\1\16\12\uffff"
        u"\1\122\7\uffff\1\14\5\uffff\1\32\1\uffff\1\17\2\uffff\1\27\3\uffff"
        u"\1\37\1\uffff\1\117\1\124\1\uffff\1\5\1\6\1\26\1\21\1\55\1\116"
        u"\1\uffff\1\125\1\11\2\uffff\1\20\4\uffff\1\40\1\2\3\uffff\1\113"
        u"\1\uffff\1\23\1\uffff\1\10\1\33\1\123\1\22\1\36"
        )

    DFA37_special = DFA.unpack(
        u"\u0139\uffff"
        )

            
    DFA37_transition = [
        DFA.unpack(u"\6\67\2\64\1\67\2\64\22\67\1\64\1\45\1\61\1\66\1\57"
        u"\1\42\1\43\1\60\1\31\1\32\1\35\1\37\1\3\1\40\1\36\1\41\1\62\11"
        u"\63\1\24\1\1\1\46\1\4\1\47\1\52\1\67\1\57\1\21\1\27\1\57\1\30\3"
        u"\57\1\25\2\57\1\56\2\57\1\26\3\57\1\11\7\57\1\33\1\65\1\34\1\50"
        u"\1\57\1\67\1\7\1\55\1\13\1\17\1\5\1\16\1\54\1\57\1\14\2\57\1\15"
        u"\5\57\1\10\1\6\1\2\1\20\1\12\1\53\3\57\1\22\1\51\1\23\1\44\uff80"
        u"\67"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\71"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\74"),
        DFA.unpack(u"\1\77\1\uffff\1\76\11\uffff\1\100"),
        DFA.unpack(u"\1\103\1\102\12\uffff\1\101\2\uffff\1\104"),
        DFA.unpack(u"\1\105"),
        DFA.unpack(u"\1\106"),
        DFA.unpack(u"\1\107"),
        DFA.unpack(u"\1\110"),
        DFA.unpack(u"\1\112\6\uffff\1\113\6\uffff\1\111"),
        DFA.unpack(u"\1\114\7\uffff\1\115"),
        DFA.unpack(u"\1\116"),
        DFA.unpack(u"\1\117\2\uffff\1\120"),
        DFA.unpack(u"\1\122\11\uffff\1\121"),
        DFA.unpack(u"\1\123"),
        DFA.unpack(u"\1\124"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\130"),
        DFA.unpack(u"\1\132\4\uffff\1\131"),
        DFA.unpack(u"\1\133"),
        DFA.unpack(u"\1\134"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\141"),
        DFA.unpack(u"\1\143\1\uffff\12\144"),
        DFA.unpack(u"\1\146\21\uffff\1\147"),
        DFA.unpack(u"\1\152\17\uffff\1\153\1\151"),
        DFA.unpack(u"\1\156\4\uffff\1\157\15\uffff\1\155"),
        DFA.unpack(u"\1\161"),
        DFA.unpack(u"\1\163\26\uffff\1\164"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\167"),
        DFA.unpack(u"\1\171\1\172"),
        DFA.unpack(u"\1\174\1\175"),
        DFA.unpack(u"\1\177"),
        DFA.unpack(u"\1\u0082\76\uffff\1\u0081"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0085"),
        DFA.unpack(u"\1\u0086"),
        DFA.unpack(u"\1\u0087"),
        DFA.unpack(u"\1\u0088\4\uffff\1\u0089"),
        DFA.unpack(u""),
        DFA.unpack(u"\47\u0089\1\uffff\uffd7\u0089"),
        DFA.unpack(u"\uffff\u0088"),
        DFA.unpack(u"\1\144\1\uffff\10\u008b\2\144\12\uffff\3\144\21\uffff"
        u"\1\u008a\13\uffff\3\144\21\uffff\1\u008a"),
        DFA.unpack(u"\1\144\1\uffff\12\u008d\12\uffff\3\144\35\uffff\3\144"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\uffff\u0090"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0091"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0092"),
        DFA.unpack(u"\1\u0093"),
        DFA.unpack(u"\1\u0094"),
        DFA.unpack(u"\1\u0095\20\uffff\1\u0096"),
        DFA.unpack(u"\1\u0097\22\uffff\1\u0098"),
        DFA.unpack(u"\1\u0099"),
        DFA.unpack(u"\1\u009a"),
        DFA.unpack(u"\1\u009b"),
        DFA.unpack(u"\1\u009c\14\uffff\1\u009d"),
        DFA.unpack(u"\1\u009e"),
        DFA.unpack(u"\1\u00a0\2\uffff\1\u009f"),
        DFA.unpack(u"\1\u00a1"),
        DFA.unpack(u"\1\u00a2"),
        DFA.unpack(u"\1\u00a3"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u00a5"),
        DFA.unpack(u"\1\u00a6"),
        DFA.unpack(u"\1\u00a7"),
        DFA.unpack(u"\1\u00a8"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\24\72\1\u00a9\5\72"),
        DFA.unpack(u"\1\u00ab"),
        DFA.unpack(u"\1\u00ac\11\uffff\1\u00ad"),
        DFA.unpack(u"\1\u00ae"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u00b0"),
        DFA.unpack(u"\1\u00b1"),
        DFA.unpack(u"\1\u00b2"),
        DFA.unpack(u"\1\u00b3"),
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
        DFA.unpack(u"\1\u00b4"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00b6"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00b8"),
        DFA.unpack(u"\1\u00b9"),
        DFA.unpack(u"\1\u00ba"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\144\1\uffff\10\u008b\2\144\12\uffff\3\144\35\uffff"
        u"\3\144"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\144\1\uffff\12\u008d\12\uffff\3\144\35\uffff\3\144"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
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
        DFA.unpack(u"\1\u00c7"),
        DFA.unpack(u"\1\u00c8"),
        DFA.unpack(u"\1\u00c9"),
        DFA.unpack(u"\1\u00ca"),
        DFA.unpack(u"\1\u00cb"),
        DFA.unpack(u"\1\u00cc\1\u00cd"),
        DFA.unpack(u"\1\u00ce"),
        DFA.unpack(u"\1\u00cf"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u00d1"),
        DFA.unpack(u"\1\u00d2"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u00d4"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00d5"),
        DFA.unpack(u"\1\u00d6"),
        DFA.unpack(u"\1\u00d7"),
        DFA.unpack(u"\1\u00d8"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u00da"),
        DFA.unpack(u"\1\u00db"),
        DFA.unpack(u"\1\u00dc"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00dd"),
        DFA.unpack(u"\1\u00de"),
        DFA.unpack(u"\1\u00df"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00e0"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u00e3"),
        DFA.unpack(u"\1\u00e4"),
        DFA.unpack(u"\1\u00e5"),
        DFA.unpack(u"\1\u00e6"),
        DFA.unpack(u"\1\u00e7"),
        DFA.unpack(u"\1\u00e8"),
        DFA.unpack(u"\1\u00e9"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u00eb"),
        DFA.unpack(u"\1\u00ec"),
        DFA.unpack(u"\1\u00ed"),
        DFA.unpack(u"\1\u00ee"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u00f0"),
        DFA.unpack(u"\1\u00f1"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u00f5"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00f6"),
        DFA.unpack(u"\1\u00f7"),
        DFA.unpack(u"\1\u00f8"),
        DFA.unpack(u"\1\u00f9"),
        DFA.unpack(u"\1\u00fa"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u00fb"),
        DFA.unpack(u"\1\u00fc"),
        DFA.unpack(u"\1\u00fd"),
        DFA.unpack(u"\1\u00fe"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u0100"),
        DFA.unpack(u"\1\u0101"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0102"),
        DFA.unpack(u"\1\u0103"),
        DFA.unpack(u"\1\u0104"),
        DFA.unpack(u"\1\u0105"),
        DFA.unpack(u"\1\u0106"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u0108"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0109"),
        DFA.unpack(u"\1\u010a"),
        DFA.unpack(u"\1\u010b"),
        DFA.unpack(u"\1\u010c"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u010e"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u0110"),
        DFA.unpack(u"\1\u0111"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u0113"),
        DFA.unpack(u"\1\u0114"),
        DFA.unpack(u"\1\u0115"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u0117"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u011a"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u0121"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u0124"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0125"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u0127"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u0128"),
        DFA.unpack(u"\1\u0129"),
        DFA.unpack(u"\1\u012a"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u012d"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\u012e"),
        DFA.unpack(u"\1\u012f"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u0131"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\u0133"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\72\13\uffff\12\72\7\uffff\32\72\4\uffff\1\72\1\uffff"
        u"\32\72"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #37

    DFA37 = DFA
 


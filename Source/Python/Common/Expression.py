## @file
# This file is used to parse and evaluate expression in directive or PCD value.
#
# Copyright (c) 2010, Intel Corporation. All rights reserved.<BR>
# This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

## Import Modules
#
import re

from CommonDataClass.Exceptions import *
from Common.GlobalData import *

# Constants
TRUE    = 1
FALSE   = 0
true    = 1
false   = 0

class ValueExpression(object):
    #
    # Pattern to match $(MACRO) or gTokenSpaceGuid.gPcdCName
    #
    SymbolPattern = re.compile("("
                                 "\$\([A-Z][A-Z0-9_]*\)|\$\(\w+\.\w+\)|\w+\.\w+|"
                                 "&&|\|\||!(?!=)|"
                                 "(?<=\W)AND(?=\W)|(?<=\W)OR(?=\W)|(?<=\W)NOT(?=\W)|(?<=\W)XOR(?=\W)|"
                                 "(?<=\W)EQ(?=\W)|(?<=\W)NE(?=\W)|(?<=\W)GT(?=\W)|(?<=\W)LT(?=\W)|(?<=\W)GE(?=\W)|(?<=\W)LE(?=\W)"
                               ")")

    # Data array pattern
    DataArrayPattern = re.compile('^\{([^{}]*)\}$')

    # Logical operator mapping
    LogicalOperators = {
        '&&' : ' and ',
        '||' : ' or ',
        '!'  : ' not ',
        'AND': 'and',
        'OR' : 'or',
        'NOT': 'not',
        'XOR': '^',
        'EQ' : '==',
        'NE' : '!=',
        'GT' : '>',
        'LT' : '<',
        'GE' : '>=',
        'LE' : '<=',
    }

    ## Constructor
    #
    #   @param  Expression  The list or string of dependency expression
    #   @param  SymbolTable The type of the module using the dependency expression
    #
    def __init__(self, Expression, SymbolTable={}):
        self._Expression = Expression
        self._SymbolTable = SymbolTable
        self._Value = None
        # To support C-style and AND/OR/NOT/XOR/EQ/NE/GT/LT/GE/LE logical operators
        self._SymbolTable.update(self.LogicalOperators)

    def __str__(self):
        return self._Expression

    def __repr__(self):
        # Don't do any replacement for string
        if self._IsString():
            return self._Expression
        return self._Replace()

    def __call__(self):
        if self._Value == None:
            try:
                if not self._IsString():
                    if not self._IsByteArray():
                        self._Value = eval(self.__repr__())
                    else:
                        self._Value = self.__repr__()
                else:
                    # Don't do eval to string
                    self._Value = self.__repr__()
            except SymbolNotFound, Excpt:
                raise
            except Exception, Excpt:
                raise BadExpression("syntax error")
        return self._Value

    def _IsString(self):
        Index = 0
        if (self._Expression[0] == '"'):
            Index = 1
        elif self._Expression.startswith('L"'):
            Index = 2
        else:
            return False

        if (self._Expression[-1] != '"'):
            return False

        End = len(self._Expression) - 1
        while Index < End:
            if self._Expression[Index] == '"':
                return False

            # Ignore the escaped quotation mark \"
            if self._Expression[Index] == '\\':
                if (Index + 1) >= End:
                    return False
                elif self._Expression[Index+1] == '"':
                    Index += 1
            Index += 1
        return True
    
    def _IsByteArray(self):
        if self._Expression.startswith("{") and self._Expression.endswith("}"):
            return True
        else:
            return False

    def _Replace(self):
        Expression = self._Expression
        while True:
            Symbols = []
            for SymbolMatch in self.SymbolPattern.finditer(Expression):
                # The enclosed $() will be removed
                Symbol = SymbolMatch.group(0)
                if Symbol.startswith('$('):
                    Symbol = Symbol[2:-1]
                Symbols.append((Symbol, SymbolMatch))

            if not Symbols:
                break

            ExpressionParts = []
            Last = 0
            for Symbol,SymbolMatch in Symbols:
                if Symbol not in self._SymbolTable:
                    raise SymbolNotFound(Symbol)
    
                ExpressionParts.append(self._Expression[Last:SymbolMatch.start()])
                ExpressionParts.append(self._SymbolTable[Symbol])
                Last = SymbolMatch.end()
    
            ExpressionParts.append(self._Expression[Last:])
            Expression = ''.join(ExpressionParts)
            if Expression == self._Expression:
                # Nothing is replaced?
                break
        # 
        # Since we use python interpreter to do the evaluation, we have to convert
        # all unicode strings in the expression to python way, as the last step
        # of macro replacement
        #
        return gWideStringPattern.sub('\\1u"', Expression)

if __name__ == '__main__':
    pass


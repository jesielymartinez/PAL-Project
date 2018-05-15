##################################################################

#####
####
###### Picture Animation Language
####
#####

##### Authors:
###
#### Lexer for PAL
###3 ICOM 4036 Prof. Wilson Rivera Gallego

###################################################################

import ply.lex as lex
import decimal

# Reserved words for PAL
reserved_words = {
    'init': 'INIT',
    'createframe':'CREATEFRAME',
    'show': 'SHOW',
    'test': 'TEST',
    'changeframe': 'CHANGEFRAME',

    'setbackground': 'SETBACKGROUND',
    'movebackground': 'MOVEBACKGROUND',

    'createasset' : 'CREATEASSET',
    'moveasset': 'MOVEASSET',
    'resizeasset': 'RESIZEASSET',
    'rotateasset': 'ROTATEASSET',
    'removeasset': 'REMOVEASSET',

    'createsprite': 'CREATESPRITE',
    'changespritestate': 'CHANGESPRITESTATE',
    'movesprite': 'MOVESPRITE',
    'resizesprite': 'RESIZESPRITE',
    'rotatesprite': 'ROTATESPRITE',
    'removesprite': 'REMOVESPRITE',

    'createanimation':'CREATEANIMATION',

    'multiplier': 'MULTIPLIER',
    'relative': 'RELATIVE',
    'absolute': 'ABSOLUTE'
}

# Tokens used by PAL

tokens = ['PAREN_L','PAREN_R','COMMA', 'PERIOD', 'NUMBER','IDENTIFIER'] \
         + list(reserved_words.values())

# Rules for tokens

t_PERIOD = r'\.'
t_COMMA = r'\,'

reserved_words_map = { }
for r in reserved_words:
    reserved_words_map[r.lower()] = r


# Find the identifiers
def t_IDENTIFIER(token):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Checking the reserved words
    token.type = reserved_words.get(token.value, 'IDENTIFIER')
    return token


def t_NUMBER(token):
    r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
    token.value = decimal.Decimal(token.value)
    return token


def t_PAREN_L(t):
    r'\('
    return t


def t_PAREN_R(t):
    r'\)'
    return t


# Line numbers
def t_NLINE(token):
    r'\n+'
    token.lexer.lineno += len(token.value)
    return token


def t_WS(t):
    r' [ ]+ '

# Ignored characters
token_ignore = ' \t'


# Error handling rule
def t_error(token):
    print("Illegal character '%s'" % token.value[0], token.lineno)
    token.lexer.skip(1)


lexer = lex.lex()

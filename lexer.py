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

import lex
# Reserved words for PAL
reserved_words = {
    'buildframe':'BUILDFRAME',
    'createasset' : 'CREATEASSET',
    'filename' : 'FILENAME',
    'assetname' : 'ASSETNAME',
    'sprite':'SPRITE',
    'createanimation':'CREATEANIMATION',
    'setbackground':'SETBACKGROUND',
    'movebackground' : 'MOVEBACKGROUND',
    'moveleft':'MOVELEFT',
    'moveright':'MOVERIGHT',
    'jump':'JUMP',
    'fly':'FLY',
    'movedown':'MOVEDOWN',
    'moveup':'MOVEUP',
    'removeframe':'REMOVEFRAME',
    'removesprite':'REMOVESPRITE',
    'background' : 'BACKGROUND',
    'mode' : 'MODE',
    'value_x' : 'VALUE_X',
    'value_y' : 'VALUE_Y'
}

# Tokens used by PAL

tokens = ['PAREN_L','PAREN_R','COMMA', 'BRACKET_L', 'BRACKET_R', 'BRACE_R', 'BRACE_L', 'NUMBER', 'IDENTIFIER'] + list(reserved_words.values())

# Rules for tokens

token_paren_L = r'\('
token_paren_R = r'\)'
token_comma = r'\,'
token_bracket_L = r'\['
token_bracket_R = r'\]'
token_brace_L = r'\{'
token_brace_R = r'\}'


reserved_words_map = { }
for r in reserved_words:
    reserved_words_map[r.lower()] = r


# Find the identifiers
def token_IDENTIFIER(token):
    r'[a-zA-Z\-0-9]*'
    # CHecking the reserved words
    token.type = reserved_words.get(token.value, 'IDENTIFIER')
    return token

# String Token
def token_STRING(token):
    r'(\".*\"|\'.*\')'
    token.value = token.value[1:-1]
    return token

 # left brace
def token_BRACE_L(token):
    r'{'
    return token

# Right brace
def token_BRACE_R(token):
    r'}'
    return token
#left bracket
def token_BRACKET_L(token):
    r'['
    return token

#RIght bracket
def token_BRACKET_R(token):
    r']'
    return token
# left parenthesis
def token_PAREN_L(token):
    r'('
    return token

# Right parenthesis
def token_PAREN_R(token):
    r')'
    return token


# Line numbers
def token_NLINE(token):
    r'\n+'
    token.lexer.lineno += len(token.value)
    return token

# Ignored characters
token_ignore = ' \t\n'


# Error handling rule
def token_error(token):
    print("Illegal character. ".format(token.value[0], token.lineno))
    token.lexer.skip(1)


lexer = lex.lex()

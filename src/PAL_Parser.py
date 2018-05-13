# ##########################################
#####
#####
############ PAL Parser
#####
#####
###########################################


from src.lexer import tokens
import ply.yacc as yacc
import src.pal as pal
from src import *


def p_init_frame(p):
    'expression : INIT PAREN_L NUMBER COMMA NUMBER PAREN_R'
    if len(pal.framesArray) > 0:
        p[0] = "Initialisation already done."
    else:
        pal.animationWidth = p[3]
        pal.animationHeight = p[5]
        pal.createFrame()
        p[0] = "Frame created with index 0."


def p_create_frame(p):
    'expression : CREATEFRAME'
    pal.createFrame()
    p[0] = "Frame created with index", pal.currentFrame


def p_show(p):
    'expression : SHOW'
    print("Displaying Frame with index", pal.currentFrame)
    print("Close Preview Window to continue imputing commands.")
    pal.makeCanvas()
    p[0] = "Closed display"


def p_changeFrame(p):
    'expression : CHANGEFRAME PAREN_L NUMBER PAREN_R'
    if (int(p[3]) < 0) or (len(pal.framesArray) - 1 < int(p[3])):
        p[0] = 'Invalid index'
    else:
        pal.frameIndex = int(p[3])
        p[0] = 'Frame created with index ', pal.currentFrame


def p_SetBackground(p):
    'expression : SETBACKGROUND PAREN_L IDENTIFIER PERIOD IDENTIFIER PAREN_R'
    pal.framesArray[pal.currentFrame].setBackground(p[3] + p[4] + p[5])
    p[0] = 'Background created'


def p_MoveBackground(p):
    'expression : MOVEBACKGROUND PAREN_L NUMBER PAREN_R'
    if pal.framesArray[pal.currentFrame].background is None:
        p[0] = 'background isnt set'
    else:
        pal.framesArray[pal.currentFrame].moveBackground(int(p[3]))
        p[0] = 'Background moved'


# ---------- ASSETS ----------

def p_CreateAsset(p):
    'expression : CREATEASSET PAREN_L IDENTIFIER COMMA IDENTIFIER PERIOD IDENTIFIER PAREN_R'
    pal.framesArray[pal.currentFrame].addAsset(pal.Asset(p[5] + p[6] + p[7], p[3]))
    p[0] = 'Asset Created with name '


def p_MoveAsset(p):
    'expression : IDENTIFIER MOVEASSET PAREN_L IDENTIFIER COMMA NUMBER COMMA NUMBER PAREN_R'
    asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
    if asset is None:
        p[0] = 'Asset cant be found'
    else:
        moveMode = p[4]
        if (moveMode != "R") & (moveMode != "A"):
            p[0] = 'Invalid Option, only <R> and <A>'
        elif moveMode == "R":
            asset.move(p[6], p[8])
        else:
            asset.moveAbs(p[6], p[8])


def p_ResizeAssetAbsolute(p):
    'expression : IDENTIFIER RESIZEASSET ABSOLUTE PAREN_L NUMBER COMMA NUMBER PAREN_R'
    asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
    if asset is None:
        p[0] = 'Asset cant be found'
    else:
        asset.resizeAsset(p[5], p[7])


def p_ResizeAssetMultiplier(p):
    'expression : IDENTIFIER RESIZEASSET MULTIPLIER PAREN_L NUMBER PAREN_R'
    asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
    if asset is None:
        p[0] = 'Asset cant be found'
    else:
        asset.resizeAssetMultiplier(p[5])


def p_RotateAssetRelative(p):
    'expression : IDENTIFIER ROTATEASSET RELATIVE PAREN_L NUMBER PAREN_R'
    asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
    if asset is None:
        p[0] = 'Asset cant be found'
    else:
        asset.rotate(p[5])


def p_RotateAssetAbsolute(p):
    'expression : IDENTIFIER ROTATEASSET ABSOLUTE PAREN_L NUMBER PAREN_R'
    asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
    if asset is None:
        p[0] = 'Asset cant be found'
    else:
        asset.rotateAbs(p[5])


def p_removeAsset(p):
    'expression : IDENTIFIER REMOVEASSET'
    asset = pal.framesArray[pal.currentFrame].getAsset(p[1])
    if asset is None:
        p[0] = 'Asset cant be found'
    else:
        pal.framesArray[pal.currentFrame].unloadAsset(asset)


# ---------- SPRITES ----------

def p_CreateSprite(p):
    'expression : CREATESPRITE PAREN_L IDENTIFIER COMMA IDENTIFIER PERIOD IDENTIFIER COMMA NUMBER COMMA NUMBER PAREN_R'
    pal.framesArray[pal.currentFrame].addSprite(pal.Sprite(p[3], p[5] + p[6] + p[7], p[9], p[11]))
    p[0] = 'Sprite Created with name '


def p_ChangeSpriteState(p):
    'expression : IDENTIFIER CHANGESPRITESTATE PAREN_L NUMBER PAREN_R'
    sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
    if sprite is not None:
        if (int(p[4]) < 0) or (len(sprite.spritesArray) - 1 < int(p[4])):
            p[0] = "Invalid index"
        else:
            sprite.changeSelectedSprite(int(p[4]))
    else:
        p[0] = "Sprite can't be found"


def p_MoveSprite(p):
    'expression : IDENTIFIER MOVESPRITE PAREN_L IDENTIFIER COMMA NUMBER COMMA NUMBER PAREN_R'
    sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
    if sprite is None:
        p[0] = 'Sprite cant be found'
    else:
        if (p[4] != "R") & (p[4] != "A"):
            p[0] = 'Invalid Option, only <R> and <A>'
        elif p[4] == "R":
            sprite.move(p[6], p[8])
        else:
            sprite.moveAbs(p[6], p[8])


def p_ResizeSpriteAbsolute(p):
    'expression : IDENTIFIER RESIZESPRITE ABSOLUTE PAREN_L NUMBER COMMA NUMBER PAREN_R'
    sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
    if sprite is None:
        p[0] = 'Sprite cant be found'
    else:
        sprite.resizeAsset(p[5], p[7])


def p_ResizeSpriteMultiplier(p):
    'expression : IDENTIFIER RESIZESPRITE MULTIPLIER PAREN_L NUMBER PAREN_R'
    sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
    if sprite is None:
        p[0] = 'Sprite cant be found'
    else:
        sprite.resizeAssetMultiplier(p[5])


def p_RotateSpriteRelative(p):
    'expression : IDENTIFIER ROTATESPRITE RELATIVE PAREN_L NUMBER PAREN_R'
    sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
    if sprite is None:
        p[0] = 'Asset cant be found'
    else:
        sprite.rotate(p[5])


def p_RotateSpriteAbsolute(p):
    'expression : IDENTIFIER ROTATESPRITE ABSOLUTE PAREN_L NUMBER PAREN_R'
    sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
    if sprite is None:
        p[0] = 'Asset cant be found'
    else:
        sprite.rotateAbs(p[5])


def p_removeSprite(p):
    'expression : IDENTIFIER REMOVESPRITE'
    sprite = pal.framesArray[pal.currentFrame].getSprite(p[1])
    if sprite is None:
        p[0] = 'Asset cant be found'
    else:
        pal.framesArray[pal.currentFrame].unloadSprite(sprite)


def p_CreateAnimation(p):
    'expression : CREATEANIMATION PAREN_L NUMBER PAREN_R'
    pal.save(p[3])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)

#test
def p_test(p):
    'expression : TEST '
    parser.parse("init (500,500)")
    parser.parse("setbackground (bg.jpg)")
    parser.parse("createsprite (sprt,sprt.png,360,260)")
    parser.parse("sprt movesprite (R,-90,230)")
    parser.parse("createasset (fire,fire.png)")
    parser.parse("fire resizeasset absolute (125,125)")
    parser.parse("fire moveasset(A,300,350)")
    # parser.parse("show")
    parser.parse("createframe")
    parser.parse("sprt movesprite (R,50,0)")
    parser.parse("movebackground (-100)")
    parser.parse("fire moveasset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createframe")
    parser.parse("sprt changespritestate(1)")
    parser.parse("sprt movesprite (R,20,-15)")
    parser.parse("movebackground (-100)")
    parser.parse("fire moveasset(R,-40,0)")
    # parser.parse("show")
    parser.parse("createframe")
    parser.parse("sprt changespritestate(3)")
    parser.parse("sprt movesprite (R,30,-15)")
    parser.parse("movebackground (-100)")
    parser.parse("fire moveasset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createframe")
    parser.parse("sprt movesprite (R,35,10)")
    parser.parse("movebackground (-100)")
    parser.parse("fire moveasset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createframe")
    parser.parse("sprt changespritestate(5)")
    parser.parse("sprt movesprite (R,20,20)")
    parser.parse("movebackground (-100)")
    parser.parse("fire moveasset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createframe")
    parser.parse("sprt changespritestate(6)")
    parser.parse("sprt movesprite (R,20,0)")
    parser.parse("movebackground (-100)")
    parser.parse("fire moveasset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createframe")
    parser.parse("sprt changespritestate(10)")
    parser.parse("sprt movesprite (R,20,0)")
    parser.parse("movebackground (-50)")
    parser.parse("fire moveasset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createframe")
    parser.parse("sprt changespritestate(11)")
    parser.parse("movebackground (-50)")
    parser.parse("fire moveasset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createframe")
    parser.parse("sprt changespritestate(13)")
    parser.parse("movebackground (-50)")
    parser.parse("fire moveasset(R,-50,0)")
    # parser.parse("show")
    parser.parse("createanimation(0.25)")
    p[0] = "finished loading test"

# Build the parser
parser = yacc.yacc()


while True:
    try:
        s = input('Animate > ')
        s.lower()
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)

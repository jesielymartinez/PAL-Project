# ##########################################
#####
#####
############ PAL Parser
#####
#####
###########################################



import ply.yacc as yacc
# Importar el file con el codigo intermedio
import main

# Import of our lexer file
import lexer.py


# Inicializa el frame
def p_init_frame(p):
    'expression : BUILDFRAME PAREN_L NUMBER COMMA NUMBER PAREN_R'
    Main.framesArray.init(p[3],p[5])
    p[0] = 'Frame created'



#Crea el frame de animacion
def buildFrame():



 #Cambia el frame. Cual no sé
def changeFrame(index):
    #el indice de frame que va a cambiar
    pass




#Set Background  (le pone background al frame que está ahora mismo activo)

def SetBackground(p):
    #Recibe una imagen que será el background del frame que se crea.
    'expression : SETBACKGROUND PAREN_L BACKGROUND PAREN_R'
    Main.framesArray[Main.currentFrame].setbackground(p[3])
    p[0] = 'Background created'

#Move Background
#deltaX - int
def MoveBackground(p):
    'expression : MOVEBACKGROUND PAREN_L NUMBER PAREN_R'
    Main.framesArray[Main.currentFrame].moveBackground(int(p[3]))
    p[0] = 'Background moved'


#Create Asset
 #    - File name - string
 #    - Asset name - string
def CreateAsset(p):
    'expression: CREATEASSET PAREN_L FILENAME COMMA ASEETNAME PAREN_R'
    Main.framesArray[Main.currentFrame].addAsset(p[3], p[5])
    p[0] = 'Asset Created'

#Move Asset
 #     -Asset name - string
 ##     - Mode - string
  #    - valueX - int
 #     - valueY - int
#%assetname%
def MoveAsset(p):
    'expression: MOVEASSET PAREN-L ASSETNAME COMMA MODE COMMA VALUE_X COMMA VALUE_Y PAREN_R'
    asset = Main.framesArray[Main.currentFrame].getAsset(p[3])
    





#Resize Asset
#Asset name - string
#Mode - string
#sizeX - int
#sizeY - int
#multiplier - int
%#assetname%
def ResizeAsset(Mode<V> , sizeX , sizeY):
    pass

#%assetname%
def ResizeAsset(Mode<M> , multiplier):
    pass

Rotate Asset
      -Asset name - string
      - Mode - string
      - valueX - int
      - valueY - int
%assetname%
def RotateAsset(Mode<R,A> , valueX, valueY):
    pass


Remove Asset
      -Asset name - string
      - Mode - string
      - valueX - int
      - valueY - int
%assetname% RemoveAsset

Create Sprite
     - File name - string
     - Asset name - string
     - spriteWidth - int
     - spriteHeight - int
def CreateAsset(fileName, assetName, spriteWidth, spriteHeight)

Move Sprite
Sprite name - string
Mode - string
valueX - int
valueY - int
%spriteName% MoveSprite (Mode<R,A> , valueX, valueY)

Resize Asset
Sprite name - string
Mode - string
sizeX - int
sizeY - int
multiplier - int
%spriteName% ResizeSpritet (Mode<V> , sizeX , sizeY)
%spriteName% ResizeSprite (Mode<M> , multiplier)

Rotate Sprite
Sprite name - string
Mode - string
valueX - int
valueY - int
%spriteName% RotateSprite (Mode<R,A> , valueX, valueY)

Remove Sprite
Sprite name - string
Mode - string
valueX - int
valueY - int
%spriteName% RemoveSprite

Change Sprite State
Sprite name - string
State index - int
%spriteName% ChangeSpriteState (stateIndex)



Save
Delay between frames in GIF - float
Save (delay)




# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


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
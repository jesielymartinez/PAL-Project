import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab
import time

assetCount = -1
assetArray = []
background = None
spritesArray = []


class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.assets = []
        self.assetsLoaded = -1
        self.background = None
        self.spritesLoaded = -1
        self.sprites = []

        self.canvasView = tk.Canvas(self, height=200, width=200, bg="black"
                                    , highlightthickness=0, relief='ridge')
        self.canvasView.grid(row=0, column=0, columnspan=1, sticky='nsew')

        self.savepic = tk.Button(self, text='SAVE', command=self.save)
        self.savepic.grid(row=1, column=0, sticky='nsew')

    def save(self):
        ImageGrab.grab(bbox=self.canvas()).save("out.jpg")
        print('Screenshot of tkinter.Canvas saved in "out.jpg"')

    def canvas(self):
        print('  def _canvas(self):')
        print('self.cv.winfo_rootx() = ', self.canvasView.winfo_rootx())
        print('self.cv.winfo_rooty() = ', self.canvasView.winfo_rooty())
        print('self.cv.winfo_x() =', self.canvasView.winfo_x())
        print('self.cv.winfo_y() =', self.canvasView.winfo_y())
        print('self.cv.winfo_width() =', self.canvasView.winfo_width())
        print('self.cv.winfo_height() =', self.canvasView.winfo_height())
        x = self.canvasView.winfo_rootx() + self.canvasView.winfo_x()
        y = self.canvasView.winfo_rooty() + self.canvasView.winfo_y()
        x1 = x + self.canvasView.winfo_width()
        y1 = y + self.canvasView.winfo_height()
        box = (x, y, x1, y1)

        print('box = ', box)
        return box

    def resizeCanvas(self, width, height):
        self.canvasView.configure(width=width, height=height)

    def loadAsset(self, asset):
        self.assetsLoaded = self.assetsLoaded + 1
        self.assets.append(asset)
        asset.setPhoto(ImageTk.PhotoImage(asset.image))
        asset.setIdentifier(self.canvasView.create_image(asset.posX,
                                                         asset.posY,
                                                         image=asset.photo,
                                                         anchor='nw'))

    def unloadAsset(self, asset):
        try:
            self.assets.remove(asset)
            self.canvasView.delete(asset.canvasID)
        except:
            print("Asset not loaded:", asset)

    def setBackground(self, background):
        background.setPhoto(ImageTk.PhotoImage(background.image))
        background.setIdentifier(self.canvasView.create_image(background.posX,
                                                              background.posY,
                                                              image=background.photo,
                                                              anchor='nw'))
        self.resizeCanvas(background.centerX*2, background.centerY*2)

    def loadSprite(self, sprite):
        self.spritesLoaded = self.spritesLoaded + 1
        self.sprites.append(sprite)

        sprite.setPhoto(ImageTk.PhotoImage(sprite.spritesArray[sprite.selectedSprite]))
        sprite.setIdentifier(self.canvasView.create_image(sprite.posX,
                                                          sprite.posY,
                                                         image=sprite.photo[sprite.selectedSprite],
                                                         anchor='nw'))


class Asset():
    def __init__(self, fileName, name):
        self.name = name
        self.image = None
        self.canvasID = None
        self.centerX = None
        self.centerY = None
        self.posX = 0
        self.posY = 0
        self.photo = None
        self.load(fileName)

    def load(self, fileName):
        if isinstance(fileName, str):
            try:
                self.image = Image.open(fileName)
                self.centerX = self.image.size[0] // 2
                self.centerY = self.image.size[1] // 2
                global assetCount
                assetCount = assetCount + 1
            except FileNotFoundError:
                print("File doesn't exist or couldn't be read:", fileName)
        else:
            print("Invalid Parameter", fileName)

    def resizeAssetMultiplier(self, multiplier):
        #Cambiar a dar resize al current sprite
        self.image = self.image.resize((multiplier*self.image.size[0],
                                        multiplier*self.image.size[1]),
                                       Image.ANTIALIAS)

    def resizeAsset(self, newSizeX, newSizeY):
        #Cambiar a dar resize al current sprite
        self.image = self.image.resize((newSizeX,newSizeY), Image.ANTIALIAS)

    def move(self, deltaX, deltaY):
        self.posX = self.posX + deltaX
        self.posY = self.posY + deltaY

    def moveAbs(self, absX, absY):
        self.posX = absX
        self.posY = absY

    def unload(self):
        global assetArray
        assetArray.remove(self)
        self.image = None

    def setIdentifier(self, id):
        self.canvasID = id

    def setPhoto(self, photo):
        self.photo = photo

class Sprite:

    def __init__(self, name, fileName, spriteWidth, spriteHeight, numberOfRows, numberOfColumns):
        self.name = name
        self.fileName = fileName
        self.image = None
        self.posX = 0
        self.posY = 0
        self.centerX = None
        self.centerY = None
        self.photo = []
        self.canvasID = []
        self.spritesArray = []
        self.spriteWidth = spriteWidth
        self.spriteHeight = spriteHeight
        self.numberOfRows = numberOfRows
        self.numberOfColumns = numberOfColumns
        self.selectedSprite = 0
        self.multiplier = 1
        self.createSprites()

    def createSprites(self):
        if isinstance(self.fileName, str):
            try:
                self.image = Image.open(self.fileName)
                for i in range(1, self.numberOfRows):
                    for j in range(1, self.numberOfColumns):
                        self.spritesArray.append(self.image.crop(
                            ((i - 1) * self.spriteWidth, (j - 1) * self.spriteHeight,
                             self.spriteWidth, self.spriteHeight)
                        ))
                        self.photo.append(None)
                        self.canvasID.append(None)
            except FileNotFoundError:
                print("File doesn't exist or couldn't be read:", self.fileName)
        else:
            print("Invalid Parameter", self.fileName)

    def move(self, deltaX, deltaY):
        self.posX = self.posX + deltaX
        self.posY = self.posY + deltaY

    def moveAbs(self, absX, absY):
        self.posX = absX
        self.posY = absY

    def changeSpriteName(self, name):
        self.name = name

    def resizeSpriteMultiplier(self, multiplier):
        self.multiplier = multiplier

    def setPhoto(self, photo):
        self.photo[self.selectedSprite] = photo

    def setIdentifier(self, id):
        self.canvasID[self.selectedSprite] = id

    def unload(self):
        global spritesArray
        spritesArray.remove(self)
        self.image = None

    def getCurrentSprite(self):
        tempImage = self.spritesArray[self.selectedSprite]
        return tempImage.resize((self.multiplier*tempImage.size[0],
                                        self.multiplier*tempImage.size[1]),
                                       Image.ANTIALIAS)

    def changeSelectedSprite(self, index):
        self.selectedSprite = index

def makeCanvas():
    root = tk.Tk()
    root.title('PAL-Project')
    root.resizable(False, False)
    app = App(root)

    app.grid(row=0, column=0, columnspan=1, sticky='nsew')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=10)
    app.rowconfigure(1, weight=1)
    app.columnconfigure(0, weight=1)
    app.columnconfigure(1, weight=1)
    app.columnconfigure(2, weight=1)

    global background
    if (background != None):
        app.setBackground(background)
    global assetArray
    for a in assetArray:
        app.loadAsset(a)
    global spritesArray
    for s in spritesArray:
        app.loadSprite(s)
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    app.mainloop()


def moveAsset(assetName, deltaX, deltaY):
    for a in assetArray:
        if (a.name == assetName):
            a.move(deltaX, deltaY)
            break


def moveAssetAbs(assetName, deltaX, deltaY):
    for a in assetArray:
        if a.name == assetName:
            a.moveAbs(deltaX, deltaY)
            break


def resizeAssetMultiplier(assetName, multiplier):
    for a in assetArray:
        if (a.name == assetName):
            a.resizeAssetMultiplier(multiplier)
            break


def resizeAsset(assetName, newSizeX, newSizeY):
    for a in assetArray:
        if (a.name == assetName):
            a.resizeAsset(newSizeX, newSizeY)
            break

def moveSprite(spriteName, deltaX, deltaY):
    for s in spritesArray:
        if (s.name == spriteName):
            s.move(deltaX, deltaY)
            break


def moveSpriteAbs(spriteName, deltaX, deltaY):
    for s in spritesArray:
        if s.name == spriteName:
            s.moveAbs(deltaX, deltaY)
            break


def resizeSpriteMultiplier(spriteName, multiplier):
    for s in spritesArray:
        if (s.name == spriteName):
            s.resizeAssetMultiplier(multiplier)
            break

def changeSpriteState(spriteName,index):
    for s in spritesArray:
        if (s.name == spriteName):
            s.changeSelectedSprite(index)
            break


if __name__ == '__main__':
    while True:
        var = input("PAL CMD:")
        if var == "create":
            print("Close Preview Window to continue imputing commands.")
            makeCanvas()
        elif var == "background":
            ast = input("PAL CMD: Enter background file name:")
            background = Asset(str(ast), "background")
        elif var == "load":
            ast = input("PAL CMD: Enter asset file name:")
            astName = input("PAL CMD: Enter name for the asset:")
            assetArray.append(Asset(str(ast), astName))
        elif var == "create sprites":
            sprt = input("PAL CMD: Enter Sprite file name:")
            sprtName = input("PAL CMD: Enter Sprite name:")
            sprtWidth = input("PAL CMD: Enter Sprites width:")
            sprtHeight = input("PAL CMD: Enter Sprite height:")
            rows = input("PAL CMD: Enter number of rows:")
            columns = input("PAL CMD: Enter number of columns:")
            spritesArray.append(Sprite(sprtName,sprt, int(sprtWidth), int(sprtHeight), int(rows), int(columns)))

        elif var == "change sprite state":
            sprtName = input("PAL CMD: Enter name of the sprite:")
            index = input("PAL CMD: Enter index to change on sprite:")
            changeSpriteState(sprtName,int(index))

        elif var == "move sprite":
            moveMode = input("PAL CMD: Relative position <R>  or absolute <A>")
            while (moveMode != "R") & (moveMode != "A"):
                print("Invalid Option, only <R> and <A>")
                moveMode = input("PAL CMD: Relative position <R>  or absolute <A>")
            sprtName = input("PAL CMD: Enter name of the sprite:")

            if moveMode == "R":
                sprtDeltaX = input("PAL CMD: Enter delta X:")
                sprtDeltaY = input("PAL CMD: Enter delta Y:")
                moveSprite(sprtName, int(sprtDeltaX), int(sprtDeltaY))
            else:
                sprtAbsX = input("PAL CMD: Enter absolute X:")
                sprtAbsY = input("PAL CMD: Enter absolute Y:")
                moveSpriteAbs(sprtName, int(sprtAbsX), int(sprtAbsY))
        elif var == "resize sprite":
            sprtName = input("PAL CMD: Enter name of the sprite:")
            multiplier = input("PAL CMD: Enter multiplier:")
            resizeAssetMultiplier(sprtName, int(multiplier))

        elif var == "move":
            moveMode = input("PAL CMD: Relative position <R>  or absolute <A>")
            while (moveMode != "R") & (moveMode != "A"):
                print("Invalid Option, only <R> and <A>")
                moveMode = input("PAL CMD: Relative position <R>  or absolute <A>")
            astName = input("PAL CMD: Enter name of the asset:")

            if moveMode == "R":
                astDeltaX = input("PAL CMD: Enter delta X:")
                astDeltaY = input("PAL CMD: Enter delta Y:")
                moveAsset(astName, int(astDeltaX), int(astDeltaY))
            else:
                astAbsX = input("PAL CMD: Enter absolute X:")
                astAbsY = input("PAL CMD: Enter absolute Y:")
                moveAssetAbs(astName, int(astAbsX), int(astAbsY))
        elif var == "resize":
            moveMode = input("PAL CMD: Resize by multiplier <M>  or values <V>")
            while (moveMode != "M") & (moveMode != "V"):
                print("Invalid Option, only <M> and <V>")
                moveMode = input("PAL CMD: Relative position <R>  or absolute <A>")
            astName = input("PAL CMD: Enter name of the asset:")

            if moveMode == "M":
                multiplier = input("PAL CMD: Enter multiplier:")
                resizeAssetMultiplier(astName, int(multiplier))
            else:
                newSizeX = input("PAL CMD: Enter size in X:")
                newSizeY = input("PAL CMD: Enter size in Y:")
                resizeAsset(astName, int(newSizeX), int(newSizeY))
        else:
            print("Invalid command")

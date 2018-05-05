import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab
from copy import deepcopy
import time

framesArray = []
currentFrame = -1
animationWidth = 500
animationHeight = 500


class App(tk.Frame):
    def __init__(self, parent, initialFrame):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.assets = []
        self.background = None
        self.sprites = []
        self.frames = []
        self.canvasView = None
        self.frames.append(initialFrame)
        self.currentFrame = 0
        self.loadFrame(0)

    def loadFrame(self, index):
        self.currentFrame = index
        self.canvasView = self.frames[index].getCanvas(self.parent)
        self.canvasView.grid(row=0, column=0, columnspan=1, sticky='nsew')

    def getCurrentFrame(self):
        return self.frames[self.currentFrame]

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


class Frame():
    def __init__(self, width, height):
        self.assets = []
        self.assetsLoaded = -1
        self.sprites = []
        self.spritesLoaded = -1
        self.background = None
        self.width = width
        self.height = height
        self.canvas = None

    def getCanvas(self, parent):
        self.canvas = tk.Canvas(parent, height=self.height, width=self.width, bg="black",
                                highlightthickness=0, relief='ridge')
        self.loadBackground()
        self.loadSprites()
        self.loadAssets()
        return self.canvas

    def addAsset(self, asset):
        self.assetsLoaded = self.assetsLoaded + 1
        self.assets.append(asset)

    def loadAssets(self):
        for asset in self.assets:
            asset.setPhoto(ImageTk.PhotoImage(asset.image, name=asset.name))
            asset.setIdentifier(self.canvas.create_image(asset.posX,
                                                         asset.posY,
                                                         image=asset.photo,
                                                         anchor='nw'))

    def addSprite(self, sprite):
        self.spritesLoaded = self.spritesLoaded + 1
        self.sprites.append(sprite)

    def loadSprites(self):
        for sprite in self.sprites:
            sprite.setPhoto(ImageTk.PhotoImage(sprite.getCurrentSprite(), name=sprite.name))
            sprite.setIdentifier(self.canvas.create_image(sprite.posX, sprite.posY,
                                                          image=sprite.photo, anchor='nw'))

    def setBackground(self, background):
        self.background = background

    def loadBackground(self):
        if self.background is not None:
            self.background.setPhoto(ImageTk.PhotoImage(self.background.image))
            self.background.setIdentifier(self.canvas.create_image(self.background.posX, self.background.posY,
                                                                   image=self.background.photo,
                                                                   anchor='nw'))

    def unloadAsset(self, asset):
        try:
            self.assets.remove(asset)
        except:
            print("Asset not loaded:", asset)

    def unloadSprite(self, sprite):
        try:
            self.sprites.remove(sprite)
        except:
            print("Sprite not loaded:", sprite)

    def getAsset(self, assetName):
        asset = None
        for a in self.assets:
            if (a.name == assetName):
                asset = a
                break
        return asset

    def getSprite(self, spriteName):
        sprite = None
        for s in self.sprites:
            if s.name == spriteName:
                sprite = s
                break
        return sprite

    def moveAsset(self, assetName, deltaX, deltaY):
        for a in self.assets:
            if (a.name == assetName):
                a.move(deltaX, deltaY)
                break

    def moveAssetAbs(self, assetName, deltaX, deltaY):
        for a in self.assets:
            if a.name == assetName:
                a.moveAbs(deltaX, deltaY)
                break

    def resizeAssetMultiplier(self, assetName, multiplier):
        for a in self.assets:
            if (a.name == assetName):
                a.resizeAssetMultiplier(multiplier)
                break

    def resizeAsset(self, assetName, newSizeX, newSizeY):
        for a in self.assets:
            if (a.name == assetName):
                a.resizeAsset(newSizeX, newSizeY)
                break

    def moveSprite(self, spriteName, deltaX, deltaY):
        for s in self.sprites:
            if (s.name == spriteName):
                s.move(deltaX, deltaY)
                break

    def moveSpriteAbs(self, spriteName, deltaX, deltaY):
        for s in self.sprites:
            if s.name == spriteName:
                s.moveAbs(deltaX, deltaY)
                break

    def resizeSpriteMultiplier(self, spriteName, multiplier):
        for s in framesArray[currentFrame].sprites:
            if s.name == spriteName:
                s.resizeSpriteMultiplier(multiplier)
                break

    def changeSpriteState(self, spriteName, index):
        for s in framesArray[currentFrame].sprites:
            if s.name == spriteName:
                s.changeSelectedSprite(index)
                break

    def __deepcopy__(self, memodict={}):
        newFrame = Frame(deepcopy(self.width), deepcopy(self.height))
        newFrame.assets = deepcopy(self.assets)
        newFrame.sprites = deepcopy(self.sprites)
        newFrame.assetsLoaded = deepcopy(self.assetsLoaded)
        newFrame.spritesLoaded = deepcopy(self.spritesLoaded)
        newFrame.background = deepcopy(self.background)
        return newFrame


class Asset:
    def __init__(self, fileName, name):
        self.name = name
        self.image = None
        self.canvasID = None
        self.centerX = None
        self.centerY = None
        self.multiplier = 1
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
            except FileNotFoundError:
                print("File doesn't exist or couldn't be read:", fileName)
        else:
            print("Invalid Parameter", fileName)

    def resizeAssetMultiplier(self, multiplier):
        self.multiplier = multiplier
        self.image = self.image.resize((multiplier * self.image.size[0],
                                        multiplier * self.image.size[1]),
                                       Image.ANTIALIAS)

    def resizeAsset(self, newSizeX, newSizeY):
        self.image = self.image.resize((newSizeX, newSizeY), Image.ANTIALIAS)

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

    def __deepcopy__(self, memodict={}):
        newAsset = Asset(self.filename, deepcopy(self.name))
        newAsset.posX = deepcopy(self.posX)
        newAsset.posY = deepcopy(self.posY)
        newAsset.multiplier = deepcopy(self.multiplier)
        return newAsset


class Sprite:
    def __init__(self, name, fileName, spriteWidth, spriteHeight):
        self.name = name
        self.fileName = fileName
        self.image = None
        self.posX = 0
        self.posY = 0
        self.centerX = None
        self.centerY = None
        self.photo = None
        self.canvasID = None
        self.spritesArray = []
        self.spriteWidth = spriteWidth
        self.spriteHeight = spriteHeight
        self.selectedSprite = 0
        self.multiplier = 1
        self.createSprites()

    def createSprites(self):
        if isinstance(self.fileName, str):
            try:
                self.image = Image.open(self.fileName)
                y = 0
                while y <= self.image.size[1]:
                    x = 0
                    while x <= self.image.size[0]:
                        box = (x, y, (x + self.spriteWidth), (y + self.spriteHeight))
                        self.spritesArray.append(self.image.crop(box))
                        x = x + self.spriteWidth
                    y = y + self.spriteHeight

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
        self.photo = photo

    def setIdentifier(self, id):
        self.canvasID = id

    def unload(self):
        global spritesArray
        spritesArray.remove(self)
        self.image = None

    def getCurrentSprite(self):
        tempImage = self.spritesArray[self.selectedSprite]
        return tempImage.resize((self.multiplier * tempImage.size[0],
                                 self.multiplier * tempImage.size[1]),
                                Image.ANTIALIAS)

    def changeSelectedSprite(self, index):
        self.selectedSprite = index

    def __deepcopy__(self, memodict={}):
        newSprite = Sprite(deepcopy(self.name), deepcopy(self.fileName),
                           deepcopy(self.spriteWidth), deepcopy(self.spriteHeight))
        newSprite.posX = deepcopy(self.posX)
        newSprite.posY = deepcopy(self.posY)
        newSprite.selectedSprite = deepcopy(self.selectedSprite)
        newSprite.multiplier = deepcopy(self.multiplier)
        return newSprite


def makeCanvas():
    root = tk.Tk()
    root.title('PAL-Project')
    root.resizable(False, False)

    app = App(root, framesArray[currentFrame])
    app.grid(row=0, column=0, columnspan=1, sticky='nsew')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=10)
    app.rowconfigure(1, weight=1)
    app.columnconfigure(0, weight=1)
    app.columnconfigure(1, weight=1)
    app.columnconfigure(2, weight=1)

    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    app.mainloop()


def createFrame():
    global currentFrame
    if currentFrame != -1:
        framesArray.append(deepcopy(framesArray[currentFrame]))
    else:
        framesArray.append(Frame(animationWidth, animationHeight))
    currentFrame = currentFrame + 1
    print("Created frame with index", currentFrame)


if __name__ == '__main__':
    animationWidth = input("PAL CMD: Enter the WIDTH of the Animation:")
    animationHeight = input("PAL CMD: Enter the HEIGHT of the Animation:")
    createFrame()
    while True:
        var = input("PAL CMD:")
        if var == "show":
            print("Displaying Frame with index", currentFrame)
            print("Close Preview Window to continue imputing commands.")
            makeCanvas()
        elif var == "create frame":
            createFrame()
        elif var == "change frame":
            frameIndex = input("PAL CMD: Enter frame index:")
            currentFrame = int(frameIndex)
        elif var == "background":
            ast = input("PAL CMD: Enter background file name:")
            framesArray[currentFrame].setBackground(Asset(str(ast), "background"))
        elif var == "create asset":
            ast = input("PAL CMD: Enter asset file name:")
            astName = input("PAL CMD: Enter name for the asset:")
            framesArray[currentFrame].addAsset(Asset(str(ast), astName))
        elif var == "move asset":
            astName = input("PAL CMD: Enter name of the asset:")
            asset = framesArray[currentFrame].getAsset(astName)
            if asset is None:
                print("Asset can't be found")
            else:
                moveMode = input("PAL CMD: Relative position <R>  or absolute <A>")
                while (moveMode != "R") & (moveMode != "A"):
                    print("Invalid Option, only <R> and <A>")
                    moveMode = input("PAL CMD: Relative position <R>  or absolute <A>")
                if moveMode == "R":
                    astDeltaX = input("PAL CMD: Enter delta X:")
                    astDeltaY = input("PAL CMD: Enter delta Y:")
                    asset.move(int(astDeltaX), int(astDeltaY))
                else:
                    astAbsX = input("PAL CMD: Enter absolute X:")
                    astAbsY = input("PAL CMD: Enter absolute Y:")
                    asset.moveAbs(int(astAbsX), int(astAbsY))
        elif var == "resize asset":
            astName = input("PAL CMD: Enter name of the asset:")
            asset = framesArray[currentFrame].getAsset(astName)
            if asset is None:
                print("Asset can't be found")
            else:
                moveMode = input("PAL CMD: Resize by multiplier <M>  or values <V>")
                while (moveMode != "M") & (moveMode != "V"):
                    print("Invalid Option, only <M> and <V>")
                    moveMode = input("PAL CMD: Relative position <R>  or absolute <A>")
                if moveMode == "M":
                    multiplier = input("PAL CMD: Enter multiplier:")
                    asset.resizeAssetMultiplier(int(multiplier))
                else:
                    newSizeX = input("PAL CMD: Enter size in X:")
                    newSizeY = input("PAL CMD: Enter size in Y:")
                    asset.resizeAsset(int(newSizeX), int(newSizeY))
        elif var == "remove asset":
            astName = input("PAL CMD: Enter name of the asset:")
            asset = framesArray[currentFrame].getAsset(astName)
            if asset is None:
                print("Asset can't be found")
            else:
                framesArray[currentFrame].unloadAsset(asset)
        elif var == "create sprite":
            sprt = input("PAL CMD: Enter Sprite file name:")
            sprtName = input("PAL CMD: Enter Sprite name:")
            sprtWidth = input("PAL CMD: Enter Sprites width:")
            sprtHeight = input("PAL CMD: Enter Sprite height:")
            framesArray[currentFrame].addSprite(Sprite(sprtName, sprt, int(sprtWidth), int(sprtHeight)))
        elif var == "change sprite state":
            sprtName = input("PAL CMD: Enter name of the sprite:")
            sprite = framesArray[currentFrame].getSprite(sprtName)
            if sprite is not None:
                index = input("PAL CMD: Enter index to change on sprite:")
                sprite.changeSelectedSprite(int(index))
            else:
                print("Sprite can't be found")
        elif var == "move sprite":
            sprtName = input("PAL CMD: Enter name of the sprite:")
            sprite = framesArray[currentFrame].getSprite(sprtName)
            if sprite is None:
                print("Sprite can't be found")
            else:
                moveMode = input("PAL CMD: Relative position <R>  or absolute <A>")
                while (moveMode != "R") & (moveMode != "A"):
                    print("Invalid Option, only <R> and <A>")
                    moveMode = input("PAL CMD: Relative position <R>  or absolute <A>")
                if moveMode == "R":
                    sprtDeltaX = input("PAL CMD: Enter delta X:")
                    sprtDeltaY = input("PAL CMD: Enter delta Y:")
                    sprite.move(int(sprtDeltaX), int(sprtDeltaY))
                else:
                    sprtAbsX = input("PAL CMD: Enter absolute X:")
                    sprtAbsY = input("PAL CMD: Enter absolute Y:")
                    sprite.moveAbs(int(sprtAbsX), int(sprtAbsY))
        elif var == "resize sprite":
            sprtName = input("PAL CMD: Enter name of the sprite:")
            sprite = framesArray[currentFrame].getSprite(sprtName)
            if sprite is None:
                print("Sprite can't be found")
            else:
                multiplier = input("PAL CMD: Enter multiplier:")
                sprite.resizeSpriteMultiplier(int(multiplier))
        elif var == "remove sprite":
            sprtName = input("PAL CMD: Enter name of the sprite:")
            sprite = framesArray[currentFrame].getSprite(sprtName)
            if sprite is None:
                print("Asset can't be found")
            else:
                framesArray[currentFrame].unloadSprite(sprite)
        else:
            print("Invalid command")

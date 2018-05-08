import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import pyscreenshot as ImageGrab
from copy import deepcopy
import imageio

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
        self.canvasView.pack()
        self.canvasView.update_idletasks()

    def getCurrentFrame(self):
        return self.frames[self.currentFrame]


class Frame:
    def __init__(self, width, height):
        self.assets = []
        self.assetsLoaded = -1
        self.sprites = []
        self.spritesLoaded = -1
        self.background = None
        self.background2 = None
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

    def save(self, filename):
        x = self.canvas.winfo_rootx() + self.canvas.winfo_x()
        y = self.canvas.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        box = (x, y, x1, y1)
        ImageGrab.grab(bbox=box).save(filename+".jpg", format="JPEG")
        return filename+".jpg"

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
        self.background = Asset(str(background), "background")
        self.background2 = Asset(str(background), "background2")
        self.background2.move(-self.background2.centerX*2, -self.background2.centerY*2)

    def moveBackground(self, deltaX):
        self.background.move(deltaX, 0)
        if self.background.posX > 0:
            self.background2.moveAbs(0, 0)
            self.background2.move(self.background.posX-self.background2.centerX*2, 0)
        elif self.background.posX+self.background.centerX*2 < self.width:
            self.background2.moveAbs(0, 0)
            self.background2.move(self.background.posX+self.background.centerX*2, 0)
        if (self.background.posX <= -self.background.centerX*2) or (self.background.posX >= self.background.centerX*2):
            self.background, self.background2 = self.background2, self.background
            if self.background.posX > 0:
                self.background2.moveAbs(0, 0)
                self.background2.move(self.background.posX - self.background2.centerX * 2, 0)
            elif self.background.posX + self.background.centerX * 2 < self.width:
                self.background2.moveAbs(0, 0)
                self.background2.move(self.background.posX + self.background.centerX * 2, 0)

    def loadBackground(self):
        if self.background is not None:
            self.background.setPhoto(ImageTk.PhotoImage(self.background.image))
            self.background.setIdentifier(self.canvas.create_image(self.background.posX, self.background.posY,
                                                                   image=self.background.photo,
                                                                   anchor='nw'))
        if self.background2 is not None:
            self.background2.setPhoto(ImageTk.PhotoImage(self.background2.image))
            self.background2.setIdentifier(self.canvas.create_image(self.background2.posX, self.background2.posY,
                                                                   image=self.background2.photo,
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
        newFrame.background2 = deepcopy(self.background2)
        return newFrame


class Asset:
    def __init__(self, fileName, name):
        self.name = name
        self.filename = fileName
        self.image = None
        self.canvasID = None
        self.centerX = None
        self.centerY = None
        self.multiplier = 1
        self.posX = 0
        self.posY = 0
        self.photo = None
        self.angle = 0
        self.load(fileName)

    def load(self, fileName):
        if isinstance(fileName, str):
            try:
                self.image = Image.open(fileName).convert('RGBA')
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

    def rotate(self, angle):
        self.angle = self.angle+angle
        self.image = self.image.rotate(angle, expand=True, center=(self.centerX, self.centerY))

    def rotateAbs(self, angle):
        self.image = self.image.rotate(-self.angle, expand=True, center=(self.centerX, self.centerY))
        self.image = self.image.rotate(angle, expand=True, center=(self.centerX, self.centerY))
        self.angle = angle


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
        self.angle = 0
        self.createSprites()

    def createSprites(self):
        if isinstance(self.fileName, str):
            try:
                self.image = Image.open(self.fileName).convert('RGBA')
                y = 0
                while y < self.image.size[1]:
                    x = 0
                    while x + self.spriteWidth < self.image.size[0]:
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

    def rotate(self, angle):
        self.angle = self.angle+angle

    def rotateAbs(self, angle):
        self.angle = angle

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
        tempImage = tempImage.resize((self.multiplier * tempImage.size[0],
                                      self.multiplier * tempImage.size[1]),
                                     Image.ANTIALIAS)
        return tempImage.rotate(self.angle, expand=True, center=(tempImage.size[0]//2, tempImage.size[1]//2))

    def changeSelectedSprite(self, index):
        self.selectedSprite = index

    def __deepcopy__(self, memodict={}):
        newSprite = Sprite(deepcopy(self.name), deepcopy(self.fileName),
                           deepcopy(self.spriteWidth), deepcopy(self.spriteHeight))
        newSprite.posX = deepcopy(self.posX)
        newSprite.posY = deepcopy(self.posY)
        newSprite.selectedSprite = deepcopy(self.selectedSprite)
        newSprite.multiplier = deepcopy(self.multiplier)
        newSprite.angle = deepcopy(self.angle)
        return newSprite


def makeCanvas():
    root = tk.Tk()
    root.title('PAL-Project')
    root.resizable(False, False)

    app = App(root, framesArray[currentFrame])
    app.pack()
    app.update_idletasks()

    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    app.mainloop()


def save(frameTime):
    count = 0
    frameImages = []
    for frame in framesArray:
        root = tk.Tk()
        root.title('PAL-Project')
        root.resizable(False, False)

        app = App(root, framesArray[count])
        app.pack()
        app.update_idletasks()

        root.after(100, lambda: root.destroy())
        root.after(50, saveFrameImage(frameImages, frame, count))

        app.mainloop()

        count = count + 1
    imageio.mimsave('animation2.gif', frameImages, duration=frameTime)


def saveFrameImage(frameImages, frame, count):
    frameImages.append(imageio.imread(frame.save("frame" + str(count))))


def createFrame():
    global currentFrame
    if currentFrame != -1:
        framesArray.append(deepcopy(framesArray[currentFrame]))
    else:
        framesArray.append(Frame(animationWidth, animationHeight))
    currentFrame = currentFrame + 1
    print("Created frame with index", currentFrame)


if __name__ == '__main__':
    animationWidth = int(input("PAL CMD: Enter the WIDTH of the Animation:"))
    animationHeight = int(input("PAL CMD: Enter the HEIGHT of the Animation:"))
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
            if (int(frameIndex) < 0) or (len(framesArray) - 1 < int(frameIndex)):
                print("Invalid index")
            else:
                currentFrame = int(frameIndex)
        elif var == "background":
            ast = input("PAL CMD: Enter background file name:")
            framesArray[currentFrame].setBackground(ast)
        elif var == "move background":
            if framesArray[currentFrame].background is None:
                print("background isn't set")
            else:
                astDeltaX = input("PAL CMD: Enter delta X:")
                framesArray[currentFrame].moveBackground(int(astDeltaX))
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
        elif var == "rotate asset":
            astName = input("PAL CMD: Enter name of the asset:")
            asset = framesArray[currentFrame].getAsset(astName)
            if asset is None:
                print("Asset can't be found")
            else:
                moveMode = input("PAL CMD: Relative rotation <R>  or absolute <A>")
                while (moveMode != "R") & (moveMode != "A"):
                    print("Invalid Option, only <R> and <A>")
                    moveMode = input("PAL CMD: Relative rotation <R>  or absolute <A>")
                if moveMode == "R":
                    angle = input("PAL CMD: Enter angle:")
                    asset.rotate(int(angle))
                else:
                    angle = input("PAL CMD: Enter angle:")
                    asset.rotateAbs(int(angle))
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
                if (int(index) < 0) or (len(sprite.spritesArray)-1 < int(index)):
                    print("Invalid index")
                else:
                    print(len(sprite.spritesArray))
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
        elif var == "rotate sprite":
            astName = input("PAL CMD: Enter name of the sprite:")
            sprite = framesArray[currentFrame].getSprite(astName)
            if sprite is None:
                print("Asset can't be found")
            else:
                moveMode = input("PAL CMD: Relative rotation <R>  or absolute <A>")
                while (moveMode != "R") & (moveMode != "A"):
                    print("Invalid Option, only <R> and <A>")
                    moveMode = input("PAL CMD: Relative rotation <R>  or absolute <A>")
                if moveMode == "R":
                    angle = input("PAL CMD: Enter angle:")
                    sprite.rotate(int(angle))
                else:
                    angle = input("PAL CMD: Enter angle:")
                    sprite.rotateAbs(int(angle))
        elif var == "remove sprite":
            sprtName = input("PAL CMD: Enter name of the sprite:")
            sprite = framesArray[currentFrame].getSprite(sprtName)
            if sprite is None:
                print("Asset can't be found")
            else:
                framesArray[currentFrame].unloadSprite(sprite)
        elif var == "save":
            frameTime = input("PAL CMD: Enter time in seconds between frames:")
            save(float(frameTime))
        else:
            print("Invalid command")

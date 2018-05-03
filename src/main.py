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
        self.image = self.image.resize((multiplier*self.image.size[0],
                                        multiplier*self.image.size[1]),
                                       Image.ANTIALIAS)

    def resizeAsset(self, newSizeX, newSizeY):
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

def createSprites(fileName, spriteWidth, spriteHeight, numberOfRows, numberOfColumns):
    img = None
    if isinstance(fileName, str):
        try:
            img = Image.open(fileName)
            width = img.size[0]
            height = img.size[1]

            for i in range(1,numberOfRows):
                for j in range(1,numberOfColumns):
                    newSprite = Sprite(fileName + str(i) + str(j))
                    newSprite.image = img.crop(
                        ((i - 1)* spriteWidth, (j - 1)* spriteHeight, spriteWidth, spriteHeight)
                     )
                    spritesArray.append(newSprite)
                    # global assetArray
                    # assetArray.append(newSprite)
        except FileNotFoundError:
            print("File doesn't exist or couldn't be read:", fileName)
    else:
        print("Invalid Parameter", fileName)


class Sprite:

    def __init__(self, name):
        self.name = name
        self.image = None
        self.posX = 0
        self.posY = 0
        self.photo = None
        self.canvasID = None


    def move(self, deltaX, deltaY):
        self.posX = self.posX + deltaX
        self.posY = self.posY + deltaY

    def moveAbs(self, absX, absY):
        self.posX = absX
        self.posY = absY

    def changeSpriteName(self, name):
        self.name = name
    def resizeSprite(self, newSizeX, newSizeY):
        self.image = self.image.resize((newSizeX,newSizeY), Image.ANTIALIAS)
    def resizeAssetMultiplier(self, multiplier):
        self.image = self.image.resize((multiplier*self.image.size[0],
                                        multiplier*self.image.size[1]),
                                       Image.ANTIALIAS)
    def setPhoto(self, photo):
        self.photo = photo

    def setIdentifier(self, id):
        self.canvasID = id

    def unload(self):
        global spritesArray
        spritesArray.remove(self)
        self.image = None



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
            sprtWidth = input("PAL CMD: Enter Sprites width:")
            sprtHeight = input("PAL CMD: Enter Sprite height:")
            rows = input("PAL CMD: Enter number of rows:")
            columns = input("PAL CMD: Enter number of columns:")
            createSprites(sprt, int(sprtWidth), int(sprtHeight), int(rows), int(columns))

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

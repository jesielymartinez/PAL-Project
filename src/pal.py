import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
from copy import deepcopy
import imageio
import _thread

framesArray = []
currentFrame = -1
animationWidth = 500
animationHeight = 500
frameImages = []


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

    # uses the current frame to add the canvas to the tkinter frame
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

    # prepares the canvas for use, adds the background, assets and sprites
    def getCanvas(self, parent):
        self.canvas = tk.Canvas(parent, height=self.height, width=self.width, bg="black",
                                highlightthickness=0, relief='ridge')
        self.loadBackground()
        self.loadSprites()
        self.loadAssets()
        return self.canvas

    # saves the canvas area as an image to a file
    def save(self, filename):
        x = self.canvas.winfo_rootx() + self.canvas.winfo_x()
        y = self.canvas.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        box = (x, y, x1, y1)
        # os.system("screencapture -R"+str(x)+str(y)+str(x1)+str(y1) + filename + ".jpg")
        ImageGrab.grab(bbox=box).save(filename + ".jpg", format="JPEG")
        return filename + ".jpg"

    def addAsset(self, asset):
        self.assetsLoaded = self.assetsLoaded + 1
        self.assets.append(asset)

    # prepares and loads the assets added to the frame
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

    # prepares and loads the sprites added to the frane
    def loadSprites(self):
        for sprite in self.sprites:
            sprite.setPhoto(ImageTk.PhotoImage(sprite.getCurrentSprite(), name=sprite.name))
            sprite.setIdentifier(self.canvas.create_image(sprite.posX, sprite.posY,
                                                          image=sprite.photo, anchor='nw'))

    def setBackground(self, background):
        self.background = Asset(str(background), "background")
        self.background2 = Asset(str(background), "background2")
        self.background2.move(-self.background2.centerX * 2, -self.background2.centerY * 2)

    # moves the background and uses a second image to make it repeat seamlessly
    def moveBackground(self, deltaX):
        self.background.move(deltaX, 0)
        if self.background.posX > 0:
            self.background2.moveAbs(0, 0)
            self.background2.move(self.background.posX - self.background2.centerX * 2, 0)
        elif self.background.posX + self.background.centerX * 2 < self.width:
            self.background2.moveAbs(0, 0)
            self.background2.move(self.background.posX + self.background.centerX * 2, 0)
        if (self.background.posX <= -self.background.centerX * 2) or (
                self.background.posX >= self.background.centerX * 2):
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

    # removes the asset form the frame
    def unloadAsset(self, asset):
        try:
            self.assets.remove(asset)
        except:
            print("Asset not loaded:", asset)

    # removes the sprite form the frame
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

    # properly loads the passed filename to an asset
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
        self.angle = self.angle + angle
        self.image = self.image.rotate(angle, expand=True, center=(self.centerX, self.centerY))

    def rotateAbs(self, angle):
        self.image = self.image.rotate(-self.angle, expand=True, center=(self.centerX, self.centerY))
        self.image = self.image.rotate(angle, expand=True, center=(self.centerX, self.centerY))
        self.angle = angle

    def setIdentifier(self, id):
        self.canvasID = id

    def setPhoto(self, photo):
        self.photo = photo

    # creates a deepcopy of the asset, creating a new asset object
    def __deepcopy__(self, memodict={}):
        newAsset = Asset(self.filename, deepcopy(self.name))
        newAsset.posX = deepcopy(self.posX)
        newAsset.posY = deepcopy(self.posY)
        newAsset.multiplier = deepcopy(self.multiplier)
        newAsset.resizeAsset(self.image.size[0], self.image.size[1])
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

    # loads the passed file and divides it into the sprite states
    def createSprites(self):
        if isinstance(self.fileName, str):
            try:
                self.image = Image.open(self.fileName).convert('RGBA')
                y = 0
                while y < self.image.size[1]:
                    x = 0
                    while x < self.image.size[0]:
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
        self.angle = self.angle + angle

    def rotateAbs(self, angle):
        self.angle = angle

    def setPhoto(self, photo):
        self.photo = photo

    def setIdentifier(self, id):
        self.canvasID = id

    # method used for getting the current sprites states, with proper resizing and rotation
    def getCurrentSprite(self):
        tempImage = self.spritesArray[self.selectedSprite]
        tempImage = tempImage.resize((self.multiplier * tempImage.size[0],
                                      self.multiplier * tempImage.size[1]),
                                     Image.ANTIALIAS)
        return tempImage.rotate(self.angle, expand=True, center=(tempImage.size[0] // 2, tempImage.size[1] // 2))

    def changeSelectedSprite(self, index):
        self.selectedSprite = index

    # creates a deepcopy of the sprite, creating a new sprite object
    def __deepcopy__(self, memodict={}):
        newSprite = Sprite(deepcopy(self.name), deepcopy(self.fileName),
                           deepcopy(self.spriteWidth), deepcopy(self.spriteHeight))
        newSprite.posX = deepcopy(self.posX)
        newSprite.posY = deepcopy(self.posY)
        newSprite.selectedSprite = deepcopy(self.selectedSprite)
        newSprite.multiplier = deepcopy(self.multiplier)
        newSprite.angle = deepcopy(self.angle)
        return newSprite

# creates and displays the tkinter frame with the current frame and canvas
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


# displays the tkinter frame long enough to save all the frames to files
def save(frameTime):
    count = 0

    for frame in framesArray:
        root = tk.Tk()
        root.title('PAL-Project')
        root.resizable(False, False)

        app = App(root, framesArray[count])
        app.pack()
        app.update_idletasks()
        root.lift()
        root.attributes('-topmost', True)
        root.after(500, lambda: saveFrameImage(frame, count))
        root.after(1000, lambda: root.destroy())

        app.mainloop()
        count = count + 1

    for x in range(0, count):
        frameImages.append(imageio.imread("frame" + str(x) + ".jpg"))
    imageio.mimsave('animation.gif', frameImages, duration=frameTime)


def saveFrameImage(frame, count):
    _thread.start_new(frame.save, ("frame" + str(count),))

# creates a new frame after the last one, with the same background, sprites and assets as the current one
def createFrame():
    global currentFrame
    if currentFrame != -1:
        framesArray.append(deepcopy(framesArray[currentFrame]))
    else:
        framesArray.append(Frame(animationWidth, animationHeight))
    currentFrame = currentFrame + 1

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab
import time

assetCount=-1
assetArray=[]

class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.canvasView = tk.Canvas(self, height=500,width=500, bg="black")
        self.canvasView.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.savepic=tk.Button(self, text='SAVE', command=self.save)
        self.savepic.grid(row=1, column=0, sticky='nsew')

    def save(self):
        canvas = self.canvas()  # Get Window Coordinates of Canvas
        self.grabcanvas = ImageGrab.grab(bbox=canvas).save("out.jpg")
        print('Screenshoot of tkinter.Canvas saved in "out.jpg"')

    def canvas(self):
        print('  def _canvas(self):')
        print('self.cv.winfo_rootx() = ', self.canvasView.winfo_rootx())
        print('self.cv.winfo_rooty() = ', self.canvasView.winfo_rooty())
        print('self.cv.winfo_x() =', self.canvasView.winfo_x())
        print('self.cv.winfo_y() =', self.canvasView.winfo_y())
        print('self.cv.winfo_width() =', self.canvasView.winfo_width())
        print('self.cv.winfo_height() =', self.canvasView.winfo_height())
        x=self.canvasView.winfo_rootx()+self.canvasView.winfo_x()+2
        y=self.canvasView.winfo_rooty()+self.canvasView.winfo_y()+2
        x1=x+self.canvasView.winfo_width()-4
        y1=y+self.canvasView.winfo_height()-4
        box=(x,y,x1,y1)

        print('box = ', box)
        return box

    def loadAsset(self, asset,centerX,CenterY):
        global assetCount
        assetCount = assetCount + 1
        assetArray.append(asset)
        assetArray[assetCount].setPhoto(ImageTk.PhotoImage(assetArray[assetCount].image))
        asset.setIdentifier(self.canvasView.create_image(centerX, CenterY, image=assetArray[assetCount].photo))

    def unloadAsset(self,asset):
        try:
            assetArray.remove(asset)
            self.canvasView.delete(asset.canvasID)
        except:
            print("Asset not loaded:", asset)


class Asset():
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

    def unload(self):
        self.image = None

    def setIdentifier(self,id):
        self.canvasID = id

    def setPhoto(self,photo):
        self.photo = photo


if __name__ == '__main__':
    root = tk.Tk()
    root.title('PAL-Project'), root.geometry("500x525")
    app = App(root)

    app.grid(row=0, column=0,columnspan=2, sticky='nsew')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=10)
    app.rowconfigure(1, weight=1)
    app.columnconfigure(0, weight=1)
    app.columnconfigure(1, weight=1)
    app.columnconfigure(2, weight=1)

    asset1 = Asset()
    asset1.load('images.jpg')
    app.loadAsset(asset1,asset1.centerX,asset1.centerY)
    asset2 = Asset()
    asset2.load("Gigaman.png")
    app.loadAsset(asset2,asset2.centerX+20,asset2.centerY+50)


    app.mainloop()


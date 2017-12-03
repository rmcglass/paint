#------------------ import statements -------------#

from tkinter import *
import tkinter.filedialog as fileDialog
from PIL import Image, ImageTk
import io
# can we add something here to make sure people have gs installed?
# ----------------- global variables --------------#

mainWindow = None
lab = None
Ent = None
can = None
col = '#DC143C'
size = 5
topX = 0
topY=0
listImg = []
newH = 200
# ------------------ function definitions ---------- #

# main GUI
def GUIPaint():
    ''' Allows user to paint in a Tkinter canvas by using mouseclicks.
    Creates a window, canvas, and buttons with drawing tools.'''
    global mainWindow
    global can
    global col
    global lab

    # creates window
    mainWindow= Tk()
    mainWindow.title("Painting GUI")

    # binds the action of clicking and dragging the mouse on the canvas to the paint function
    can = Canvas(mainWindow, bg = '#FFFFFF', relief = 'groove', bd=5, width=1200, height=700)
    #can = Canvas(mainWindow, bg='#FFFFFF', relief='groove', bd=5, width=500, height=300)
    can.grid(row=1,column=1)
    can.bind("<B1-Motion>", paint)

    # guitButton quits program and closes the window
    quitButton = Button(text="Quit", command=quitCallback)  # no parentheses means wait until this button is clicked
    quitButton.grid(row=0, column=0)

    # reset button erases all paint from canvas, save button opens a dialog box to save image
    f3 = Frame(mainWindow)
    f3.grid(row=2, column=1)
    resetButton = Button(f3, text='Reset', command=resetCanvas)
    resetButton.grid(row=0,column=0)
    saveButton = Button(f3, text='Save', command=FileSave)
    saveButton.grid(row=0, column=1)

    # just a label
    lab = Label(text='Paint!')
    lab.grid(row=0, column=1)

    # a frame with buttons to select a paint color
    f= Frame(mainWindow)
    f.grid(row=1, column=0)
    lab = Label(f, text='Pen Colors')
    lab.grid(row=0,column=0)
    redButton = Button(f, text='Red', command=colorRed)
    redButton.grid(row=1,column=0)
    orangeButton = Button(f, text='Orange', command=colorOrange)
    orangeButton.grid(row=2, column=0)
    yellowButton = Button(f, text='Yellow', command=colorYellow)
    yellowButton.grid(row=3, column=0)
    greenButton = Button(f, text='Green', command=colorGreen)
    greenButton.grid(row=4, column=0)
    blueButton = Button(f, text='Blue', command=colorBlue)
    blueButton.grid(row=5, column=0)
    purpleButton = Button(f, text='Purple', command=colorPurple)
    purpleButton.grid(row=6, column=0)
    blackButton = Button(f, text='Black', command=colorBlack)
    blackButton.grid(row=7, column=0)

    # a frame with buttons to select tool and pensize
    f2 = Frame(mainWindow)
    f2.grid(row=1,column=2)
    # tools
    lab = Label(f2, text='Tools')
    lab.grid(row=0, column=0)
    paintButton = Button(f2, text='Paintbrush', command=selectPaint)
    paintButton.grid(row=1, column=0)
    eraseButton = Button(f2, text='Eraser', command=selectErase)
    eraseButton.grid(row=2, column=0)
    rectButton = Button(f2, text='Rectangle', command=selectRectangle)
    rectButton.grid(row=3, column=0)
    ovalButton = Button(f2, text='Oval', command=selectOval)
    ovalButton.grid(row=4,column=0)
    lineButton = Button(f2, text='Line', command=selectLine)
    lineButton.grid(row=5, column=0)
    picButton = Button(f2, text="Image", command=selectImage)
    picButton.grid(row=6, column=0)

    lab = Label(f2, text='')
    lab.grid(row=7, column=0)

    # pen sizes
    lab = Label(f2, text='Brush Sizes')
    lab.grid(row=8,column=0)
    smallButton = Button(f2, text='Small', command=smallPen)
    smallButton.grid(row=9, column=0)
    medButton = Button(f2, text='Medium', command=medPen)
    medButton.grid(row=10, column=0)
    bigButton = Button(f2, text='Big', command=bigPen)
    bigButton.grid(row=11, column=0)

    mainWindow.mainloop()

# tool functions
def paint(event):
    '''places ovals on screen as mouse moves'''
    global can
    x0, y0 = (event.x - size), (event.y - size)
    x1, y1 = (event.x + size), (event.y + size)
    can.create_oval(x0,y0,x1,y1,fill = col, outline = col, tags='paint')
def selectPaint():
    '''binds mouseclicks to paint'''
    global can
    can.bind("<B1-Motion>", paint)
    can.unbind("<Button-1>")
    can.unbind("<ButtonRelease-1>")
def erase(event):
    '''places white ovals on screen as mouse moves'''
    global can
    x0, y0 = (event.x - size), (event.y - size)
    x1, y1 = (event.x + size), (event.y + size)
    can.create_oval(x0,y0,x1,y1,fill = '#FFFFFF', outline = '#FFFFFF', tags='paint')
def selectErase():
    '''binds mouseclicks to erase'''
    global can
    can.bind("<B1-Motion>", erase)
    can.unbind("<Button-1>")
    can.unbind("<ButtonRelease-1>")
def topCorner(event):
    '''sets an x,y coordinate for use as the top left corner in rectangle'''
    global topX
    global topY
    topX = event.x
    topY = event.y
def selectRectangle():
    '''binds mouseclicks to rectangle and topCorner'''
    global can
    can.unbind("<B1-Motion>")
    can.bind("<Button-1>", topCorner)
    can.bind("<ButtonRelease-1>",rectangle)
    # can.bind("<B1-Motion>",rectangle)
def rectangle(event):
    '''draws rectangle. click and drag mouse to designate the top left corner (click) and bottom right corner (release)'''
    global can
    global topX
    global topY
    can.create_rectangle(topX,topY, event.x, event.y, fill=col, outline=col, tags='paint')
def selectOval():
    '''binds mouseclicks to oval'''
    global can
    can.unbind("<B1-Motion>")
    can.bind("<Button-1>", topCorner)
    can.bind("<ButtonRelease-1>",oval)
def oval(event):
    '''draws oval. click and drag mouse to designate the top left corner (click)
     and bottom right corner (release)'''
    global can
    global topX
    global topY
    can.create_oval(topX,topY,event.x, event.y, fill=col, outline=col, tags='paint')
def selectLine():
    '''binds mouseclicks to line'''
    global can
    can.unbind("<B1-Motion>")
    can.bind("<Button-1>", topCorner)
    can.bind("<ButtonRelease-1>",line)
def line(event):
    '''draws line. click and drag mouse to designate the start point (click)
     and end point (release)'''
    global can
    global topX
    global topY
    can.create_line(topX,topY,event.x, event.y, fill=col, tags='paint', width=size)
def selectImage():
    "Binds mouseclick to imageStamp"
    global can
    global path
    can.bind("<Button-1>",imageStamp)
    can.unbind("<B1-Motion>")
    can.unbind("<ButtonRelease-1>")
    path = fileDialog.askopenfilename()
def imageStamp(event):
    """This function stamps a photograph selected in selectImage.
    It then resizes the image and places it at a mouseclick. """
    global newH
    global can
    global path
    global listImg
    phot = Image.open(path)
    [w,h]=phot.size
    newW = int(newH*w/h)
    phot = phot.resize((newW,newH), Image.ANTIALIAS)
    photphot = ImageTk.PhotoImage(phot)
    listImg.append(photphot)
    can.create_image(event.x, event.y, image=photphot, tags='paint')

# color functions
def colorRed():
    '''changes global variable color to red'''
    global col
    col = '#DC143C'
def colorOrange():
    '''changes global variable color to orange'''
    global col
    col = '#FF8C00'
def colorYellow():
    '''changes global variable color to yellow'''
    global col
    col = '#FFD700'
def colorGreen():
    '''changes global variable color to green'''
    global col
    col = '#228B22'
def colorBlue():
    '''changes global variable color to blue'''
    global col
    col = '#4682B4'
def colorPurple():
    '''changes global variable color to purple'''
    global col
    col = '#663399'
def colorBlack():
    '''changes global variable color to black'''
    global col
    col = '#000000'

# pensize functions
def smallPen():
    '''changes pensize to a 2x2 pixel circle
     and newH (the image height for imageStamp) to 200 pixels'''
    global size
    global newH
    size = 1
    newH = 200
def medPen():
    '''changes pensize to a 10x10 pixel circle
    and newH (the image height for imageStamp) to 400 pixels'''
    global size
    global newH
    newH = 400
    size = 5
def bigPen():
    '''changes pensize to a 20x20 pixel circle
    and newH (the image height for imageStamp) to 600 pixels'''
    global size
    global newH
    size = 10
    newH = 600

# canvas functions
def resetCanvas():
    '''deletes all objects with tag 'paint' from canvas'''
    global can
    can.delete('paint')
def quitCallback():
    '''closes window'''
    global mainWindow
    mainWindow.destroy()
def FileSave():
    '''Saves canvas as a jpeg file.'''
    global can
    fName = fileDialog.asksaveasfilename(defaultextension = '.jpg')
    ps = can.postscript(colormode ='color')
    im = Image.open(io.BytesIO(ps.encode('utf-8')))
    im.save(fName, 'jpeg', subsampling=0, quality=100)


# ------------ script elements ---------- #

GUIPaint()

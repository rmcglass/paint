#Riley McGlasson and Vincent Mougin
#COMP 123 Lian Duan
# This is a Tkinter GUI that allows the user to 'paint'
# or insert objects onto a canvas.

# ------------------ import statements -------------#

from tkinter import *
import tkinter.filedialog as fileDialog
from PIL import Image, ImageTk
import io

# NOTE: requires ghostscript for save function to work.

# ----------------- global variables --------------#

mainWindow = None
lab = None
Ent = None
can = None
col = '#DC143C'
size = 5
topX = 0
topY = 0
listImg = []
newH = 200


# ------------------ function definitions ---------- #

# main GUI
def GUIPaint():
    ''' Takes no inputs. The main funciton.
    Allows user to 'paint' in a Tkinter canvas by using mouseclicks.
    Creates a window, canvas, and buttons with drawing tools.'''
    global mainWindow
    global can
    global col
    global lab

    # creates window
    mainWindow = Tk()
    mainWindow.title("Painting GUI")

    # binds the action of clicking and dragging the mouse on the canvas to the paint function
    can = Canvas(mainWindow, bg='#FFFFFF', relief='groove', bd=5, width=1000, height=600)
    can.grid(row=1, column=1)
    can.bind("<B1-Motion>", paint)
    can.bind("<Button-1>", paint)

    # guitButton quits program and closes the window
    quitButton = Button(text="Quit", command=quitCallback)
    quitButton.grid(row=0, column=0)

    # reset button erases all objects with tag 'paint' from canvas, save button opens a dialog box to save image
    f3 = Frame(mainWindow)
    f3.grid(row=2, column=1)
    resetButton = Button(f3, text='Reset', command=resetCanvas)
    resetButton.grid(row=0, column=0)
    saveButton = Button(f3, text='Save', command=FileSave)
    saveButton.grid(row=0, column=1)

    # just a label
    lab = Label(text='Paint!')
    lab.grid(row=0, column=1)

    # a frame with buttons to select a paint color
    f = Frame(mainWindow)
    f.grid(row=1, column=0)
    lab = Label(f, text='Pen Colors')
    lab.grid(row=0, column=0)
    redButton = Button(f, text='Red', command=colorRed)
    redButton.grid(row=1, column=0)
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
    f2.grid(row=1, column=2)
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
    ovalButton.grid(row=4, column=0)
    lineButton = Button(f2, text='Line', command=selectLine)
    lineButton.grid(row=5, column=0)
    picButton = Button(f2, text="Image Stamp", command=selectImage)
    picButton.grid(row=6, column=0)

    lab = Label(f2, text='')
    lab.grid(row=7, column=0)

    # pen sizes
    lab = Label(f2, text='Brush Sizes')
    lab.grid(row=8, column=0)
    smallButton = Button(f2, text='Small', command=smallPen)
    smallButton.grid(row=9, column=0)
    medButton = Button(f2, text='Medium', command=medPen)
    medButton.grid(row=10, column=0)
    bigButton = Button(f2, text='Big', command=bigPen)
    bigButton.grid(row=11, column=0)
    jumboButton = Button(f2, text='Jumbo', command=jumboPen)
    jumboButton.grid(row=12, column=0)

    mainWindow.mainloop()


# tool functions
def paint(event):
    '''Takes an event as an input. Places ovals on screen as mouse clicks and drags'''
    global can
    x0, y0 = (event.x - size), (event.y - size)
    x1, y1 = (event.x + size), (event.y + size)
    can.create_oval(x0, y0, x1, y1, fill=col, outline=col, tags='paint')
def selectPaint():
    '''Takes no inputs. Binds the actions
     of clicking and dragging and just clicking
     to the function paint(event).'''
    global can
    can.bind("<B1-Motion>", paint)
    can.unbind("<Button-1>")
    can.unbind("<ButtonRelease-1>")
    can.bind("<Button-1>", paint)
def erase(event):
    '''Takes an event as an input. Places white ovals on screen as mouse clicks and drags.'''
    global can
    x0, y0 = (event.x - size), (event.y - size)
    x1, y1 = (event.x + size), (event.y + size)
    can.create_oval(x0, y0, x1, y1, fill='#FFFFFF', outline='#FFFFFF', tags='paint')
def selectErase():
    '''Takes no inputs. Binds the actions
     of clicking and dragging and just clicking
     to the function erase(event).'''
    global can
    can.bind("<B1-Motion>", erase)
    can.unbind("<Button-1>")
    can.unbind("<ButtonRelease-1>")
    can.bind("<Button-1>", erase)
def topCorner(event):
    '''Takes an event as the input. Sets an x,y coordinate
     for use as the top left corner in rectangle(event), oval(event), and line(event)'''
    global topX
    global topY
    topX = event.x
    topY = event.y
def selectRectangle():
    '''Takes no inputs. Binds mouseclick to topCorner(event) and a mouse release to rectangle(event).'''
    global can
    can.unbind("<B1-Motion>")
    can.bind("<Button-1>", topCorner)
    can.bind("<ButtonRelease-1>", rectangle)
    # can.bind("<B1-Motion>",rectangle)
def rectangle(event):
    '''Takes an event as the input.
    Draws a rectangle. Click and drag mouse to designate
    the top left corner (click) and bottom right corner (release)'''
    global can
    global topX
    global topY
    can.create_rectangle(topX, topY, event.x, event.y, fill=col, outline=col, tags='paint')
def selectOval():
    '''Takes no inputs. binds mouseclick to
     topCorner(event) and mouse release to oval(event).'''
    global can
    can.unbind("<B1-Motion>")
    can.bind("<Button-1>", topCorner)
    can.bind("<ButtonRelease-1>", oval)
def oval(event):
    '''Takes an event as the input. Draws an oval.
    click and drag mouse to designate the top left corner (click)
    and bottom right corner (release)'''
    global can
    global topX
    global topY
    can.create_oval(topX, topY, event.x, event.y, fill=col, outline=col, tags='paint')
def selectLine():
    '''Takes no input. binds mouseclicks to topCorner(event) and mouse release to line(event).'''
    global can
    can.unbind("<B1-Motion>")
    can.bind("<Button-1>", topCorner)
    can.bind("<ButtonRelease-1>", line)
def line(event):
    '''Takes an event as the input. Draws a line.
     click and drag mouse to designate the start point (click)
     and end point (release)'''
    global can
    global topX
    global topY
    can.create_line(topX, topY, event.x, event.y, fill=col, tags='paint', width=size)
def selectImage():
    '''Takes no input. Binds mouseclick to imageStamp(event)
    and opens a dialog box to select an image for use in imageStamp.'''
    global can
    global path
    can.bind("<Button-1>", imageStamp)
    can.unbind("<B1-Motion>")
    can.unbind("<ButtonRelease-1>")
    path = fileDialog.askopenfilename()
def imageStamp(event):
    """Takes an event as the input. This function stamps a photograph selected in selectImage.
    It then resizes the image and places it at a mouseclick. """
    global newH
    global can
    global path
    global listImg
    if '.png' in path:
        phot = Image.open(path).convert("RGB")
    else:
        phot = Image.open(path)
    [w, h] = phot.size
    newW = int(newH * w / h)
    phot = phot.resize((newW, newH), Image.ANTIALIAS)
    photphot = ImageTk.PhotoImage(phot)
    listImg.append(photphot)
    can.create_image(event.x, event.y, image=photphot, tags='paint')


# color functions
def colorRed():
    '''Takes no inputs. Changes global variable color to red'''
    global col
    col = '#DC143C'
def colorOrange():
    '''Takes no inputs. Changes global variable color to orange'''
    global col
    col = '#FF8C00'
def colorYellow():
    '''Takes no inputs. Changes global variable color to yellow'''
    global col
    col = '#FFD700'
def colorGreen():
    '''Takes no inputs. Changes global variable color to green'''
    global col
    col = '#228B22'
def colorBlue():
    '''Takes no inputs. Changes global variable color to blue'''
    global col
    col = '#4682B4'
def colorPurple():
    '''Takes no inputs. Changes global variable color to purple'''
    global col
    col = '#663399'
def colorBlack():
    '''Takes no inputs. Changes global variable color to black'''
    global col
    col = '#000000'

# pensize functions
def smallPen():
    '''Takes no inputs. Changes pensize radius to 1
     and newH (the image height for imageStamp) to 100 pixels'''
    global size
    global newH
    size = 1
    newH = 100
def medPen():
    '''Takes no inputs. Changes pensize radius to 5
    and newH (the image height for imageStamp) to 300 pixels'''
    global size
    global newH
    newH = 300
    size = 5
def bigPen():
    '''Takes no inputs. Changes pensize radius to 10
    and newH (the image height for imageStamp) to 400 pixels'''
    global size
    global newH
    size = 10
    newH = 400
def jumboPen():
    '''Takes no inputs. Changes pensize radius to 25
    and newH (the image height for imageStamp) to 600 pixels'''
    global size
    global newH
    size = 25
    newH = 600

# canvas functions
def resetCanvas():
    '''Takes no input. deletes all objects with tag 'paint' from canvas'''
    global can
    can.delete('paint')
def quitCallback():
    '''Takes no inputs. closes window'''
    global mainWindow
    mainWindow.destroy()
def FileSave():
    '''Takes no input. Opens a dialog box then
     saves canvas as a jpeg file to the selected path.'''
    global can
    fName = fileDialog.asksaveasfilename(defaultextension='.jpg')
    ps = can.postscript(colormode='color')
    im = Image.open(io.BytesIO(ps.encode('utf-8')))
    im.save(fName, 'jpeg', subsampling=0, quality=100)


# ------------ script elements ---------- #

GUIPaint()

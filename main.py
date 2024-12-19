#create the Easy Editor photo editor here!
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap #screen optimised

from PIL import Image

from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog, #Dialogufor opening files(and folders)
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout, QDialog
)
import PIL

from PIL import ImageFilter
from PIL.ImageFilter import(
    BLUR, CONTOUR,DETAIL,EDGE_ENHANCE,EDGE_ENHANCE_MORE,
    EMBOSS,FIND_EDGES,SMOOTH,SMOOTH_MORE,SHARPEN,
    GaussianBlur, UnsharpMask
)

import os

app = QApplication([])
'''Application interface'''
#application window parameters
win = QWidget()
win.setWindowTitle('Easy Editor App')
win.resize(900, 600)
lb_image = QLabel("Image")
btn_dir = QPushButton("Folder")
lw_files = QListWidget()

#application window widgets
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_flip = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("B/W")

row = QHBoxLayout() #Main line
col1 = QVBoxLayout() #divided into two columns
col2 = QVBoxLayout()
col1.addWidget(btn_dir) #in the first - directory selection button
col1.addWidget(lw_files) #and file list
col2.addWidget(lb_image, 95) #in the second - image
row_tools = QHBoxLayout() #and button bar
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg','.jpeg','.png','.gif','.bmp']
    chooseWorkdir()
    try:
        filenames = filter(os.listdir(workdir), extensions)
        lw_files.clear()
        for filename in filenames:
            lw_files.addItem(filename)
    except Exception as e:
        #Show QDialog if an error happens
        dialog = ErrorDialog("Error file name cannot be empty")
        dialog.exec_() #show the dialog error through

class ErrorDialog(QDialog):
    def __init__(self,error_message):
        super().__init__()
        self.setWindowTitle("Error")
        layout = QVBoxLayout()

        #Label for showing an error message
        label = QLabel(error_message)
        layout.addWidget(label)

        #Button for closing the dialog
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self. save_dir = "Modified/"

    def loadImage(self, dir, filename):
        '''When loading, remember the path and file name'''
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        Image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(Image_path) 

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        '''saves a copy of the file in a sub-folder'''
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

def showChosenImage(): 
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)
workimage = ImageProcessor()

lw_files.currentRowChanged.connect(showChosenImage)

btn_dir.clicked.connect(showFilenamesList)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)


win.show()
#run the application
app.exec_()
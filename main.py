# https://velog.io/@davkim1030/Image-Stitching

import cv2, glob, os, sys
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import uic

ui_file = uic.loadUiType("ui_design.ui")[0]

class WindowClass(QMainWindow, ui_file):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Panorama Maker')

        self.root = ''
        self.dest = ''
        self.btnFlag = False

        self.btn1.clicked.connect(self.button1Function)
        self.btn2.clicked.connect(self.button2Function)
        self.btn3.clicked.connect(self.button3Function)

    def button1Function(self):
        foldername = self.selectFolder(self)
        self.root = foldername
        self.folder1.setText(foldername)

    def button2Function(self):
        foldername = self.selectFolder(self)
        self.dest = foldername
        self.folder2.setText(foldername)
        
    def button3Function(self):
        if not self.btnFlag:
            makePanorama(self, self.root, self.dest)

    def selectFolder(self, arg):
        foldername = QFileDialog.getExistingDirectory(self, "Select Directory")
        return foldername

def makePanorama(self, root, dest):
    if root.replace(' ', '') == '' or dest.replace(' ', '') == '':
        buttonReply = QMessageBox.warning(self, 'Warning', 'Please enter the folder path', QMessageBox.Cancel)
    else:
        self.btnFlag = True
        img_list = []
        imgs = []

        for file in glob.iglob(root + '\\**', recursive=True):
            if os.path.splitext(file)[1] not in ['.jpg', '.png']:
                continue
            
            img_list.append(file)
            print(file)

        img_list = sorted(img_list)

        try:
            for i, img_path in enumerate(img_list):
                img = cv2.imread(img_path)
                imgs.append(img)

            stitcher = cv2.Stitcher_create(cv2.STITCHER_PANORAMA)
            status, stitched = stitcher.stitch(imgs)

            # if status == 0:
            #     plt.imshow(cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB))
            #     plt.show()
            # else:
            #     print('failed... %s' % status)

            gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
            thresh = cv2.bitwise_not(cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1])
            thresh = cv2.medianBlur(thresh, 5)

            stitched_copy = stitched.copy()
            thresh_copy = thresh.copy()

            while np.sum(thresh_copy) > 0:
                thresh_copy = thresh_copy[1:-1, 1:-1]
                stitched_copy = stitched_copy[1:-1, 1:-1]

            cv2.imwrite(os.path.join(dest, 'result_crop.jpg'), stitched_copy)
            buttonReply = QMessageBox.information(self, 'Succeess', 'Make Panorama Succeed', QMessageBox.Ok)
            self.btnFlag = False
            # plt.imshow(cv2.cvtColor(stitched_copy, cv2.COLOR_BGR2RGB))
            # plt.show()
        except Exception as e:
            buttonReply = QMessageBox.critical(self, 'Error', "It's not a similar image or can't find anything in common between the images.", QMessageBox.Ok)
            self.btnFlag = False
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qss_file = open('ui_style.qss').read()
    app.setStyleSheet(qss_file)

    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
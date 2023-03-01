import cv2
import numpy as np
from skimage import exposure
import sys
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QStyle,QFileDialog,QLabel,QCheckBox
from PyQt5.QtGui import QIcon,QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import pyautogui as pg
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QStyle,QFileDialog,QLabel,QLineEdit,QCheckBox
import time
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("player.ico"))
        self.setWindowTitle("Welding Video Annotator")
        self.setGeometry(350,200,862,712)
        

        self.create_player()


    def create_player(self):

        self.setWindowTitle("Welding Video Annotator")
        self.disply_width = 2000
        self.display_height = 2000
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)


        self.openBtn=QPushButton('Open(o)')
        self.openlabel=QLabel("o")
        self.openBtn.clicked.connect(self.open_file)
        self.openBtn.setShortcut('o')

        self.playBtn=QPushButton('(p)')
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.startVideo)
        self.playlabel=QLabel("p")
        self.playBtn.setShortcut('p')
        self.line_editlabel=QLabel("    ")
        self.line_edit = QLabel("    ")
       
        self.pauseBtn=QPushButton('(SP)')
        self.pauseBtn.setEnabled(False)
        self.pauseBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pauseBtn.clicked.connect(self.pauseVideo)
        self.pauselabel=QLabel("space")
        self.pauseBtn.setShortcut('Space')

        self.previousBtn=QPushButton('(j)')
        self.previousBtn.setEnabled(False)
        self.previousBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.previousBtn.clicked.connect(self.backward_video)
        self.previouslabel=QLabel("j")
        self.previousBtn.setShortcut('j')

        self.nextBtn=QPushButton('(k)')
        self.nextBtn.setEnabled(False)
        self.nextBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.nextBtn.clicked.connect(self.forward_video)
        self.nextlabel=QLabel("k")
        self.nextBtn.setShortcut('k')

        
        self.brightness_value_now = 30 # Updated brightness value

        self.filterBtn=QCheckBox('(f)')
        self.filterBtn.setShortcut('f')
        self.filterlabel=QLabel("f")

        self.cursorBtn=QCheckBox('(c)')
        self.cursorBtn.setShortcut('c')
        self.cursorlabel=QLabel("c")

        self.lBtn2=QCheckBox('2')
        self.lBtn2.setShortcut('2')

        self.lBtn3=QCheckBox('3')
        self.lBtn3.setShortcut('3')

        self.lBtn4=QCheckBox('4')
        self.lBtn4.setShortcut('4')

        #self.line = QLineEdit(self)
        #self.linelabel=QLabel("Label")

        hbox=QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.line_edit)
        hbox.addWidget(self.line_editlabel)
        
        #
        hbox.addWidget(self.previousBtn)
        #
        hbox.addWidget(self.playBtn)
        #
        hbox.addWidget(self.pauseBtn)
        #
        hbox.addWidget(self.nextBtn)
        #

        hbox.addWidget(self.filterBtn)
        #hbox.addWidget(self.line)
        hbox.addWidget(self.lBtn2)
        hbox.addWidget(self.lBtn3)
        hbox.addWidget(self.lBtn4)

        hbox.addWidget(self.cursorBtn)
        #
        hbox1=QHBoxLayout()
        hbox1.addWidget(self.openlabel)
        hbox1.addWidget(self.line_edit)
        hbox1.addWidget(self.line_editlabel)
        hbox1.addWidget(self.previouslabel)
        hbox1.addWidget(self.playlabel)
        hbox1.addWidget(self.pauselabel)
        hbox1.addWidget(self.nextlabel)
        hbox1.addWidget(self.filterlabel)
        #hbox1.addWidget(self.linelabel)
        hbox1.addWidget(self.cursorlabel)
        hbox1.setSpacing(1)
        

        vbox=QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def startVideo(self):
        self.pauseBtn.setEnabled(True)

        self.filterBtn.setEnabled(False)
        self.cursorBtn.setEnabled(False)
        self.dir=self.filename.replace(self.filename.split('/')[-1],'')[:-1]
        
        self.files=os.listdir(self.dir)
        if self.cap==0:

            self.cap = cv2.VideoCapture(str(self.filename))
            self.name='label_'+self.filename.split('/')[-1][:-4]+'.npy'

            if self.name in self.files:
                self.cursor=list(np.load(self.dir+'/'+self.name))

            else:
                self.cursor=list(np.zeros((int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)),2)))
            

            self.frame_num=1
            
          
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.setTimerType(Qt.PreciseTimer)
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.millisecs = int(1000.0 / fps)#mobinaa
        self.timer.start(self.millisecs)
        
        self.line_editlabel.setText(' / ' +str(int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))*self.millisecs/1000))
        
        
    def pauseVideo(self):
        self.timer.stop()

        self.filterBtn.setEnabled(True)
        self.cursorBtn.setEnabled(True)

        self.previousBtn.setEnabled(True)
        self.nextBtn.setEnabled(True)
        

    def open_file(self):
        self.start=time.time()
        self.filename,_=QFileDialog.getOpenFileName(self,"Open(o)")
        self.cap=0


        if self.filename!='':

            self.playBtn.setEnabled(True)

            
        self.dir=self.filename.replace(self.filename.split('/')[-1],'')[:-1]
        self.files=os.listdir(self.dir)

        if self.cap==0:

            self.cap = cv2.VideoCapture(str(self.filename))
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.millisecs = int(1000.0 / fps)
            self.name='label_'+self.filename.split('/')[-1][:-4]+'.npy'
            if self.name in self.files:
                self.cursor=list(np.load(self.dir+'/'+self.name))
                
            else:
                self.cursor=list(np.zeros((int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)),2)))

            self.frame_num=1
        
            self.nextFrameSlot()
            self.cap=0

    
    def backward_video(self):
        self.frame_num-=10
        if self.frame_num*self.millisecs/1000<0:
            self.frame_num=0
        
        self.line_edit.setText(str(self.frame_num*self.millisecs/1000))

        self.timer.stop()


    def bbackward_video(self):
        self.frame_num-=10


    def forward_video(self):
        self.frame_num+=10
        if self.frame_num*self.millisecs/1000<0:
            self.frame_num=0

        self.line_edit.setText(str(self.frame_num*self.millisecs/1000))
        self.timer.stop()


    def fforward_video(self):
        self.frame_num+=10


    def nextFrameSlot(self):
        self.cap.set(1,self.frame_num)
        ret, self.frame = self.cap.read()
        if self.frame_num*self.millisecs/1000<0:
            self.frame_num=0
        self.line_edit.setText(str(self.frame_num*self.millisecs/1000))
        
        if ret == True:
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame=cv2.resize(self.frame,(self.image_label.width(),self.image_label.height()),interpolation = cv2.INTER_AREA)
            self.filter()
                      

            if self.cursorBtn.isChecked()==True:
                
                self.setCursor(Qt.BlankCursor)
                
                self.cursor[self.frame_num-1]=[(pg.position()[0]-self.pos().x()-self.image_label.x())/self.image_label.width(),(pg.position()[1]-self.pos().y()-self.image_label.y())/self.image_label.height()]


                self.unsetCursor()
            cv2.circle(self.frame,(int(self.cursor[self.frame_num-1][0]*self.image_label.width()),int(self.cursor[self.frame_num-1][1]*self.image_label.height())),radius=10,color=(0,255,0),thickness=-1)

            if self.lBtn2.isChecked()==True: #and self.line.text()=='2':
                self.setCursor(Qt.BlankCursor)
                numm=[(pg.position()[0]-self.pos().x()-self.image_label.x())/self.image_label.width(),(pg.position()[1]-self.pos().y()-self.image_label.y())/self.image_label.height()]
               
                if 0<=numm[0]<1/2-0.05:
                    self.cursor[self.frame_num-1]=[0,0]
                elif 1/2-0.05<=numm[0]<1/2+0.05:
                    self.cursor[self.frame_num-1]=[0.5,0.5]
                else:
                    self.cursor[self.frame_num-1]=[1,1]

                self.frame=cv2.line(self.frame,(int(self.image_label.width()/2-0.1*self.image_label.width()),0),(int(self.image_label.width()/2-0.1*self.image_label.width()),self.image_label.height()),(255,0,255),5)
                self.frame=cv2.line(self.frame,(int(self.image_label.width()/2+0.1*self.image_label.width()),0),(int(self.image_label.width()/2+0.1*self.image_label.width()),self.image_label.height()),(255,0,255),5)
             

            elif self.lBtn3.isChecked()==True:# and self.line.text()=='3':
                self.setCursor(Qt.BlankCursor)
                numm=[(pg.position()[0]-self.pos().x()-self.image_label.x())/self.image_label.width(),(pg.position()[1]-self.pos().y()-self.image_label.y())/self.image_label.height()]
                
                if 0<=numm[0]<1/3-0.05:
                    self.cursor[self.frame_num-1]=[0,0]
                elif 1/3-0.05<=numm[0]<1/3+0.05:
                    self.cursor[self.frame_num-1]=[0.5,0.5]
                elif 1/3+0.05<=numm[0]<2/3-0.05:
                    self.cursor[self.frame_num-1]=[1,1]
                elif 2/3-0.05<=numm[0]<2/3+0.05:
                    self.cursor[self.frame_num-1]=[1.5,1.5]
                else:
                    self.cursor[self.frame_num-1]=[2,2]

                self.frame=cv2.line(self.frame,(int(self.image_label.width()/3-0.05*self.image_label.width()),0),(int(self.image_label.width()/3-0.05*self.image_label.width()),self.image_label.height()),(255,0,255),5)
                self.frame=cv2.line(self.frame,(int(self.image_label.width()/3+0.05*self.image_label.width()),0),(int(self.image_label.width()/3+0.05*self.image_label.width()),self.image_label.height()),(255,0,255),5)
    
                self.frame=cv2.line(self.frame,(int(2*self.image_label.width()/3-0.05*self.image_label.width()),0),(int(2*self.image_label.width()/3-0.05*self.image_label.width()),self.image_label.height()),(255,0,255),5)
                self.frame=cv2.line(self.frame,(int(2*self.image_label.width()/3+0.05*self.image_label.width()),0),(int(2*self.image_label.width()/3+0.05*self.image_label.width()),self.image_label.height()),(255,0,255),5)
    
            elif self.lBtn4.isChecked()==True:# and self.line.text()=='4':
                self.setCursor(Qt.BlankCursor)
                numm=[(pg.position()[0]-self.pos().x()-self.image_label.x())/self.image_label.width(),(pg.position()[1]-self.pos().y()-self.image_label.y())/self.image_label.height()]
                
                if 0<=numm[0]<1/2-0.05 and  0<=numm[1]<1/2-0.05:
                    self.cursor[self.frame_num-1]=[0,0]
                elif 1/2<=numm[1]<1/2+0.05 and 1/2-0.05<=numm[0]<1/2+0.05:
                    self.cursor[self.frame_num-1]=[0.5,0.5]
                elif 1/2+0.05<=numm[0] and 1/2+0.05<=numm[1]:
                    self.cursor[self.frame_num-1]=[1,1]
                elif 1/2-0.05<=numm[1]<1/2 and 0<=numm[0]<1/2-0.05:
                    self.cursor[self.frame_num-1]=[1.5,1.5]
                elif 0<=numm[0]<1/2-0.05 and 0<=numm[1]<1/2-0.05:
                    self.cursor[self.frame_num-1]=[2,2]
                elif 0<=numm[0]<1/2-0.05 and 1/2<=numm[1]<1/2+0.05:
                    self.cursor[self.frame_num-1]=[2.5,2.5]
                else:
                    self.cursor[self.frame_num-1]=[3,3]

                self.frame=cv2.line(self.frame,(int(self.image_label.width()/2-0.05*self.image_label.width()),0),(int(self.image_label.width()/2-0.05*self.image_label.width()),self.image_label.height()),(255,0,255),5)
                self.frame=cv2.line(self.frame,(int(self.image_label.width()/2+0.05*self.image_label.width()),0),(int(self.image_label.width()/2+0.05*self.image_label.width()),self.image_label.height()),(255,0,255),5)
     
                self.frame=cv2.line(self.frame,(0,int(self.image_label.height()/2-0.05*self.image_label.height())),(self.image_label.width(),int(self.image_label.height()/2-0.05*self.image_label.height())),(255,0,255),5)
                self.frame=cv2.line(self.frame,(0,int(self.image_label.height()/2+0.05*self.image_label.height())),(self.image_label.width(),int(self.image_label.height()/2+0.05*self.image_label.height())),(255,0,255),5)
    

            #print((int(self.cursor[self.frame_num][0]*self.image_label.width()),int(self.cursor[self.frame_num][1]*self.image_label.height())))


            self.frame_num+=1
            
            img = QImage(self.frame,self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)            

            self.image_label.setPixmap(pix) 
            self.end=time.time()
            self.td=self.end-self.start

            np.save(self.dir+'/'+self.name,self.cursor) 
            np.savetxt(self.dir+'/'+self.name[:-4]+'.txt', self.cursor, fmt='%s', delimiter=',', newline=' ', header='', footer='', comments='# ', encoding=None)
            np.save(self.dir+'/'+self.name[:-4]+'_time'+'.npy', self.td)

    def filter(self):

        if self.filterBtn.isChecked()==True:

            #Adaptive Equalization
            self.frame = exposure.equalize_adapthist(self.frame, clip_limit=0.03)
            self.frame=self.frame*255
            self.frame=self.frame.astype(np.uint8)

    def changeBrightness(self,img,value):
        """ This function will take an image (img) and the brightness
            value. It will perform the brightness change using OpenCv
            and after split, will merge the img and return it.
        """
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        lim = 255 - value
        v[v>lim] = 255
        v[v<=lim] += value
        final_hsv = cv2.merge((h,s,v))
        img = cv2.cvtColor(final_hsv,cv2.COLOR_HSV2BGR)
        return img

    def brightness(self,value):
        self.brightness_value_now=value
        #print("Brightness: ",value)
        self.update()
    
    def update(self):
        self.frame= self.changeBrightness(self.frame,self.brightness_value_now)



app=QApplication(sys.argv)
window=Window()
window.show()
sys.exit(app.exec_())

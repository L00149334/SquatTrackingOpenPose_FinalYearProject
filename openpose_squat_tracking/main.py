#Importing necessary libraries & packages
import sys
import numpy as np
import cv2
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QComboBox
import math
import os
from sys import platform
import argparse



#This line loads the user interface (UI) file
form_class = uic.loadUiType("openpose.ui")[0]

#This is a class that reads an image and stores its name.
class img:
    def __init__(self, img_name):
        self.img = cv2.imread(img_name)
        self.name = img_name[6: ]

#This function calculates the angle between three points.
def calculate_angle(a,b,c) -> float:
    """
    * a,b,c : Take 3 leg points to calculate the angle
    """
    a = np.array(a) #First
    b = np.array(b) #Mid
    c = np.array(c) # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

#This is a class that inherits from QMainWindow and form_class. It sets up the GUI and connects buttons to functions.
class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.videopath = ""


        self.m_btnimport.clicked.connect(self.openInputVideoFile)
        self.m_btnstart.clicked.connect(self.process)
        self.lblWidth = self.m_lblimage.frameGeometry().width()
        self.lblHeight = self.m_lblimage.frameGeometry().height()
        
        


        # initialize variables

    def dropdownChanged(self, index):
        #Do something when the dropdown changes
        print(f"Selected option: {self.dropdown.itemText(index)}")
    
    def openInputVideoFile(self):
        #set QFileDialog options to not use native dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #open a file dialog to choose a video file with .avi or .mp4 extension
        self.videopath, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Video files (*.avi *.mp4)")

        #if a video path is selected, set the import text to the path
        if self.videopath:
            self.m_strimport.setText(self.videopath)
        # otherwise, set the video path to 0 (default)    
        else:
            self.videopath = 0
            
 
    def process(self):
        print("Start")
        #if no video path is selected, set video_path to 0 (default)
        if self.videopath == "":
            video_path = 0
        #otherwise, set video_path to the selected video path    
        else:
            video_path = self.videopath
                # Windows Import(YOU HAVE TO CHANGE FOLDER WITH YOUR OPENPOSE PATH)
        sys.path.append('C:/Users/hawnc/OneDrive/Documents/openpose/build/python/openpose/Release/')
        #set openpose path for Windows
        os.environ['PATH']  = os.environ['PATH'] + ';'  + 'C:/Users/hawnc/OneDrive/Documents/openpose/build/python/openpose/Release;' + 'C:/Users/hawnc/OneDrive/Documents/openpose/build/bin;'
        # import pyopenpose library
        import pyopenpose as op

        #set argparse for image and video paths
        parser = argparse.ArgumentParser()
        parser.add_argument("--image_path", default="test.png", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
        parser.add_argument("--video_path", default="test.mp4", help="Pass the path of video or pass 0 for the live feed.",type=str)

        #Parsing command line arguments
        args = parser.parse_known_args()
        
        #Creating a dictionary to store the parameters
        params = dict()
        params["model_folder"] = "C:/Users/hawnc/OneDrive/Documents/openpose/models"

        # Add others in path
        for i in range(0, len(args[1])):
            curr_item = args[1][i]
            if i != len(args[1])-1: next_item = args[1][i+1]
            else: next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-','')
                if key not in params:  params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-','')
                if key not in params: params[key] = next_item

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        datum = op.Datum()

        #Opening video capture
        cap = cv2.VideoCapture(video_path)

        while(True):
            
            #Reading frame, Getting image height and width
            ret, frame = cap.read()

            if not ret:
                break

            img_h,img_w,_=frame.shape

            # Setting the input data of OpenPose
            datum.cvInputData = frame
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))

            # Getting pose keypoints + Extracting keypoints
            pose_keypoints = datum.poseKeypoints.tolist()[0]

            r_knee = datum.poseKeypoints[0][10]
            r_knee = r_knee[0:2]

            l_knee = datum.poseKeypoints[0][13]
            l_knee = r_knee[0:2]

            right_hip = pose_keypoints[9]

            left_hip = pose_keypoints[12]

            right_knee = pose_keypoints[10]

            left_knee = pose_keypoints[13]

            right_foot = pose_keypoints[11]

            left_foot = pose_keypoints[14]

            #Calulating average angle for Squat 
            r_knee_angle = calculate_angle(right_hip, right_knee, right_foot)
            l_knee_angle = calculate_angle(left_hip, left_knee, left_foot)
            message = "Good"
            if r_knee_angle > 120 and l_knee_angle > 120:           # If angle is greater than 120 then GO deeper
                message ="Go Deeper"
            elif r_knee_angle < 90 and l_knee_angle < 90:           # If angle is less than 90 then Too Low
                message =  "Come Back Up"
            angle = (r_knee_angle + l_knee_angle) / 2

            frame = datum.cvOutputData
            
            # Displaying text above the angle
            caption = "Squat Angle"
            cv2.putText(frame, caption, (img_w-120, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(frame, format(angle, ".2f"), (img_w-80, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
            
            cv2.putText(frame, message, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 1, cv2.LINE_AA)

        
            dst = cv2.resize(frame, (self.lblWidth, self.lblHeight))
            hei, wid, channel = dst.shape
            bytesPerLine = 3 * wid
            tImg = QImage(dst.data, wid, hei, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            self.m_lblimage.setPixmap(QtGui.QPixmap.fromImage(tImg))
            
            cv2.waitKey(20)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()


#'calculate_angle' took inspiration from https://github.com/francesco-mazzoni/Mini-project-Computer-Vision

import sys
import numpy as np
import cv2
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *
import math
import os


from sys import platform
import argparse



class img:
    def __init__(self, img_name):
        self.img = cv2.imread(img_name)
        self.name = img_name[6: ]

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

# class MyWindow(QMainWindow, form_class):

#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#         self.videopath = ""
#         self.m_btnimport.clicked.connect(self.openInputVideoFile)
#         self.m_btnstart.clicked.connect(self.process)
#         self.lblWidth = self.m_lblimage.frameGeometry().width()
#         self.lblHeight = self.m_lblimage.frameGeometry().height()
        
        


#         # ============================================== initialize variables ==================================================


#     def openInputVideoFile(self):
#         options = QFileDialog.Options()
#         options |= QFileDialog.DontUseNativeDialog
#         self.videopath, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Video files (*.avi *.mp4)")

        
        

#         if self.videopath:
#             self.m_strimport.setText(self.videopath)
#         else:
#             QMessageBox().information(self, "Alert", "Please choose video file")
            


#     def process(self):
#         print("Start")
#         if self.videopath == "":
#             QMessageBox().information(self, "Alert", "Please choose video file")
#         else:
#             # try:    
#             # try:
#                 # Windows Import(YOU HAVE TO CHANGE FOLDER WITH YOUR OPENPOSE PATH)
#             sys.path.append('C:/Users/hawnc/OneDrive/Documents/openpose/build/python/openpose/Release/')
#             os.environ['PATH']  = os.environ['PATH'] + ';'  + 'C:/Users/hawnc/OneDrive/Documents/openpose/build/python/openpose/Release;' + 'C:/Users/hawnc/OneDrive/Documents/openpose/build/bin;'
#             import pyopenpose as op

#             # except ImportError as e:
#             #     print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
#             #     raise e
#             print("1111111111111111111111111111111111111111")
#             parser = argparse.ArgumentParser()
#             parser.add_argument("--image_path", default="test.png", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
#             parser.add_argument("--video_path", default="test.mp4", help="Pass the path of video or pass 0 for the live feed.",type=str)

#             args = parser.parse_known_args()
            
#             params = dict()
#             params["model_folder"] = "C:/Users/hawnc/OneDrive/Documents/openpose/models"
#             print("222222222222222222222222222222222222")
#             # Add others in path?
#             for i in range(0, len(args[1])):
#                 curr_item = args[1][i]
#                 if i != len(args[1])-1: next_item = args[1][i+1]
#                 else: next_item = "1"
#                 if "--" in curr_item and "--" in next_item:
#                     key = curr_item.replace('-','')
#                     if key not in params:  params[key] = "1"
#                 elif "--" in curr_item and "--" not in next_item:
#                     key = curr_item.replace('-','')
#                     if key not in params: params[key] = next_item

#             # Starting OpenPose
#             opWrapper = op.WrapperPython()
#             opWrapper.configure(params)
#             opWrapper.start()

#             datum = op.Datum()

#             # cap = cv2.VideoCapture(self.videopath)
#             cap = cv2.VideoCapture(args.video_path)

#             print("Development")

#             while(True):
                
#                 ret, frame = cap.read()

#                 datum.cvInputData = frame
#                 opWrapper.emplaceAndPop(op.VectorDatum([datum]))

#                 pose_keypoints = datum.poseKeypoints.tolist()[0]

#                 r_knee = datum.poseKeypoints[0][10]
#                 r_knee = r_knee[0:2]

#                 l_knee = datum.poseKeypoints[0][13]
#                 l_knee = r_knee[0:2]

#                 right_hip = pose_keypoints[9]

#                 left_hip = pose_keypoints[12]

#                 right_knee = pose_keypoints[10]

#                 left_knee = pose_keypoints[13]

#                 right_foot = pose_keypoints[11]

#                 left_foot = pose_keypoints[14]

#                 #Calulating average angle for Squat 
#                 r_knee_angle = calculate_angle(right_hip, right_knee, right_foot)
#                 l_knee_angle = calculate_angle(left_hip, left_knee, left_foot)
#                 message = "Good"
#                 if r_knee_angle > 160 and l_knee_angle > 160:           # If angle is greater than 160 then GO deeper
#                     message ="Go Deeper"
#                 elif r_knee_angle < 90 and l_knee_angle < 90:           # If angle is less than 90 then Too Low
#                     message =  "Too Low"
#                 angle = (r_knee_angle + l_knee_angle) / 2

#                 frame = datum.cvOutputData
                
#                 cv2.putText(frame, str(angle), (int(r_knee[0]), int(r_knee[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
#                 cv2.putText(frame, message, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 1, cv2.LINE_AA)

            
#                 dst = cv2.resize(frame, (self.lblWidth, self.lblHeight))
#                 hei, wid, channel = dst.shape
#                 bytesPerLine = 3 * wid
#                 tImg = QImage(dst.data, wid, hei, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
#                 self.m_lblimage.setPixmap(QtGui.QPixmap.fromImage(tImg))
#                 print("***************************************************")
#                 cv2.waitKey(20)
#             # except:
#             #     return

def process():
    print("Start")

    # try:    
    # try:
        # Windows Import(YOU HAVE TO CHANGE FOLDER WITH YOUR OPENPOSE PATH)
    sys.path.append('C:/Users/hawnc/OneDrive/Documents/openpose/build/python/openpose/Release/')
    os.environ['PATH']  = os.environ['PATH'] + ';'  + 'C:/Users/hawnc/OneDrive/Documents/openpose/build/python/openpose/Release;' + 'C:/Users/hawnc/OneDrive/Documents/openpose/build/bin;'
    import pyopenpose as op

    # except ImportError as e:
    #     print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    #     raise e
    print("1111111111111111111111111111111111111111")
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="test.png", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    parser.add_argument("--video_path", default="test.mp4", help="Pass the path of video or pass 0 for the live feed.",type=str)

    args = parser.parse_known_args()
    
    params = dict()
    params["model_folder"] = "C:/Users/hawnc/OneDrive/Documents/openpose/models"
    print("222222222222222222222222222222222222")
    # Add others in path?
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

    # cap = cv2.VideoCapture(self.videopath)
    cap = cv2.VideoCapture(args.video_path)

    print("Development")

    while(True):
        try:
            ret, frame = cap.read()

            datum.cvInputData = frame
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))

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
            if r_knee_angle > 160 and l_knee_angle > 160:           # If angle is greater than 160 then GO deeper
                message ="Go Deeper"
            elif r_knee_angle < 90 and l_knee_angle < 90:           # If angle is less than 90 then Too Low
                message =  "Too Low"
            angle = (r_knee_angle + l_knee_angle) / 2

            frame = datum.cvOutputData
            
            cv2.putText(frame, str(angle), (int(r_knee[0]), int(r_knee[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(frame, message, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 1, cv2.LINE_AA)

        
            dst = cv2.resize(frame, (1280,720))
            hei, wid, channel = dst.shape
            bytesPerLine = 3 * wid
            # tImg = QImage(dst.data, wid, hei, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            # self.m_lblimage.setPixmap(QtGui.QPixmap.fromImage(tImg))
            print("***************************************************")
            # cv2.waitKey(20)
            cv2.imshow("output",dst)
            # cv2.waitKey(0)
        except KeyboardInterrupt as e:
            print(e)
            cv2.destroyAllWindows()
            cap.release()
if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # myWindow = MyWindow()
    # myWindow.show()
    # app.exec_()

    process()

# SquatTrackingOpenPose_FinalYearProject

This is a project that uses OpenPose to analyze squat form in videos. It uses the PyOpenPose library to extract pose keypoints from video frames and calculate the angles between the joints in the legs to determine whether the squat form is correct.

To use this project, you will need to have the following installed on your machine:

- Python 3.9
- Numpy
- OpenCV
- PyQt5

In addition, you will need to install OpenPose. This project was tested with OpenPose version 1.7.0. Please follow the installation instructions on the OpenPose GitHub page.

To use the program, run the `main.py` file. This will open a GUI with two buttons: "Import Video" and "Start Analysis". Click the "Import Video" button to select the video you want to analyse. The video must be in AVI or MP4 format. Once you have selected the video, the path to the video file will be displayed in the text box. 

Click the "Start Analysis" button to begin analyzing the video. The program will calculate the angles between the joints in the legs for each frame of the video and display the average angle at the end of the analysis. If the average angle is less than 90 degrees, the squat form is considered correct. If the average angle is greater than or equal to 120 degrees, the squat form is considered incorrect.

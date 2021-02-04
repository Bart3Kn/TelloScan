#I need more imports
from Tello import tello
import time
import datetime
import cv2
import numpy as np
from  matplotlib import pyplot as plt


#VIDEO FEED
def droneTesting():

    print("Drone Testing")
    drone = tello()

    drone.startConnection()
    drone.streamOn()
    time.sleep(2)
    drone.startProcesses()

def cameraTesting():

    print("Camera Testing")
    width = 1280
    height = 720
    capture = cv2.VideoCapture(0)

    captureStatus = capture.isOpened()

    print(captureStatus)
    while (captureStatus==True) :
                
        works, frame = capture.read()
        print(works)

        resized = cv2.resize(frame,(width,height))

        bwVideo = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Video Feed", frame)

        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

def depthTesting():
    #Test images
    imgL = cv2.imread(r'C:\Users\barte\Desktop\Photo Left.jpg',0)
    imgR = cv2.imread(r'C:\Users\barte\Desktop\Photo Right.jpg',0)

    #Resoltion of image
    height, width = imgL.shape

    #Depth Map from images
    stereo = cv2.StereoBM_create(16,15)
    disparity = stereo.compute(imgL,imgR)

    plt.imshow(disparity, 'gray')
    plt.show()

    #Resizing Images
    imgL = cv2.resize(imgL,(int(width/4),int(height/4)))
    imgR = cv2.resize(imgR,(int(width/4),int(height/4)))

    cv2.imshow("LEFT", imgL)
    cv2.imshow("RIGHT", imgR)
    cv2.waitKey(0)

def findCameras():
    num = 0
    while num<10:
        cap = cv2.VideoCapture(num)
        if cap.isOpened():
            # working capture
            num += 1
            print(num)
        else:
            break

    print("Number of Cameras:" + str(num))

#LEARNING THIS
def HarrisCorner():
    print("Harris Corner")

    width = 1280
    height = 720
    capture = cv2.VideoCapture(0)

    captureStatus = capture.isOpened()

    print(captureStatus)
    while (captureStatus==True) :
                
        works, frame = capture.read()
        resized  = frame
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        #HARRIS CORNER DETECTION

        # find Harris corners
        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray,2,3,0.04)
        dst = cv2.dilate(dst,None)
        ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
        dst = np.uint8(dst)

        # find centroids
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

        # define the criteria to stop and refine the corners
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

        # Now draw them
        res = np.hstack((centroids,corners))
        res = np.int0(res)
        frame[res[:,1],res[:,0]]=[0,0,255]
        frame[res[:,3],res[:,2]] = [0,255,0]

        cv2.imshow("Harris", frame)



def orbSLAM():
        print("ORB SLAM")
        capture = cv2.VideoCapture(0)

        captureStatus = capture.isOpened()
        orb = cv2.ORB_create(nfeatures = 100000)

        print(captureStatus)
        while (captureStatus==True) :
                
            works, frame = capture.read()
            resized  = frame
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

            
            keypoints_orb, descriptors = orb.detectAndCompute(gray, None)
            bwFrame_orb = cv2.drawKeypoints(gray, keypoints_orb, None, color = (0,0,255), flags = 0)
            cv2.imshow("orb", bwFrame_orb)

            if(cv2.waitKey(1) & 0xFF == ord('q')):
                break



def siftSLAM():
    print("SIFT SLAM")
    capture = cv2.VideoCapture(0)
    captureStatus = capture.isOpened()

    while (captureStatus==True) :
                
        works, frame = capture.read()
        gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        sift = cv2.SIFT()
        kp = sift.detect(gray,None)

        img=cv2.drawKeypoints(gray,kp)
        cv2.imshow("SIFT", img)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break


#Works fine
def odometryTesting():
    drone = tello()
    drone.startConnection()
    drone.startProcesses()
    while(True):
        drone.printStates()



if __name__ == "__main__":
    droneTesting()

    
    
    
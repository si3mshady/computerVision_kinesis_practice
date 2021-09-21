import cv2
import numpy as np

cap = cv2.VideoCapture('./bestSwings.mp4')

def cropImage(frame,row_percentage=.1,column_percentage=.1):
    x, y, _ = frame.shape  
    startX = int(x * row_percentage)
    endX = int(x - startX)
    startY = int(y * column_percentage)
    endY = int(y - startY)   
    return startX,endX,startY,endY

def flip_image(frame):
    return cv2.flip(frame,1)


def cannyEdge(frame):
    return cv2.Canny(frame, 10, 180)


def threshold(frame):
   return cv2.threshold(frame,30, 100, cv2.THRESH_BINARY )[1]
    

def adjustContrast(frame,intensity=.91):       
      contrast_matrix = np.ones(frame.shape, dtype = "uint8") * intensity
      frame_adjusted = np.uint8(cv2.multiply(np.float64(frame), contrast_matrix ))
      return frame_adjusted

def greyscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY )

while cap.isOpened():
    _, frame = cap.read()

    startX,endX,startY,endY =  cropImage(frame,.2,.3)
    cropped_frame = frame[startX:endX,startY:endY]  
    cropped_frame = greyscale(cropped_frame)
    # newFrame = cannyEdge(cropped_frame)     
    cv2.imshow('si3mshady', cannyEdge(cropped_frame))
    cv2.waitKey(0)

    if cv2.waitKey(1) == 27:
        break
    
cv2.destroyAllWindows()
cv2.release()


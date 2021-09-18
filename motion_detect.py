import cv2 as cv
import numpy as np
from PIL import Image
from  utility import getStream, getBucket


s3, bucket = getBucket()
kinesis, stream = getStream()

cap = cv.VideoCapture('./yp.mp4')

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():

    motiondiff = cv.absdiff(frame1, frame2)
   
    gray = cv.cvtColor(motiondiff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5,5), 0)

    _, thresh = cv.threshold(blur, 80, 255, cv.THRESH_BINARY)

    dilate = cv.dilate(thresh, None, iterations=3)   

    contours, _ = cv.findContours(dilate, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv.boundingRect(contour)

        if cv.contourArea(contour) < 800:
            continue        
        cv.rectangle(frame1, (x,y), (x+w, y+h), (0, 255, 0), 2)

        success, encoded_image = cv.imencode('.jpg', frame1.copy())
        data_encode = np.array(encoded_image)
        strencode = data_encode.tostring()
     
        kinesis.put_record(StreamName=stream, Data=strencode,PartitionKey="888")
       
        cv.putText(frame1, "Motion: {}".format("Yes"), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv.imshow("Motion", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv.waitKey(50) == 27:
        break

cap.release()
cv.destroyAllWindows()

# https://stackoverflow.com/questions/50630045/how-to-turn-numpy-array-image-to-bytes
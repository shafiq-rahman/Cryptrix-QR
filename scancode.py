import cv2
import numpy as np
from pyzbar.pyzbar import decode
check = 0

def decoder(image, count):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)
    x = 0
    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
        x = 1
        # cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
        print("Barcode: "+barcodeData +" | Type: "+barcodeType)
    # count += 1
    return str(barcodeData)

cap = cv2.VideoCapture(0)
count = 0
while True:
    ret, frame = cap.read()
    try:
        val = decoder(frame, count)
        if val:
            print(val)
            break
    except:
        pass
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break
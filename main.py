from asyncio import subprocess
import email
from urllib import request
from flask import Flask, render_template, redirect, url_for, request
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import requests

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        check = 0
        def check(barcode):
            values = []
            temp = ""
            spec_char = ['\'', '[', ']', ' ']
            for each in barcode:
                if each not in spec_char:
                    temp += each
                if each == ',':
                    values.append(temp[:-1])
                    temp = ""
            return values

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
            return check(barcodeData)

        cap = cv2.VideoCapture(0)
        count = 0
        while True:
            ret, frame = cap.read()
            try:
                val = decoder(frame, count)
                if val:
                    print(val)
                    return redirect(url_for("profile", name = val[0], email = val[5], num = val[6]))
            except:
                pass
            cv2.imshow('Image', frame)
            code = cv2.waitKey(10)
            if code == ord('q'):
                break
    return render_template("scanPage.html")

@app.route("/<name>")
def profile(name):
    email = request.args['email']
    num = request.args['num']
    return render_template("studentinfo.html", name = name, email = email, number = num)

if __name__ == "__main__":
    app.run(debug = True)

# return redirect(url_for("test"))
#Video kütüphanelerini yüklüyoruz
from imutils.video import VideoStream
from imutils.video import FPS
import imutils

import time 
from datetime import datetime
import pyautogui 

#argparse kütüphanesi, uygulamaya parametre geçmek için kullanılır
#argparse kütüphanesini debug modda çalışırken kullanmayacağız.
#İlerde uygulamayı exe olarak çalıştırdığımızda gerekebilr
import argparse

#uygulamayı duraksatmak, yavaşlatmak için kullanacağız
import threading
import time

#opencv görüntü işleme kütüphanesi
import cv2

ap = argparse.ArgumentParser()
args = vars(ap.parse_args())
pyautogui.FAILSAFE = False

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def moveMouse(x, y, dur):
    print("deneme")

#obje tanıma işleminde, objeyi bilgisayara tanıtmak için bazı hazır şablon
#dosyalarından yararlanacağız

#bizim projemizde, kamera yüzümüze zaten çok yakın konumda bulunacağından
#dolayı, yüzün çerçevesini algılamaya gerek yok
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #yüz tanıma şablonu
mouth_cascade = cv2.CascadeClassifier("data_haarcascades_haarcascade_mcs_mouth.xml") #ağız tanıma şablonu
upperbody_cascade = cv2.CascadeClassifier("haarcascade_mcs_upperbody.xml") #ağız tanıma şablonu



#istersek uygulamamızı video üzerinden de çalıştırabiliriz
#videopath="firdevs_goz.mov"
videopath = ""

#hangi kameradan çalışmak istersek onun numarasını veriyoruz.
#genellikle dahili kamera 0 numaradır.  USB'den bağlanan kameralar 1,2,3...
#şeklinde sıralanır
camNo = 0

#resmi iki boyuta indirgerken kullanacağımız eşik değer.  0 ile 255 arasında
#bir değer olabilir.
#ortam ışığı, görüntü kalitesi, göz rengi gibi ortam koşullarına göre
#ayarlanması gerek
#projenin ileri aşamalarında kalibrasyon eklenmesi, mümkünse uygulamanın en
#uygun değeri otomatik bularak bu değeri belirlemesi hedefleniyor
thresholdValue = 3

yatay = 1280
dikey = 800

#bu değişkeni boş bırakırsak uygulama kameradan çalışır
if videopath != "":
    vs = cv2.VideoCapture(videopath)

else:
    print("[DIKKAT] kameradan görüntü algilama baslatiliyor...")
    vs = VideoStream(src=camNo).start()
    time.sleep(1.0)

fps = None

#uygulamamız biz kapatmadığımız sürece sürekli çalışacak.
#bu nedenle sonsuz bir while döngüsü içine alıyoruz

faceDetected = 0
mouthDetected = 0
upperbodyDetected = 0

while True:

    #video modu
    if videopath != "":
        ret, frame = vs.read()
        if ret is False:
            break

        roi = frame[0: 500, 0: 1400] #dikkate alınacak resmin çerçeve alanı
        rows, cols, ret = roi.shape
        gray_roi = cv2.cvtColor(roi, 6)
        gray_roi = cv2.GaussianBlur(gray_roi, (1, 1), 0)

    #kamera modu
    else:
        frame = vs.read()
        frame = frame[0: int(dikey / 2), 0: int(yatay / 2)]
        #frame = cv2.flip(frame,0) #burası kameradan alınan görüntüyü ters
        #çevirmek için.
        frame = frame[1] if args.get("video", False) else frame
        #resmi siyah beyaz moduna dönüştürüyoruz.  yani siyah beyaz sinema
        #filmi gibi.
        #bizim siyah dışında bir renkle işimiz olmadığından performans
        #açısından avantajlı
        gray_roi = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #yüzü tespit ediyoruz.
    faces = face_cascade.detectMultiScale(gray_roi, 1.3, 3)
    #üst vücudu tespit ediyoruz
    upperbodies = upperbody_cascade.detectMultiScale(gray_roi, 1.3, 3)
    #ağzı tespit ediyoruzz
    mouths = mouth_cascade.detectMultiScale(gray_roi, 1.3, 3)
    


    if (faceDetected == 1 or upperbodyDetected == 1) and mouthDetected == 0:
        print("maske var")
        time.sleep(1.0)
    if (faceDetected == 1 or upperbodyDetected == 1) and mouthDetected == 1:
        print("maske yok")
        time.sleep(1.0)
    if faceDetected == 0 and upperbodyDetected == 0:
        print("görüntüde insan yok")
        time.sleep(1.0)

    faceDetected = 0
    mouthDetected = 0
    upperbodyDetected = 0


    faceDetected = 0

    for (x,y,w,h) in faces:
     faceDetected = 1
     roi_gray = gray_roi[y:y + h, x:x + w]
     roi_color = frame[y:y + h, x:x + w]


     rows, cols, ret = roi_color.shape
     #iki renge düşürme işi burada yapılıyor.  Optimum değeri bulmak gerek
     ret, threshold = cv2.threshold(roi_gray, thresholdValue, 255, cv2.THRESH_BINARY_INV) 
 

 
     #yüzü ekrana veriyoruz
     cv2.imshow("Threshold", threshold)
     cv2.imshow("roi_gray", roi_gray)

    for (x,y,w,h) in upperbodies:
     upperbodyDetected = 1
     roi_gray = gray_roi[y:y + h, x:x + w]
     roi_color = frame[y:y + h, x:x + w]


     rows, cols, ret = roi_color.shape
     #iki renge düşürme işi burada yapılıyor.  Optimum değeri bulmak gerek
     ret, threshold = cv2.threshold(roi_gray, thresholdValue, 255, cv2.THRESH_BINARY_INV) 
 
     cv2.imshow("Threshold", threshold)
     #siyah beyaz (film gibi) göz bebeği görüntüsünü ekrana veriyoruz
     cv2.imshow("roi_gray", roi_gray)

    for (x,y,w,h) in mouths:
     mouthDetected = 1
     roi_gray = gray_roi[y:y + h, x:x + w]
     roi_color = frame[y:y + h, x:x + w]


     rows, cols, ret = roi_color.shape
     #iki renge düşürme işi burada yapılıyor.  Optimum değeri bulmak gerek
     ret, threshold = cv2.threshold(roi_gray, thresholdValue, 255, cv2.THRESH_BINARY_INV) 
 

     cv2.imshow("Threshold", threshold)
     #siyah beyaz (film gibi) göz bebeği görüntüsünü ekrana veriyoruz
     cv2.imshow("roi_gray", roi_gray)

    #ana görüntü çerçevesini ekrana veriyoruz
    cv2.imshow("frame",frame)

    #uygulamayı kapatmak için herhangi bir ESC tuşuna basıyoruz
    key = cv2.waitKey(30)
    if key == 27:
        break

#tüm pencereleri kapatıp uygulamayı kapatıyoruz
cv2.destroyAllWindows()

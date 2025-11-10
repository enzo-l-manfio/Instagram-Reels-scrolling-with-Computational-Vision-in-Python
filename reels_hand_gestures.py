from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import time


# If geckodriver is in your PATH:
driver = webdriver.Firefox()

    # If geckodriver is not in your PATH, specify the executable_path:
    # service = Service(executable_path='/path/to/your/geckodriver')
    # driver = webdriver.Firefox(service=service)

driver.get("https://www.instagram.com")

base_options = python.BaseOptions(model_asset_path=r"C:\gesture_recognizer.task")
#Substitute with the path of the .task file in your computer

options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)
results = []

video = cv.VideoCapture(0)

ultimo_reel = time.time()

while True:
    sucesso, imagem = video.read()
    if not sucesso:
        break
    imagem = cv.flip(imagem, 1)
    imagem_rgb = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)
    mp_imagem = mp.Image(image_format=mp.ImageFormat.SRGB, data=imagem_rgb)
    recognition_result = recognizer.recognize(mp_imagem)
    if recognition_result.gestures and recognition_result.gestures[0]:
        agora = time.time()
        top_gesture = recognition_result.gestures[0][0]
        print(recognition_result.gestures[0][0].category_name)
        if recognition_result.gestures[0][0].category_name == 'Thumb_Down' and agora - ultimo_reel >=3:
            ultimo_reel = time.time()
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_UP)
    
        elif recognition_result.gestures[0][0].category_name == 'Pointing_Up' and agora - ultimo_reel >=3 :
            ultimo_reel == time.time()
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_DOWN)
        
        elif recognition_result.gestures[0][0].category_name == 'Open_Palm' :
            break
    else:
        print("No gesture detected")

    cv.imshow("Image", imagem)
    cv.waitKey(1)

video.release()
cv.destroyAllWindows()
driver.close()

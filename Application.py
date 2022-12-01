# Importing Libraries

from turtle import color
import numpy as np

import cv2
import os
import sys
import time
import operator

from string import ascii_uppercase

import tkinter as tk
from PIL import Image, ImageTk

from hunspell import Hunspell
import enchant

from keras.models import model_from_json

os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"

# Application :


class Application:

    def __init__(self):

        self.hs = Hunspell('en_US')
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None
        self.json_file = open(
            "F:\capstone project\Sign-Language-To-Text-Conversion\Models\model_new.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()

        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights(
            "F:\capstone project\Sign-Language-To-Text-Conversion\Models\model_new.h5")

        self.json_file_dru = open(
            "F:\capstone project\Sign-Language-To-Text-Conversion\Models\model-bw_dru.json", "r")
        self.model_json_dru = self.json_file_dru.read()
        self.json_file_dru.close()

        self.loaded_model_dru = model_from_json(self.model_json_dru)
        self.loaded_model_dru.load_weights(
            "F:\capstone project\Sign-Language-To-Text-Conversion\Models\model-bw_dru.h5")
        self.json_file_tkdi = open(
            "F:\capstone project\Sign-Language-To-Text-Conversion\Models\model-bw_tkdi.json", "r")
        self.model_json_tkdi = self.json_file_tkdi.read()
        self.json_file_tkdi.close()

        self.loaded_model_tkdi = model_from_json(self.model_json_tkdi)
        self.loaded_model_tkdi.load_weights(
            "F:\capstone project\Sign-Language-To-Text-Conversion\Models\model-bw_tkdi.h5")
        self.json_file_smn = open(
            "F:\capstone project\Sign-Language-To-Text-Conversion\Models\model-bw_smn.json", "r")
        self.model_json_smn = self.json_file_smn.read()
        self.json_file_smn.close()

        self.loaded_model_smn = model_from_json(self.model_json_smn)
        self.loaded_model_smn.load_weights(
            "F:\capstone project\Sign-Language-To-Text-Conversion\Models\model-bw_smn.h5")

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0

        for i in ascii_uppercase:
            self.ct[i] = 0

        print("Loaded model from disk")

        self.root = tk.Tk()
        self.root.title("Indian Sign Language To Text Conversion")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("1200x900")
        self.root.config(bg = "white")
        self.panel = tk.Label(self.root)
        self.panel.place(x=560, y=20, width=600, height=400)
        self.panel.config(borderwidth=1, relief=tk.SOLID)

        self.dummy = tk.Label(self.root)
        self.dummy.place(x = 5, y= 70, width=545, height=560)
        self.dummy.config(bg="light cyan")

        self.dummy1 = tk.Label(self.root)
        self.dummy1.place(x = 70, y=100)
        self.dummy1.config(text = "HOW TO USE THE INTERFACE", font=("Courier", 20, "bold"), bg="light cyan")


        self.dummy2 = tk.Label(self.root)
        self.dummy2.place(x = 75, y=150)
        self.dummy2.config(text = "1. Hold your hand in position for atleast 5 sec.", font=("Courier", 10, "bold"), bg="light cyan")
        
        self.dummy3 = tk.Label(self.root)
        self.dummy3.place(x = 75, y=200)
        self.dummy3.config(text = "2. Double click on the words coming in suggestions.", font=("Courier", 10, "bold"), bg="light cyan")

        self.dummy4 = tk.Label(self.root)
        self.dummy4.place(x = 75, y=250)
        self.dummy4.config(text = "3. Sentences are formed to convey your message.", font=("Courier", 10, "bold"), bg="light cyan")

        self.dummy = tk.Label(self.root)
        self.dummy.place(x = 5, y= 320, width=545, height=310)
        self.dummy.config(bg="antique white")

        self.dummy4 = tk.Label(self.root)
        self.dummy4.place(x = 75, y=400)
        self.dummy4.config(text = "CAPSTONE PROJECT", font=("Courier", 30, "bold"), bg="antique white")


        self.dummy4 = tk.Label(self.root)
        self.dummy4.place(x = 160, y=450)
        self.dummy4.config(text = "-CPG NO 93", font=("Courier", 30, "bold"), bg="antique white")

        self.dummy4 = tk.Label(self.root)
        self.dummy4.place(x = 55, y=550)
        self.dummy4.config(text = "Divya Goel, Shubham Jindal, Aashish Bansal, Lavish Garg", font=("Courier", 10, "bold"), bg="antique white")

        self.panel2 = tk.Label(self.root)  # initialize image panel
        self.panel2.place(x=840, y=72, width=315, height=340)
        self.panel2.config(borderwidth=1, relief=tk.SOLID)
        self.T = tk.Label(self.root)
        self.T.place(x=35, y=5)
        self.T.config(text="Indian Sign Language To Text Conversion",
                      font=("Courier", 37, "bold"))

        self.panel3 = tk.Label(self.root)  # Current Symbol
        self.panel3.place(x=960, y=425)
        self.panel3.config(bg = "white")
        
        self.T1 = tk.Label(self.root)
        self.T1.place(x=560, y=425)
        self.T1.config(text="Character :", font=("Courier", 20, "bold"), bg = "white")

        self.panel4 = tk.Label(self.root)  # Word
        self.panel4.place(x=730, y=470)
        self.panel4.config(bg = "white")

        self.T2 = tk.Label(self.root)
        self.T2.place(x=560, y=470)
        self.T2.config(text="Word :", font=("Courier", 20, "bold"), bg = "white")

        self.panel5 = tk.Label(self.root)  # Sentence
        self.panel5.place(x=730, y=515)
        self.panel5.config(bg = "white")

        self.T3 = tk.Label(self.root)
        self.T3.place(x=560, y=515)
        self.T3.config(text="Sentence :", font=("Courier", 20, "bold"), bg = "white")

        self.T4 = tk.Label(self.root)
        self.T4.place(x=710, y=550)
        self.T4.config(text="Suggestions :", fg="blue",
                       font=("Courier", 30, "bold"), borderwidth=1, relief=tk.SOLID)

        self.bt1 = tk.Button(
            self.root, command=self.action1, height=0, width=0)
        self.bt1.place(x=560, y=600)
        self.bt1.config(bg="lawn green", borderwidth=1, relief=tk.SOLID)
        self.bt2 = tk.Button(
            self.root, command=self.action2, height=0, width=0)
        self.bt2.place(x=860, y=600)
        self.bt2.config(bg="lawn green", borderwidth=1, relief=tk.SOLID)
        

        self.bt3 = tk.Button(
            self.root, command=self.action3, height=0, width=0)
        self.bt3.place(x=1100, y=600)
        self.bt3.config(bg="lawn green", borderwidth=1, relief=tk.SOLID)

        self.str = ""
        self.word = " "
        self.current_symbol = "Empty"
        self.photo = "Empty"
        self.video_loop()

    def video_loop(self):
        ok, frame = self.vs.read()

        if ok:
            cv2image = cv2.flip(frame, 1)

            x1 = int(0.5 * frame.shape[1])
            y1 = 10
            x2 = frame.shape[1] - 10
            y2 = int(0.5 * frame.shape[1])

            cv2.rectangle(frame, (x1 - 1, y1 - 1),
                          (x2 + 1, y2 + 1), (255, 0, 0), 1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)

            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)

            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            cv2image = cv2image[y1: y2, x1: x2]

            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)

            blur = cv2.GaussianBlur(gray, (5, 5), 2)

            th3 = cv2.adaptiveThreshold(
                blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

            ret, res = cv2.threshold(
                th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            self.predict(res)

            self.current_image2 = Image.fromarray(res)

            imgtk = ImageTk.PhotoImage(image=self.current_image2)

            self.panel2.imgtk = imgtk
            self.panel2.config(image=imgtk)

            self.panel3.config(text=self.current_symbol, font=("Courier", 30))

            self.panel4.config(text=self.word, font=("Courier", 30))

            self.panel5.config(text=self.str, font=("Courier", 30))

            predicts = self.hs.suggest(self.word)

            if(len(predicts) > 1):

                self.bt1.config(text=predicts[0], font=("Courier", 20))

            else:

                self.bt1.config(text="")

            if(len(predicts) > 2):

                self.bt2.config(text=predicts[1], font=("Courier", 20))

            else:

                self.bt2.config(text="")

            if(len(predicts) > 3):

                self.bt3.config(text=predicts[2], font=("Courier", 20))

            else:

                self.bt3.config(text="")

        self.root.after(5, self.video_loop)

    def predict(self, test_image):

        test_image = cv2.resize(test_image, (128, 128))

        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))

        result_dru = self.loaded_model_dru.predict(
            test_image.reshape(1, 128, 128, 1))

        result_tkdi = self.loaded_model_tkdi.predict(
            test_image.reshape(1, 128, 128, 1))

        result_smn = self.loaded_model_smn.predict(
            test_image.reshape(1, 128, 128, 1))

        prediction = {}

        prediction['blank'] = result[0][0]

        inde = 1

        for i in ascii_uppercase:

            prediction[i] = result[0][inde]

            inde += 1

        # LAYER 1

        prediction = sorted(prediction.items(),
                            key=operator.itemgetter(1), reverse=True)

        self.current_symbol = prediction[0][0]

        # LAYER 2

        if(self.current_symbol == 'D' or self.current_symbol == 'R' or self.current_symbol == 'U'):

            prediction = {}

            prediction['D'] = result_dru[0][0]
            prediction['R'] = result_dru[0][1]
            prediction['U'] = result_dru[0][2]

            prediction = sorted(prediction.items(),
                                key=operator.itemgetter(1), reverse=True)

            self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'D' or self.current_symbol == 'I' or self.current_symbol == 'K' or self.current_symbol == 'T'):

            prediction = {}

            prediction['D'] = result_tkdi[0][0]
            prediction['I'] = result_tkdi[0][1]
            prediction['K'] = result_tkdi[0][2]
            prediction['T'] = result_tkdi[0][3]

            prediction = sorted(prediction.items(),
                                key=operator.itemgetter(1), reverse=True)

            self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'M' or self.current_symbol == 'N' or self.current_symbol == 'S'):

            prediction1 = {}

            prediction1['M'] = result_smn[0][0]
            prediction1['N'] = result_smn[0][1]
            prediction1['S'] = result_smn[0][2]

            prediction1 = sorted(prediction1.items(),
                                 key=operator.itemgetter(1), reverse=True)

            if(prediction1[0][0] == 'S'):

                self.current_symbol = prediction1[0][0]

            else:

                self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'blank'):

            for i in ascii_uppercase:
                self.ct[i] = 0

        self.ct[self.current_symbol] += 1

        if(self.ct[self.current_symbol] > 60):

            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue

                tmp = self.ct[self.current_symbol] - self.ct[i]

                if tmp < 0:
                    tmp *= -1

                if tmp <= 20:
                    self.ct['blank'] = 0

                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return

            self.ct['blank'] = 0

            for i in ascii_uppercase:
                self.ct[i] = 0

            if self.current_symbol == 'blank':

                if self.blank_flag == 0:
                    self.blank_flag = 1

                    if len(self.str) > 0:
                        self.str += " "

                    self.str += self.word

                    self.word = ""

            else:

                if(len(self.str) > 16):
                    self.str = ""

                self.blank_flag = 0

                self.word += self.current_symbol

    def action1(self):

        predicts = self.hs.suggest(self.word)

        if(len(predicts) > 0):

            self.word = ""

            self.str += " "

            self.str += predicts[0]

    def action2(self):

        predicts = self.hs.suggest(self.word)

        if(len(predicts) > 1):
            self.word = ""
            self.str += " "
            self.str += predicts[1]

    def action3(self):

        predicts = self.hs.suggest(self.word)

        if(len(predicts) > 2):
            self.word = ""
            self.str += " "
            self.str += predicts[2]

    def action4(self):

        predicts = self.hs.suggest(self.word)

        if(len(predicts) > 3):
            self.word = ""
            self.str += " "
            self.str += predicts[3]

    def action5(self):

        predicts = self.hs.suggest(self.word)

        if(len(predicts) > 4):
            self.word = ""
            self.str += " "
            self.str += predicts[4]

    def destructor(self):

        print("Closing Application...")

        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()


print("Starting Application...")

(Application()).root.mainloop()

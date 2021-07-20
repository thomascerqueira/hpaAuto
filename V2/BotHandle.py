from tkinter.constants import TRUE
from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import Key, Listener, Controller as keyboardController
import time
import pyperclip

usleep = lambda x: time.sleep(x/1000000.0)

def mouseClick(mouse, wich=False):
    if not wich:
        mouse.press(Button.left)
        mouse.release(Button.left)
    else:
        mouse.press(Button.right)
        mouse.release(Button.right)

def keyboardPress(keyboard, key, maj=False):
    if maj:
        with keyboard.pressed(Key.shift):
            keyboard.press(key)
            keyboard.release(key)
    else:
        keyboard.press(key)
        keyboard.release(key) 

class GetMousePos:
    cegiPos = (0,0)
    copyPos = (0,0)
    mouse = mouseController()
    keyboard = keyboardController()
    status = 0

    def on_release(self, key):
        try:
            if key.char == 'c' or key.char == 'C':
                if self.status == 0:
                    self.cegiPos = self.mouse.position
                    self.status = 1
                    print("Positionner la souris sur 'Copy All to Clipboard'")
                else:
                    self.copyPos = self.mouse.position
                    self.mouse.position = (self.mouse.position, self.mouse.position + 200)
                    mouseClick(self.mouse)
                    return False
        except:
            pass

    def get_Mouse_Pos(self):
        with Listener(on_release=self.on_release) as listener:
            listener.join()
        return self.cegiPos, self.copyPos

class Bot:
    mouse = mouseController()
    keyboard = keyboardController()

    def __init__(self, mousePos1, mousePos2):
        self.cegiPos = mousePos1
        self.copyPos = mousePos2

    def copyPage(self, num):
        #faire un right clique pour copier le numero du dossier
        self.mouse.position = self.copyPos
        time.sleep(2)
        mouseClick(self.mouse)
        time.sleep(2)
        mouseClick(self.mouse, TRUE)
        print("je colle ", pyperclip.paste())
        time.sleep(2)
        self.mouse.position = self.cegiPos
        time.sleep(2)
        mouseClick(self.mouse)
        print("je clique")
        time.sleep(2)
        self.mouse.position = self.copyPos
        time.sleep(2)
        mouseClick(self.mouse)
        print("Je clique")
        time.sleep(2)        

    def printPos(self):
        print(self.cegiPos, self.copyPos)
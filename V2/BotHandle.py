from pynput import keyboard
from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import Key, Listener, Controller as keyboardController
import time

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
        keyboard.press('a')
        keyboard.release('a') 

class GetMousePos:
    mousePos = (0,0)
    mouse = mouseController()

    def on_release(self, key):
        self.mousePos
        try:
            if key.char == 'c' or key.char == 'C':
                self.mousePos = self.mouse.position
                return False
        except:
            pass

    def get_Mouse_Pos(self):
        with Listener(on_release=self.on_release) as listener:
            listener.join()
        return self.mousePos

class Bot:
    mouse = mouseController()
    keyboard = keyboardController()

    def __init__(self, mousePos1, mousePos2):
        self.cegiPos = mousePos1
        self.copyPos = mousePos2

    def copyPage(self, num):
        #faire un right clique pour copier le numero du dossier
        self.mouse.position = self.cegiPos
        usleep(20)
        mouseClick(self.mouse)
        usleep(20)
        self.mouse.position = self.copyPos
        usleep(20)
        mouseClick(self.mouse)
        usleep(20)
        keyboardPress(self.keyboard, 'a')
        usleep(20)

    def printPos(self):
        print(self.cegiPos, self.copyPos)
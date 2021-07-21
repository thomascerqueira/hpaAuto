from tkinter.constants import TRUE
from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import Key, Listener, Controller as keyboardController
import time
import pyperclip
import os


def usleep(x): return time.sleep(x/1000000.0)


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
    cegiPos = (0, 0)
    copyPos = (0, 0)
    mouse = mouseController()
    keyboard = keyboardController()
    status = 0

    def on_release(self, key):
        try:
            if key.char == 'c' or key.char == 'C':
                if self.status == 0:
                    self.cegiPos = self.mouse.position
                    self.status = 1
                    print(
                        "Positionner la souris sur 'Copy All to Clipboard' et appuyer sur c")
                else:
                    self.copyPos = self.mouse.position
                    return False
        except:
            pass

    def get_Mouse_Pos(self):
        with Listener(on_release=self.on_release) as listener:
            listener.join()
        self.mouse.position = (
            self.mouse.position[0] + 350, self.mouse.position[1])
        time.sleep(2)
        mouseClick(self.mouse)
        time.sleep(1)
        return self.cegiPos, self.copyPos


class Bot:
    mouse = mouseController()
    keyboard = keyboardController()

    def __init__(self, mousePos1, mousePos2):
        self.cegiPos = mousePos1
        self.copyPos = mousePos2

    def emergencyStop(self, key):
        if (key == keyboard.Key.f8):
            print("ERMERGENCY STOP")
            os._exit(84)

    def __loop__(self, patients, fileHandler):
        actual = 0
        keyBoard = keyboardController()
        timeStart = time.time()
        timeActual = time.time()
        timeMax = time.time() + len(patients) * 2

        keyListener = keyboard.Listener(on_release=self.emergencyStop)
        keyListener.start()
        for patient in patients:
            timeActual = time.time() - timeStart
            pyperclip.copy(str(patient["Code"]))
            # print("clipboard = ", pyperclip.paste())
            actual += 1
            print("Pourcentage terminé:\t%.2f%%\tTemps total: %02d:%02d\tTemps restant: %02d:%02d" %
                  (actual/len(patients) * 100, int(timeActual / 60), int(timeActual % 60),
                  int((timeMax - time.time()) / 60), int((timeMax - time.time()) % 60)))
            self.copyPage(patient["Code"])
            patient["Type"] = fileHandler.__getType__()
            keyboardPress(keyBoard, Key.esc)
            usleep(100)

    def copyPage(self, num):
        # faire un right clique pour copier le numero du dossier
        self.mouse.position = self.copyPos
        mouseClick(self.mouse)
        usleep(100)
        mouseClick(self.mouse, TRUE)
        # print("je colle ", pyperclip.paste())
        usleep(100)
        self.mouse.position = self.cegiPos
        usleep(100)
        mouseClick(self.mouse)
        # print("je clique")
        usleep(100)
        self.mouse.position = self.copyPos
        time.sleep(1)
        mouseClick(self.mouse)
        # print("Je clique")
        time.sleep(1)

    def printPos(self):
        print(self.cegiPos, self.copyPos)

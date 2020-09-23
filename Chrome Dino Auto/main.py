import pyautogui
from PIL import Image, ImageGrab
#from numpy import asarray
import time

def hit(key):
    pyautogui.keyDown(key)

#def draw():
def isCollide(data):
    for x in range(340, 455):
        for y in range(650, 690):
            if data[x, y] <100:
                return True
    return False

if __name__ == "__main__":
    time.sleep(3)
    hit ('up')
    
    while (True):
        image = ImageGrab.grab().convert('L')
        data = image.load()
        if isCollide(data):
            hit("up")
        #print(asarray(image))
        # for x in range(280, 370):
        #     for y in range(610, 700):
        #         data[x, y] = 0
    
        #image.show()

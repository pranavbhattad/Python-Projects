import pyautogui
from PIL import Image, ImageGrab
import time

#def draw():
    
def hit(key):
    pyautogui.keyDown(key)
    
def takeScreenshot():
    image = ImageGrab.grab().convert('L')
    return image 

if __name__ == "__main__":
    time.sleep(2)
    image = takeScreenshot()
    data =image.load()
    for x in range (340, 455):
        for y in range (650, 690):
            data[x, y] = 0

    image.show()
# for y in range (650, 700):
# for y in range (650, 690):
#  for x in range(340, 455):
# for x in range (298, 435):
# for x in range (250, 385):
# for x in range (200, 300):

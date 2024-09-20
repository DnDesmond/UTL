import pyautogui
import time
tim = 0
import pygame
import random
pygame.init()
clock = pygame.time.Clock()
pyautogui.press("win")
pyautogui.click(693,876)
pyautogui.PAUSE = 0
time.sleep(1)
while True:
    if tim % 60 == 0:
        pyautogui.click(33,99)
        time.sleep(random.randint(1,10)/10)
    tim += 1
    clock.tick(60)



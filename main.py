import math
import os
import sys
import threading
import pygame
from pygame.locals import QUIT  # Pygame 초기화

pygame.init()

# --- 화면 설정 ---

Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
ScreenWidth = Screen.get_width()
ScreenHeight = Screen.get_height()

pygame.display.set_caption("Whale")  # 게임 제목 설정

Clock = pygame.time.Clock()  # fps 설정을 위한 Clock 변수 설정

SceneValue = 0  # 장면 값

# --- image load & setup ---
BasicImagePath = os.path.abspath(
  '.') + '/' + "sources/images/"  # image 기본 경로 설정
TestImage = pygame.image.load(BasicImagePath + "m.png")

TestImageRect = TestImage.get_rect()
TestImageSize = TestImageRect.size
TestImageWidth = TestImageSize[0]
TestImageHeight = TestImageSize[1]

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  Screen.blit(TestImage, (ScreenWidth / 2 - TestImageWidth / 2,
                          ScreenHeight / 2 - TestImageHeight / 2))

  pygame.display.update()

pygame.quit()

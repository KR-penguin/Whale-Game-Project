import math
import os
import threading
import pygame
from pygame.locals import QUIT  # Pygame 초기화

pygame.init()

# --- 화면 설정 ---

Screen = pygame.display.set_mode((1920, 1080))  # 화면 크기
ScreenWidth = 1920
ScreenHeight = 1080

pygame.display.set_caption("Whale")  # 게임 제목 설정

Clock = pygame.time.Clock()  # fps 설정을 위한 Clock 변수 설정

SceneValue = 0  # 장면 값

# --- 이미지 불러오기 ---
BasicImagePath = os.path.abspath(
  '.') + '/' + "sources/images/"  # image 기본 경로 설정
PlayerImage = pygame.image.load(BasicImagePath + "test.png")

# --- classes ---


class Object:
  Size = 0
  Width = 0
  Height = 0
  Xpos = 0
  Ypos = 0


class HUD:
  Xpos = 0
  Ypos = 0


class DynamicObject(Object):
  ToXpos = 0
  ToYpos = 0


class StaticObject(Object):
  pass


class Character(DynamicObject):

  def __init__(self, Image, Xpos, Ypos, Speed):
    # 상속된 변수들
    self.Size = Image.get_rect().size
    self.Width = self.Size[0]
    self.Height = self.Size[1]
    self.Xpos = Xpos
    self.Ypos = Ypos
    # 이 class에서 새로 선언된 변수들
    self.ToXpos = 0
    self.ToYpos = 0
    self.speed = Speed


class Background(DynamicObject):

  def __init__(self, Image, Xpos, Ypos, Speed):
    # 상속된 변수들
    self.Size = Image.get_rect().size
    self.Width = self.Size[0]
    self.Height = self.Size[1]
    self.Xpos = Xpos
    self.Ypos = Ypos
    # 이 class에서 새로 선언된 변수들
    self.ToXpos = 0
    self.ToYpos = 0
    self.speed = Speed


class VirtualJoystick(HUD):

  def __init__(self, Image, Xpos, Ypos):
    # 상속된 변수들
    self.Size = Image.get_rect().size
    self.Width = self.Size[0]
    self.Height = self.Size[1]
    self.Xpos = Xpos
    self.Ypos = Ypos


# --- create instance ---

Player = Character(PlayerImage, 0, 0, 0.3)

# --- begin setup ---

Running = True

# --- main loop ---

while Running:
  for event in pygame.event.get():
    if event.type == QUIT:
      Running = False

    # --- Key binding ---

    # Key가 눌러졌는가?
    if event.type == pygame.KEYDOWN:

      # 좌우 Movement 키바인딩
      if event.key == pygame.K_d:
        Player.ToXpos += Player.speed
      elif event.key == pygame.K_a:
        Player.ToXpos -= Player.speed
      # 상하 Movement 키바인딩
      elif event.key == pygame.K_w:
        Player.ToYpos += Player.speed
      elif event.key == pygame.K_s:
        Player.ToYpos -= Player.speed

  # --- draw objects on screen ---

  Screen.fill((255, 255, 255))
  Screen.blit(PlayerImage, (0, 0))

  pygame.display.update()

pygame.quit()

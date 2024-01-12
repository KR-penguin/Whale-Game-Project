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
BasicImagePath = os.path.abspath('.') + '/' + "sources/images/"  # image 기본 경로 설정
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

  def __init__(self, Image, Xpos, Ypos, Speed, FrictionalForce):
    # 상속된 변수들
    self.Size = Image.get_rect().size
    self.Width = self.Size[0]
    self.Height = self.Size[1]
    self.Xpos = Xpos
    self.Ypos = Ypos
    # 이 class에서 새로 선언된 변수들
    self.ToXpos = 0
    self.ToYpos = 0
    self.Speed = Speed
    self.FrictionalForce = FrictionalForce


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

Player = Character(PlayerImage, 0, 0, 3, 0.8)

# --- begin setup ---

Running = True
Player.Xpos = ScreenWidth / 2 - Player.Width / 2
Player.Ypos = ScreenHeight / 2 - Player.Height / 2

# --- main loop ---
pygame.key.set_repeat(60)

while Running:

    DeltaTime = Clock.tick(60)
    Player.Xpos += Player.ToXpos
    Player.Ypos += (-1 * Player.ToYpos)
    Player.ToXpos *= Player.FrictionalForce
    Player.ToYpos *= Player.FrictionalForce

    for event in pygame.event.get():
      if event.type == QUIT:
        Running = False

      # --- Key binding ---

      keys = pygame.key.get_pressed()  # 눌려진 키의 상태를 모두 가져옵니다.
      if keys[pygame.K_d]:  # 'd' 키가 눌려진 경우
        Player.ToXpos += Player.Speed
      if keys[pygame.K_a]:  # 'a' 키가 눌려진 경우
        Player.ToXpos -= Player.Speed

    # --- draw objects on screen ---
    Screen.fill((255, 255, 255))
    Screen.blit(PlayerImage, (Player.Xpos, Player.Ypos))

    pygame.display.update()

pygame.quit()
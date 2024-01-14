import math
import os
import threading
import pygame
from pygame.locals import QUIT  # Pygame 초기화

pygame.init()

# --- 화면 설정 ---

ScreenWidth = 1920
ScreenHeight = 1080
Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))

pygame.display.set_caption("Whale")  # 게임 제목 설정

Clock = pygame.time.Clock()  # fps 설정을 위한 Clock 변수 설정

SceneValue = 0  # 장면 값

# --- 이미지 불러오기 ---
BasicImagePath = os.path.abspath('.') + '/' + "sources/images/"  # image 기본 경로 설정

PlayerImage = pygame.image.load(BasicImagePath + "test_player.png")
PlayerImage = pygame.transform.scale(PlayerImage, (100, 100))

BackgroundImage = pygame.image.load(BasicImagePath + "test_background.jpg")
BackgroundImage = pygame.transform.scale(BackgroundImage, (3060, 1835))

LeftMoveButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png")
LeftMoveButtonImage = pygame.transform.scale(LeftMoveButtonImage, (400, 400))
LeftMoveButtonImage = pygame.transform.rotate(LeftMoveButtonImage, 180.0)

RightMoveButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png")
RightMoveButtonImage = pygame.transform.scale(RightMoveButtonImage, (400, 400))

# --- classes ---


class Object:
  def __init__(self, Image, Xpos, Ypos):
    self.Rect = Image.get_rect()
    self.Size = self.Rect.size
    self.Width = self.Size[0]
    self.Height = self.Size[1]
    self.Xpos = Xpos
    self.Ypos = Ypos


class HUD:
  def __init__(self, Xpos, Ypos):
    self.Xpos = Xpos
    self.Ypos = Ypos


class MouseInfo:
  def __init__(self):
    self.Xpos = 0
    self.Ypos = 0


class DynamicObject(Object):
  def __init__(self, Image, Xpos, Ypos):
    super().__init__(Image, Xpos, Ypos)
    self.ToXpos = 0
    self.ToYpos = 0

  def update_rect_info(self):
    self.Rect.top = self.Ypos
    self.Rect.bottom = self.Ypos - self.Height
    self.Rect.right = self.Xpos - self.Width
    self.Rect.left = self.Xpos


class StaticObject(Object):
  def __init__(self, Image, Xpos, Ypos):
    super().__init__(Image, Xpos, Ypos)


class Character(DynamicObject):

  def __init__(self, Image, Xpos, Ypos, Speed, FrictionalForce):
    super().__init__(Image, Xpos, Ypos)
    self.Speed = Speed
    self.FrictionalForce = FrictionalForce
    self.bMove = False

  def update_rect_info(self):
    super().update_rect_info()

  def update_movement(self):
    global DeltaTime
    self.Xpos += self.ToXpos * DeltaTime
    self.Ypos += (-1 * self.ToYpos) * DeltaTime
    self.ToXpos *= self.FrictionalForce
    self.ToYpos *= self.FrictionalForce


class Background(DynamicObject):

  def __init__(self, Image, Xpos, Ypos):
    super().__init__(Image, Xpos, Ypos)
    self.bMove = False
  
  def update_rect_info(self):
    super().update_rect_info()

  def update_movement(self, FrictionalForce):
    global DeltaTime
    self.Xpos += self.ToXpos * DeltaTime
    self.Ypos += (-1 * self.ToYpos) * DeltaTime
    self.ToXpos *= FrictionalForce
    self.ToYpos *= FrictionalForce

class Button(HUD):

  def __init__(self, Image, Xpos, Ypos):
    # 상속된 변수들
    super().__init__(Xpos, Ypos)
    self.Rect = Image.get_rect()
    self.Size = self.Rect.size
    self.Width = self.Size[0]
    self.Height = self.Size[1]

  def update_rect_info(self):
    self.Rect.x = self.Xpos
    self.Rect.y = self.Ypos

# --- functions ---

def RightMove():
    
    global GameBackground
    global Player
    global ScreenWidth

    if (GameBackground.Rect.right <= ScreenWidth + 15): # 배경이 오른쪽 끝에 다다름. (15 더해주는 이유는 pygame의 성능때문)
        GameBackground.bMove = False
        Player.bMove = True
        Player.ToXpos = Player.Speed
    else:
        if (Player.Xpos + Player.Width / 2 >= ScreenWidth / 2): # Player가 화면 중앙보다 오른쪽에 있는가?
            GameBackground.bMove = True
            Player.bMove = False
            GameBackground.ToXpos = -1 * Player.Speed # 배경은 Player의 반대로 이동해야 함.
        else:
            GameBackground.bMove = False
            Player.bMove = True
            Player.ToXpos = Player.Speed

def LeftMove():

    global GameBackground
    global Player
    global ScreenWidth

    if (GameBackground.Rect.left >= -15): # 배경이 왼쪽 끝에 다다름. (15 빼주는 이유는 pygame의 성능때문)
        GameBackground.bMove = False
        Player.bMove = True
        Player.ToXpos = -1 * Player.Speed
    else:
        if (Player.Xpos + Player.Width / 2 <= ScreenWidth / 2): # Player가 화면 중앙보다 왼쪽에 있는가?   
          GameBackground.bMove = True
          Player.bMove = False
          GameBackground.ToXpos = Player.Speed
        else:
          GameBackground.bMove = False
          Player.bMove = True
          Player.ToXpos = -1 * Player.Speed # 배경은 Player의 반대로 이동해야 함.

# --- create instance ---

Player = Character(PlayerImage, 0, 0, 1, 0.8)
GameBackground = Background(BackgroundImage, 0, 0)
LeftMoveButton = Button(LeftMoveButtonImage, 0, 0)
RightMoveButton = Button(RightMoveButtonImage, 0, 0)

# --- begin setup ---

Running = True
Player.Xpos = ScreenWidth / 2 - Player.Width / 2
Player.Ypos = ScreenHeight / 2 - Player.Height / 2
GameBackground.Xpos = ScreenWidth / 2 - GameBackground.Width / 2
GameBackground.Ypos = ScreenHeight - GameBackground.Height
LeftMoveButton.Xpos = 100
LeftMoveButton.Ypos = ScreenHeight - LeftMoveButton.Height - 100
RightMoveButton.Xpos = ScreenWidth - RightMoveButton.Width - 100
RightMoveButton.Ypos = ScreenHeight - RightMoveButton.Height - 100
LeftMoveButton.update_rect_info()
RightMoveButton.update_rect_info()
MouseCursor = MouseInfo()

# --- main loop ---
pygame.key.set_repeat(10)

while Running:

    
    DeltaTime = Clock.tick(60)

    if Player.bMove:
      Player.update_movement()
    elif GameBackground.bMove:
      GameBackground.update_movement(Player.FrictionalForce)

    Player.update_rect_info()
    GameBackground.update_rect_info()

    for event in pygame.event.get():
      if event.type == QUIT:
        Running = False


      # --- Key binding ---

      keys = pygame.key.get_pressed()  # 눌려진 키의 상태를 모두 가져옴
      if keys[pygame.K_d]: # 'd' 키가 눌려진 경우
        RightMove()

      elif keys[pygame.K_a]:  # 'a' 키가 눌려진 경우
        LeftMove()

      # --- Mouse binding ---

    mouse_button = pygame.mouse.get_pressed() # 눌러진 마우스 버튼의 상태를 모두 가져옴
    if mouse_button[0] or mouse_button[1]: # 좌클릭 또는 우클릭을 했을 때 (모바일은 상관 없음)
      MouseCursor.Xpos = pygame.mouse.get_pos()[0]
      MouseCursor.Ypos = pygame.mouse.get_pos()[1]

      if RightMoveButton.Rect.collidepoint(MouseCursor.Xpos, MouseCursor.Ypos):
        RightMove()

      elif LeftMoveButton.Rect.collidepoint(MouseCursor.Xpos, MouseCursor.Ypos):
        LeftMove()


    # --- draw objects on screen ---
    Screen.fill((255, 255, 255))
    Screen.blit(BackgroundImage, (GameBackground.Xpos, GameBackground.Ypos))
    Screen.blit(PlayerImage, (Player.Xpos, Player.Ypos))
    Screen.blit(LeftMoveButtonImage, (LeftMoveButton.Xpos, LeftMoveButton.Ypos))
    Screen.blit(RightMoveButtonImage, (RightMoveButton.Xpos, RightMoveButton.Ypos))

    pygame.display.update()

pygame.quit()
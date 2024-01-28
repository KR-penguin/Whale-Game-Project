import math
import os
import threading
import pygame

pygame.init()

# --- 화면 설정 ---

Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
ScreenWidth = Screen.get_width()
ScreenHeight = Screen.get_height()

pygame.display.set_caption("Whale")  # 게임 제목 설정

Clock = pygame.time.Clock()  # fps 설정을 위한 Clock 변수 설정

SceneValue = 0  # 장면 값

# --- 이미지 불러오기 ---
BasicImagePath = os.path.abspath('.') + '/' + "sources/images/"  # image 기본 경로 설정

PlayerImage = []
PlayerImage.append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_0.png")) # 0이 기본 Image
PlayerImage.append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_1.png"))
PlayerImage.append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_2.png"))
PlayerImage.append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_3.png"))
PlayerImage.append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_4.png"))
PlayerImage.append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_5.png"))
PlayerImage.append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_6.png"))
PlayerImage.append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_7.png"))
for i in range (8): # 모든 Image에 동일하게 크기 설정
  PlayerImage[i] = pygame.transform.scale(PlayerImage[i], (ScreenHeight / 10, ScreenHeight / 10))

BackgroundImage = pygame.image.load(BasicImagePath + "test_background.jpg")
BackgroundImage = pygame.transform.scale(BackgroundImage, (ScreenWidth * 3, ScreenHeight * 3))

LeftMoveButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png")
LeftMoveButtonImage = pygame.transform.scale(LeftMoveButtonImage, (ScreenHeight / 3, ScreenHeight / 3))
LeftMoveButtonImage = pygame.transform.rotate(LeftMoveButtonImage, 180.0)

RightMoveButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png")
RightMoveButtonImage = pygame.transform.scale(RightMoveButtonImage, (ScreenHeight / 3, ScreenHeight / 3))

JumpBlockImage = pygame.image.load(BasicImagePath + "jump block.png")
JumpBlockImage = pygame.transform.scale(JumpBlockImage, (ScreenHeight / 3, ScreenHeight / 3))

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



class GameModeBase:
  def __init__(self):
    self.AnimationIndex = 0
    self.Temp = 0
  
  def update_property(self):
    self.Temp += 0.1 # Temp가 Animation이 얼마나 빨리 update 될 지 결정함
    self.AnimationIndex = math.floor(self.Temp)
    if (self.AnimationIndex >= 8):
      self.AnimationIndex = 0
      self.Temp = 0

       
  



class DynamicObject(Object):
  def __init__(self, Image, Xpos, Ypos):
    super().__init__(Image, Xpos, Ypos)
    self.Xpos = Xpos
    self.Ypos = Ypos
    self.ToXpos = 0
    self.ToYpos = 0

  def update_rect_info(self, Image):
    self.Image = Image
    self.Rect = self.Image.get_rect()
    self.Size = self.Rect.size
    self.Width = self.Size[0]
    self.Height = self.Size[1]
    self.Rect.top = self.Ypos
    self.Rect.bottom = self.Ypos - self.Height
    self.Rect.right = self.Xpos - self.Width
    self.Rect.left = self.Xpos

  def update_movement(self, FrictionalForce, DeltaTime):
    self.Xpos += self.ToXpos * DeltaTime
    self.Ypos += (-1 * self.ToYpos) * DeltaTime
    self.ToXpos *= FrictionalForce
    self.ToYpos *= FrictionalForce



class StaticObject(Object):
  def __init__(self, Image, Xpos, Ypos):
    super().__init__(Image, Xpos, Ypos)



class Character(DynamicObject):

  def __init__(self, Image, Xpos, Ypos, Speed, FrictionalForce):
    super().__init__(Image, Xpos, Ypos)
    self.Speed = Speed
    self.FrictionalForce = FrictionalForce
    self.bMove = False

  def update_movement(self, DeltaTime):
    self.Xpos += self.ToXpos * DeltaTime
    self.Ypos += (-1 * self.ToYpos) * DeltaTime
    self.ToXpos *= self.FrictionalForce
    self.ToYpos *= self.FrictionalForce



class Background(DynamicObject):

  def __init__(self, Image, Xpos, Ypos):
    super().__init__(Image, Xpos, Ypos)
    self.bMove = False



class Button(HUD, Object):

  def __init__(self, Image, Xpos, Ypos):
    # 상속된 변수들
    HUD.__init__(self, Xpos, Ypos)
    Object.__init__(self, Image, Xpos, Ypos)

  def update_rect_info(self):
    self.Rect.x = self.Xpos
    self.Rect.y = self.Ypos



# --- functions ---
def move(direction):
    global GameBackground
    global Player
    global ScreenWidth

    if direction == "Right":
        edge = GameBackground.Rect.right <= ScreenWidth + 30
        beyond_screen = Player.Rect.right >= ScreenWidth
        beyond_middle = Player.Xpos + Player.Width / 2 >= ScreenWidth / 2
        opposite_direction = "Left"
    else:  # "Left"
        edge = GameBackground.Rect.left >= -30
        beyond_screen = Player.Xpos <= 0
        beyond_middle = Player.Xpos + Player.Width / 2 <= ScreenWidth / 2
        opposite_direction = "Right"

    if edge:
        if beyond_screen:
            GameBackground.bMove = False
            Player.bMove = False
        else:
            GameBackground.bMove = False
            Player.bMove = True
            Player.ToXpos = Player.Speed if direction == "Right" else -1 * Player.Speed
    else:
        if beyond_middle:
            GameBackground.bMove = True
            Player.bMove = False
            background_move(opposite_direction)
        else:
            GameBackground.bMove = False
            Player.bMove = True
            Player.ToXpos = Player.Speed if direction == "Right" else -1 * Player.Speed



def background_move(Direction : str):
# 이 함수에서 배경이 움직이는 것을 관리함

   global Player
   global GameBackground
   global JumpBlock

   if (Direction == "Right"):
      GameBackground.ToXpos = Player.Speed
      JumpBlock.ToXpos = Player.Speed
   else:
      GameBackground.ToXpos = -1 * Player.Speed
      JumpBlock.ToXpos = -1 * Player.Speed



def mouse_input():
    mouse_button = pygame.mouse.get_pressed() # 눌러진 마우스 버튼의 상태를 모두 가져옴
    if mouse_button[0] or mouse_button[1]: # 좌클릭 또는 우클릭을 했을 때 (모바일은 상관 없음)
      MouseCursor.Xpos = pygame.mouse.get_pos()[0]
      MouseCursor.Ypos = pygame.mouse.get_pos()[1]

      if RightMoveButton.Rect.collidepoint(MouseCursor.Xpos, MouseCursor.Ypos):
        move("Right")

      elif LeftMoveButton.Rect.collidepoint(MouseCursor.Xpos, MouseCursor.Ypos):
        move("Left")
        


def draw_scence(scene : int, animation_frame : int):

    if (scene == 0):
      Screen.fill((255, 255, 255))

      # Dynamic Objects
      Screen.blit(BackgroundImage, (GameBackground.Xpos, GameBackground.Ypos))
      Screen.blit(JumpBlockImage, (JumpBlock.Xpos, JumpBlock.Ypos))
      Screen.blit(PlayerImage[animation_frame], (Player.Xpos, Player.Ypos))

      # Static Objects
      Screen.blit(LeftMoveButtonImage, (LeftMoveButton.Xpos, LeftMoveButton.Ypos))
      Screen.blit(RightMoveButtonImage, (RightMoveButton.Xpos, RightMoveButton.Ypos))
    pygame.display.update()

# --- create instance ---

WhaleGameModeBase = GameModeBase()
Player = Character(PlayerImage[0], 0, 0, 1, 0.8) # Dynamic Object
GameBackground = Background(BackgroundImage, 0, 0) # Dynamic Object
LeftMoveButton = Button(LeftMoveButtonImage, 0, 0) # Static Object
RightMoveButton = Button(RightMoveButtonImage, 0, 0) # Static Object
JumpBlock = DynamicObject(JumpBlockImage, 0, 0) # Dynamic Object
MouseCursor = MouseInfo()

# --- begin setup ---

Running = True
Player.Xpos = ScreenWidth / 2 - Player.Width / 2
Player.Ypos = ScreenHeight / 2 - Player.Height / 2
GameBackground.Xpos = ScreenWidth / 2 - GameBackground.Width / 2
GameBackground.Ypos = ScreenHeight - GameBackground.Height + ScreenHeight / 8
LeftMoveButton.Xpos = 0
LeftMoveButton.Ypos = ScreenHeight - LeftMoveButton.Height
RightMoveButton.Xpos = ScreenWidth - RightMoveButton.Width
RightMoveButton.Ypos = ScreenHeight - RightMoveButton.Height
JumpBlock.Xpos = ScreenWidth / 2 - JumpBlock.Width / 2
JumpBlock.Ypos = ScreenHeight / 2 - JumpBlock.Height / 2

# Dynamic Object들은 update_rect_info 할 때 Image가 필요함.
Player.update_rect_info(PlayerImage[0])
GameBackground.update_rect_info(BackgroundImage)
JumpBlock.update_rect_info(JumpBlockImage)
# Static Object들은 upate_rect_info 할 때 Image가 필요없음.
LeftMoveButton.update_rect_info()
RightMoveButton.update_rect_info()

# --- main loop ---
pygame.key.set_repeat(10)

while Running:

    DeltaTime = Clock.tick(60)
    WhaleGameModeBase.update_property()

    # update 하는 부분 {
    if Player.bMove:
      Player.update_movement(DeltaTime)
    elif GameBackground.bMove:
      GameBackground.update_movement(Player.FrictionalForce, DeltaTime)
      JumpBlock.update_movement(Player.FrictionalForce, DeltaTime)

    Player.update_rect_info(PlayerImage[WhaleGameModeBase.AnimationIndex])
    GameBackground.update_rect_info(BackgroundImage)
    JumpBlock.update_rect_info(JumpBlockImage)
    # }

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        Running = False

    # --- Mouse binding ---
    mouse_input()


    # --- draw objects on screen ---
    draw_scence(SceneValue, WhaleGameModeBase.AnimationIndex)

pygame.quit()
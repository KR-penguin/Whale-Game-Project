import math
import os
import threading
import pygame
import game_class

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

PlayerImage = [[], [], []]
PlayerImage[0].append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_0.png")) # 0이 기본 Image
PlayerImage[0].append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_1.png"))
PlayerImage[0].append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_2.png"))
PlayerImage[0].append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_3.png"))
PlayerImage[0].append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_4.png"))
PlayerImage[0].append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_5.png"))
PlayerImage[0].append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_6.png"))
PlayerImage[0].append(pygame.image.load(BasicImagePath + "test_player/" + "test_player_7.png"))
for i in range (8): # 모든 Image에 동일하게 크기 설정
  PlayerImage[0][i] = pygame.transform.scale(PlayerImage[0][i], (ScreenHeight / 10, ScreenHeight / 10))

BackgroundImage = pygame.image.load(BasicImagePath + "test_background.jpg")
BackgroundImage = pygame.transform.scale(BackgroundImage, (ScreenWidth * 3, ScreenHeight * 3))

LeftMoveButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png")
LeftMoveButtonImage = pygame.transform.scale(LeftMoveButtonImage, (ScreenHeight / 3, ScreenHeight / 3))
LeftMoveButtonImage = pygame.transform.rotate(LeftMoveButtonImage, 180.0)

RightMoveButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png")
RightMoveButtonImage = pygame.transform.scale(RightMoveButtonImage, (ScreenHeight / 3, ScreenHeight / 3))

JumpBlockImage = pygame.image.load(BasicImagePath + "jump block.png")
JumpBlockImage = pygame.transform.scale(JumpBlockImage, (ScreenHeight / 3, ScreenHeight / 3))



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
        


def draw_scence(scene : int):

    global Player
    global GameBackground # 지금은 안씀

    if (scene == 0):
      Screen.fill((255, 255, 255))

      # Dynamic Objects
      Screen.blit(BackgroundImage, (GameBackground.Xpos, GameBackground.Ypos))
      Screen.blit(JumpBlockImage, (JumpBlock.Xpos, JumpBlock.Ypos))
      Screen.blit(PlayerImage[Player.AnimationFrame[0]][Player.AnimationFrame[1]], (Player.Xpos, Player.Ypos))

      # Static Objects
      Screen.blit(LeftMoveButtonImage, (LeftMoveButton.Xpos, LeftMoveButton.Ypos))
      Screen.blit(RightMoveButtonImage, (RightMoveButton.Xpos, RightMoveButton.Ypos))
    pygame.display.update()

# --- create instance ---

WhaleGameModeBase = game_class.GameModeBase(0.8)
Player = game_class.Character(PlayerImage[0][0], 0, 0, 1) # Dynamic Object
GameBackground = game_class.Background(BackgroundImage, 0, 0) # Dynamic Object
LeftMoveButton = game_class.Button(LeftMoveButtonImage, 0, 0) # Static Object
RightMoveButton = game_class.Button(RightMoveButtonImage, 0, 0) # Static Object
JumpBlock = game_class.DynamicObject(JumpBlockImage, 0, 0) # Dynamic Object
MouseCursor = game_class.MouseInfo()

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
Player.update_rect_info(PlayerImage[0][0])
GameBackground.update_rect_info(BackgroundImage)
JumpBlock.update_rect_info(JumpBlockImage)
# Static Object들은 upate_rect_info 할 때 Image가 필요없음.
LeftMoveButton.update_rect_info()
RightMoveButton.update_rect_info()

# --- main loop ---
pygame.key.set_repeat(10)

while Running:

    DeltaTime = Clock.tick(60)

    # update 하는 부분 {
    if Player.bMove:
      Player.update_movement(WhaleGameModeBase.FrictionalForce, DeltaTime)
    elif GameBackground.bMove:
      GameBackground.update_movement(WhaleGameModeBase.FrictionalForce, DeltaTime)
      JumpBlock.update_movement(WhaleGameModeBase.FrictionalForce, DeltaTime)

    Player.update_rect_info(PlayerImage[Player.AnimationFrame[0]][Player.AnimationFrame[1]])
    GameBackground.update_rect_info(BackgroundImage)
    JumpBlock.update_rect_info(JumpBlockImage)

    Player.update_animation()
    GameBackground.update_animation()
    # }

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        Running = False

    # --- Mouse binding ---
    mouse_input()


    # --- draw objects on screen ---
    draw_scence(SceneValue)

pygame.quit()
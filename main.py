import math
import os
import threading
import pygame
import game_class
import typing

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
Player_Idle_0_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_0.png").convert_alpha()
Player_Idle_1_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_1.png").convert_alpha()
Player_Idle_2_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_2.png").convert_alpha()
Player_Idle_3_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_3.png").convert_alpha()
Player_Idle_4_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_4.png").convert_alpha()
Player_Idle_5_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_5.png").convert_alpha()
Player_Idle_6_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_6.png").convert_alpha()
Player_Idle_7_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_7.png").convert_alpha()

PlayerImage[0].append(Player_Idle_0_Image) # 0이 기본 Image
PlayerImage[0].append(Player_Idle_1_Image)
PlayerImage[0].append(Player_Idle_2_Image)
PlayerImage[0].append(Player_Idle_3_Image)
PlayerImage[0].append(Player_Idle_4_Image)
PlayerImage[0].append(Player_Idle_5_Image)
PlayerImage[0].append(Player_Idle_6_Image)
PlayerImage[0].append(Player_Idle_7_Image)

for i in range (8): # 모든 Image에 동일하게 크기 설정
  PlayerImage[0][i] = pygame.transform.scale(PlayerImage[0][i], (ScreenHeight / 10, ScreenHeight / 10))



BackgroundImage = pygame.image.load(BasicImagePath + "test_background.jpg").convert_alpha()
BackgroundImage = pygame.transform.scale(BackgroundImage, (ScreenWidth * 3, ScreenHeight * 3))

LeftMoveButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png").convert_alpha()
LeftMoveButtonImage = pygame.transform.scale(LeftMoveButtonImage, (ScreenHeight / 3, ScreenHeight / 3))
LeftMoveButtonImage = pygame.transform.rotate(LeftMoveButtonImage, 180.0)

RightMoveButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png").convert_alpha()
RightMoveButtonImage = pygame.transform.scale(RightMoveButtonImage, (ScreenHeight / 3, ScreenHeight / 3))

JumpBlockImage = pygame.image.load(BasicImagePath + "jump block.png").convert_alpha()
JumpBlockImage = pygame.transform.scale(JumpBlockImage, (ScreenHeight / 3, ScreenHeight / 3))



# --- functions ---
def move(direction):

    if direction == "Right":
      Player.ToXpos = Player.Speed
    else:  # "Left"
      Player.ToXpos = -1 * Player.Speed



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
GameCamera = game_class.Camera(ScreenWidth, ScreenHeight)
Player = game_class.Character(PlayerImage[0][0], 0, 0, 1) # Dynamic Object
GameBackground = game_class.Background(BackgroundImage, 0, 0) # Static Object
LeftMoveButton = game_class.Button(LeftMoveButtonImage, 0, 0) # Static Object
RightMoveButton = game_class.Button(RightMoveButtonImage, 0, 0) # Static Object
JumpBlock = game_class.StaticObject(JumpBlockImage, 0, 0) # Static Object
MouseCursor = game_class.MouseInfo()

Entities = [Player, GameBackground, JumpBlock] # 이 게임의 Entity 리스트

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
# Static Object들은 upate_rect_info 할 때 Image가 필요없음.
GameBackground.update_rect_info()
JumpBlock.update_rect_info()
LeftMoveButton.update_rect_info()
RightMoveButton.update_rect_info()

# --- main loop ---
pygame.key.set_repeat(10)

while Running:

    DeltaTime = Clock.tick(60)

    # update 하는 부분 {
    Player.update_movement(WhaleGameModeBase.FrictionalForce, DeltaTime)

    Player.update_rect_info(PlayerImage[Player.AnimationFrame[0]][Player.AnimationFrame[1]])
    GameCamera.update_rect_info(Player, GameBackground)

    Player.update_animation()
    GameBackground.update_animation()
    # }

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        Running = False

    # --- Mouse binding ---
    mouse_input()


    # --- draw objects on screen ---

#    for Entity in Entities:
#       rect = GameCamera.modify_rect_for_camera(Entity)

    draw_scence(SceneValue)

pygame.quit()
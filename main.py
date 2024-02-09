import os
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

PlayerImage = [[], [], [], []] # Idle, Run, Jump, Fall
Player_Idle_0_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_idle_0.png").convert_alpha()
Player_Idle_1_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_idle_1.png").convert_alpha()
Player_Idle_2_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_idle_2.png").convert_alpha()
Player_Idle_3_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_idle_3.png").convert_alpha()
Player_Idle_4_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_idle_4.png").convert_alpha()
Player_Idle_5_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_idle_5.png").convert_alpha()
Player_Idle_6_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_idle_6.png").convert_alpha()
Player_Idle_7_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_idle_7.png").convert_alpha()

Player_Jump_0_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_jump_0.png").convert_alpha()
Player_Jump_1_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_jump_1.png").convert_alpha()

Player_Falling_0_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_falling_0.png").convert_alpha()
Player_Falling_1_Image = pygame.image.load(BasicImagePath + "test_player/" + "test_player_falling_1.png").convert_alpha()

PlayerImage[0].append(Player_Idle_0_Image) # 0이 기본 Image
PlayerImage[0].append(Player_Idle_1_Image)
PlayerImage[0].append(Player_Idle_2_Image)
PlayerImage[0].append(Player_Idle_3_Image)
PlayerImage[0].append(Player_Idle_4_Image)
PlayerImage[0].append(Player_Idle_5_Image)
PlayerImage[0].append(Player_Idle_6_Image)
PlayerImage[0].append(Player_Idle_7_Image)

PlayerImage[2].append(Player_Jump_0_Image) # 0이 기본 Image
PlayerImage[2].append(Player_Jump_1_Image)

PlayerImage[3].append(Player_Falling_0_Image) # 0이 기본 Image
PlayerImage[3].append(Player_Falling_1_Image)

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

GroundImage = pygame.image.load(BasicImagePath + "Ground.png").convert_alpha()
GroundImage = pygame.transform.scale(GroundImage, (ScreenWidth * 10, ScreenHeight / 2.5))


# --- functions ---
def move(Direction : str):
  
    if (Direction == "Right"):
      if (Player.Xpos > GameBackground.Xpos + (GameBackground.Rect.width - GameBackground.Rect.width * 0.1)): # player가 오른쪽 끝까지 이동했을 때
        # GameBackground.Rect.width - GameBackground.Rect.width * 0.1   ==> 화면 오른쪽 끝보다 조금 왼쪽
        return
      Player.ToXpos = Player.Speed

    elif (Direction == "Left"):
      if (Player.Xpos < (GameBackground.Xpos + GameBackground.Rect.width * 0.1)): # player가 왼쪽 끝까지 이동했을 때
        return
      Player.ToXpos = -1 * Player.Speed

    elif (Direction == "Up"):
      if (Player.Ypos < (GameBackground.Ypos + GameBackground.Rect.height * 0.1)): # player가 위쪽 끝까지 이동했을 때
        return
      Player.ToYpos = Player.Speed

    elif (Direction == "Down"):
      if (Player.Ypos > GameBackground.Ypos + (GameBackground.Rect.height - GameBackground.Rect.height * 0.1)): # player가 아래쪽 끝까지 이동했을 때
        return
      Player.ToYpos = -1 * Player.Speed

def draw_scence(scene : int):

    if (scene == 0):
      Screen.fill((255, 255, 255))

      # Dynamic Objects
      Screen.blit(BackgroundImage, (GameBackground.Rect.x, GameBackground.Rect.y))
      Screen.blit(GroundImage, (Ground.Rect.x, Ground.Rect.y))
      Screen.blit(JumpBlockImage, (JumpBlock.Rect.x, JumpBlock.Rect.y))
      Screen.blit(PlayerImage[Player.AnimationFrame[0]][Player.AnimationFrame[1]], (Player.Rect.x, Player.Rect.y))

      # Static Objects
      Screen.blit(LeftMoveButtonImage, (LeftMoveButton.Rect.x, LeftMoveButton.Rect.y))
      Screen.blit(RightMoveButtonImage, (RightMoveButton.Rect.x, RightMoveButton.Rect.y))
    pygame.display.update()

# --- create instance ---

WhaleGameModeBase = game_class.GameModeBase(Screen, "TargetXY")
GameCamera = game_class.Camera(WhaleGameModeBase)
Player = game_class.Character(PlayerImage[0][0], 1, WhaleGameModeBase) # Dynamic Object
GameBackground = game_class.Background(BackgroundImage) # Static Object
LeftMoveButton = game_class.Button(LeftMoveButtonImage) # Static Object
RightMoveButton = game_class.Button(RightMoveButtonImage) # Static Object
JumpBlock = game_class.StaticObject(JumpBlockImage) # Static Object
Ground = game_class.StaticObject(GroundImage) # Static Object
MouseCursor = game_class.MouseInfo()

Entities = [Player, JumpBlock, Ground] # 이 게임의 Entity 리스트


# --- begin setup ---

Running = True
Player.Xpos = ScreenWidth / 2 - Player.Rect.width / 2
Player.Ypos = ScreenHeight / 2 - Player.Rect.height
GameBackground.Xpos = ScreenWidth / 2 - GameBackground.Rect.width / 2
GameBackground.Ypos = ScreenHeight - GameBackground.Rect.height + ScreenHeight / 8
LeftMoveButton.Xpos = 0
LeftMoveButton.Ypos = ScreenHeight - LeftMoveButton.Rect.height
RightMoveButton.Xpos = ScreenWidth - RightMoveButton.Rect.width
RightMoveButton.Ypos = ScreenHeight - RightMoveButton.Rect.height
JumpBlock.Xpos = ScreenWidth / 2 - JumpBlock.Rect.width / 2
JumpBlock.Ypos = ScreenHeight / 2 - JumpBlock.Rect.height / 2
Ground.Xpos = ScreenWidth / 2 - Ground.Rect.width / 2
Ground.Ypos = (GameBackground.Ypos + GameBackground.Rect.height) - Ground.Rect.height

GameCamera.Rect.x = 100
GameCamera.Rect.y = 100

# --- main loop ---
pygame.key.set_repeat(10)

while Running:

    DeltaTime = Clock.tick(60)

    # update 하는 부분 {
    Player.update_movement(WhaleGameModeBase, Ground, DeltaTime)

    Player.update_animation()
    GameBackground.update_animation()
    # }

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        Running = False

    # --- Keyboard binding ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        move("Right")
    if keys[pygame.K_a]:
        move("Left")
    if keys[pygame.K_SPACE]:
        Player.jump_start()

    

    # --- draw objects on screen ---
    GameBackground.Rect = GameCamera.update_rect_info(GameBackground)
    GameCamera.update_all_entities(Entities)
    GameCamera.follow_target(Player, GameBackground, WhaleGameModeBase)
    draw_scence(SceneValue)

pygame.quit()
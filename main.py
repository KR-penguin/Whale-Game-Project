import os
import pygame
import game_class
import math

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

PlayerImage = [[], [], [], [], []]  # Idle, Run_Right, Run_Left, Jump, Fall

# Idle Images
for i in range(8):
    image_path = BasicImagePath + "test_player/test_player_idle_" + str(i) + ".png"
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (ScreenHeight // 5, ScreenHeight // 5))
    PlayerImage[0].append(image)

# Run Images
for i in range(8):
    image_path = BasicImagePath + "test_player/test_player_run_" + str(i) + ".png"
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (ScreenHeight // 6, ScreenHeight // 6))
    PlayerImage[1].append(image)

# Jump Images
for i in range(2):
    image_path = BasicImagePath + "test_player/test_player_jump_" + str(i) + ".png"
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (ScreenHeight // 5, ScreenHeight // 5))
    PlayerImage[2].append(image)

# Fall Images
for i in range(2):
    image_path = BasicImagePath + "test_player/test_player_fall_" + str(i) + ".png"
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (ScreenHeight // 5, ScreenHeight // 5))
    PlayerImage[3].append(image)

BackgroundImage = pygame.image.load(BasicImagePath + "test_background.jpg").convert_alpha()
BackgroundImage = pygame.transform.scale(BackgroundImage, (ScreenWidth * 3, ScreenHeight * 3))

LeftMoveButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png").convert_alpha()
LeftMoveButtonImage = pygame.transform.scale(LeftMoveButtonImage, (ScreenHeight / 4, ScreenHeight / 4))
LeftMoveButtonImage = pygame.transform.rotate(LeftMoveButtonImage, 180.0)

RightMoveButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png").convert_alpha()
RightMoveButtonImage = pygame.transform.scale(RightMoveButtonImage, (ScreenHeight / 4, ScreenHeight / 4))

JumpButtonImage = pygame.image.load(BasicImagePath + "MoveButton.png").convert_alpha()
JumpButtonImage = pygame.transform.scale(LeftMoveButtonImage, (ScreenHeight / 4, ScreenHeight / 4))
JumpButtonImage = pygame.transform.rotate(LeftMoveButtonImage, 270.0)

JumpBlockImage = pygame.image.load(BasicImagePath + "jump block.png").convert_alpha()
JumpBlockImage = pygame.transform.scale(JumpBlockImage, (ScreenHeight / 3, ScreenHeight / 3))

GroundImage = pygame.image.load(BasicImagePath + "Ground.png").convert_alpha()
GroundImage = pygame.transform.scale(GroundImage, (ScreenWidth * 10, ScreenHeight / 2.5))


# --- functions ---

def draw_scence(scene: int):
    if (scene == 0):
        Screen.fill((255, 255, 255))

        Screen.blit(GameBackground.Image, (GameBackground.Rect.x, GameBackground.Rect.y))
        Screen.blit(Ground.Image, (Ground.Rect.x, Ground.Rect.y))
        Screen.blit(JumpBlock.Image, (JumpBlock.Rect.x, JumpBlock.Rect.y))
        Screen.blit(Player.Image, (Player.Rect.x, Player.Rect.y))

        Screen.blit(LeftMoveButton.Image, (LeftMoveButton.Rect.x, LeftMoveButton.Rect.y))
        Screen.blit(RightMoveButton.Image, (RightMoveButton.Rect.x, RightMoveButton.Rect.y))
        Screen.blit(JumpButton.Image, (JumpButton.Rect.x, JumpButton.Rect.y))
    pygame.display.update()


# --- create instance ---

WhaleGameModeBase = game_class.GameModeBase(Screen, "TargetXY")
GameCamera = game_class.Camera(WhaleGameModeBase)
Player = game_class.Character(PlayerImage[0][0], 1, WhaleGameModeBase)  # Dynamic Object
GameBackground = game_class.Background(BackgroundImage)  # Static Object
LeftMoveButton = game_class.Button(LeftMoveButtonImage)  # HUD
RightMoveButton = game_class.Button(RightMoveButtonImage)  # HUD
JumpButton = game_class.Button(JumpButtonImage)  # HUD
JumpBlock = game_class.StaticObject(JumpBlockImage)  # Static Object
Ground = game_class.StaticObject(GroundImage)  # Static Object
MouseCursor = game_class.MouseInfo()

Entities = [Player, JumpBlock, Ground, GameBackground] # 이 게임의 Entity 리스트
LevelComponents = [Ground, JumpBlock]

# --- begin setup ---

Running = True
Player.Xpos = ScreenWidth / 2 - Player.Rect.width / 2
Player.Ypos = ScreenHeight / 2 - Player.Rect.height
GameBackground.Xpos = ScreenWidth / 2 - GameBackground.Rect.width / 2
GameBackground.Ypos = ScreenHeight - GameBackground.Rect.height + ScreenHeight / 8
# 버튼 테스트
RightMoveButton.Rect = pygame.Rect(ScreenWidth - RightMoveButton.Rect.width, ScreenHeight - RightMoveButton.Rect.height, RightMoveButton.Rect.width,
                      RightMoveButton.Rect.height)
LeftMoveButton.Rect = pygame.Rect(RightMoveButton.Rect.x - LeftMoveButton.Rect.width, ScreenHeight - LeftMoveButton.Rect.height, LeftMoveButton.Rect.width,
                      LeftMoveButton.Rect.height)
JumpButton.Rect = pygame.Rect(0, ScreenHeight - RightMoveButton.Rect.height, RightMoveButton.Rect.width,
                      RightMoveButton.Rect.height)
# 버튼 테스트 끝
JumpBlock.Xpos = ScreenWidth / 2 - JumpBlock.Rect.width / 2
JumpBlock.Ypos = ScreenHeight / 2 - JumpBlock.Rect.height / 2
Ground.Xpos = ScreenWidth / 2 - Ground.Rect.width / 2
Ground.Ypos = (GameBackground.Ypos + GameBackground.Rect.height) - Ground.Rect.height

# --- main loop ---
pygame.key.set_repeat(10)

while Running:
    DeltaTime = Clock.tick(60)

    # update 하는 부분 {
    Player.update_movement(LevelComponents, WhaleGameModeBase, Ground, DeltaTime)
    Player.update_image(PlayerImage[Player.AnimationFrame[0]][Player.AnimationFrame[1]])
    Player.update_animation()
    GameBackground.update_animation()
    # }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        elif event.type == pygame.FINGERDOWN:
            TouchPos = (event.x * Screen.get_width(), event.y * Screen.get_height())
            if LeftMoveButton.Rect.collidepoint(TouchPos):
                LeftMoveButton.Pressed = True
            elif RightMoveButton.Rect.collidepoint(TouchPos):
                RightMoveButton.Pressed = True
            if JumpButton.Rect.collidepoint(TouchPos):
                JumpButton.Pressed = True

        elif event.type == pygame.FINGERUP:
            TouchPos = (event.x * Screen.get_width(), event.y * Screen.get_height())
            if LeftMoveButton.Rect.collidepoint(TouchPos):
                LeftMoveButton.Pressed = False
            elif RightMoveButton.Rect.collidepoint(TouchPos):
                RightMoveButton.Pressed = False
            if JumpButton.Rect.collidepoint(TouchPos):
                JumpButton.Pressed = False

    if (JumpButton.Pressed):
        Player.jump_start()

    if (LeftMoveButton.Pressed == False and RightMoveButton.Pressed == False):
        if (Player.Status != "Jump" or Player.Status != "Fall"):
            Player.change_status("Idle")

    # --- Keyboard binding ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or RightMoveButton.Pressed:
        Player.move("Right", GameBackground)
    if keys[pygame.K_a] or LeftMoveButton.Pressed:
        Player.move("Left", GameBackground)
    if keys[pygame.K_SPACE]:
        Player.jump_start()

    # --- draw objects on screen ---
    GameCamera.update_all_entities(Entities)
    GameCamera.follow_target(Player, GameBackground, WhaleGameModeBase)
    draw_scence(SceneValue)

pygame.quit()
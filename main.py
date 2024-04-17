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

PlayerImage = [[], []]  # Idle, Run

# Idle Images
for i in range(8):
    image_path = BasicImagePath + "test_player/test_player_idle_" + str(i) + ".png"
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (ScreenHeight / 5, ScreenHeight / 5))
    PlayerImage[0].append(image)

# Run Images
for i in range(8):
    image_path = BasicImagePath + "test_player/test_player_run_" + str(i) + ".png"
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (ScreenHeight / 6, ScreenHeight / 6))
    PlayerImage[1].append(image)

BackgroundImage = pygame.image.load(BasicImagePath + "Background.jpg").convert_alpha()
BackgroundImage = pygame.transform.scale(BackgroundImage, (ScreenWidth, ScreenWidth))
BackgroundImage = pygame.transform.rotate(BackgroundImage, 0)

WallBlockImage = pygame.image.load(BasicImagePath + "WallBlock.jpg").convert_alpha()
WallBlockImage = pygame.transform.scale(WallBlockImage, (ScreenWidth/ 5, ScreenWidth / 5))

# --- functions ---

def draw_scence(scene: int):
    if (scene == 0):
        Screen.fill((255, 255, 255))

        Screen.blit(GameBackground.Image, (GameBackground.Rect.x, GameBackground.Rect.y))
        Screen.blit(Player.Image, (Player.Rect.x, Player.Rect.y))
        Screen.blit(WallBlock.Image, (WallBlock.Rect.x, WallBlock.Rect.y))
    pygame.display.update()


# --- create instance ---

WhaleGameModeBase = game_class.GameModeBase(Screen, "TargetXY")
GameCamera = game_class.Camera(WhaleGameModeBase)
MouseCursor = game_class.MouseInfo()

Player = game_class.Character(PlayerImage[0][0], 1, WhaleGameModeBase)  # Dynamic Object
GameBackground = game_class.Background(BackgroundImage)  # Static Object
WallBlock = game_class.StaticObject(WallBlockImage) # Static Object

Entities = [Player, GameBackground, WallBlock] # 이 게임의 Entity 리스트

# --- begin setup ---

Running = True
Player.Xpos = ScreenWidth / 2 - Player.Rect.width / 2
Player.Ypos = ScreenHeight / 2 - Player.Rect.height
GameBackground.Xpos = ScreenWidth / 2 - GameBackground.Rect.width / 2
GameBackground.Ypos = ScreenHeight - GameBackground.Rect.height + ScreenHeight / 8
WallBlock.Xpos = ScreenWidth / 2 - WallBlock.Rect.width / 2
WallBlock.Ypos = ScreenHeight / 2 - WallBlock.Rect.height / 2

# --- main loop ---
pygame.key.set_repeat(10)

while Running:
    DeltaTime = Clock.tick(60)

    # update 하는 부분 {
    Player.update_movement(DeltaTime)
    Player.update_image(PlayerImage[Player.AnimationFrame[0]][Player.AnimationFrame[1]])
    Player.update_animation()
    GameBackground.update_animation()
    # }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    # --- Keyboard binding ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        Player.move("Right", GameBackground)
    if keys[pygame.K_a]:
        Player.move("Left", GameBackground)
    if keys[pygame.K_w]:
        Player.move("Up", GameBackground)
    if keys[pygame.K_s]:
        Player.move("Down", GameBackground)

    if int(Player.ToXpos) == 0 and int(Player.ToYpos) == 0:
        Player.change_status("Idle")

    # --- draw objects on screen ---
    GameCamera.update_all_entities(Entities)
    GameCamera.follow_target(Player, GameBackground, WhaleGameModeBase)
    draw_scence(SceneValue)

pygame.quit()
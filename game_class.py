import pygame
import math
import typing

# Xpos와 Rect.x는 다르다
# Xpos는 게임 세상의 x좌표를 뜻하지만,
# Rect.x는 카메라에 그려지는 x좌표를 뜻한다.

# --- classes ---
class Object:
    def __init__(self, Image):
        self.Image = Image
        self.Rect = self.Image.get_rect()
        self.Xpos = 0
        self.Ypos = 0
        self.Mask = pygame.mask.from_surface(self.Image)
    
    def update_image(self, NewImage):
        self.Image = NewImage
        self.Rect = self.Image.get_rect()
        self.Mask = pygame.mask.from_surface(self.Image)

    def update_image(self, NewImage):
        self.Image = NewImage
        self.Rect = self.Image.get_rect()
        self.Mask = pygame.mask.from_surface(self.Image)



class HUD:
    def __init__(self, Image):
        self.Image = Image
        self.Rect = self.Image.get_rect()



class MouseInfo:
    def __init__(self):
        self.Xpos = 0
        self.Ypos = 0



class GameModeBase:
    def __init__(self, GameScreen, FollowMethod : str):
        self.GravityAcceleration = GameScreen.get_width() / 7714
        self.GameScreenWidth = GameScreen.get_width()
        self.GameScreenHeight = GameScreen.get_height()
        self.CameraFollowMethod = FollowMethod # "TargetXY", "TargetX", "TargetY"이 있음
        # 1080 / 1102 = 0.98

class BasicAnimation():
    def __init__(self, MaxFrame):
        self.Temp = 0
        self.AnimationFrame = 0
        self.AnimationTotalFrame = MaxFrame
  
    def update_animation(self):
        self.Temp += 0.1
        self.AnimationFrame = math.floor(self.Temp)

        if (self.AnimationFrame >= self.AnimationTotalFrame): # Animation Frame이 끝났다면
          self.AnimationFrame = 0
          self.Temp = 0



class HighQualityAnimation():
    def __init__(self, MaxFrame : typing.List[int]):
        self.Temp = 0
        self.Status = "Idle" # Status에는 Idle, Run_Right, Run_Left, Jump 등이 있다.
        self.AnimationFrame = [0, 0] # 첫번째 index는 status를 나타내고, 두번째 index는 현재 Animation의 frame을 나타냄.
        self.AnimationTotalFrame = MaxFrame # AnimationTotalFrame은 list로써 첫번째 index는 첫번째 status(idle)의 총 frame 개수를 나타낸다.
        self.Direction = "Left"

    def update_animation(self):
        self.Temp += 0.1

        if (self.Status == "Idle"):
            if (math.floor(self.Temp) >= self.AnimationTotalFrame[0]): # Animation Frame이 Animation Max Frame의 첫번째 index(Idle 애니메이션의 Max Frame)과 같거나 더 클때 (Animation이 끝났을 때)
                self.AnimationFrame[1] = 0 # Animation Frame을 0으로 초기화함.
                self.Temp = 0
            else:
                self.AnimationFrame = [0, math.floor(self.Temp)]

        elif (self.Status == "Run"):
            if (math.floor(self.Temp) >= self.AnimationTotalFrame[1] - 1): # Animation Frame이 8과 같거나 더 클때 (Animation이 끝났을 때)
                self.AnimationFrame[1] = 0 # Animation Frame을 0으로 초기화함.
                self.Temp = 0
            else:
                self.AnimationFrame = [1, math.floor(self.Temp)]

    def change_status(self, NewStatus : str):
        if (self.Status == NewStatus):
            return
        self.Status = NewStatus
        self.AnimationFrame[1] = 0
        self.Temp = 0



class DynamicObject(Object):
    def __init__(self, Image):
        super().__init__(Image)
        self.ToXpos = 0
        self.ToYpos = 0
        self.bApplyGravity = True
        self.FrictionalForce = 0.8

    def update_movement(self, DeltaTime):
        self.Xpos += self.ToXpos * DeltaTime
        self.ToXpos *= self.FrictionalForce
        self.Ypos += -1 * self.ToYpos * DeltaTime
        self.ToYpos *= self.FrictionalForce

    def update_image(self, Image):
        self.Image = Image



class StaticObject(Object):
    def __init__(self, Image):
        super().__init__(Image)



class Background(StaticObject, BasicAnimation):

    def __init__(self, Image):
        StaticObject.__init__(self, Image)
        BasicAnimation.__init__(self, 8)



class Character(DynamicObject, HighQualityAnimation):

    def __init__(self, Image, Speed, GameModeBase : GameModeBase):
        DynamicObject.__init__(self, Image)
        HighQualityAnimation.__init__(self, [8, 8]) # HighQualityAnimation 참고
        self.Speed = Speed

    def move(self, Direction : str, GameBackground :  Background):

        if (Direction == "Right"):
            self.change_status("Run")
            self.Direction = "Right"
            if (self.Xpos > GameBackground.Xpos + (GameBackground.Rect.width - GameBackground.Rect.width * 0.1)): # player가 오른쪽 끝까지 이동했을 때
              # GameBackground.Rect.width - GameBackground.Rect.width * 0.1   ==> 화면 오른쪽 끝보다 조금 왼쪽
              return
            self.ToXpos = self.Speed

        elif (Direction == "Left"):
            self.change_status("Run")
            self.Direction = "Left"
            if (self.Xpos < (GameBackground.Xpos + GameBackground.Rect.width * 0.1)): # player가 왼쪽 끝까지 이동했을 때
              return
            self.ToXpos = -1 * self.Speed

        elif (Direction == "Up"):
            self.change_status("Run")
            self.Direction = "Up"
            if (self.Ypos < (GameBackground.Ypos + GameBackground.Rect.height * 0.1)): # player가 왼쪽 끝까지 이동했을 때
              return
            self.ToYpos = self.Speed

        elif (Direction == "Down"):
            self.change_status("Run")
            self.Direction = "Down"
            if (self.Ypos > (GameBackground.Rect.bottom - GameBackground.Rect.height * 0.1)): # player가 왼쪽 끝까지 이동했을 때
              return
            self.ToYpos = -1 * self.Speed

    def update_animation(self):
      super().update_animation()
       # Animation Filp
      if (self.Direction == "Right"):
          self.Image = pygame.transform.flip(self.Image, True, False)

class Button(HUD):

    def __init__(self, Image):
        # 상속된 변수들
        super().__init__(Image)
        self.Pressed = False

    def update_rect_info(self):
        self.Rect.x = self.Xpos
        self.Rect.y = self.Ypos



class Camera():
    def __init__(self, GameModeBase : GameModeBase):
        self.Rect = pygame.Rect(0, 0, GameModeBase.GameScreenWidth, GameModeBase.GameScreenHeight)
        self.Rect.width = GameModeBase.GameScreenWidth
        self.Rect.height = GameModeBase.GameScreenHeight

    def update_rect_info(self, entity):  # Camera에 맞게 entity의 좌표를 수정함
        return pygame.Rect(entity.Xpos - self.Rect.x, entity.Ypos - self.Rect.y, entity.Rect.width, entity.Rect.height)
  
    def follow_target(self, target, GameBackground : Background, GameModeBase : GameModeBase):  
        # 카메라가 특정 대상을 추적하도록 업데이트합니다.

        if (GameModeBase.CameraFollowMethod == "TargetXY"):
          # Target의 center top좌표(in gameworld) + 화면 너비의 절반
          self.Rect.x = (target.Xpos + target.Rect.width / 2) - self.Rect.width / 2
          self.Rect.x = min(self.Rect.x, GameBackground.Xpos + GameBackground.Rect.width - self.Rect.width) # 카메라의 x좌표가 GameBackground를 넘지 않도록 함.
          self.Rect.x = max(self.Rect.x, GameBackground.Xpos)  # 카메라의 x좌표가 GameBackground의 왼쪽을 넘지 않도록 함.
          # Target의 left center좌표(in gameworld) + 화면 높이의 절반
          self.Rect.y = (target.Ypos + target.Rect.height / 2) - self.Rect.height / 2
          self.Rect.y = min(self.Rect.y, GameBackground.Ypos + GameBackground.Rect.height - self.Rect.height)  # 카메라의 y좌표가 GameBackground의 아래쪽을 넘지 않도록 함.
          self.Rect.y = max(self.Rect.y, GameBackground.Ypos)  # 카메라의 y좌표가 GameBackground의 위쪽을 넘지 않도록 함.

        elif (GameModeBase.CameraFollowMethod == "TargetX"):
          # Target의 center top좌표(in gameworld) + 화면 너비의 절반
          self.Rect.x = (target.Xpos + target.Rect.width / 2) - self.Rect.width / 2
          self.Rect.x = min(self.Rect.x, GameBackground.Xpos + GameBackground.Rect.width - self.Rect.width) # 카메라의 x좌표가 GameBackground를 넘지 않도록 함.
          self.Rect.x = max(self.Rect.x, GameBackground.Xpos)  # 카메라의 x좌표가 GameBackground의 왼쪽을 넘지 않도록 함.

        elif (GameModeBase.CameraFollowMethod == "TargetY"):
          self.Rect.y = (target.Ypos + target.Rect.height / 2) - self.Rect.height / 2
          self.Rect.y = min(self.Rect.y, GameBackground.Ypos + GameBackground.Rect.height - self.Rect.height)  # 카메라의 y좌표가 GameBackground의 아래쪽을 넘지 않도록 함.
          self.Rect.y = max(self.Rect.y, GameBackground.Ypos)  # 카메라의 y좌표가 GameBackground의 위쪽을 넘지 않도록 함.


    def update_all_entities(self, entities : typing.List):
        for entity in entities:
          entity.Rect = self.update_rect_info(entity)
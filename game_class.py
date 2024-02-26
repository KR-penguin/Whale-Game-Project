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
    def __init__(self):
        self.Xpos = 0
        self.Ypos = 0



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

    def detect_collision(self, A, B):
        self.offset_x = A.Xpos - B.Xpos
        self.offset_y = A.Ypos - B.Ypos
        
        if A.Mask.overlap(B.Mask, (self.offset_x, self.offset_y)):
            return True
        else:
            return False



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
          if (self.AnimationFrame[1] >= self.AnimationTotalFrame[0] - 1): # Animation Frame이 Animation Max Frame의 첫번째 index(Idle 애니메이션의 Max Frame)과 같거나 더 클때 (Animation이 끝났을 때)
            self.AnimationFrame[1] = 0 # Animation Frame을 0으로 초기화함.
            self.Temp = 0
          else:
            self.AnimationFrame = [0, math.floor(self.Temp)]

        elif (self.Status == "Run"):
          if (self.AnimationFrame[1] >= self.AnimationTotalFrame[1] - 1): # Animation Frame이 8과 같거나 더 클때 (Animation이 끝났을 때)
            self.AnimationFrame[1] = 0 # Animation Frame을 0으로 초기화함.
            self.Temp = 0
          else:
            self.AnimationFrame = [1, math.floor(self.Temp)]

        elif (self.Status == "Jump"):
          if (self.AnimationFrame[1] >= self.AnimationTotalFrame[2] - 1): # Animation Frame이 2과 같거나 더 클때 (Animation이 끝났을 때)
            self.AnimationFrame[1] = self.AnimationTotalFrame[2] - 1
          else: # Animation Frame을 마지막 frame으로 초기화함. 
            self.AnimationFrame = [2, math.floor(self.Temp)]

        elif (self.Status == "Fall"):
          if (self.AnimationFrame[1] >= self.AnimationTotalFrame[3] - 1): # Animation Frame이 2과 같거나 더 클때 (Animation이 끝났을 때)
            self.AnimationFrame[1] = self.AnimationTotalFrame[3] - 1
          else: # Animation Frame을 마지막 frame으로 초기화함.
            self.AnimationFrame = [3, math.floor(self.Temp)]

    def change_status(self, NewStatus : str):
        if (self.Status == NewStatus):
          return
        elif ((self.Status == "Jump" or self.Status == "Fall") and (NewStatus == "Run")):
          # Jump거나 Fall인 상태에서는 Run_Right나 Run_Left 상태로 바꾸지 못하도록 함
          return  
        self.Status = NewStatus
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
        HighQualityAnimation.__init__(self, [8, 8, 2, 2]) # HighQualityAnimation 참고
        self.Speed = Speed
        self.Gravity = 0

        self.JumpValue = 1
        self.MaxJumpVelocity = GameModeBase.GameScreenHeight / 270
        self.bStepOnGround = None # boolean
        self.bBlockByEntity = None # boolean

    def update_movement(self, LevelComponents : typing.List, GameModeBase : GameModeBase, Ground : StaticObject, DeltaTime):
        super().update_movement(DeltaTime)

        if (self.Status == "Fall"):
          self.ToYpos = -self.Gravity
          if (self.Gravity < 55.6): # 최대 중력
            self.Gravity += GameModeBase.GravityAcceleration

        elif (self.Status == "Jump"):
          if (self.ToYpos <= 0):
            self.jump_stop()
          else:
            self.ToYpos -= 0.25
          
        self.update_collision(LevelComponents, GameModeBase)

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

    def jump_start(self):
        if (self.JumpValue >= 1):
          self.JumpValue -= 1
          self.change_status("Jump")
          self.ToYpos = self.MaxJumpVelocity

    def jump_stop(self):
        self.Gravity = 0
        self.change_status("Fall")

    def update_animation(self):
      super().update_animation()

       # Animation Filp
      if (self.Direction == "Right"):
          self.Image = pygame.transform.flip(self.Image, True, False)

    def update_collision(self, LevelComponents : typing.List, WhaleGameMode : GameModeBase):

        self.Collision = False
        # Collision 판단 (감지)
        for LevelComponent in LevelComponents:
            self.Collision = WhaleGameMode.detect_collision(self, LevelComponent)

            if (self.Collision): # Collision이 감지되었을 때

                if (self.Rect.bottom <= LevelComponent.Rect.top): # 위에서 Collision 되었을 때
                    self.bStepOnGround = True
                    self.bBlockByEntity = False

                elif (self.Rect.bottom > LevelComponent.Rect.top): # 옆에서 Collision 되었을 때
                    self.bStepOnGround = False
                    self.bBlockByEntity = True

            else: # 콜리전 감지가 안되었을 때
                self.bStepOnGround = False
                self.bBlockByEntity = False

        if (self.bStepOnGround == False):
            self.change_status("Fall")

      # Idle Again

    def update_collision(self, LevelComponents : typing.List, WhaleGameMode : GameModeBase):
        self.Collision = False
        # Collision 판단 (감지)
        for LevelComponent in LevelComponents:
            self.Collision = WhaleGameMode.detect_collision(self, LevelComponent)

class Button(HUD, Object):

    def __init__(self, Image):
        # 상속된 변수들
        HUD.__init__(self)
        Object.__init__(self, Image)
        self.pressed = False

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
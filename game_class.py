import pygame
import math
import typing

# Xpos와 Rect.x는 다르다
# Xpos는 게임 세상의 x좌표를 뜻하지만,
# Rect.x는 카메라에 그려지는 x좌표를 뜻한다.

# --- classes ---
class Object:
  def __init__(self, Image, Xpos, Ypos):
    self.Image = Image
    self.Rect = self.Image.get_rect()
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
  def __init__(self, FrictionalForce):
    self.FrictionalForce = FrictionalForce



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
    self.Status = "Idle" # Status에는 Idle, Run, Jump 등이 있다.
    self.AnimationFrame = [0, 0] # 첫번째 index는 status를 나타내고, 두번째 index는 현재 Animation의 frame을 나타냄.
    self.AnimationTotalFrame = MaxFrame # AnimationTotalFrame은 list로써 첫번째 index는 첫번째 status(idle)의 총 frame 개수를 나타낸다.

  def update_animation(self):
    self.Temp += 0.1

    if (self.Status == "Idle"):
      self.AnimationFrame = [0, math.floor(self.Temp)]
      if(self.AnimationFrame[1] >= self.AnimationTotalFrame[0]): # Animation Frame이 Animation Max Frame의 첫번째 index(Idle 애니메이션의 Max Frame)과 같거나 더 클때 (Animation이 끝났을 때)
        self.AnimationFrame[1] = 0 # Animation Frame을 0으로 초기화함.
        self.Temp = 0

    elif (self.Status == "Run"):
      self.AnimationFrame = [1, math.floor(self.Temp)]
      if(self.AnimationFrame[1] >= self.AnimationTotalFrame[1]): # Animation Frame이 8과 같거나 더 클때 (Animation이 끝났을 때)
        self.AnimationFrame[1] = 0 # Animation Frame을 0으로 초기화함.
        self.Temp = 0

    elif (self.Status == "Jump"):
      self.AnimationFrame = [2, math.floor(self.Temp)]
      if(self.AnimationFrame[1] >= self.AnimationTotalFrame[2]): # Animation Frame이 8과 같거나 더 클때 (Animation이 끝났을 때)
        self.AnimationFrame[1] = 0 # Animation Frame을 0으로 초기화함.
        self.Temp = 0    



class DynamicObject(Object):
  def __init__(self, Image, Xpos, Ypos):
    super().__init__(Image, Xpos, Ypos)
    self.Xpos = Xpos
    self.Ypos = Ypos
    self.ToXpos = 0
    self.ToYpos = 0

  def update_movement(self, FrictionalForce, DeltaTime):
    self.Xpos += self.ToXpos * DeltaTime
    self.Ypos += self.ToYpos * DeltaTime
    self.ToXpos *= FrictionalForce
    self.ToYpos *= FrictionalForce

  def update_image(self, Image):
    self.Image = Image



class StaticObject(Object):
  def __init__(self, Image, Xpos, Ypos):
    super().__init__(Image, Xpos, Ypos)



class Character(DynamicObject, HighQualityAnimation):

  def __init__(self, Image, Xpos, Ypos, Speed):
    DynamicObject.__init__(self, Image, Xpos, Ypos)
    HighQualityAnimation.__init__(self, [8, 8, 4])
    self.Speed = Speed



class Background(StaticObject, BasicAnimation):

  def __init__(self, Image, Xpos, Ypos):
    StaticObject.__init__(self, Image, Xpos, Ypos)
    BasicAnimation.__init__(self, 8)



class Button(HUD, Object):

  def __init__(self, Image, Xpos, Ypos):
    # 상속된 변수들
    HUD.__init__(self, Xpos, Ypos)
    Object.__init__(self, Image, Xpos, Ypos)

  def update_rect_info(self):
    self.Rect.x = self.Xpos
    self.Rect.y = self.Ypos



class Camera():
  def __init__(self, ScreenWidth, ScreenHeight):
    self.Rect = pygame.Rect(0, 0, ScreenWidth, ScreenHeight)
    self.Rect.width = ScreenWidth
    self.Rect.height = ScreenHeight

  def update_rect_info(self, entity):  # Camera에 맞게 entity의 좌표를 수정함
    return pygame.Rect(entity.Xpos - self.Rect.x, entity.Ypos - self.Rect.y, entity.Rect.width, entity.Rect.height)
  
  def follow_target(self, target, GameBackground : Background):  
    # 카메라가 특정 대상을 추적하도록 업데이트합니다.

    # Target의 center top좌표(in gameworld) + 화면 너비의 절반
    self.Rect.x = (target.Xpos + target.Rect.width / 2) - self.Rect.width / 2
    # Target의 left center좌표(in gameworld) + 화면 높이의 절반
    self.Rect.y = (target.Ypos + target.Rect.height / 2) - self.Rect.height / 2

    self.Rect.x = min(self.Rect.x, GameBackground.Xpos + GameBackground.Rect.width - self.Rect.width) # 카메라의 x좌표가 GameBackground를 넘지 않도록 함.
    self.Rect.x = max(self.Rect.x, GameBackground.Xpos)  # 카메라의 x좌표가 GameBackground의 왼쪽을 넘지 않도록 함.
    self.Rect.y = min(self.Rect.y, GameBackground.Ypos + GameBackground.Rect.height - self.Rect.height)  # 카메라의 y좌표가 GameBackground의 아래쪽을 넘지 않도록 함.
    self.Rect.y = max(self.Rect.y, GameBackground.Ypos)  # 카메라의 y좌표가 GameBackground의 위쪽을 넘지 않도록 함.

  def update_all_entities(self, entities : typing.List):
    for entity in entities:
      entity.Rect = self.update_rect_info(entity)
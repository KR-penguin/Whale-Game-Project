import pygame
import math
import typing

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



class Character(DynamicObject, HighQualityAnimation):

  def __init__(self, Image, Xpos, Ypos, Speed):
    DynamicObject.__init__(self, Image, Xpos, Ypos)
    HighQualityAnimation.__init__(self, [8, 8, 4])
    self.Speed = Speed
    self.bMove = False



class Background(DynamicObject, BasicAnimation):

  def __init__(self, Image, Xpos, Ypos):
    DynamicObject.__init__(self, Image, Xpos, Ypos)
    BasicAnimation.__init__(self, 8)
    self.bMove = False



class Button(HUD, Object):

  def __init__(self, Image, Xpos, Ypos):
    # 상속된 변수들
    HUD.__init__(self, Xpos, Ypos)
    Object.__init__(self, Image, Xpos, Ypos)

  def update_rect_info(self):
    self.Rect.x = self.Xpos
    self.Rect.y = self.Ypos
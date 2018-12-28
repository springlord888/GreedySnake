# SnakeBlock
from GlobalDef import *

class SnakeBlock:
    empCount = 0
     # 位置坐标与当前速度
    def __init__(self, position,velocity):
        self.position = position
        self.velocity = velocity

    def SetVelocity(self,velocity):
        self.velocity = velocity


    def SetPosition(self,position):
        self.position = position


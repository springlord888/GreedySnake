# SnakeBlock
from GlobalDef import *

print(SNAKE_BLOCK_RADIUS)


class SnakeBlock:
    empCount = 0
     # 位置坐标与当前速度
    def __init__(self, xx, yy,vxx,vyy):
        self.x = xx
        self.y = yy
        self.vx = vxx
        self.vy = vyy

    def SetVelocity(self,vxx,vyy):
        self.x = vxx
        self.y = vyy

    def GetVelocity(self):
        return {self.vxx,self.vyy}

    def GetPosition(self):
        return {self.x,self.y}


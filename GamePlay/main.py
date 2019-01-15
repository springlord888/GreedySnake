
import pygame
import random
import math
from SnakeBlock import *
from GlobalDef import *
from Position import *
from Velocity import *



def _IsVelocityLegal(oldVelocity,newVelocity):
        vxSum = oldVelocity.vx+newVelocity.vx
        vySum = oldVelocity.vy+newVelocity.vy
        if vxSum == 0 and vxSum == 0 :
            return False
        else:
            return True

# 判断两个block是否碰撞
def _IsTwoBlockCollide(blocka,blockb):
    positionAx = blocka.position.x
    positionAy = blocka.position.y
    positionBx = blockb.position.x
    positionBy = blockb.position.y
    if (positionBx>(positionAx-SNAKE_BLOCK_RADIUS))\
            and (positionBx<(positionAx+SNAKE_BLOCK_RADIUS))\
            and (positionBy>(positionAy-SNAKE_BLOCK_RADIUS))\
            and (positionBy<(positionAy+SNAKE_BLOCK_RADIUS)):
        return  True
    return  False

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREY = (126,126,126)

SnakeBlockColors = []
SnakeBlockColors.append(WHITE)
#SnakeBlockColors.append(GREEN)
#SnakeBlockColors.append(RED)
SnakeBlockColors.append(BLUE)
SnakeBlockColors.append(GREY)
SnakeBlockColors.append((0,255,255))
SnakeBlockColors.append((238,173,14))
SnakeBlockColors.append((160,32,240))
SnakeBlockColors.append((178,223,238))



# Speed and direction of rectangle

SnakeHeadBlockVelocity = Velocity(SNAKE_VELOCITY*SNAKE_BLOCK_RADIUS,0) #头部初始速度向右
SnakeInitLength = 5
ScreenWidth = 500
ScreenHeight = 500
Score = 0
DeathReason = ''
IsDead = False



#追加一个block
def AddOneBlock(blockList):
    length = len(blockList)
    finalBlock = blockList[length-1]
    finalBlockVx = finalBlock.velocity.vx
    finalBlockVy = finalBlock.velocity.vy
    tempBlcokPos = Position(finalBlock.position.x,finalBlock.position.y)
    if finalBlockVx>0 and finalBlockVy==0 :
        tempBlcokPos.x = tempBlcokPos.x-SNAKE_BLOCK_RADIUS
    elif finalBlockVx<0 and finalBlockVy==0 :
        tempBlcokPos.x = tempBlcokPos.x + SNAKE_BLOCK_RADIUS
    elif finalBlockVx == 0 and finalBlockVy > 0:
        tempBlcokPos.y = tempBlcokPos.y - SNAKE_BLOCK_RADIUS
    elif finalBlockVx == 0 and finalBlockVy < 0:
        tempBlcokPos.y = tempBlcokPos.y + SNAKE_BLOCK_RADIUS

    tempBlcok = SnakeBlock(tempBlcokPos, Velocity(finalBlockVx,finalBlockVy))
    blockList.append(tempBlcok)

# 随机一个苹果的位置
def CaculateApplePosition():
    # todo 不应该与蛇重合
    x = random.randrange(2*SNAKE_BLOCK_RADIUS, ScreenWidth-2*SNAKE_BLOCK_RADIUS)
    y = random.randrange(2*SNAKE_BLOCK_RADIUS, ScreenHeight-2*SNAKE_BLOCK_RADIUS)
    #  x 与 y应该是蛇块半径的整数倍，这样可以和蛇头严格对准
    x = math.floor(x/SNAKE_BLOCK_RADIUS) *SNAKE_BLOCK_RADIUS
    y = math.floor(y/SNAKE_BLOCK_RADIUS) *SNAKE_BLOCK_RADIUS
    pos = Position(x,y)
    return  pos


# 初始化数据
SnakeBlockList = []
for i in range(SnakeInitLength):
    position = Position(220-(i*SNAKE_BLOCK_RADIUS),100)
    tempBlcok = SnakeBlock(position,SnakeHeadBlockVelocity)
    SnakeBlockList.append(tempBlcok)

# 苹果
AppleBlock = SnakeBlock(CaculateApplePosition(),Velocity(0,0))




pygame.init()

# Set the width and height of the screen [width, height]
size = (ScreenWidth, ScreenHeight)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("GreedySnake")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # User let up on a key
        elif event.type == pygame.KEYUP:
            newVelocity = SnakeHeadBlockVelocity
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT:
                newVelocity = Velocity(-SNAKE_VELOCITY*SNAKE_BLOCK_RADIUS, 0)
            elif event.key == pygame.K_RIGHT:
                newVelocity = Velocity(SNAKE_VELOCITY*SNAKE_BLOCK_RADIUS, 0)
            elif event.key == pygame.K_UP:
                newVelocity = Velocity(0, -SNAKE_VELOCITY*SNAKE_BLOCK_RADIUS)
            elif event.key == pygame.K_DOWN:
                newVelocity = Velocity(0, SNAKE_VELOCITY*SNAKE_BLOCK_RADIUS)

            isLegal = _IsVelocityLegal(SnakeHeadBlockVelocity, newVelocity)
            if isLegal:
                SnakeHeadBlockVelocity = newVelocity

    # 除头部外的速度设置
    for i in range(len(SnakeBlockList)-1, 0, -1):
        lastBlockVelocity = SnakeBlockList[i-1].velocity
        SnakeBlockList[i].SetVelocity(lastBlockVelocity)

    # 头部速度设置
    SnakeBlockList[0].SetVelocity(SnakeHeadBlockVelocity)

    #蛇块的位置更新
    for i in range(len(SnakeBlockList)):
        tempBlcok = SnakeBlockList[i]
        tempPosition = SnakeBlockList[i].position
        tempVelocity = SnakeBlockList[i].velocity
        newPosition = Position(tempPosition.x+tempVelocity.vx,tempPosition.y+tempVelocity.vy)
        SnakeBlockList[i].SetPosition(newPosition)
        #检查头部与身体是否碰撞
        if  i!= 0 :
            snakeHeadBlock = SnakeBlockList[0]
            isCollide = _IsTwoBlockCollide(snakeHeadBlock,tempBlcok)
            if isCollide :
                #print("头撞到身体了啊啊啊啊啊")
                DeathReason = 'SNKAE HITS HIMSELF'
                IsDead = True
                done = True


    # 检查蛇头与苹果的碰撞
    isCollideApple = _IsTwoBlockCollide(SnakeBlockList[0], AppleBlock)
    if  isCollideApple :
        #print("吃到一颗红苹果")
        # 更新苹果位置
        AppleBlock = SnakeBlock(CaculateApplePosition(), Velocity(0, 0))
        # 增加蛇的长度
        AddOneBlock(SnakeBlockList)
        #print("蛇长===",len(SnakeBlockList))
        # 更新分数
        Score = Score +1

    # 检查蛇头与墙的碰撞(注意蛇头的坐标在左上角)
    snakeheadPosx = SnakeBlockList[0].position.x
    snakeheadPosy = SnakeBlockList[0].position.y
    if snakeheadPosx<=SNAKE_BLOCK_RADIUS\
        or snakeheadPosx>=(ScreenWidth-2*SNAKE_BLOCK_RADIUS)\
        or snakeheadPosy<=SNAKE_BLOCK_RADIUS\
        or snakeheadPosy>=(ScreenHeight - 2*SNAKE_BLOCK_RADIUS):
        # print("大兄弟你撞墙了啊")
        DeathReason = 'SNKAE HITS THE WALL'
        IsDead = True
        done = True

    # --- Screen-clearing code goes here
    # background image.
    screen.fill(BLACK)

    # --- Drawing code should go here

    # 画图
    # snake
    for i in range(len(SnakeBlockList)):
        block = SnakeBlockList[i]
        blockColor = SnakeBlockColors[i% len(SnakeBlockColors)]
        pygame.draw.rect(screen, blockColor, [block.position.x, block.position.y, SNAKE_BLOCK_RADIUS, SNAKE_BLOCK_RADIUS])

    # apple
    pygame.draw.rect(screen, RED, [AppleBlock.position.x, AppleBlock.position.y, SNAKE_BLOCK_RADIUS, SNAKE_BLOCK_RADIUS])

    #border
    """
    # 一块一块的
    for i in range(int(ScreenWidth/SNAKE_BLOCK_RADIUS)):
        pygame.draw.rect(screen, GREEN,[SNAKE_BLOCK_RADIUS*i, 0, SNAKE_BLOCK_RADIUS, SNAKE_BLOCK_RADIUS])
        pygame.draw.rect(screen, GREEN,[SNAKE_BLOCK_RADIUS*i, ScreenHeight-SNAKE_BLOCK_RADIUS, SNAKE_BLOCK_RADIUS, SNAKE_BLOCK_RADIUS])
    """
    pygame.draw.rect(screen, GREEN, [0, 0, ScreenWidth, SNAKE_BLOCK_RADIUS])
    pygame.draw.rect(screen, GREEN, [0, ScreenHeight-SNAKE_BLOCK_RADIUS, ScreenWidth, SNAKE_BLOCK_RADIUS])
    pygame.draw.rect(screen, GREEN, [0, 0, SNAKE_BLOCK_RADIUS, ScreenHeight])
    pygame.draw.rect(screen, GREEN, [ScreenWidth-SNAKE_BLOCK_RADIUS, 0, SNAKE_BLOCK_RADIUS, ScreenHeight])

    # 得分显示
    font = pygame.font.SysFont('Arial', 25, True, False)
    textScore = font.render("Score:"+str(Score), True, WHITE)
    screen.blit(textScore, [20, 20])
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(8)


# 显示最后分数并点击后退出游戏
done2 = False
# -------- Main Program Loop -----------
while not done2:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done2 = True
    screen.fill(BLACK)
    font = pygame.font.SysFont('Arial', 30, True, False)
    textScore = font.render("Final Socre:"+str(Score), True, WHITE)
    screen.blit(textScore, [180, 180])
    if IsDead:
        textReason = font.render("Reason:" + DeathReason, True, RED)
        screen.blit(textReason, [80, 220])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 4 frames per second
    clock.tick(4)

# Close the window and quit.
pygame.quit()
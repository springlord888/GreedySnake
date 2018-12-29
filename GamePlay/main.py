
import pygame
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

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
rect_x = 50
rect_y = 50

# Speed and direction of rectangle
rect_change_x = 5
rect_change_y = 5

SnakeHeadBlockVelocity = Velocity(SNAKE_VELOCITY*SNAKE_BLOCK_RADIUS,0) #头部出事速度向右



# 初始化数据
SnakeBlockList = []
for i in range(10):
    position = Position(220-(i*SNAKE_BLOCK_RADIUS),20)
    tempBlcok = SnakeBlock(position,SnakeHeadBlockVelocity)
    SnakeBlockList.append(tempBlcok)



pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

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

    # --- Game logic should go here
    for i in range(9, 0, -1):
        lastBlockVelocity = SnakeBlockList[i-1].velocity
        SnakeBlockList[i].SetVelocity(lastBlockVelocity)

    # 头部速度设置
    SnakeBlockList[0].SetVelocity(SnakeHeadBlockVelocity)
    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)

    # --- Drawing code should go here
    for i in range(10):
        # 数据
        tempBlcok = SnakeBlockList[i]
        tempPosition = SnakeBlockList[i].position
        tempVelocity = SnakeBlockList[i].velocity
        newPosition = Position(tempPosition.x+tempVelocity.vx,tempPosition.y+tempVelocity.vy)
        SnakeBlockList[i].SetPosition(newPosition)
        # 画图
        pygame.draw.rect(screen, WHITE, [newPosition.x+SNAKE_VELOCITY, newPosition.y+SNAKE_VELOCITY, SNAKE_BLOCK_RADIUS, SNAKE_BLOCK_RADIUS])

    # Bounce the rectangle if needed
    if rect_y > 450 or rect_y < 0:
        rect_change_y = rect_change_y * -1
    if rect_x > 650 or rect_x < 0:
        rect_change_x = rect_change_x * -1

    pygame.draw.rect(screen, WHITE, [rect_x, rect_y, 50, 50])
    pygame.draw.rect(screen, RED, [rect_x + 10, rect_y + 10, 30, 30])

    rect_x += rect_change_x
    rect_y += rect_change_y
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(2)

# Close the window and quit.
pygame.quit()
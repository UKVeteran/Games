import random
import pygame
pygame.init()


def moveAnimation(image1, image2, count):
    if 10 < count % 20 <= 20:
        return image2
    else:
        return image1


def upClear(x, y):
    canMove = True

    if verticalDoorLeft <= x <= verticalDoorRight and y - 1 < topWall:
        canMove = True
    elif y - 1 < topWall:
        canMove = True
    elif (x < leftWall or x > rightWall) and y - 1 < middleDoorsTop:
        canMove = True

    if canMove:
        return 1
    else:
        return 0


def downClear(x, y):
    canMove = True

    if verticalDoorLeft <= x <= verticalDoorRight and bottomWall < y + 1:
        canMove = True
    elif bottomWall < y + 1:
        canMove = True
    elif (x < leftWall or x > rightWall) and y + 1 > middleDoorsBottom:
        canMove = True

    if canMove:
        return 1
    else:
        return 0


def leftClear(x, y):
    canMove = True

    if middleDoorsTop <= y <= middleDoorsBottom and x - 1 < leftWall:
        canMove = True
    elif x - 1 < leftWall:
        canMove = True
    elif (y > bottomWall or y < topWall) and x - 1 < verticalDoorLeft:
        canMove = True

    if canMove:
        return 1
    else:
        return 0


def rightClear(x, y):
    canMove = True

    if middleDoorsTop <= y <= middleDoorsBottom and x + 1 > rightWall:
        canMove = True
    elif x + 1 > rightWall:
        canMove = True
    elif (y > bottomWall or y < topWall) and x + 1 > verticalDoorRight:
        canMove = True

    if canMove:
        return 1
    else:
        return 0


def checkOffscreen(x, y):
    if x < -14:
        x = windowSize[0] - 14
    elif x > windowSize[0] - 14:
        x = -14

    if y < -20:
        y = windowSize[1] - 20
    elif y > windowSize[1] - 20:
        y = -20
    return x, y


def playersTouching():
    global pOneX, pOneY, pTwoX, pTwoY

    if -32 < pOneX - pTwoX < 32 and -40 < pOneY - pTwoY < 40:
        xDiff = pOneX - pTwoX
        yDiff = pOneY - pTwoY

        for dist in range(abs(xDiff) / 2):
            pOneMove = leftClear(pOneX, pOneY) + rightClear(pOneX, pOneY)
            pTwoMove = leftClear(pTwoX, pTwoY) + rightClear(pTwoX, pTwoY)
            if xDiff > 0:
                pOneX += pOneMove / 2 * xDiff / xDiff
                pTwoX -= pTwoMove / 2 * xDiff / xDiff
            else:
                pOneX -= pOneMove / 2 * xDiff / xDiff
                pTwoX += pTwoMove / 2 * xDiff / xDiff

        for dist in range(abs(yDiff) / 2):
            pOneMove = upClear(pOneX, pOneY) + downClear(pOneX, pOneY)
            pTwoMove = upClear(pTwoX, pTwoY) + downClear(pTwoX, pTwoY)
            if yDiff > 0:
                pOneY += pOneMove / 2 * yDiff / yDiff
                pTwoY -= pTwoMove / 2 * yDiff / yDiff
            else:
                pOneY -= pOneMove / 2 * yDiff / yDiff
                pTwoY += pTwoMove / 2 * yDiff / yDiff

def touchingBombe(x, y):
    return -32 < x - bombePos[0] < 20 and -40 < y - bombePos[1] < 20

def randomPosition():
    # return x and y
    x = random.randrange(32, windowSize[0] - 52)
    y = random.randrange(32, windowSize[1] - 52)
    return x, y

windowSize = [640, 384]
screen = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()

# Font for points
pointFont = pygame.font.SysFont("Monospace", 15)

# Variables for position etc.
pOneX = windowSize[0] / 4
pOneY = windowSize[1] / 2

pTwoX = windowSize[0] / 4 * 3
pTwoY = windowSize[1] / 2

pOnePoints = 0
pTwoPoints = 0

pOneCount = 0
pTwoCount = 0

bombePos = randomPosition()

pOneMoving = False
pTwoMoving = False

# Variables for walls
leftWall = 28
topWall = 16
rightWall = windowSize[0] - 60
bottomWall = 312

middleDoorsTop = 144
middleDoorsBottom = 182
verticalDoorLeft = 284
verticalDoorRight = verticalDoorLeft + 40

# Load images
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, windowSize)

pOneMove1 = pygame.image.load("arken.png")
pOneMove1 = pygame.transform.scale2x(pOneMove1)

pOneMove2 = pygame.image.load("arken1.png")
pOneMove2 = pygame.transform.scale2x(pOneMove2)

pOneStanding = pygame.image.load("arken1.png")
pOneStanding = pygame.transform.scale2x(pOneStanding)

bombe = pygame.image.load("bombe.png")
bombe = pygame.transform.scale2x(bombe)

# Load music and sound
coinSound = pygame.mixer.Sound("coin.wav")
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

   # Game loop
done = False
while not done:

    # Get movement
    # Player 1 movement
    pOneMoving = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        pOneY += downClear(pOneX, pOneY)
        pOneMoving = True
    if keys[pygame.K_w]:
        pOneY -= upClear(pOneX, pOneY)
        pOneMoving = True
    if keys[pygame.K_a]:
        pOneX -= leftClear(pOneX, pOneY)
        pOneMoving = True
    if keys[pygame.K_d]:
        pOneX += rightClear(pOneX, pOneY)
        pOneMoving = True


    pOneX, pOneY = checkOffscreen(pOneX, pOneY)

    # Player 1 animation
    if pOneMoving:
        pOneCount += 1
        pOneImage = moveAnimation(pOneMove1, pOneMove2, pOneCount)
    else:
        pOneImage = pOneStanding

    # Check touching coin
    if touchingBombe(pOneX, pOneY):
        pOnePoints += 1
        coinSound.play()
          
    # Move coin if touching
    if touchingBombe(pOneX, pOneY):
            bombePos = randomPosition()
    
    # Render points for display
    pOnePointLabel = pointFont.render(str(pOnePoints), 1, (255, 255, 255))
    
    # Update display
    screen.blit(background, (0, 0))
    screen.blit(bombe, bombePos )
    screen.blit(pOneImage, [pOneX, pOneY])

    screen.blit(pOnePointLabel, [pOneX - 12, pOneY - 12])
    pygame.display.flip()
    # exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    clock.tick(60)
pygame.quit()

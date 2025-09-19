import math

currBallPos = [0.5, 0.5]

currDirectionDeg = 30.5
directionAfterRightWallBounce = 180 - currDirectionDeg

currDirectionDeg = directionAfterRightWallBounce

count = 0
while count < 10:
    count += 1
    currDirectionRad = currDirectionDeg * (math.pi / 180)
    speed = 1 / 600

    deltaY = speed * math.sin(currDirectionRad)
    deltaX = speed * math.cos(currDirectionRad)

    newBallPos = [currBallPos[0] + deltaX, currBallPos[1] - deltaY]
    currBallPos = newBallPos
    print(currBallPos[0], currBallPos[1])

import cv2
import mediapipe
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
from enum import Enum
from random import randint

class RPS_Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class RPS_Result(Enum):
    PLAYER1_WIN = 1
    PLAYER2_WIN = 2
    TIE = 3

def getRPSMove(fingers):
    if fingers == [0,0,0,0,0]: return RPS_Move.ROCK
    if fingers == [1,1,1,1,1]: return RPS_Move.PAPER
    if fingers == [0,1,1,0,0]: return RPS_Move.SCISSORS

def getAIRPSMove():
    randI = randint(1,3)
    return randI
    if randI == 1: return RPS_Move.ROCK
    if randI == 2: return RPS_Move.PAPER
    if randI == 3: return RPS_Move.SCISSORS

def CheckRPSWinner(move1, move2):
    if move1 == move2: return RPS_Result.TIE
    if move1 == RPS_Move.ROCK and move2 == RPS_Move.PAPER: return RPS_Result.PLAYER2_WIN
    if move1 == RPS_Move.ROCK and move2 == RPS_Move.SCISSORS: return RPS_Result.PLAYER1_WIN
    if move1 == RPS_Move.PAPER and move2 == RPS_Move.SCISSORS: return RPS_Result.PLAYER2_WIN
    else: return RPS_Result.PLAYER2_WIN if CheckRPSWinner(move2, move1) == RPS_Result.PLAYER1_WIN else RPS_Result.PLAYER1_WIN


H, W = 3, 4

cap = cv2.VideoCapture(0)
cap.set(H, 640)
cap.set(W, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0]

while True:
    imgBG = cv2.imread("src/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    imgScaled = imgScaled[:,80:480]


    # Find Hands
    hands, img = detector.findHands(imgScaled)


    if startGame:

        if stateResult is False:
            timer = time.time() - intialTime
            cv2.putText(imgBG, str(int(timer)),(605,435), cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 4)

        if timer > 3:
            stateResult = True
            timer = 0

            if hands:
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                playerMove = getRPSMove(fingers)

                AIMove = getAIRPSMove()
                imgAI = cv2.imread(f'src/{AIMove}.png', cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgAI, (149,310))

                print(AIMove)
                print(playerMove)
                if playerMove != None:
                    if CheckRPSWinner(RPS_Move(AIMove), playerMove) == RPS_Result.PLAYER1_WIN: scores[0]+=1
                    elif CheckRPSWinner(RPS_Move(AIMove), playerMove) == RPS_Result.PLAYER2_WIN: scores[1]+=1
                else: cv2.putText(imgBG, "NO MOVE",(605,435), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 2)








    imgBG[234:654,795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    #cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    #cv2.imshow("scaled", imgScaled)
    key = cv2.waitKey(1)

    if key == ord('s'):
        startGame = True
        intialTime = time.time()
        stateResult = False


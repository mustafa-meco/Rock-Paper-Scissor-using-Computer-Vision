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

def getMoveString(move):
    if move == RPS_Move.ROCK: return "Rock"
    if move == RPS_Move.PAPER: return "Paper"
    if move == RPS_Move.SCISSORS: return  "Scissors"
    return "No Move"

H, W = 3, 4

cap = cv2.VideoCapture("https://192.168.1.11:4343/video")
cap.set(H, 640)
cap.set(W, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0]

while True:
    imgBG = cv2.imread("src/Background.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    imgScaled = imgScaled[:,80:480]


    # Find Hands
    hands = detector.findHands(imgScaled,draw=False)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        playerMove = getRPSMove(fingers)

        cv2.rectangle(imgScaled, (hand["bbox"][0] - 20, hand["bbox"][1] - 20),
                      (hand["bbox"][0] + hand["bbox"][2] + 20, hand["bbox"][1] + hand["bbox"][3] + 20),
                      (255, 182, 56), 2)
        cv2.putText(imgScaled, getMoveString(playerMove), (hand["bbox"][0] - 30, hand["bbox"][1] - 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    2, (255, 182, 56), 2)

    if startGame:

        if stateResult is False:
            timer = time.time() - intialTime
            cv2.putText(imgBG, str(int(timer)),(605,435), cv2.FONT_HERSHEY_PLAIN, 6, (255,182,56), 4)

        if timer > 3:
            stateResult = True
            timer = 0

            AIMove = getAIRPSMove()
            imgAI = cv2.imread(f'src/{AIMove}.png', cv2.IMREAD_UNCHANGED)
            imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

            if hands:

                if playerMove in [RPS_Move.PAPER, RPS_Move.ROCK, RPS_Move.SCISSORS]:
                    if CheckRPSWinner(RPS_Move(AIMove), playerMove) == RPS_Result.PLAYER1_WIN: scores[0]+=1
                    elif CheckRPSWinner(RPS_Move(AIMove), playerMove) == RPS_Result.PLAYER2_WIN: scores[1]+=1

            else:
                NoMove = True
                cv2.putText(imgBG, "NO MOVE",(530,420), cv2.FONT_HERSHEY_PLAIN, 6, (255,182,56), 4)


    imgBG[234:654,795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
        if NoMove: cv2.putText(imgBG, "NO MOVE", (530, 420), cv2.FONT_HERSHEY_PLAIN, 3, (255,182,56), 2)

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    #cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    #cv2.imshow("scaled", imgScaled)
    key = cv2.waitKey(1)

    if key == ord('s'):
        NoMove = False
        startGame = True
        intialTime = time.time()
        stateResult = False
    if key == ord('q'):
        break


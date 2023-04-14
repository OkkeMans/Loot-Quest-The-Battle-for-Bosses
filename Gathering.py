import pygame, easygui, random, time
from Functions import *
from Endgame import *
from PIL import *

#----- Global variables -----#

# Amount of players
players = 0

# Space cords
spaces = [[823,820],
[731,820], [642,820], [552,820], [463,820], [373,820], [283,820], [193,820],
[33,820],
[33,726], [33,639], [33,549], [33,459], [33,371], [33,281], [33,191],
[33,30],
[193,30], [283,30], [373,30], [463,30], [551,30], [641,30], [731,30],
[823,30],
[823,190], [823,280], [823,370], [823,460], [823,548], [823,638], [823,725]]

# Special spaces
shopSpace = [1,3,6,9,13,15,18,21,23,25,26,29]
clueSpace = [2,10,17,30]
stationSpace = [4,12,20,28]
goldSpace = [5,11,14,19,27,31]
swapSpace = [7,22]

# Character positions
position = [0,0,0,0,0,0,0,0]
walkPos = [0,0,0,0,0,0,0,0]

# Turn
turn = 0

# Rounds
rounds = 0

# Throw
throw = 0

# Day/night
day = True

# Are we still in the first lap?
firstLap = True

# Background fill
timeColor = 200,180,160
textColor = 65,60,50
highlightColor = 0,0,0

# Travel locations
locations = {"Station 1": 4,"Station 2": 12,"Station 3": 20,"Station 4": 28,}

# Board image
boardDay = pygame.image.load("Bijlagen\BoardDay.png")
boardNight = pygame.image.load("Bijlagen\BoardNight.png")
boardSize = (1000,1000)
boardDay = pygame.transform.scale(boardDay, boardSize)
boardNight = pygame.transform.scale(boardNight, boardSize)

# Character images
character1 = pygame.image.load("Bijlagen\Character1.png") 
character2 = pygame.image.load("Bijlagen\Character2.png")
character3 = pygame.image.load("Bijlagen\Character3.png")
character4 = pygame.image.load("Bijlagen\Character4.png")
character5 = pygame.image.load("Bijlagen\Character5.png")
character6 = pygame.image.load("Bijlagen\Character6.png")
character7 = pygame.image.load("Bijlagen\Character7.png")
character8 = pygame.image.load("Bijlagen\Character8.png")
characterImages = [character1, character2, character3, character4, character5, character6, character7, character8]

ticketImage = pygame.image.load("Bijlagen\Ticket.png")
ticketImage = pygame.transform.scale(ticketImage,(35,35))

# Character distribution
baseExtra = [(0,5),(37,5),(0,42),(37,42),(0,79),(37,79),(0,116),(37,116)]

# Items/inventory (First digit = Attack damage, second = Magic damage, third = armor and fourth = magic shield)
inv = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

# Amount of HP per player
health = [20,20,20,20,20,20,20,20]

# Amount of HP the boss has
bossHealth = 200

# Amount of damage the player does to the boss
damage = [0,0,0,0,0,0,0,0]

# Check movement
walking = False

# Gambler responses
gamblerOptions = ["You recieve an epic sword",
"You recieve an epic wand",
"You recieve epic armor",
"You recieve epic magic protection",
"You recieve 500 gold",
"You lose 500 gold",
"Your Attack damage and Magic damage switch values",
"Your Armor and Magic protection switch values",
"You can choose your next throw value",
"Your skip your next turn",
"Your next visit to the epic shop will grant you access to the legendary shop"]

# Does the player have a train ticket?
trainTicket = [False,False,False,False,False,False,False,False]

# Can this player choose their next throw?
chooseThrow = [False,False,False,False,False,False,False,False]

# Does this player skip their next turn?
gambleSkip = [False,False,False,False,False,False,False,False]

# Does this player have access to the legendary shop next time they pass it?
legendaryAccess = [False,False,False,False,False,False,False,False]

# Player gold
gold = [0,0,0,0,0,0,0,0]

# Shop items
shopB = [{"Basic sword": [(3,0,0,0), 250]}, {"Basic wand": [(0,3,0,0), 250]}, {"Basic armor": [(0,0,2,0), 200]}, {"Basic magic shield": [(0,0,0,2), 200]}]
shopE = [{"Epic sword": [(7,0,0,0), 550]}, {"Epic wand": [(0,7,0,0), 600]}, {"Epic armor": [(0,0,5,0), 450]}, {"Epic magic shield": [(0,0,0,5), 450]}]
shopL = [{"Legendary sword": [(13,0,0,0), 1000]}, {"Legendary wand": [(0,13,0,0), 1200]}, {"Legendary armor": [(0,0,9,0), 750]}, {"Legendary magic shield": [(0,0,0,9), 750]}]

# Boss clues
clues = {
    "AD": "The boss deals Attack Damage",
    "MD": "The boss deals Magic Damage",
    "AP": "The boss has Attack Protection",
    "MP": "The boss has Magic Protection"
}

# Boss decide
bossType = random.choice(["ADAP", "ADMP", "MDAP", "MDMP"])
damageType = bossType[:2]
shieldType = bossType[2:]
bossStats = [0,0,0,0]
if damageType == "AD":
    bossStats[0] = 25
else:
    bossStats[1] = 25
if shieldType == "AP":
    bossStats[2] = 20
else:
    bossStats[3] = 20

# Leaderboard player cords
leaderboardCords = [(200, 205), (200, 282.5), (200, 360), (200, 437.5), (200, 515), (200, 592.5), (200, 670), (200, 747.5)]

# The cords for where the higlight should be
highlightCords = [(195, 200), (195, 277.5), (195, 355), (195, 432.5), (195, 510), (195, 587.5), (195, 665), (195, 742.5)]

# Where should the train ticket appear
ticketCords = [(769, 193), (769, 270.5), (769, 348), (769, 425.5), (769, 503), (769, 580.5), (769, 658), (769, 735.5)]

# Players that are out of the game
skippedTurns = []

#----- Start menu -----#

start = False
while not start:
    menuOptions = easygui.buttonbox("Hello there, what do you want to do?", "START MENU", ("Start Game", "Story", "Exit"))
    if menuOptions == "Story":
        story()
    elif menuOptions == "Exit":
        start = True
        done = True
    elif menuOptions == "Start Game":
        start = True
        try:
            players = int(easygui.buttonbox("Choose player count", "AMOUNT OF PLAYERS", str(2345678)))
        except TypeError:
            done = True
        else:
            easygui.msgbox(f"Amount of players selected : {players}", "SELECTED PLAYER COUNT", "Lets go!")
            done = False
        playerlist = []
        for i in range(players):
            playerlist.append(str(i + 1))

        #----- Pygame initialisation -----#

        # Initialise Pygame
        pygame.init()

        # Initialise Mixer
        pygame.mixer.init()

        # Screen size
        WINDOW_SIZE = [1920,1080]

        # Load sounds
        walkSound = pygame.mixer.Sound("Bijlagen\Walk.wav")
        # goldSound = pygame.mixer.music.load("Bijlagen\SOUND.mp3")

        # Create screen
        screen = pygame.display.set_mode(WINDOW_SIZE)

        # Screen title
        pygame.display.set_caption("THE CURSED TOWN - Gathering")

        # Clock setup
        clock = pygame.time.Clock()


#----- Main program ----#

while not done:
    
    if rounds < 1:

    #--- Check activities (mouseclicks, button presses etc.) ---#

        # Change board and colors depending on day/time
        if day:
            board = boardDay
            timeColor = 200,180,160
            textColor = 65,60,50
            highlightColor = 0,0,0

        else:
            board = boardNight
            timeColor = 45,40,35
            textColor = 200,175,150
            highlightColor = 255,255,255
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Execute keypress
                if event.key == pygame.K_SPACE:
                    if not chooseThrow[turn]:
                        throw = random.randint(1,6) + random.randint(1,6)
                    else:
                        throw = easygui.integerbox("Choose what you want your next throw to be", "CHOOSE YOUR THROW", None, 1, 12)
                    walking = True
                    position[turn] += throw

                    if position[turn] > 31:
                        position[turn] -= 32     

                elif event.key == pygame.K_e:
                    easygui.msgbox(f"You have {str(inv[turn][0])} attack damge, {str(inv[turn][1])} magic damage, {str(inv[turn][2])} armor and {str(inv[turn][3])} magic protection.", "Stats", "BACK TO BOARD")
                    pygame.event.clear()


        #--- Draw/update graphics ---#

        if not walking:
            updateText(screen, timeColor, board, throw, textColor, highlightColor, highlightCords, turn, players, inv, gold, leaderboardCords, trainTicket, ticketCords, ticketImage)
            updatePositions(players, walkPos, baseExtra, spaces, screen, characterImages)
        else:
            for i in range(throw):
                walkPos[turn] += 1
                if walkPos[turn] > 31:
                    walkPos[turn] -= 32
                    firstLap = False 
                pygame.mixer.Sound.play(walkSound)  
                updateText(screen, timeColor, board, throw, textColor, highlightColor, highlightCords, turn, players, inv, gold, leaderboardCords, trainTicket, ticketCords, ticketImage)
                updatePositions(players, walkPos, baseExtra, spaces, screen, characterImages)
                pygame.display.flip()
                specialCheckWalk(walkPos, turn, gamblerOptions, shopE, shopL, gold, inv, day, firstLap, chooseThrow, gambleSkip, legendaryAccess)
                time.sleep(0.2)

            walking = False
            updateText(screen, timeColor, board, throw, textColor, highlightColor, highlightCords, turn, players, inv, gold, leaderboardCords, trainTicket, ticketCords, ticketImage)
            updatePositions(players, walkPos, baseExtra, spaces, screen, characterImages)
            pygame.display.flip()
            specialCheckPos(position, turn, shopSpace, shopE, gold, inv, clueSpace, clues, damageType, shieldType, stationSpace, trainTicket, firstLap, locations, walkPos, goldSpace, swapSpace, playerlist)

            #----- Check if broke -----#
            
            updateText(screen, timeColor, board, throw, textColor, highlightColor, highlightCords, turn, players, inv, gold, leaderboardCords, trainTicket, ticketCords, ticketImage)
            updatePositions(players, walkPos, baseExtra, spaces, screen, characterImages)
            pygame.display.flip()
            for i in range(players): 
                if gold[i] < 0 and str(i + 1) in playerlist:
                    skippedTurns.append(i)
                    easygui.msgbox(f"Player {i + 1} does not have enough gold to continue playing. Player {i + 1} is now eliminated", "PLAYER ELIMINATED", "Continue")
                    playerlist.remove(str(i + 1))
                    if len(playerlist) == 1:
                        easygui.msgbox(f"Oh, there is only one player remaining. I guess you win? \nPLAYER {playerlist[0]} YOU WON!", f"PLAYER {playerlist[0]} WON", "CONGRATULATIONS")
                        done = True
            
            updateText(screen, timeColor, board, throw, textColor, highlightColor, highlightCords, turn, players, inv, gold, leaderboardCords, trainTicket, ticketCords, ticketImage)
            updatePositions(players, walkPos, baseExtra, spaces, screen, characterImages)
            pygame.display.flip()
            # Switch turns
            if turn < players - 1:
                turn += 1
            else:
                turn = 0
                rounds += 1
                if day:
                    day = False
                    if firstLap:
                        easygui.msgbox("Its getting dark outside...", "Whats happening?", "Continue")
                else:
                    day = True
                    if firstLap:
                        easygui.msgbox("Whats that light?", "Whats happening?", "Continue")
                    
            while gambleSkip[turn] or turn in skippedTurns:
                gambleSkip[turn] = False
                if turn < players - 1:
                    turn += 1
                else:
                    turn = 0
        
    else:
        ending(players, inv, bossStats, health, bossHealth, damage, skippedTurns, screen, bossType, playerlist)
        for i in range(players):
            print(inv[i])
            done = True

    # Refresh screen
    updateText(screen, timeColor, board, throw, textColor, highlightColor, highlightCords, turn, players, inv, gold, leaderboardCords, trainTicket, ticketCords, ticketImage)
    updatePositions(players, walkPos, baseExtra, spaces, screen, characterImages)
    clock.tick(60)
    pygame.display.flip()


#----- Quit -----#
pygame.quit()
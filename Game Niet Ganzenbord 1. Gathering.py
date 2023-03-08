import pygame, easygui, random, time
#----- Functions -----#

# Refresh screen
def updateScreen():
    screen.fill(timeColor)

    boardrect = board.get_rect()
    screen.blit(board, boardrect)

    for i in range(players):
        if walkPos[i] in [0, 8, 16, 24]:
            extraX, extraY = baseExtra[i]
            extraX += 35
        elif walkPos[i] in range(1, 8) or walkPos[i] in range(17, 24):
            extraX = 32 * (i % 2) + (2 if i in (0, 2, 4, 6) else 12)
            extraY = 32 * (i // 2) + 5
            if i in [2, 3]:
                extraY += 5
            elif i in [4, 5]:
                extraY += 10
            elif i in [6, 7]:
                extraY += 15
        elif walkPos[i] in range(9, 16) or walkPos[i] in range(25, 32):
            extraX = 32 * (i // 2) + 2
            if i in [2, 3]:
                extraX += 5
            elif i in [4, 5]:
                extraX += 10
            elif i in [6, 7]:
                extraX += 15
            extraY = 32 * (i % 2) + (5 if i in (0, 2, 4, 6) else 12)

        player_x = spaces[walkPos[i]][0] + extraX
        player_y = spaces[walkPos[i]][1] + extraY
        screen.blit(characterImages[i], (player_x, player_y))
    
    # Draw text
    font = pygame.font.Font("LuckiestGuy-Regular.ttf", 50)
    # Show last throw
    # text = (f"Last throw: {throw}")
    # label = font.render(text,True,(textColor))
    # screen.blit(label,(200,200))
    highlight = pygame.Surface((600,55))
    highlight.set_alpha(30)
    highlight.fill((highlighColor))
    screen.blit(highlight, ((highlightCords[turn])))
    
    for i in range (players):
        text = (f"Player {i + 1} | {inv[i]} | {gold[i]}")
        label = font.render(text,True,(textColor))
        screen.blit(label,(leaderboardCords[i]))

# Check special space with walking
def specialCheckWalk(turn):
    updateScreen()
    if walkPos[turn] == 8: # check if at space 8
        extraX, extraY = baseExtra[turn]
        player_x = 65 + extraX
        player_y = 820 + extraY
        screen.blit(characterImages[turn], (player_x, player_y))
        pygame.display.flip()

    elif walkPos[turn] == 16: # check if at space 16
        extraX, extraY = baseExtra[turn]
        player_x = 65 + extraX
        player_y = 30 + extraY
        screen.blit(characterImages[turn], (player_x, player_y))
        pygame.display.flip()
        buyShop = easygui.ynbox(f"Welcome to the shop! \nDo you want to buy something or make some money player {turn + 1}?", "Standard shop", ["Buy something", "Make money"])
        if buyShop == True:
            options = random.sample(shop1, 3)
            option1, = options[0].keys()
            option2, = options[1].keys()
            option3, = options[2].keys()
            bought = easygui.buttonbox(f"Welcome to the shop! \nWhat do you want to buy? player {turn + 1}?", "Standard shop", [option1, option2, option3])
            for item in shop1:
                if bought in item:
                    selected_item = item[bought]
                    selected_item = list(selected_item)
                    break
            for i in range(len(selected_item)):
                inv[turn][i] += selected_item[i]
        if buyShop == False:
            easygui.msgbox(f"[how to earn money]", "Money")

    elif walkPos[turn] == 24: # check if at space 24
        extraX, extraY = baseExtra[turn]
        player_x = 855 + extraX
        player_y = 30 + extraY
        screen.blit(characterImages[turn], (player_x, player_y))
        pygame.display.flip()
        if day == True:
            easygui.msgbox(f"Congratulations! You won [AMOUNT] gold!", "YOU FOUND GOLD!")
        else:
            easygui.msgbox(f"Oh no you have been robbed, they took [AMOUNT] gold!", "YOU GOT ROBBED!")
        pygame.event.clear()
        
    
    elif walkPos[turn] == 32: # check if at space 32
        extraX, extraY = baseExtra[turn]
        player_x = 855 + extraX
        player_y = 820 + extraY
        screen.blit(characterImages[turn], (player_x, player_y))
        pygame.display.flip()
    pygame.event.clear()

# Check special space with final pos
def specialCheckPos(turn):
    if position[turn] in shopSpace:
        buyShop = easygui.ynbox(f"Welcome to the shop! \nDo you want to buy something or make some money player {turn + 1}?", "[WHAT KIND OF] shop", ["Buy something", "Make money"])
        if buyShop == True:
            options = random.sample(shop2, 3)
            option1, = options[0].keys()
            option2, = options[1].keys()
            option3, = options[2].keys()
            bought = easygui.buttonbox(f"Welcome to the shop! \nWhat do you want to buy? player {turn + 1}?", "[WHAT KIND OF] shop", [option1, option2, option3])
            for item in shop2:
                if bought in item:
                    selected_item = item[bought]
                    selected_item = list(selected_item)
                    break
            for i in range(len(selected_item)):
                inv[turn][i] += selected_item[i]
        if buyShop == False:
            easygui.msgbox(f"[how to earn money]", "Money")


    if position[turn] in clueSpace:
        buyClue = easygui.ynbox(f"Do you want to buy a clue player {turn + 1}?", "Buy a clue?", ["Yes", "No"])
        if buyClue == True:
            message = clues[random.choice([DamageType, ShieldType])]
            easygui.msgbox(message, "Your special clue")

    if position[turn] in stationSpace:
        if firstLap == True:
            travel = easygui.ynbox(f"Do you want to travel to another station player {turn + 1}?", "Travel the world", ["Yes", "No"])
            if travel == True:
                travelLocation = easygui.buttonbox("Where do you want to travel?", "Travel location", list(locations))
                walkPos[turn] = locations[travelLocation]
                position[turn] = locations[travelLocation]
                updateScreen()
                pygame.display.flip()
        else:
            easygui.msgbox("The train has not not arrived yet", "An empty station")

    pygame.event.clear()
            

#----- Global variables -----#

# Amount of players
players = 0

# Space cords
spaces = [[820,820],
[728,820],[639,820],[549,820],[460,820],[370,820],[280,820],[190,820],
[30,820],
[30,726],[30,639],[30,549],[30,459],[30,371],[30,281],[30,191],
[30,30],
[190,30],[280,30],[370,30],[460,30],[548,30],[638,30],[728,30],
[820,30],
[820,190],[820,280],[820,370],[820,460],[820,548],[820,638],[820,725]]

# Special spaces
shopSpace = [1,3,6,9,13,15,18,21,23,25,26,29]
clueSpace = [2,10,17,30]
stationSpace = [4,12,20,28]
goldSpace = [5,11,14,19,27,31]
stealSpace = [7,22]

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

# Has someone made a full lap yet?
firstLap = False

# Background fill
timeColor = 200,180,160
textColor = 65,60,50
highlighColor = 0,0,0

# Travel locations
locations = {"Station 1": 4,"Station 2": 12,"Station 3": 20,"Station 4": 28,}

# Board image
boardDay = pygame.image.load("Foto's\BoardDay.png")
boardNight = pygame.image.load("Foto's\BoardNight.png")
boardSize = (1000,1000)
boardDay = pygame.transform.scale(boardDay, boardSize)
boardNight = pygame.transform.scale(boardNight, boardSize)

# Character images
character1 = pygame.image.load("Foto's\Character1.png") 
character2 = pygame.image.load("Foto's\Character2.png")
character3 = pygame.image.load("Foto's\Character3.png")
character4 = pygame.image.load("Foto's\Character4.png")
character5 = pygame.image.load("Foto's\Character5.png")
character6 = pygame.image.load("Foto's\Character6.png")
character7 = pygame.image.load("Foto's\Character7.png")
character8 = pygame.image.load("Foto's\Character8.png")
characterImages = [character1, character2, character3, character4, character5, character6, character7, character8]


# Character distribution
baseExtra = [(0,5),(37,5),(0,42),(37,42),(0,79),(37,79),(0,116),(37,116)]

# Items/inventory (First digit = Attack damage, second = Magic damage, third = armor and fourth = magic shield)
inv = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

# Check movement
walking = False

# Player gold
gold = [0,0,0,0,0,0,0,0]

# Shop items
shop1 = [{"Basic sword": (3,0,0,0)}, {"Basic wand": (0,3,0,0)}, {"Basic armor": (0,0,2,0)}, {"Basic magic shield": (0,0,0,2)}]
shop2 = [{"Epic sword": (7,0,0,0)}, {"Epic wand": (0,7,0,0)}, {"Epic armor": (0,0,5,0)}, {"Epic magic shield": (0,0,0,5)}]
shop3 = [{"Legendary sword": (12,0,0,0)}, {"Legendary wand": (0,12,0,0)}, {"Legendary armor": (0,0,8,0)}, {"Legendary magic shield": (0,0,0,8)}]

# Boss clues
clues = {
    "AD": "The boss deals Attack Damage",
    "MD": "The boss deals Magic Damage",
    "AP": "The boss has Attack Protection",
    "MP": "The boss has Magic Protection"
}

# Boss decide
DamageType = random.choice(["AD","MD"])
ShieldType = random.choice(["AP","MP"])

# Formulas
# playerDamage = (player attack damage - boss armor) + (player magic damage - boss magic protection)
# bossDamage = (boss attack damage - player armor) + (boss magic damage - player magic protection)
# playerHealth -= bossDamage

# Leaderboard player cords
leaderboardCords = [(205, 205), (205, 282.5), (205, 360), (205, 437.5), (205, 515), (205, 592.5), (205, 670), (205, 747.5)]

# The cords for where the higlight should be
highlightCords = [(200, 200), (200, 277.5), (200, 355), (200, 432.5), (200, 510), (200, 587.5), (200, 665), (200, 742.5)]

# Opacity of the highlight

#----- Start menu -----#

try:
    players = int(easygui.buttonbox("Choose player count", "Amount of players", str(12345678)))
except TypeError:
    done = True
    pygame.quit()

else:
    msg = easygui.msgbox(f"Amount of players selected : {players}\nLets go!", "Selected player count")
    done = False

#----- Pygame initialisation -----#

if not done:
# Initialise Pygame
    pygame.init()

    # Screen size
    WINDOW_SIZE = [1900,1000]

    # Create screen
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Screen title
    pygame.display.set_caption("GAME NAME")

    # Clock setup
    clock = pygame.time.Clock()


#----- Main program ----#

while not done:
    
    if rounds < 3:

    #--- Check activities (mouseclicks, button presses etc.) ---#

        if day == True:
            board = boardDay
            timeColor = 200,180,160
            textColor = 65,60,50
            highlighColor = 0,0,0

        else:
            board = boardNight
            timeColor = 45,40,35
            textColor = 200,175,150
            highlighColor = 255,255,255
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Execute keypress
                if event.key == pygame.K_SPACE:
                    throw = random.randint(1,6)
                    if throw > 0:
                        walking = True
                    position[turn] += throw

                    if position[turn] > 31:
                        position[turn] -= 32      
                    if not firstLap == True:
                        firstLap == True      

                elif event.key == pygame.K_e:
                    powerupturn = inv[turn]
                    powerup = easygui.msgbox(f"You have {str(inv[turn][0])} attack damge, {str(inv[turn][1])} magic damage, {str(inv[turn][2])} armor and {str(inv[turn][3])} magic protection.", "Stats")
                    pygame.event.clear()

        #--- Draw/update graphics ---#

        if walking != True:
            updateScreen()
        else:
            for i in range(throw):
                walkPos[turn] += 1
                if walkPos[turn] > 31:
                    walkPos[turn] -= 32  
                specialCheckWalk(turn)
                updateScreen()
                pygame.display.flip()
                time.sleep(0.2)
            walking = False
            specialCheckPos(turn)
            
            # Switch turns
            if turn < (players - 1):
                turn += 1
            else:
                turn = 0
                rounds += 1
                if day == True:
                    day = False
                    easygui.msgbox(f"Its getting dark outside...", "Whats happening?")
                else:
                    day = True
                    easygui.msgbox(f"Whats that light?", "Whats happening?")
                pygame.event.clear()
    
    else:
        for i in range(players):
            print(inv[i])
            done = True

    # Refresh screen
    updateScreen()
    clock.tick(60)
    pygame.display.flip()


#----- Quit -----#
pygame.quit()
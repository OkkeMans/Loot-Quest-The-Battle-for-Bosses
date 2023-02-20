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

# Check special space with walking
def specialCheckWalk(turn):
    
    if walkPos[turn] == 8: # check if at space 8
        updateScreen()
        extraX, extraY = baseExtra[turn]
        player_x = 65 + extraX
        player_y = 30 + extraY
        screen.blit(characterImages[turn], (player_x, player_y))
        pygame.display.flip()
    
    elif walkPos[turn] == 16: # check at space 16
        updateScreen()
        extraX, extraY = baseExtra[turn]
        player_x = 65 + extraX
        player_y = 30 + extraY
        screen.blit(characterImages[turn], (player_x, player_y))
        pygame.display.flip()
        starbuy = easygui.ynbox(f"Do you want to buy a star player {turn + 1}?", "You found a star!", ["Yes", "No"])

    elif walkPos[turn] == 24: # check if at space 24
        updateScreen()
        extraX, extraY = baseExtra[turn]
        player_x = 65 + extraX
        player_y = 30 + extraY
        screen.blit(characterImages[turn], (player_x, player_y))
        pygame.display.flip()
    
    elif walkPos[turn] == 32: # check if at space 32
        updateScreen()
        extraX, extraY = baseExtra[turn]
        player_x = 65 + extraX
        player_y = 30 + extraY
        screen.blit(characterImages[turn], (player_x, player_y))
        pygame.display.flip()
    pygame.event.clear()

# Check special space with final pos
def specialCheckPos(turn):
    if position[turn] == 4 or position[turn] == 12 or position[turn] == 20 or position[turn] == 28 and 1 in inv[turn]:
        travel = easygui.ynbox(f"Do you want to travel to another station player {turn + 1}?", "Travel the world", ["Yes", "No"])
        if travel == True:
            travelLocation = easygui.buttonbox("Where do you want to travel?", "Travel location", list(locations))
            walkPos[turn] = locations[travelLocation]
            position[turn] = locations[travelLocation]
            updateScreen()
            pygame.display.flip()

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

# Background fill
timeColor = 255,255,255

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

# Items/inventory
inv = [[],[],[],[],[],[],[],[]]

# Check movement
walking = False

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
    
    if rounds < 10:

        #--- Check activities (mouseclicks, button presses etc.) ---#

        if day == True:
            board = boardDay
            timeColor = 255,255,255
        else:
            board = boardNight
            timeColor = 0,0,0
            
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

                elif event.key == pygame.K_e:
                    powerupturn = inv[turn]
                    powerup = easygui.buttonbox(f"What powerup do you want to use player {turn + 1}?", "Powerups", powerupturn)
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
                pygame.event.clear()

                updateScreen()
                pygame.display.flip()
                time.sleep(0.2)
            walking = False
            specialCheckPos(turn)
            pygame.event.clear()
            
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
    

    # Draw text
    # font = pygame.font.Font("SuperMario256.ttf", 30)
    # Show last throw
    # TODO: Do you want this in your game   ?

    # Show current player
    # text = (f"Current player {turn}")
    # label = font.render(text,1,(0,0,0))
    # #FIXME:
    # screen.blit(label, (X,Y))

    # Refresh screen
    else:
        "Fight"

    updateScreen()
    clock.tick(60)
    pygame.display.flip()


#----- Quit -----#
pygame.quit()
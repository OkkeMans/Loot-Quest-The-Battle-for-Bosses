import pygame, easygui, random, time
from PIL import *

#----- Functions -----#

# Refresh text on screen
def updateText(screen, timeColor, board, throw, textColor, highlightColor, highlightCords, turn, players, inv, gold, leaderboardCords, trainTicket, ticketCords, ticketImage):
    
    # Set board
    screen.fill(timeColor)
    boardrect = board.get_rect()
    screen.blit(board, boardrect)

    # Draw text
    font = pygame.font.Font("Bijlagen\LuckiestGuy-Regular.ttf", 50)
    
    # Show last throw
    text = (f"Last throw: {throw}")
    label = font.render(text,True,(textColor))
    screen.blit(label,(1000,20))
    
    # Highlight current player
    highlight = pygame.Surface((612,55))
    highlight.set_alpha(30)
    highlight.fill((highlightColor))
    screen.blit(highlight, ((highlightCords[turn])))
    
    # Show playerlist (Inventory + Gold)
    for i in range(players):
        text = (f"Player {i + 1} {inv[i]} {gold[i]}")
        label = font.render(text,True,(textColor))
        screen.blit(label,(leaderboardCords[i]))
        if trainTicket[i]:
            screen.blit(ticketImage, (ticketCords[i]))

# Refresh player positions
def updatePositions(players, walkPos, baseExtra, spaces, screen, characterImages):
    
    # Calculate player offset
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
def specialCheckWalk(walkPos, turn, gamblerOptions, shopE, shopL, gold, inv, day, firstLap, chooseThrow, gambleSkip, legendaryAccess):
    
    if walkPos[turn] == 8: # check if at space 8
        gambling = easygui.ynbox("Welcome to the gambler, do you want to play a game?", "THE GAMBLER", ["Yes", "No"])
        if gambling:
        # Define a dictionary mapping messages to actions
            actions = {
                0: lambda: inv[turn].__setitem__(0, inv[turn][0] + 7),
                1: lambda: inv[turn].__setitem__(1, inv[turn][1] + 7),
                2: lambda: inv[turn].__setitem__(2, inv[turn][2] + 5),
                3: lambda: inv[turn].__setitem__(3, inv[turn][3] + 5),
                4: lambda: gold.__setitem__(turn, gold[turn] + 500),
                5: lambda: gold.__setitem__(turn, gold[turn] - 500),
                6: lambda: (inv[turn].__setitem__(0, inv[turn][1]), inv[turn].__setitem__(1, inv[turn][0])),
                7: lambda: (inv[turn].__setitem__(2, inv[turn][3]), inv[turn].__setitem__(3, inv[turn][2])),
                8: lambda: chooseThrow.__setitem__(turn, True),
                9: lambda: gambleSkip.__setitem__(turn, True),
                10: lambda: legendaryAccess.__setitem__(turn, True),
            }

            # Generate a random message and execute its corresponding action
            gamble = random.randint(0,10)
            easygui.msgbox(gamblerOptions[gamble])
            actions[gamble]()

    elif walkPos[turn] == 16: # check if at space 16
        if legendaryAccess[turn]:
            buyShop = easygui.buttonbox(f"Welcome to the shop! \nDo you want to buy something player {turn + 1}?", "LEGENDARY SHOP", ["Yes", "No"])
            if buyShop == "Yes":
                options = random.sample(shopL, 3)
                option1, = options[0].keys()
                option2, = options[1].keys()
                option3, = options[2].keys()
                bought = easygui.buttonbox(f"Welcome to the shop! \nWhat do you want to buy? player {turn + 1}?", "LEGENDARY SHOP", [option1, option2, option3])
                for item in shopL:
                    if bought in item:
                        itemValue = item[bought][0]
                        itemValue = list(itemValue)
                        break
                for price in shopL:
                    if bought in price:
                        itemPrice = price[bought][1]
                        break
                try:
                    if gold[turn] >= itemPrice:
                            for i in range(len(itemValue)):
                                inv[turn][i] += itemValue[i] 
                            gold[turn] -= itemPrice
                    else:
                        easygui.msgbox("You dont have enough gold to buy this item right now.", "L", "Continue")
                except UnboundLocalError:
                    pass

        else:
            buyShop = easygui.buttonbox(f"Welcome to the shop! \nDo you want to buy something player {turn + 1}?", "EPIC SHOP", ["Yes", "No"])
            if buyShop == "Yes":
                options = random.sample(shopE, 3)
                option1, = options[0].keys()
                option2, = options[1].keys()
                option3, = options[2].keys()
                bought = easygui.buttonbox(f"Welcome to the shop! \nWhat do you want to buy? player {turn + 1}?", "EPIC SHOP", [option1, option2, option3])
                for item in shopE:
                    if bought in item:
                        itemValue = item[bought][0]
                        itemValue = list(itemValue)
                        break
                for price in shopE:
                    if bought in price:
                        itemPrice = price[bought][1]
                        break
                try:
                    if gold[turn] >= itemPrice:
                            for i in range(len(itemValue)):
                                inv[turn][i] += itemValue[i] 
                            gold[turn] -= itemPrice
                    else:
                        easygui.msgbox("You dont have enough gold to buy this item right now.", "L", "Continue")
                except UnboundLocalError:
                            easygui.msgbox("You left the shop withouth buying anything, how could you!? The shopkeeper demands 200 gold", "Left without buying?", "Continue")
                            gold[turn] -= 200

    elif walkPos[turn] == 24: # check if at space 24
        if day:
            easygui.msgbox("Congratulations! You won 400 gold!", "YOU FOUND GOLD!", "COLLECT GOLD")
            gold[turn] += 400
        else:
            if not firstLap:
                easygui.msgbox("Oh no you have been robbed, they took 350 gold!", "YOU GOT ROBBED!", "HAND OVER GOLD")
                gold[turn] -= 350
            else:
                easygui.msgbox("They tried to rob you but you were able to escape, you got lucky", "YOU GOT OUT!", "HIDE")
    
    pygame.event.clear()

# Check special space with final pos
def specialCheckPos(position, turn, shopSpace, shopB, gold, inv, clueSpace, clues, damageType, shieldType, stationSpace, trainTicket, firstLap, locations, walkPos, goldSpace, swapSpace, playerlist,):
    
    if position[turn] in shopSpace:
        buyShop = easygui.buttonbox(f"Welcome to the shop! \nDo you want to buy something or gather some gold player {turn + 1}?", "STANDARD SHOP", ["Buy something", "Gather gold"])
        if buyShop == "Buy something":
            options = random.sample(shopB, 3)
            option1, = options[0].keys()
            option2, = options[1].keys()
            option3, = options[2].keys()
            bought = easygui.buttonbox(f"Welcome to the shop! \nWhat do you want to buy? player {turn + 1}?", "STANDARD SHOP", [option1, option2, option3])
            for item in shopB:
                if bought in item:
                    itemValue = item[bought][0]
                    itemValue = list(itemValue)
                    break
            for price in shopB:
                if bought in price:
                    itemPrice = price[bought][1]
                    break
            try:
                if gold[turn] >= itemPrice:
                        for i in range(len(itemValue)):
                            inv[turn][i] += itemValue[i] 
                        gold[turn] -= itemPrice
                else:
                    easygui.msgbox("You dont have enough gold to buy this item right now.", "L", "Continue")
            except UnboundLocalError:
                        easygui.msgbox("You left the shop withouth buying anything, how could you!? The shopkeeper demands 200 gold", "Left without buying?", "Continue")
                        gold[turn] -= 200

        if buyShop == "Gather gold":
            easygui.msgbox(f"You got 250 gold for helping at the shop", "GOLD", "COLLECT GOLD")
            gold[turn] += 250


    if position[turn] in clueSpace:
        buyClue = easygui.ynbox(f"Do you want to buy a clue player {turn + 1}?", "Buy a clue?", ["Yes", "No"])
        if buyClue:
            if gold[turn] >= 800:
                message = clues[random.choice([damageType, shieldType])]
                gold[turn] -= 800
                easygui.msgbox("Make sure nobody is looking!", "YOUR SPECIAL CLUE", "Continue")
                easygui.msgbox(message, "YOUR SPECIAL CLUE", "Continue")
            else:
                easygui.msgbox("You dont have enough gold to buy a clue", "L", "Continue")


    if position[turn] in stationSpace:
        if not firstLap:
            if not trainTicket[turn]:
                buyTicket = easygui.ynbox(f"Do you want to buy a train ticket player {turn + 1}?", "BUY A TICKET", ["Yes", "No"])
                if buyTicket and gold[turn] >= 750:
                    gold[turn] -= 750
                    trainTicket[turn] = True
                elif buyTicket and gold[turn] < 750:
                    easygui.msgbox("You dont have enough gold to buy this item right now.", "L", "Continue")
            else:
                travel = easygui.ynbox(f"Do you want to travel to another station player {turn + 1}?", "TRAVEL THE WORLD", ["Yes", "No"])
                if travel:
                    travelLocation = easygui.buttonbox("Where do you want to travel?", "TRAVEL LOCATION", list(locations))
                    walkPos[turn] = locations[travelLocation]
                    position[turn] = locations[travelLocation]
        else:
            if not trainTicket[turn]:
                buyTicket = easygui.ynbox(f"The train has not arrived yet, do you want to buy a ticket player {turn + 1}?", "BUY A TICKET", ["Yes", "No"])
                if buyTicket and gold[turn] >= 600:
                    gold[turn] -= 750
                    trainTicket[turn] = True
                elif buyTicket and gold[turn] < 600:
                    easygui.msgbox("You dont have enough gold to buy this item right now.", "L", "Continue")
            else:
                easygui.msgbox("The train has not not arrived yet", "AN EMPTY STATION", "Continue")
    if position[turn] in goldSpace:
        easygui.msgbox("You found 600 gold!", "YOU FOUND GOLD!", "COLLECT GOLD")
        gold[turn] += 600

    if position[turn] in swapSpace:
        switchplayer = int(easygui.buttonbox("Choose a player to switch gold with", "SWITCH GOLD", (playerlist)))
        transfer1 = (gold[turn])
        transfer2 = (gold[(switchplayer - 1)])
        gold[turn] = transfer2
        gold[int(switchplayer - 1)] = transfer1

    pygame.event.clear()

def story():
    easygui.msgbox("Story", "THE STORY OF THE CURSED TOWN", "Exit")
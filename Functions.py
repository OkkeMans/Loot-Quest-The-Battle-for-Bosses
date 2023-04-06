import pygame, easygui, random, time
from PIL import *

#----- Functions -----#

# Refresh text on screen
def updateText(screen, timeColor, board, throw, textColor, highlightColor, highlightCords, turn, players, inv, gold, leaderboardCords, trainTicket, ticketCords, ticketImage):
    
    screen.fill(timeColor)

    boardrect = board.get_rect()
    screen.blit(board, boardrect)

    # Draw text
    font = pygame.font.Font("Bijlagen\LuckiestGuy-Regular.ttf", 50)
    
    # Show last throw
    text = (f"Last throw: {throw}")
    label = font.render(text,True,(textColor))
    screen.blit(label,(1000,20))
    
    highlight = pygame.Surface((612,55))
    highlight.set_alpha(30)
    highlight.fill((highlightColor))
    screen.blit(highlight, ((highlightCords[turn])))
    
    for i in range(players):
        text = (f"Player {i + 1} {inv[i]} {gold[i]}")
        label = font.render(text,True,(textColor))
        screen.blit(label,(leaderboardCords[i]))
        if trainTicket[i]:
            screen.blit(ticketImage, (ticketCords[i]))

# Refresh player positions
def updatePositions(players, walkPos, baseExtra, spaces, screen, characterImages):
    
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
def specialCheckWalk(walkPos, turn, gamblerOptions, shop1, gold, inv, day, firstLap, chooseThrow, gambleSkip):
    
    if walkPos[turn] == 8: # check if at space 8
        gambling = easygui.ynbox("Welcome to the gambler, do you want to play a game?", "The gambler", ["Yes", "No"])
        if gambling:
            message = random.randint(0,9)
            easygui.msgbox(gamblerOptions[message])
            if message == 0:
                inv[turn][0] += 7
            elif message == 1:
                inv[turn][1] += 7
            elif message == 2:
                inv[turn][2] += 5
            elif message == 3:
                inv[turn][3] += 5
            elif message == 4:
                gold[turn] += 500
            elif message == 5:
                gold[turn] -= 500
            elif message == 6:
                temp = inv[turn][0]
                inv[turn][0] = inv[turn][1]
                inv[turn][1] = temp
            elif message == 7:
                temp = inv[turn][2]
                inv[turn][2] = inv[turn][3]
                inv[turn][3] = temp
            elif message == 8:
                chooseThrow[turn] = True
            elif message == 9:
                gambleSkip[turn] = True

    elif walkPos[turn] == 16: # check if at space 16
        buyShop = easygui.buttonbox(f"Welcome to the shop! \nDo you want to buy something player {turn + 1}?", "Standard shop", ["Yes", "No"])
        if buyShop == "Yes":
            options = random.sample(shop1, 3)
            option1, = options[0].keys()
            option2, = options[1].keys()
            option3, = options[2].keys()
            bought = easygui.buttonbox(f"Welcome to the shop! \nWhat do you want to buy? player {turn + 1}?", "Standard shop", [option1, option2, option3])
            for item in shop1:
                if bought in item:
                    itemValue = item[bought][0]
                    itemValue = list(itemValue)
                    break
            for price in shop1:
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
    
    # elif walkPos[turn] == 32: # check if at space 32
    pygame.event.clear()

# Check special space with final pos
def specialCheckPos(position, turn, shopSpace, shop2, gold, inv, clueSpace, clues, damageType, shieldType, stationSpace, trainTicket, firstLap, locations, walkPos, goldSpace, swapSpace, playerlist,):
    
    if position[turn] in shopSpace:
        buyShop = easygui.buttonbox(f"Welcome to the shop! \nDo you want to buy something or gather some gold player {turn + 1}?", "Epic shop", ["Buy something", "Gather gold"])
        if buyShop == "Buy something":
            options = random.sample(shop2, 3)
            option1, = options[0].keys()
            option2, = options[1].keys()
            option3, = options[2].keys()
            bought = easygui.buttonbox(f"Welcome to the shop! \nWhat do you want to buy? player {turn + 1}?", "Epic shop", [option1, option2, option3])
            for item in shop2:
                if bought in item:
                    itemValue = item[bought][0]
                    itemValue = list(itemValue)
                    break
            for price in shop2:
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
            easygui.msgbox(f"You got 250 gold for helping at the shop", "Gold", "COLLECT GOLD")
            gold[turn] += 250


    if position[turn] in clueSpace:
        buyClue = easygui.ynbox(f"Do you want to buy a clue player {turn + 1}?", "Buy a clue?", ["Yes", "No"])
        if buyClue:
            if gold[turn] >= 1000:
                message = clues[random.choice([damageType, shieldType])]
                gold[turn] -= 1000
                easygui.msgbox("Make sure nobody is looking!", "Your special clue", "Continue")
                easygui.msgbox(message, "Your special clue", "Continue")
            else:
                easygui.msgbox("You dont have enough gold to buy a clue", "L", "Continue")


    if position[turn] in stationSpace:
        if not firstLap:
            if not trainTicket[turn]:
                buyTicket = easygui.ynbox(f"Do you want to buy a train ticket player {turn + 1}?", "Buy a ticket", ["Yes", "No"])
                if buyTicket and gold[turn] >= 750:
                    gold[turn] -= 750
                    trainTicket[turn] = True
                elif buyTicket and gold[turn] < 750:
                    easygui.msgbox("You dont have enough gold to buy this item right now.", "L", "Continue")
            else:
                travel = easygui.ynbox(f"Do you want to travel to another station player {turn + 1}?", "Travel the world", ["Yes", "No"])
                if travel:
                    travelLocation = easygui.buttonbox("Where do you want to travel?", "Travel location", list(locations))
                    walkPos[turn] = locations[travelLocation]
                    position[turn] = locations[travelLocation]
        else:
            if not trainTicket[turn]:
                buyTicket = easygui.ynbox(f"The train has not arrived yet, do you want to buy a ticket player {turn + 1}?", "Buy a ticket", ["Yes", "No"])
                if buyTicket and gold[turn] >= 750:
                    gold[turn] -= 750
                    trainTicket[turn] = True
                elif buyTicket and gold[turn] < 750:
                    easygui.msgbox("You dont have enough gold to buy this item right now.", "L", "Continue")
            else:
                easygui.msgbox("The train has not not arrived yet", "An empty station", "Continue")
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
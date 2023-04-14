import pygame, easygui, random, time
from PIL import *

#----- Functions -----#
def ending(players, inv, bossStats, health, bossHealth, damage, skippedTurns, screen, bossType, playerlist):
    while len(skippedTurns) != players:
        for i in range (players):
            if not i in skippedTurns:
                playerDamage = max((inv[i][0] - bossStats[2]) + (inv[i][1] - bossStats[3]), 0)
                bossDamage = max((bossStats[0] - inv[i][2]) + (bossStats[1] - inv[i][3]), 0)
                health[i] -= bossDamage
                bossHealth -= playerDamage
                damage[i] += playerDamage
                if health[i] <= 0:
                    skippedTurns.append(i)
    if bossHealth <= 0:
        bossKilled = True
    elif len(skippedTurns) == players:
        bossKilled = False
    winners = []
    highest_damage = max(damage)
    for i, val in enumerate(damage):
        if val == highest_damage:
            winners.append(str(i + 1))
    for i in skippedTurns:
        skippedTurns[i] += 1

    pygame.display.set_caption("THE CURSED TOWN - Ending")
    screen.fill((255,255,255))
    boardADAP = pygame.image.load("Bijlagen\ADAP.jpg")
    boardADMP = pygame.image.load("Bijlagen\ADMP.jpg")
    boardMDAP = pygame.image.load("Bijlagen\MDAP.jpg")
    boardMDMP = pygame.image.load("Bijlagen\MDMP.jpg")
    if bossType == "ADAP":
        board = boardADAP
    elif bossType == "ADMP":
        board = boardADMP
    elif bossType == "MDAP":
        board = boardMDAP
    elif bossType == "MDMP":
        board = boardMDMP
    boardrect = board.get_rect()
    screen.blit(board, boardrect)
    pygame.display.flip()
    remainingPlayers = (', '.join(playerlist))
    lostPlayers = map(str, skippedTurns)
    lostPlayers = (', '.join(lostPlayers))
    easygui.msgbox(f"It's time to fight the boss, only players {remainingPlayers} are remaining. Lets see if they are able to kill the boss", "TIME TO FIGHT", "Continue")
    for i in range (8):
        screen.fill((255,255,255))
        pygame.display.flip()
        time.sleep(0.1)
        screen.fill((0,0,0))
        pygame.display.flip()
        time.sleep(0.1)

    if bossKilled:
        easygui.msgbox("You have managed to defeat the boss! Congratulations!!", "THE BOSS IS DEAD", "Continue")
    else:
        easygui.msgbox("Unfortunately we lost all of our players before and in the fight against the boss", "THE BOSS SURVIVED", "Continue")
    
    easygui.msgbox("But who dealt the most damage to the boss and won the game?", "WHO WINS?", "Continue")
    if len(skippedTurns) > 0:
        easygui.msgbox(f"These are the players that we lost before and in the fight: \n{lostPlayers}", "YOU WILL BE REMEMBERED", "F")
    else:
        easygui.msgbox("All players managed to survive!", "EVERYONE IS HERE", "Continue")
    
    easygui.msgbox("The player that dealt the most damage to the boss,", "*drumroll*", "Continue")
    easygui.msgbox("is,", "*drumroll*", "Continue")
    if len(winners) > 1:
        winnersStr = (', '.join(winners))
        easygui.msgbox(f"oh, wait. 2 or more players dealt the exact same amount of damage to the boss!?", "A TIE!?", "Continue")
        if max(damage) == 0:
            easygui.msgbox(f"Even worse, no one did any damage to the boss! Everyone died withouth doing anything", "lmao bozo's", "End game")
        else:
            easygui.msgbox(f"These players have dealt the same amount of damage to the boss, and won the game together! \n{winnersStr}", "A TIE!?", "End game")
    else:
        winners = (', '.join(winners))
        easygui.msgbox(f"PLAYER {winners} HAS DEALT THE MOST DAMAGE AGAINST THE BOSS AND HAS WON THE GAME", f"PLAYER {winnersStr} WINS!", "End game")
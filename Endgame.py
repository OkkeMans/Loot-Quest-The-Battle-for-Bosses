import pygame, easygui, random, time
from PIL import *

#----- Functions -----#
def calculateDamage(players, inv, bossStats, health, bossHealth, damage, skippedTurns):
    for i in range (players):
        if not i in skippedTurns:
            playerDamage = (inv[i][0] - bossStats[2]) + (inv[i][1] - bossStats[3])
            bossDamage = (bossStats[0] - inv[i][2]) + (bossStats[1] - inv[i][3])
            health[i] -= bossDamage
            bossHealth -= playerDamage
            damage[i] += playerDamage
            if health[i] <= 0:
                skippedTurns.append(i)
    if bossHealth <= 0:
        bossKilled = True
    elif len(skippedTurns) == players:
        playersKilled = True
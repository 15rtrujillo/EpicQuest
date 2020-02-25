# Epic Quest: Text Quest
# Python ALPHA Version 0.2
from time import sleep
from random import randint

class Player:
    """Holds all the data for the current player. Can also be used to create
        enemy players."""

    def __init__(self):
        """Sets all the values to their default. These can be changed with
            setStats() and load() methods."""
        self.name = ""
        self.gold = 100
        self.hp = 100
        self.maxhp = 100
        self.lvl = 1
        self.xp = 0
        self.loc = "Falconwood"
        self.house = False

    def load(self, name):
        """Attempts to load a file with the name provided by the user.
            Reads the stats from the file, and then applies them to the
            player."""
        try:
            saveFile = open(name + ".eq", "r")
            stats = []
            for line in saveFile:
                stat = line[line.find('=')+1:]
                stats.append(stat[:-1])
            self.name = stats[0]
            self.gold = int(stats[1])
            self.hp = int(stats[2])
            self.maxhp = int(stats[3])
            self.lvl = int(stats[4])
            self.xp = int(stats[5])
            self.loc = stats[6]
            self.house = toBool(stats[7])
            saveFile.close()
            return True
        except Exception as ex:
            return False

    def save(self):
        """Saves the player's stats to a file called \"[playername].eq.\""""
        saveFile = open(self.name + ".eq", "w")
        stats = [
            "name="+self.name,
            "gold="+str(self.gold),
            "hp="+str(self.hp),
            "maxhp="+str(self.maxhp),
            "lvl="+str(self.lvl),
            "xp="+str(self.xp),
            "loc="+str(self.loc),
            "house="+str(self.house)]
        try:
            for stat in stats:
                print(stat, file=saveFile)
            saveFile.close()
            return True
        except Exception as ex:
            return False

    def setStats(self, name, gold, hp, maxhp, lvl):
        """This is used for creating enemy players. Maybe if I implement a duel
            arena one day."""
        pass

class Enemy:
    "This is an enemy object that the player will fight."

    def __init__(self, name, level, maxhp, weapon, damage):
        """Creates a new enemy with the given name and level and gives him a
        weapon that does the specified damage."""
        self.name = name
        self.level = int(level)
        self.maxhp = int(maxhp)
        self.hp = self.maxhp
        self.weapon = weapon
        self.damage = int(damage)

    def attack(self):
        "Calculates the damage delt by this enemy."
        pass

    def damage(self, damage):
        "Deals damage to this enemy and returns the new hp value."
        self.hp -= damage
        return self.hp

### START ###
player = Player()
version = "Python ALPHA Version 0.2"

def main():
    print("Welcome to Epic Quest: Text Quest, the Python game.")
    pause()
    if startMenu():
        while mainMenu():
            pass
    print("\nThank you for playing Epic Quest: Text Quest.")
    pause()
    ## CHANGE TO EXIT
    clearScreen()

def startMenu():
    while True:
        clearScreen()
        print("Epic Quest: Text Quest")
        print(version)
        print("\nPlease Select an Option:")
        createMenu(
            "New Game",
            "Load Game",
            "About the Game",
            "Change Log",
            "Exit")
        c = getChoice(5)
        
        if c == "1":
            if newGame():
                return True
            
        elif c == "2":
            if loadGame():
                return True
            
        elif c == "3":
            about()
            
        elif c == "4":
            changeLog()
            
        elif c == "5":
            if yesOrNo("Are you sure you want to quit?"):
                return False

        else:
            clearScreen()
            print("\n\n***FATAL ERROR, TERMINATING***\n\n")
            sleep(2)
            exit()

def newGame():
    while True:
        clearScreen()
        print("New Game\n")
        name = input("Please enter the name of your character ('C' to cancel): ")
        if name.lower() == "c":
            return False
        if yesOrNo("Are you sure you want to create a new character named " + name + "?"):
            # story()
            player.name = name
            player.save()
            return True

def story():
    pass

def loadGame():
    while True:
        clearScreen()
        print("Load Game\n")
        fileName = input("Please enter the name of the character " +
                     "you'd like to load ('C' to cancel): ")
        
        if player.load(fileName):
            print("\nCharacter " + fileName + " loaded successfully!")
            pause()
            return True
        else:
            if fileName.lower() == "c":
                return False
            else:
                print("\nThere was no character found by the name " + fileName +
                      ".\nPlease try again")
                pause()
    
            
def about():
    clearScreen()
    print("Epic Quest: Text Quest")
    print(version)
    print("Made by Ryan\n")
    print("Based off Epic Quest: Quest for Epicness, the\ncomputer",
          "role-playing game by the same author.\n")
    print("Copyright (C) RyGuyGames Inc. All rights reserved.")
    pause()

def changeLog():
    clearScreen()
    print("Epic Quest: Text Quest")
    print(version + "\n")
    print("Change Log:")
    print("* Fixed a bug that broke saving that popped up while migrating to the new\n" +
          "engine.")
    print("* Added save and load menus.")
    print("* Added this screen.")
    print("* Reworked the way the player's data is stored,\n"
          "allowing for a possible future duel arena where you\n"
          "can duel other players saved on the same computer.\n"
          "More details to come.")
    print("* Added more descriptions to the environment.\n"
          "Going to focus more on the story in the future.")
    print("* Rewrote basically the entire engine.\n"
          "(Yes, this game has an engine.)")
    print("* Fixed a bug where the game would begin to slow\n"
          "down the longer you played.")
    pause()


def mainMenu():
    pass

### HELPER FUNCTIONS ###
def pause():
    input("\nPress [ENTER] to continue...")

def clearScreen():
    for i in range(50):
        print()

def createMenu(*args):
    for i in range(0, len(args)):
        print(str(i+1) + ".", args[i])

def getChoice(numberOfChoices, question="Your Choice: "):
    while True:
        c = input('\n' + question)
        try:
            if int(c) in range(numberOfChoices+1):
                return c
            else:
                print("\nPlease select an option from the menu.")
                pause()
        except:
            print("\nPlease select an option from the menu.")
            pause()

def yesOrNo(question):
    while True:
        c = input('\n' + question + " [Y/N]: ")
        if c.lower() == "y":
            return True
        elif c.lower() == "n":
            return False
        else:
            print("\nPlease type either 'Y' or 'N' to make your selection.\n")

def toBool(value):
    return value.lower() in ["true"]


main()

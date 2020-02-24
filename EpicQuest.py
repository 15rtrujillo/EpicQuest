# Epic Quest: Text Quest
# Python ALPHA Version 0.1
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
        except:
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
            "loc="+self.loc,
            "house="+str(self.house)]
        try:
            for stat in stats:
                print(stat, file=saveFile)
                saveFile.close()
                return True
        except:
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
    

player = Player()
version = "Python ALPHA Version 0.1"

def start():
    print("Welcome to Epic Quest: Text Quest, the Python game.\n")
    pause()
    mainMenu()

def mainMenu():
    while True:
        clearScreen()
        print("Epic Quest: Text Quest")
        print(version + "\n")
        print("Select an Option:\n")
        createMenu(
            "New Game",
            "Load Game",
            "About the Game",
            "Change Log",
            "Exit to Shell")
    
        choice = input("Your choice: ")
        if choice == "1":
            newGame()
            break
        elif choice == "2":
            loadGame()
            break
        elif choice == "3":
            about()
            break
        elif choice == "4":
            changeLog()
            break
        elif choice == "5":
            quitGame("main")
            break
        else:
            clearScreen()
            print("Please select a option from the list.\n")
            pause()

def newGame():
    while True:
        clearScreen()
        print("New Game\n")
        name = input("What is your name? (No spaces, 'C' to go back) ")
        if name == "":
            clearScreen()
            print("Please enter a name.\n")
            pause()
        elif name == 'C':
            mainMenu()
            break
        else:
            player.name = name
            player.save()
            actionMenu() # Change to intro()
            break

def loadGame():
    clearScreen()
    print("Load Game\n")
    name = input("Please enter the name of your character: ")
    if player.load(name):
        clearScreen()
        print("Your game was successfully loaded!")
        pause()
        actionMenu()
        return
    else:
        clearScreen()
        print("Could not find a save file with the name you entered.")
        pause()
        mainMenu()
        return
    
def about():
    clearScreen()
    print("Epic Quest: Text Quest\n")
    print(version + "\n")
    print("Made by Ryan\n")
    print("Based off Epic Quest: Quest for Epicness, the computer",
          "role-playing game by the same author.\n")
    print("Copyright (C) RyGuyGames Inc. All rights reserved.\n")
    pause()
    mainMenu()

def changeLog():
    clearScreen()
    print("Epic Quest: Text Quest\n")
    print(version + "\n")
    print("Change Log:\n")
    print("* Added this screen\n")
    print("* Reworked the way the player's data is stored, allowing for faster\n"
          "retrieval and future player-like enemies. Perhaps for a duel arena.\n")
    print("* Fixed a problem where the game would become laggy after long\n"
          "play sessions.\n")
    pause()
    mainMenu()

def quitGame(caller):
    while True:
        clearScreen()
        choice = input("Are you sure you want to quit? [Y/N]: ")
        choice = choice.lower()
        if choice == "y":
            clearScreen()
            print("Thank you for playing Epic Quest: Text Quest.\n"
                  "\nHope you enjoyed the game!\n")
            pause()
            clearScreen()
            break
        elif choice == "n":
            if caller == "main":
                mainMenu()
                break
            elif caller == "action":
                actionMenu()
                break
        else:
            clearScreen()
            print("Please type either 'Y' or 'N' to make your selection.\n")
            pause()

def intro():
    clearScreen()
    print("Hello, welcome to Epic Quest: Text Quest\n")
    sleep(2.5)
    print("Long ago, the land of Ethandor was ruled by a great "
          "King and Queen.\n")
    sleep(2.5)
    print("One day, the kingdom was taken over by the evil "
          "Lord Darksword, and the King and Queen were murdered.\n")
    sleep(2.5)
    print("Luckily, the great wizard, Damen was able to "
          "escape the castle, carrying with him the true "
          "heir to the throne.\n")
    sleep(2.5)
    print("One day, this child will return to retake the "
          "throne of Ethandor and return peace to the "
          "land...\n")
    sleep(2.5)
    print("This...", end=' ')
    sleep(2.5)
    print("is Epic Quest!\n")
    sleep(1)
    pause()
    actionMenu()

def actionMenu():
    while True:
        clearScreen()
        print("Epic Quest: Text Quest\n")
        print("Name:", player.name)
        print("\nHealth:", str(player.hp) + "/" + str(player.maxhp))
        print("\nLocation:", player.loc)
        print("\nSelect an Option:\n")
        if player.loc == "Falconwood":
            if player.house:
                createMenu(
                    "Go Home",
                    "Look Around",
                    "View Inventory",
                    "Travel",
                    "Rest at the Inn",
                    "Quit to Shell")
            else:
                createMenu(
                    "Buy a House",
                    "Look Around",
                    "View Inventory",
                    "Travel",
                    "Rest at the Inn",
                    "Quit to Shell")
        else:
            createMenu(
                "Wander Around",
                "Look Around",
                "View Inventory",
                "Travel",
                "Rest at the Inn",
                "Quit to Shell")
        choice = input("Your Choice: ")
        if player.loc == "Falconwood":
            if player.house:
                if choice == "1":
                    home()
                    break
            else:
                if choice == "1":
                    houseShop()
                    break
        if choice == "3":
            inventory()
            break
        elif choice == "4":
            travel()
            break
        elif choice == "5":
            rest()
            break
        elif choice == "6":
            quitGame("action")
            break
        else:
            clearScreen()
            print("You must select an option from the list.\n")
            pause()

def houseShop():
    while True:
        clearScreen()
        print("Gold:", player.gold)
        print("\nYou enter the house shop. Looking around, "
              "you see a large man standing behind a desk "
              "counting money and looking very pleased "
              "with the total.\n")
        print("\"Hello!\" he says as you approach the desk.\n"
              "\"Are you here to buy a house? I have one for "
              "sale here in town. It's only 1,000 gold!\"\n")
        print("Select an Option:\n")
        createMenu("Buy a House\n",
                   "\"Why would I want a house?\"\n",
                   "Leave\n")
        choice = input("Your Choice: ")
        if choice == "1":
            buyHouse()
            break
        elif choice == "2":
            clearScreen()
            print("\n\"Why would you want to buy a house? That's a good question,\" says the clerk,\n"
                  "\"With a house, you can sleep there to restore your health for free.\n"
                  "Otherwise, you'll have to pay 10 gold to rest at an inn.\"\n")
            pause()
        elif choice == "3":
            actionMenu()
            break
        else:
            clearScreen()
            print("Please select an option from the menu.\n")
            pause()

def buyHouse():
    while True:
        clearScreen()
        choice = input("Are you sure you want to buy a house for 1,000 gold? [Y/N]: ")
        choice = choice.lower()
        if choice == "y":
            if player.gold >= 1000:
                player.house = True
                player.gold -= 1000
                clearScreen()
                print("Gold:",player.gold)
                print("\nYou have bought a house!\n")
                pause()
                player.save()
                actionMenu()
                break
            else:
                clearScreen()
                print("Gold:",player.gold)
                print("\nYou don't have enough gold to buy a house!")
                print("\nYou will need " + str(1000 - player.gold) +
                      " more gold to buy a house.")
                pause()
                actionMenu()
                break
        elif choice == "n":
            actionMenu()
            break
        else:
            clearScreen()
            print("Please type either 'Y' or 'N' to make your selection.\n")
            pause()

def inventory():
    clearScreen()
    print("Name:", player.name)
    print("\nHealth:", str(player.hp) + "/" + str(player.maxhp))
    print("\nGold:", player.gold)
    print("\nLevel:", player.lvl)
    print("\nXP:", player.xp)
    if player.house:
        print("\nHouse: Yes\n")
    else:
        print("\nHouse: No\n")
    input("Press ENTER to return to the menu...")
    actionMenu()

def travel():
    while True:
        clearScreen()
        print("Travel to Another Location\n")
        print("Current Location:",player.loc + "\n")
        print("Locations:\n")
        createMenu("Falconwood",
                   "Bywater",
                   "The Badlands",
                   "Old Thanadar Ruins",
                   "New Thanadar")
        choice = input("Where would you like to go? ")
        good = False
        if choice == "1":
            player.loc = "Falconwood"
            good = True
        elif choice == "2":
            player.loc = "Bywater"
            good = True
        elif choice == "3":
            player.loc = "The Badlands"
            good = True
        elif choice == "4":
            player.loc = "Old Thanadar Ruins"
            good = True
        elif choice == "5":
            player.loc = "New Thanadar"
            good = True
        else:
            clearScreen()
            print("Please select an option from the menu.\n")
            pause()
            
        if good:
            clearScreen()
            print("You have traveled to", player.loc + ".\n")
            pause()
            player.save()
            actionMenu()
            break

def rest():
    while True:
        clearScreen()
        print("Health:", str(player.hp) + "/" + str(player.maxhp))
        print("\nGold:", player.gold)
        print("You enter the inn and approach the keeper.")
        print("\"How much for a room,\" you ask.")
        print("\"That'll be 10 gold. What do you say?\"\n")
        choice = input("Do you want to rest at the inn to restore your health? [Y/N]: ")
        choice = choice.lower()
        if choice == 'y':
            clearScreen()
            if player.hp == player.maxhp:
                print("You don't need to rest.\n")
                pause()
                actionMenu()
                break
            
            if player.gold < 10:
                player.hp += 10
                print("Health:", str(player.hp) + "/" + str(player.maxhp))
                print("\nGold:", player.gold)
                print("\nYou don't have enough gold to rest at the inn.\n")
                print("However, you do regain 10 HP by sleeping under a tree.\n")
                pause()
                player.save()
                actionMenu()
                break
            
            elif player.gold >= 10:
                player.gold -= 10
                player.hp = player.maxhp
                print("Health:", str(player.hp) + "/" + str(player.maxhp))
                print("\nGold:", player.gold)
                print("\nYou rest for the night and wake up feeling "
                      "refreshed.\n")
                pause()
                player.save()
                actionMenu()
                break
                
        elif choice == 'n':
            actionMenu()
            break
        else:
            clearScreen()
            print("Please type either 'Y' or 'N' to make your selection.\n")
            pause()

def home():
    while True:
        clearScreen()
        print("Health:", str(player.hp) + "/" + str(player.maxhp))
        print("\nWelcome home!\n")
        choice = input("Would you like to rest to restore your health? [Y/N]: ")
        choice = choice.lower()
        if choice == 'y':
            clearScreen()
            player.hp = player.maxhp
            print("Health:", str(player.hp) + "/" + str(player.maxhp))
            print("\nYou rest for the night and wake up feeling refreshed.\n")
            pause()
            player.save()
            actionMenu()
            break
        elif choice == 'n':
            actionMenu()
            break
        else:
            clearScreen()
            print("Please type either 'Y' or 'N' to make your selection.\n")
            pause()

def wander():
    pass

def createMenu(*args):
    for item in args:
        print(str(args.index(item)+1) + ".", item + "\n")

def clearScreen():
    for i in range(50):
        print()

def pause():
    input("Press ENTER to continue...")

def toBool(value):
    return value.lower() in ["true"]

# Maybe I should rewrite the engine...
    """
def main():
    start()
    """

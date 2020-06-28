import pygame
import sys
import random


# NOTE THAT FOR THE SHOP, THE CARD HAVE YET TO HAVE AN ATREIVUYTE (MONSTER, SHIELD, ETC)
# WE NEED TO ADD THIS LATER


class Deck:
    def __init__(self):
        self.deck = []  # Contains the actual deck
        self.max_length = 30

    def shuffle(self):
        random.shuffle(self.deck)

    def new_deck(self):
        global monsters, shields, healing, weapons
        for i in range(int(self.max_length * (20 / 30))):  # monsters
            health = random.randint(4, 8)
            attack = random.randint(2, 8)
            if attack < 4:
                image = "Images\BalloonMonster.png"
            elif attack < 6:
                image = "Images\Candley.png"
            elif attack < 8:
                image = "Images\BoyBalloon.png"
            elif attack == 8:
                image = "Images\MuffinMan.png"

            self.deck.append(Monster(0, 0, 60, 100, image, health, attack))

        for i in range(int(self.max_length * (2 / 30))):  # potions
            power = random.randint(4, 10)
            if power <= 8:
                image = "Images\Potion.png"
            else:
                image = "Images\Cake.png"

            self.deck.append(Potion(0, 0, 60, 100, image, power))

        for i in range(int(self.max_length * (4 / 30))):  # weapons
            damage = random.randint(4, 6)
            durability = 1

            if damage < 6:
                image = "Images\Lolipop.png"
            else:
                image = "Images\Crayon.png"

        for i in range(int(self.max_length * (4 / 30))):  # shields
            power = random.randint(2, 6)
            durability = 1

            if power < 4:
                image = "Images\Pizza.png"
            elif power < 6:
                image = "Images\plate.png"
            else:
                image = "Images\Table.png"

            self.deck.append(Shield(0, 0, 60, 100, image, power, durability))

        for i in range(len(ability_images)):
            deck.deck.append(Ability(0, 0, 60, 100, ability_images[i], abilities[i]))


class DungeonHand:
    def __init__(self):
        self.layouts = [Layout(129, 145, 105, 130), Layout(275, 140, 120, 137), Layout(445, 130, 120, 140),
                        Layout(117, 290, 110, 137), Layout(260, 290, 125, 135), Layout(444, 290, 130, 130)]
        self.inventory = [None, None, None, None, None, None]

    def newHand(self, deck):
        # Shuffle in new dungeon hand cards
        for i in range(len(self.inventory)):
            card = self.inventory[i]
            if card == None and len(deck) > 0:
                newCard = deck.pop()
                newCard.x = self.layouts[i].x + int(self.layouts[i].w / 2 - newCard.w / 2)
                newCard.y = self.layouts[i].y + int(self.layouts[i].h / 2 - newCard.h / 2)
                self.inventory[i] = newCard

    def countCards(self):
        # Checks if we need the addition of cards into the dungeon hand
        # Find the amt of remaining cards within the dungeon hand
        cardCnt = 0
        for el in self.inventory:
            if el != None: cardCnt += 1
        return cardCnt


class PlayerHand:
    def __init__(self):
        self.layouts = [Layout(380, 560, 110, 145), Layout(512, 566, 110, 145), Layout(380, 715, 110, 125),
                        Layout(509, 715, 112,
                               135)]  # The inventory for the player should only hold the trinkets/special abilities
        self.used = [False, False, False, False]
        self.inventory = [None, None, None, None]
        self.crosses = []
        for i in range(4):
            card = Card(0, 0, 120, 175, "Images\Cross.png")
            card.x = self.layouts[i].x
            card.y = self.layouts[i].y - 15
            self.crosses.append(card)
        self.weaponLayout = Layout(80, 590, 120, 145)
        self.shieldLayout = Layout(220, 594, 110, 139)
        self.weapon = None
        self.shield = None
        self.weaponCross = Card(self.weaponLayout.x + 7, self.weaponLayout.y - 15, 120, 175, "Images\\Cross.png")
        self.shieldCross = Card(self.shieldLayout.x + 7, self.shieldLayout.y - 15, 120, 175, "Images\Cross.png")
        self.playerIconLayout = Layout(90, 735, 130, 130)
        self.playerIcon = Card(90, 735, 130, 130, "Images\PlayerIcon.png")

        self.weaponUsed = False
        self.shieldUsed = False  # Has this item been used once yet


class Layout:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.card = None

    def within_border(self, x, y, w, h):
        if self.x <= x and x + w <= self.x + self.w:
            if self.y <= y and y + h <= self.y + self.h:
                return True

        return False


class Window:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_icon(pygame.image.load('icon_uzz_icon.ico'))

    def fill(self):
        self.screen.fill((255, 255, 255))


class Card:
    def __init__(self, x, y, w, h, img):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (self.w, self.h))
        self.offsetX = 0
        self.offsetY = 0

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def withinBorder(self, pos):  # Border check for seeing if mouse click is within boarder
        mx, my = pos
        if self.x < mx < self.x + self.w:
            if self.y < my < self.y + self.h:
                return True  # Clicking on it
        return False  # Not clicking it

    def moveTo(self, pos):
        mx, my = pos
        self.x = mx - self.offsetX
        self.y = my - self.offsetY

    def calculateOffset(self, pos):
        mx, my = pos
        self.offsetX = mx - self.x
        self.offsetY = my - self.y


class PlayerInfo:
    def __init__(self):
        self.maxHealth = 13
        self.health = 13
        self.money = 50

    def die(self):
        global currentPage
        currentPage = 'Death'
        pass


class Ability(Card):
    def __init__(self, x, y, w, h, image, function):
        super().__init__(x, y, w, h, image)
        self.function = function


class Shield(Card):
    def __init__(self, x, y, w, h, image, power, durability):
        super().__init__(x, y, w, h, image)
        self.power = power
        self.durability = durability

    def block(self, damage, character):
        damage -= self.power
        if damage < 0:
            damage = 0
        self.durability -= 1
        character.health -= damage
        if character.health <= 0:
            return True  # dead
        if self.durability == 0:
            playerHand.shield = None
            del self

        moneyMade = random.randint(1, 10)
        print("Monster blocked! You made " + str(moneyMade) + "g")
        character.money += moneyMade

    def draw(self, screen):
        super().draw(screen)
        font = pygame.font.SysFont('Arial', 13, True)
        textsurface = font.render("Blc= " + str(self.power), True, (0, 0, 0))
        screen.blit(textsurface, (int(self.x + self.w / 2 - 25), int(self.y + self.h - 22)))
        textsurface = font.render("Dur= " + str(self.durability), True, (0, 0, 0))
        screen.blit(textsurface, (int(self.x + self.w / 2 - 25), int(self.y + self.h - 12)))


class Weapon(Card):
    def __init__(self, x, y, w, h, image, damage, durability):
        super().__init__(x, y, w, h, image)
        self.damage = damage
        self.durability = durability

    def hit(self, monster):
        monster.health -= self.damage
        # print(monster.health)
        self.durability -= 1
        if self.durability == 0:
            # print('hi')
            playerHand.weapon = None
            del self
        if monster.health <= 0:
            return True  # monster died

    def draw(self, screen):
        super().draw(screen)
        font = pygame.font.SysFont('Arial', 13, True)
        textsurface = font.render("Dmg= " + str(self.damage), True, (0, 0, 0))
        screen.blit(textsurface, (int(self.x + self.w / 2 - 25), int(self.y + self.h - 22)))
        textsurface = font.render("Dur= " + str(self.durability), True, (0, 0, 0))
        screen.blit(textsurface, (int(self.x + self.w / 2 - 25), int(self.y + self.h - 12)))


class Mouse:
    def __init__(self):
        self.held = False  # Boolean for if the mouse is being held
        self.holdingCard = False  # Boolean for if a card is being held (Stores the actual card if this var is not False)
        self.prevCardLocation = None  # References the card's location prior to being moved (Used for snap back action)


class Shop:
    def __init__(self):
        self.inventory = [None, None, None]
        self.layouts = [Layout(35, 126, 210, 200), Layout(306, 129, 187, 197), Layout(552, 132, 182, 195)]


class Monster(Card):
    def __init__(self, x, y, w, h, image, health, attack):
        super().__init__(x, y, w, h, image)
        self.health = health
        self.full_health = health
        self.attack = attack

    def hit(self, character):
        character.health -= self.attack
        del self

    def die(self, index):
        dungeonHand.inventory[index] = None
        return random.randint(1, 10)
        del self

    def draw(self, screen):
        super().draw(screen)
        font = pygame.font.SysFont('Arial', 13, True)
        textsurface = font.render("Att=" + str(self.attack), True, (0, 0, 0))
        screen.blit(textsurface, (int(self.x + self.w / 2 - 20), int(self.y + self.h - 25)))
        textsurface = font.render("Hp=" + str(self.health), True, (0, 0, 0))
        screen.blit(textsurface, (int(self.x + self.w / 2 - 20), int(self.y + self.h - 15)))


class Potion(Card):
    def __init__(self, x, y, w, h, image, power):
        super().__init__(x, y, w, h, image)
        self.power = power  # amount the character will be healed by

    def heal(self, character: "Character"):
        if character.health + self.power > character.maxHealth:
            character.health = character.maxHealth
        else:
            character.health += self.power
        del self

    def draw(self, screen):
        super().draw(screen)
        font = pygame.font.SysFont('Arial', 13, True)
        textsurface = font.render("Heal= " + str(self.power), True, (0, 0, 0))
        screen.blit(textsurface, (int(self.x + self.w / 2 - 25), int(self.y + self.h - 15)))


def nextTurn(dungeonHand, deck, playerHand):
    # Perform refilling of dungeon hand
    dungeonHand.newHand(deck)

    # Refresh the crosses
    for i in range(len(playerHand.used)):
        playerHand.used[i] = False
    playerHand.weaponUsed = False
    playerHand.shieldUsed = False

    # Refresh shop
    # Make shop
    for i in range(3):  # Draw the 3 purchaseable cards
        if i == 0:
            power = random.randint(4, 10)
            if power <= 8:
                image = "Images\Potion.png"
            else:
                image = "Images\Cake.png"

            card = Potion(shop.layouts[i].x + 65, shop.layouts[i].y + 50, 60, 100,
                          image, power)
        elif i == 1:
            damage = random.randint(4, 10)
            durability = random.randint(1, 2)

            if damage < 6:
                image = "Images\Crayon.png"
            else:
                image = "Images\Lolipop.png"

            card = Weapon(shop.layouts[i].x + 65, shop.layouts[i].y + 50, 60, 100,
                          image, damage, durability)
        else:
            power = random.randint(4, 10)
            durability = random.randint(1, 2)

            if power < 4:
                image = "Images\Pizza.png"
            elif power < 6:
                image = "Images\plate.png"
            else:
                image = "Images\Table.png"

            card = Shield(shop.layouts[i].x + 65, shop.layouts[i].y + 50, 60, 100,
                          image, power, durability)

        card.cost = random.randint(10, 40)
        shop.inventory[i] = card


def check_end():
    global currentPage
    for i in range(6):
        if type(dungeonHand.inventory[i]) is Monster:
            return
    if len(deck.deck) == 0:
        currentPage = "Win"


# SET UP AREA

# boss setup

bossPres = False
boss = Monster(0, 0, 60, 100, "Images\Boss.png", 15, 20)

# Initiate pygame
screen = Window(760, 880)
pygame.init()
clock = pygame.time.Clock()

# General usage
m = Mouse()
playerInfo = PlayerInfo()

# Main game play variables
gameBackground = Card(0, 0, screen.w, screen.h, "Images\Gui3.png")
dungeonHand = DungeonHand()
playerHand = PlayerHand()
deck = Deck()
nextTurnButton = Layout(214, 452, 264, 63)
shopButton = Layout(610, 235, 85, 104)

currentPage = "Main menu"
sellItemButton = Layout(614, 81, 90, 126)
cross = Card(0, 0, 75, 150, "Images\Cross.png")


def leech(monster, idx):
    if type(monster) is Monster:
        if playerInfo.health + monster.health > playerInfo.maxHealth:
            playerInfo.health = playerInfo.maxHealth
        else:
            playerInfo.health += monster.health
        monster.die(idx)


def sap(monster, idx):
    if type(monster) is Monster:
        monster.die(idx)


def execute(monster, idx):
    if type(monster) is Monster:
        if monster.health != monster.full_health:
            monster.die(idx)


def fortify(monster, idx):
    count = 0
    i = 0
    while (count < 2):
        if type(dungeonHand.inventory[i]) is Monster:
            dungeonHand.inventory[i] = None
            count += 1
        i += 1
        if i == 5:
            break


def vanish(monster, idx):
    for i in range(6):
        dungeonHand.inventory[i] = None


# Deck management
monsters = ["Images\BoyBalloon.png", "Images\spoon.png", "Images\Candley.png"]
shields = ["Images\Table.png", "Images\plate.png", "Images\Pizza.png"]
healing = ["Images\Potion.png", "Images\Cake.png"]
weapons = ["Images\Lolipop.png", "Images\Crayon.png"]
money = ["Images\Gold.png", "Images\Bag.png", 'dollar_sign.png']
ability_images = ["Images\Leech.png", "Images\Fortify.png", "Images\Execute.png", "Images\Vanish.png", "Images\Sap.png"]
abilities = [leech, fortify, execute, vanish, sap]
deck.new_deck()
deck.shuffle()
cardDisplay = pygame.Rect(250, 10, 200, 67)

# Can be removed later
# card = Card(0, 0, 60, 100, "Images\Cake.png")
# dungeonHand.inventory[3] = card

# Main shop variables
pygame.font.init()
StopToMenuButton = pygame.Rect(606, 804, 115, 60)
myfont = pygame.font.SysFont('Arial', 90)
shopBackground = Card(0, 0, screen.w, screen.h, "Images\ShopGui.png")
refresh_button = pygame.Rect(10, 10, 260, 60)
shop_cards = []
shop = Shop()

# Main menu variables
menuBackground = Card(0, 0, screen.w, screen.h, "Images\Background.png")
winBackground = Card(0, 0, screen.w, screen.h, "Images\end.png")
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
play_button = pygame.Rect(screen.w // 2 - 100, screen.h // 2 + 50 - 225, 150, 50)
replay_button = pygame.Rect(screen.w // 2 - 100, screen.h // 2 + 50, 150, 50)


def update():
    global currentPage, bossPres

    check_end()
    # Check inputs
    if currentPage == "Gameplay":

        # Check to see if we want to spawn the Boss
        if len(deck.deck) == 0:
            if bossPres == False:
                bossPres = True
                dungeonHand.inventory[2] = boss
                boss.x = dungeonHand.layouts[2].x + 10
                boss.y = dungeonHand.layouts[2].y + 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m.held = True
                pos = pygame.mouse.get_pos()
                x, y = pos

                # Check for next turn click
                if nextTurnButton.within_border(x, y, 1, 1):
                    if dungeonHand.countCards() <= 2:
                        print("Initiating next turn")
                        nextTurn(dungeonHand, deck.deck, playerHand)
                    else:
                        print("You need to clear the dungeon hand until at least 2 cards remain")

                # Check for shop click
                elif shopButton.within_border(x, y, 1, 1):  # Transition into shop screen
                    currentPage = "Shop"

                # Check which card (if any) are gonna be dragged by the mouse
                for i in range(len(dungeonHand.inventory)):
                    card = dungeonHand.inventory[i]
                    if card != None:
                        if card.withinBorder(pos):
                            m.holdingCard = card
                            m.prevCardLocation = {"pos": [card.x, card.y], "location": "dungeon", "i": i}
                            card.calculateOffset(
                                pos)  # Offset is required so that the card can be moved without being centered at the mouse
                            break

                for i in range(len(playerHand.inventory)):
                    card = playerHand.inventory[i]
                    if card != None:
                        if card.withinBorder(pos):
                            if playerHand.used[i] == False:  # Make sure we have not used this item yet
                                m.holdingCard = card
                                m.prevCardLocation = {"pos": [card.x, card.y], "location": "player", "i": i}
                                card.calculateOffset(
                                    pos)  # Offset is required so that the card can be moved without being centered at the mouse
                                break

                if playerHand.shield != None:
                    card = playerHand.shield
                    if playerHand.shield.withinBorder(pos):
                        if playerHand.shieldUsed == False:
                            m.holdingCard = card
                            m.prevCardLocation = {"pos": [card.x, card.y], "location": "shield", "i": None}
                            card.calculateOffset(
                                pos)  # Offset is required so that the card can be moved without being centered at the mouse

                if playerHand.weapon != None:
                    card = playerHand.weapon
                    if playerHand.weapon.withinBorder(pos):
                        if playerHand.weaponUsed == False:
                            m.holdingCard = card
                            m.prevCardLocation = {"pos": [card.x, card.y], "location": "weapon", "i": None}
                            card.calculateOffset(
                                pos)  # Offset is required so that the card can be moved without being centered at the mouse

            elif event.type == pygame.MOUSEBUTTONUP:
                m.held = False

                # In here, handle the ability for a card to jump back to its original position if the final position
                # doesn't belong to either dungeon or player hands

                if m.holdingCard != False:
                    # Check to see if the card fits in any player or dungeon slots
                    card = m.holdingCard
                    flag = False  # Bool for if the card has found a new slot (False = no slot found, True = slot found)

                    # Are we selling an item?
                    if sellItemButton.within_border(card.x, card.y, card.w, card.h):
                        if type(card) != Monster:
                            moneyMade = random.randint(3, 6)
                            print("Item Sold! You made " + str(moneyMade) + "g")
                            playerInfo.money += moneyMade
                            flag = True

                    # Monster hit player icon?
                    layout = playerHand.playerIconLayout
                    if layout.within_border(card.x, card.y, card.w, card.h) and type(card) is Monster:
                        playerInfo.health -= card.attack
                        if playerInfo.health <= 0:
                            playerInfo.die()
                        dungeonHand.inventory[m.prevCardLocation["i"]] = None

                    # Heal player?
                    layout = playerHand.playerIconLayout
                    if layout.within_border(card.x, card.y, card.w, card.h) and type(card) is Potion:
                        if m.prevCardLocation["location"] == "player":
                            card.heal(playerInfo)
                            playerHand.inventory[m.prevCardLocation["i"]] = None
                            playerHand.used[m.prevCardLocation["i"]] = True

                    # See if it belongs now to player hand
                    for i in range(len(playerHand.layouts)):
                        layout = playerHand.layouts[i]
                        if layout.within_border(card.x, card.y, card.w, card.h) and playerHand.inventory[
                            i] == None and type(
                            card) is not Monster:  # Make sure that the card fits and that the slot is no occupied
                            if playerHand.used[i] == False:  # We can only move cards to slots which have unused items
                                playerHand.inventory[i] = card
                                flag = True

                    # See if it belongs now to dungeon hand
                    for i in range(len(dungeonHand.layouts)):
                        layout = dungeonHand.layouts[i]
                        if layout.within_border(card.x, card.y, card.w, card.h):
                            if not dungeonHand.inventory[i]:
                                dungeonHand.inventory[i] = card
                                flag = True
                            # Check for attack combat
                            elif type(dungeonHand.inventory[i]) is Monster and type(card) is Weapon and \
                                    m.prevCardLocation['location'] == 'weapon':
                                if not playerHand.weaponUsed:
                                    if card.hit(dungeonHand.inventory[i]):
                                        # Monster has died
                                        moneyMade = dungeonHand.inventory[i].die(i)
                                        print("Monster slain! You made " + str(moneyMade) + "g")
                                        playerInfo.money += moneyMade
                                    playerHand.weaponUsed = True
                            elif (type(dungeonHand.inventory[i]) is Monster and type(card) is Ability and
                                  m.prevCardLocation['location'] == 'player'):
                                card.function(dungeonHand.inventory[i], i)
                                playerHand.inventory[m.prevCardLocation["i"]] = None

                    # Belongs to shield slot?
                    layout = playerHand.shieldLayout
                    if layout.within_border(card.x, card.y, card.w, card.h):
                        if type(card) is Shield and not playerHand.shield and playerHand.shieldUsed == False:
                            playerHand.shield = card
                            flag = True
                        elif type(card) is Monster and playerHand.shield:
                            if not playerHand.shieldUsed:
                                if playerHand.shield.block(card.attack, playerInfo): playerInfo.die()
                                card.die(m.prevCardLocation["i"])
                                playerHand.shieldUsed = True

                    # Belongs to weapon slot?
                    layout = playerHand.weaponLayout
                    if layout.within_border(card.x, card.y, card.w, card.h) and not playerHand.weapon and type(card) is \
                            Weapon and playerHand.weaponUsed == False:
                        playerHand.weapon = card
                        flag = True

                    # In case that the card hasn't found a new slot, we send it back to its original spot
                    if not flag:
                        card.x, card.y = m.prevCardLocation["pos"]
                    else:
                        # Remove history of the card in its original location
                        location = m.prevCardLocation["location"]
                        if location == "dungeon":
                            dungeonHand.inventory[m.prevCardLocation["i"]] = None
                        elif location == "player":
                            playerHand.inventory[m.prevCardLocation["i"]] = None
                        elif location == "weapon":
                            playerHand.weapon = None
                        elif location == "shield":
                            playerHand.shield = None

                    m.holdingCard = False  # We are now no longer holding a card

        # Update positions of held card
        if m.holdingCard != False:
            pos = pygame.mouse.get_pos()
            m.holdingCard.moveTo(pos)
    elif currentPage == "Shop":
        #print(shop.inventory[0].power)
        screen.fill()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print(playerHand.inventory,"plus", playerHand.weapon, playerHand.shield)
                m.held = True
                # print(pos)

                # Check if we are purchasing a shop item
                for i in range(len(shop.inventory)):
                    card = shop.inventory[i]
                    if card != None:
                        if card.withinBorder(pos):
                            if playerInfo.money - card.cost >= 0:
                                flag = False  # False = no space for the new card, True = available space
                                storedI = i  # Stores the info of the position of the card in the shop (Used to remove card from shop (possibly))
                                for i in range(len(playerHand.inventory)):
                                    slot = playerHand.inventory[i]
                                    if slot == None and playerHand.used[i] == False:
                                        playerHand.inventory[i] = card
                                        # Update the card's position
                                        card.x = playerHand.layouts[i].x + 20
                                        card.y = playerHand.layouts[i].y + 20
                                        shop.inventory[storedI] = None
                                        flag = True
                                        break
                                if flag:
                                    playerInfo.money -= card.cost

                # Work on things inside the player hand
                # Check which card (if any) are gonna be dragged by the mouse

                for i in range(len(playerHand.inventory)):
                    card = playerHand.inventory[i]
                    if card != None:
                        if card.withinBorder(pos):
                            if playerHand.used[i] == False:  # Make sure we have not used this item yet
                                m.holdingCard = card
                                m.prevCardLocation = {"pos": [card.x, card.y], "location": "player", "i": i}
                                card.calculateOffset(
                                    pos)  # Offset is required so that the card can be moved without being centered at the mouse
                                break

                if playerHand.shield != None:
                    card = playerHand.shield
                    if playerHand.shield.withinBorder(pos):
                        if playerHand.shieldUsed == False:
                            m.holdingCard = card
                            m.prevCardLocation = {"pos": [card.x, card.y], "location": "shield", "i": None}
                            card.calculateOffset(
                                pos)  # Offset is required so that the card can be moved without being centered at the mouse

                if playerHand.weapon != None:
                    card = playerHand.weapon
                    if playerHand.weapon.withinBorder(pos):
                        if playerHand.weaponUsed == False:
                            m.holdingCard = card
                            m.prevCardLocation = {"pos": [card.x, card.y], "location": "weapon", "i": None}
                            card.calculateOffset(
                                pos)  # Offset is required so that the card can be moved without being centered at the mouse

                # Work on Things outside of the player hand
                x, y = pos
                if (refresh_button.collidepoint(x, y)):  # Refresh button
                    # Check to see if we have enough money for refresh
                    if playerInfo.money - 15 > 0:
                        playerInfo.money -= 15  # Pay refresh fee
                        # Refresh shop items
                        for i in range(3):  # Draw the 3 purchaseable cards
                            if i == 0:
                                card = Potion(shop.layouts[i].x + 65, shop.layouts[i].y + 50, 60, 100,
                                              healing[random.randint(0, len(healing) - 1)], random.randint(1, 3))
                            elif i == 1:
                                card = Weapon(shop.layouts[i].x + 65, shop.layouts[i].y + 50, 60, 100,
                                              weapons[random.randint(0, len(weapons) - 1)], random.randint(4, 10),
                                              random.randint(1, 2))
                            else:
                                card = Shield(shop.layouts[i].x + 65, shop.layouts[i].y + 50, 60, 100,
                                              shields[random.randint(0, len(shields) - 1)], random.randint(4, 10),
                                              random.randint(1, 2))

                            card.cost = random.randint(10, 50)
                            shop.inventory[i] = card

                elif StopToMenuButton.collidepoint(x, y):
                    # Return to main gameplay
                    currentPage = "Gameplay"

            elif event.type == pygame.MOUSEBUTTONUP:
                m.held = False

                # In here, handle the ability for a card to jump back to its original position if the final position
                # doesn't belong to either dungeon or player hands

                if m.holdingCard != False:
                    card = m.holdingCard

                    flag = False  # Bool for if the card has found a new slot (False = no slot found, True = slot found)

                    # See if it belongs now to player hand
                    for i in range(len(playerHand.layouts)):
                        layout = playerHand.layouts[i]
                        if layout.within_border(card.x, card.y, card.w, card.h) and playerHand.inventory[
                            i] == None:  # Make sure that the card fits and that the slot is no occupied
                            playerHand.inventory[i] = card
                            flag = True

                    # Belongs to shield slot?
                    layout = playerHand.shieldLayout
                    if layout.within_border(card.x, card.y, card.w, card.h):
                        if type(card) is Shield and not playerHand.shield and playerHand.shieldUsed == False:
                            playerHand.shield = card
                            flag = True

                    # Belongs to weapon slot?
                    layout = playerHand.weaponLayout
                    if layout.within_border(card.x, card.y, card.w, card.h) and not playerHand.weapon and type(card) is \
                            Weapon and playerHand.weaponUsed == False:
                        print("placed")
                        playerHand.weapon = card
                        flag = True

                    # Heal player?
                    layout = playerHand.playerIconLayout
                    if layout.within_border(card.x, card.y, card.w, card.h) and type(card) is Potion:
                        card.heal(playerInfo)
                        if m.prevCardLocation["location"] == "player":
                            playerHand.inventory[m.prevCardLocation["i"]] = None
                            playerHand.used[m.prevCardLocation["i"]] = True

                    # In case that the card hasn't found a new slot, we send it back to its original spot
                    if not flag:
                        card.x, card.y = m.prevCardLocation["pos"]
                    else:
                        # Remove history of the card in its original location
                        location = m.prevCardLocation["location"]
                        if location == "player":
                            playerHand.inventory[m.prevCardLocation["i"]] = None
                        elif location == "shield":
                            playerHand.shield = None
                        elif location == "weapon":
                            playerHand.weapon = None

                    m.holdingCard = False  # We are now no longer holding a card

        # Update positions of held card
        if m.holdingCard != False:
            pos = pygame.mouse.get_pos()
            m.holdingCard.moveTo(pos)

    elif currentPage == "Death":
        screen.fill()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            x, y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(x, y):
                    currentPage = "Gameplay"
                    playerInfo.health = playerInfo.maxHealth
                    playerInfo.money = 50
                    dungeonHand.inventory = [None for i in range(6)]
                    playerHand.inventory = [None for i in range(4)]
                    playerHand.weapon = None
                    playerHand.shield = None
                    deck.new_deck()

    elif currentPage == "Main menu":
        screen.fill()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            x, y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(x, y):
                    currentPage = "Gameplay"

    elif currentPage == "Win":
        screen.fill()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def draw():
    if currentPage == "Gameplay":
        screen.fill()
        gameBackground.draw(screen.screen)  # Draw background

        # mCard.draw(screen.screen)
        pygame.draw.rect(screen.screen, (255, 255, 255), cardDisplay)
        myfont = pygame.font.SysFont('Arial', 30)
        textsurface = myfont.render(str(len(deck.deck)) + " Cards Left", False, (0, 0, 0))
        screen.screen.blit(textsurface, (260, 30))

        # Draw dungeon hand
        for card in dungeonHand.inventory:
            if card != None: card.draw(screen.screen)
        # Draw player hand
        for card in playerHand.inventory:
            if card != None: card.draw(screen.screen)
        # Draw Shield
        if playerHand.shield != None:
            playerHand.shield.draw(screen.screen)
        # Draw Sword
        if playerHand.weapon != None:
            playerHand.weapon.draw(screen.screen)

        # Draw player info
        # Draw health
        myfont = pygame.font.SysFont('Arial', 30)
        textsurface = myfont.render("health = " + str(playerInfo.health), False, (0, 0, 0))
        screen.screen.blit(textsurface, (235, 760))
        # Draw money
        textsurface = myfont.render("money = " + str(playerInfo.money), False, (0, 0, 0))
        screen.screen.blit(textsurface, (235, 805))

        # Draw the player icon
        playerHand.playerIcon.draw(screen.screen)

        # Draw the crosses for items which have been used once
        if playerHand.shieldUsed:
            playerHand.shieldCross.draw(screen.screen)
        if playerHand.weaponUsed:
            playerHand.weaponCross.draw(screen.screen)
        for i in range(len(playerHand.inventory)):
            if playerHand.used[i]:
                playerHand.crosses[i].draw(screen.screen)

        pygame.display.update()
        clock.tick(70)  # Fps (Don't know why/how it does it)
    elif currentPage == "Shop":

        myfont = pygame.font.SysFont('Arial', 30)
        shopBackground.draw(screen.screen)  # Draw background

        # Draw refresh button
        pygame.draw.rect(screen.screen, (255, 255, 255), refresh_button)
        textsurface = myfont.render('Refresh (15 cost)', False, (0, 0, 0))
        screen.screen.blit(textsurface, (30, 30))

        # Draw back button
        textsurface = myfont.render('Back', False, (0, 0, 0))
        pygame.draw.rect(screen.screen, (255, 255, 255), StopToMenuButton)
        screen.screen.blit(textsurface, (StopToMenuButton.x + 35, StopToMenuButton.y + 20))

        # Draw Shield
        if playerHand.shield != None:
            playerHand.shield.draw(screen.screen)
        # Draw Sword
        if playerHand.weapon != None:
            playerHand.weapon.draw(screen.screen)

        # Draw Player Hand
        for card in playerHand.inventory:
            if card != None: card.draw(screen.screen)

        # Draw shop cards
        for i in range(len(shop.inventory)):
            card = shop.inventory[i]
            if card != None:
                textsurface = myfont.render(str(card.cost), False, (0, 255, 0))
                screen.screen.blit(textsurface, (shop.layouts[i].x + 80, shop.layouts[i].y + 210))
                textsurface = myfont.render("cost", False, (0, 255, 0))
                screen.screen.blit(textsurface, (shop.layouts[i].x + 70, shop.layouts[i].y + 250))
                card.draw(screen.screen)

        # Draw player info
        # Draw health
        textsurface = myfont.render("health = " + str(playerInfo.health), False, (0, 0, 0))
        screen.screen.blit(textsurface, (235, 760))
        # Draw money
        textsurface = myfont.render("money = " + str(playerInfo.money), False, (0, 0, 0))
        screen.screen.blit(textsurface, (235, 805))

        # Draw the player icon
        playerHand.playerIcon.draw(screen.screen)

        # Draw the crosses for items which have been used once
        if playerHand.shieldUsed:
            playerHand.shieldCross.draw(screen.screen)
        if playerHand.weaponUsed:
            playerHand.weaponCross.draw(screen.screen)
        for i in range(len(playerHand.inventory)):
            if playerHand.used[i]:
                playerHand.crosses[i].draw(screen.screen)

        pygame.display.update()
        clock.tick(70)  # Fps (Don't know why/how it does it)
    elif currentPage == "Death":
        img = pygame.image.load("Images\\Death.png")
        screen.screen.blit(img, (0, 0))

        button_font = pygame.font.SysFont('Arial', 46)

        play_text = button_font.render("Retry", True, (0, 0, 0))
        play_text_rect = play_text.get_rect(center=(screen.w // 2 - 25, screen.h // 2 + 75))
        pygame.draw.rect(screen.screen, RED, replay_button)

        screen.screen.blit(play_text, play_text_rect)

        pygame.display.update()

    elif currentPage == "Main menu":
        menuBackground.draw(screen.screen)

        button_font = pygame.font.SysFont('Arial', 46)

        play_text = button_font.render("Play", True, (0, 0, 0))
        play_text_rect = play_text.get_rect(center=(screen.w // 2 - 25, screen.h // 2 - 150))
        pygame.draw.rect(screen.screen, RED, play_button)

        screen.screen.blit(play_text, play_text_rect)

        pygame.display.update()

    elif currentPage == "Win":
        winBackground.draw(screen.screen)
        pygame.display.update()


while True:
    # print(currentPage)
    update()
    draw()

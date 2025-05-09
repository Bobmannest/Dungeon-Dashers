import pygame, sys, random, pygamegui, time, copy
from pygame.locals import QUIT
from sprites import *
from stats import *
from layouts import *

# Initialise
pygame.init()
Display = pygame.display.set_mode((704, 576), pygame.NOFRAME)
Surface = pygame.Surface((704, 576), pygame.SRCALPHA)

# Font
font = pygame.font.Font('freesansbold.ttf', 50)
font2 = pygame.font.Font('freesansbold.ttf', 25)
font3 = pygame.font.Font('freesansbold.ttf', 35)
font4 = pygame.font.Font('freesansbold.ttf', 15)
font5 = pygame.font.Font('freesansbold.ttf', 20)

# Title
title = font.render('Dungeon Dashers', True, coolred)
titletext = title.get_rect()
titletext.center = (352, 80)

# Upgrades menu: "Upgrades", "Perm Strength +5", "Perm Max HP +10", "Perm walkspeed +1)
upgrade = font3.render('Upgrades:', True, black)
upgradetxt = upgrade.get_rect()
upgradetxt.center = (250, 140)

strengthup = font2.render("Perm Strength +5", True, black)
strengthuptxt = strengthup.get_rect()
strengthuptxt.center = (270, 240)

maxhpup = font2.render("Perm Max HP +10", True, black)
maxhpuptxt = maxhpup.get_rect()
maxhpuptxt.center = (268, 340)

walkspeedup = font2.render("Perm walkspeed +1", True, black)
walkspeeduptxt = walkspeedup.get_rect()
walkspeeduptxt.center = (277, 440)

# "Dungeon Cleared!"
floornum = "Floor " + str(floor) + " Cleared!"
cleared = font3.render(floornum, True, black)
clearedtxt = cleared.get_rect()
clearedtxt.center = (350, 90)

# "Paused"
pause = font3.render('Paused', True, black)
pausetxt = pause.get_rect()
pausetxt.center = (352, 245)

#If room is locked: "There are enemies in this room!
lock = font3.render('There are enemies in this room!', True, coolred)
locktxt = lock.get_rect()
locktxt.center = (352, 80)

# "Game Over"
over = font3.render('Game Over', True, black)
overtxt = over.get_rect()
overtxt.center = (350, 245)

# "Loading"
load = font.render('Loading...', True, white)
loadtxt = load.get_rect()
loadtxt.center = (352, 200)

# Background image
backimage = pygame.image.load("BackgroundImage.png").convert()
backimage2 = pygame.transform.scale(backimage, (704, 576))

# Tutorial: "To Move", "To Attack"
move = font4.render('Arrow Keys To Move', True, black)
movetxt = move.get_rect()
movetxt.center = (550, 150)

attack = font4.render('Left Mouse To Attack', True, black)
attacktxt = attack.get_rect()
attacktxt.center = (550, 175)

# Hitboxes for going to another room
def hitboxleft():
    global Left_box
    Left_box = pygame.draw.rect(Display, normal,
                                pygame.Rect(0, 256, 10, 64))


def hitboxright():
    global Right_box
    Right_box = pygame.draw.rect(Display, normal,
                                 pygame.Rect(694, 256, 10, 64))


def hitboxup():
    global Up_box
    Up_box = pygame.draw.rect(Display, normal,
                              pygame.Rect(324, 0, 56, 10))


def hitboxdown():
    global Down_box
    Down_box = pygame.draw.rect(Display, normal,
                                pygame.Rect(320, 566, 64, 10))


# Loading screen
def loading():
    global barx, loadcontrol, playerx, playery, movelayer, moveroom
    Display.fill(lblue)
    Display.blit(load, loadtxt)
    pygame.draw.rect(Display, black, pygame.Rect(235, 236, 241, 55))
    pygame.draw.rect(Display, white, pygame.Rect(236, 237, 239, 53))
    pygame.draw.rect(Display, coolgreen, pygame.Rect(236, 237, barx, 53))
    while barx != 239:
        barx += random.randint(10, 75)
        if barx > 239:
            barx = 239
        pygame.draw.rect(Display, coolgreen, pygame.Rect(236, 237, barx, 53))
        pygame.display.flip()
        time.sleep(0.05)
    loadcontrol = 1
    playerx = 352
    playery = 277
    movelayer = 1
    moveroom = -1


# Healthbar
def playerhpbar():
    global hpbarx, maxhpbarx
    if hpbarx <= (maxhpbarx * 0.25):
        hpindicator = critred
    else:
        hpindicator = green
    pygame.draw.rect(Display, black, pygame.Rect(10, 10, maxhpbarx + 4, 44))
    pygame.draw.rect(Display, coolred, pygame.Rect(12, 12, maxhpbarx, 40))
    pygame.draw.rect(Display, coolgreen, pygame.Rect(12, 12, hpbarx, 40))
    # HP text
    hpwords = "HP:" + str(hpbarx)
    hp = font2.render(hpwords, True, hpindicator)
    hptxt = hp.get_rect()
    hptxt.center = (60, 33)
    # Text output
    Display.blit(hp, hptxt)

#Tutorial
def tutorial():
    global tutorialcheck
    if tutorialcheck == 1:
        #Display UI
        pygame.draw.rect(Display, black, pygame.Rect(450, 100, 190, 100))
        pygame.draw.rect(Display, lblue, pygame.Rect(451, 101, 188, 98))
        #Display X button
        Exit_button5 = Button('X', 25, 612, 109, 605, 105, 30, 30)
        Exit_button5.draw()
        #Display text
        Display.blit(move, movetxt)
        Display.blit(attack, attacktxt)
        #Exits menu
        if Exit_button5.checkclick() == False:
            tutorialcheck = 0
# Upgrades menu
def upgrades():
    global upgradesmenu, currency, permstrength, permmaxhp, permmovespeed
    # UI Boxes and outlines
    pygame.draw.rect(Display, black, pygame.Rect(145, 45, 414, 486))
    pygame.draw.rect(Display, lblue, pygame.Rect(146, 46, 412, 484))
    pygame.draw.rect(Display, black, pygame.Rect(165, 65, 252, 42))
    pygame.draw.rect(Display, gold, pygame.Rect(166, 66, 250, 40))
    # Metaprogression currency text
    money = "Balance: $" + str(currency)
    balance = font2.render(money, True, dgold)
    balancetxt = balance.get_rect()
    balancetxt.center = (260, 89)
    #Permanent upgrade buttons
    strengthupbutton = Button('BUY - $50', 15, 440, 228, 425, 210, 100, 50)
    maxhpupbutton = Button('BUY - $50', 15, 440, 333, 425, 315, 100, 50)
    walkspeedupbutton = Button('BUY - $100', 15, 435, 433, 425, 415, 100, 50)
    strengthupbutton.draw()
    maxhpupbutton.draw()
    walkspeedupbutton.draw()
    #Used so player can purchase upgrades
    if strengthupbutton.checkclick() == False and currency >= 50:
        currency -= 50
        permstrength += 1
    if maxhpupbutton.checkclick() == False and currency >= 50:
        currency -= 50
        permmaxhp += 1
    if walkspeedupbutton.checkclick() == False and currency >= 100:
        currency -= 100
        permmovespeed += 1
    # Text outputs
    Display.blit(balance, balancetxt)
    Display.blit(upgrade, upgradetxt)
    Display.blit(strengthup, strengthuptxt)
    Display.blit(maxhpup, maxhpuptxt)
    Display.blit(walkspeedup, walkspeeduptxt)
    # Exit button(text,textsize,textx,texty,xpos,ypos,width,height)
    Exit_button = Button('X', 35, 506, 71, 498, 66, 40, 40)
    Exit_button.draw()
    if Exit_button.checkclick() == False:
        upgradesmenu = 0

#Upgrades menu for upgrades you get at the start of every dungeon floor
def dungeonupgrade():
    global playerdmg, hpbarx, maxhpbarx, chosenupgrade, strength, maxhp
    #Upgrade 1
    Strength_button = Button('Strength - +5 Attack DMG', 15, 92, 145, 84, 128, 200, 96)
    #Upgrade 2
    Maxhp_button = Button('Max Health - +10 Max HP', 15, 92, 255, 84, 240, 200, 96)
    #Upgrade 3
    Heal_button = Button('Heal - Heals 25%', 15, 120, 370, 84, 352, 200, 96)
    if chosenupgrade == 0:
        #Draws UI boxes
        pygame.draw.rect(Display, black, pygame.Rect(74, 118, 221, 343))
        pygame.draw.rect(Display, green, pygame.Rect(76, 120, 217, 339))
        #Draws Buttons
        Strength_button.draw()
        Maxhp_button.draw()
        Heal_button.draw()
        #Checks if buttons are clicked
        if Strength_button.checkclick() == False:
            playerdmg += 5
            chosenupgrade = 1
        if Maxhp_button.checkclick() == False:
            maxhpbarx += 10
            chosenupgrade = 1
        if Heal_button.checkclick() == False:
            hpbarx += (maxhpbarx*0.25)
            if hpbarx > maxhpbarx:
                hpbarx = maxhpbarx
            chosenupgrade = 1

# Quit dungeon menus
def Quitdungeon():
    global quitmenu, menu, loadcontrol, newmap, floorcomplete, lockedroom, chosenupgrade
    if Exit_button3.checkclick() == False:
        quitmenu = 1
    if quitmenu == 1:
        # UI Boxes and outlines
        pygame.draw.rect(Display, black, pygame.Rect(198, 198, 308, 180))
        pygame.draw.rect(Display, lblue, pygame.Rect(200, 200, 304, 176))
        # Pause text output
        Display.blit(pause, pausetxt)
        # Exit button(text,textsize,textx,texty,xpos,ypos,width,height)
        Return_button = Button('Return to \n   Game', 20, 372, 306, 360, 300, 120, 50)
        Return_button.draw()
        Gomenu_button = Button('Main Menu', 20, 230, 315, 225, 300, 120, 50)
        Gomenu_button.draw()
        #If button are clicked
        if Return_button.checkclick() == False:
            quitmenu = 0
        if Gomenu_button.checkclick() == False:
            quitmenu = 0
            menu = 1
            loadcontrol = 0
            newmap = 1
            floorcomplete = 0


# Quit dungeon menus
def Gameover():
    global quitmenu, menu, loadcontrol, newmap, gameover, hpbarx, lockedroom, chosenupgrade
    # Check to see if player is at 0 Health
    if hpbarx <= 0:
        gameover = 1
        # UI Boxes and outlines
        pygame.draw.rect(Display, black, pygame.Rect(145, 45, 414, 486))
        pygame.draw.rect(Display, lblue, pygame.Rect(146, 46, 412, 484))
        # Game over text output
        Display.blit(over, overtxt)
        # Exit button(text,textsize,textx,texty,xpos,ypos,width,height)
        Gomenu_button = Button('Main Menu', 20, 300, 315, 295, 300, 120, 50)
        Gomenu_button.draw()
        #If button is clicked, variables are reset so that the game can start from fresh
        if Gomenu_button.checkclick() == False:
            quitmenu = 0
            menu = 1
            loadcontrol = 0
            newmap = 1
            gameover = 0
            hpbarx = 100
            lockedroom = False
            chosenupgrade = 0


# Menu for completing a dungeon
def floorwinner():
    global floorcomplete, floor, menu, loadcontrol, newmap, chosenupgrade, lockedroom, enemyspawnlayer, enemyspawnroom, enemyclearconfirm
    # UI Boxes and outlines
    pygame.draw.rect(Display, black, pygame.Rect(145, 45, 414, 486))
    pygame.draw.rect(Display, lblue, pygame.Rect(146, 46, 412, 484))
    # Clear floor text output
    Display.blit(cleared, clearedtxt)
    # Exit button(text,textsize,textx,texty,xpos,ypos,width,height)
    Exit_button4 = Button('Quit and return to menu', 15, 170, 486, 166, 474, 180, 40)
    Exit_button4.draw()
    Continue_button = Button('Continue', 15, 420, 486, 360, 474, 180, 40)
    Continue_button.draw()
    #If buttons are clicked
    if Exit_button4.checkclick() == False:
        menu = 1
        loadcontrol = 0
        newmap = 1
    if Continue_button.checkclick() == False:
        loadcontrol = 0
        newmap = 1
        floor += 1
        floorcomplete = 0
        lockedroom = False
        chosenupgrade = 0
        enemyspawnlayer = 1
        enemyspawnroom = -1
        enemyclearconfirm = 0

# Map generator
#      ROOM ROOM ROOM
# START ROOM ROOM ROOM END
#      ROOM ROOM ROOM
def generate_map():
    global map, enemymap, cx, cy, layout
    # Map which tracks which rooms have enemies defeated(E for Enemies are present and C for room cleared)
    enemymap = [["E", "E", "E"],
                ["E", "E", "E"],
                ["E", "E", "E"]]
    # Empty map
    map = [[], [], []]
    # test map
    map2 = [[], [], []]
    # Y layer
    layer = 1
    # for each layer
    for _ in range(3):
        # for each item in each layer
        for _ in range(3):
            randomint = random.randint(1, len(pool))
            #Makes copies of the room layouts instead of modifying the actual layout array permanently
            map[layer - 1].append(copy.deepcopy(pool[randomint - 1]))
            # test
            map2[layer - 1].append(copy.deepcopy(pool2[randomint - 1]))
        layer += 1
    print(map2)
    # Secondary layout generator
    layout = [["LU", "U", "U"],
              ["", "", ""],
              ["LD", "D", "D"]]
    # Options:
    # L=left closed
    # R=right closed
    # U=up closed
    # D=down closed
    cx = 0
    # Places 2 "R" in every column
    for _ in range(3):
        for _ in range(2):
            # Variable to randomly choose which paths will be closed off
            columnclose = random.randint(0, 2)
            # Adds to layout
            if columnclose == 0:
                layout[0][cx] += "R"
            elif columnclose == 1:
                layout[1][cx] += "R"
            elif columnclose == 2:
                layout[2][cx] += "R"
        cx += 1
    print("", layout[0], "\n", layout[1], "\n", layout[2], "\n")


def generate_map2():
    # Checks paths starting from first column in the middle
    dy = 1
    dx = 0
    # Checks every column
    for _ in range(3):
        # checks every row
        for _ in range(3):
            if dy == 3:
                dy = 0
            if dx > 0:
                # If a left entrance is closed, the room to the left has its right entrance closed
                if "L" in layout[dy][dx]:
                    layout[dy][dx - 1] += "R"
            if dx < 2:
                # If a right entrance is closed, the room to the right has its left entrance closed
                if "R" in layout[dy][dx]:
                    layout[dy][dx + 1] += "L"
            if dy > 0:
                # If above entrance is closed, the room above has its down  entrance closed
                if "U" in layout[dy][dx]:
                    layout[dy - 1][dx] += "D"
            if dy < 2:
                # If below entrance is closed, the room below has its up entrance closed
                if "D" in layout[dy][dx]:
                    layout[dy + 1][dx] += "U"
            dy += 1
            if dx == 3:
                dx = 2
        dx += 1
    print("", layout[0], "\n", layout[1], "\n", layout[2], "\n")


def generate_map3():
    # Modifies map based on layout
    global ey, ex
    ey = 0
    ex = 0
    # Modifies every room in the map to have entrances closed based on layout map array
    for _ in range(3):
        for _ in range(3):
            if "L" in layout[ey][ex]:
                map[ey][ex][3][0] = LW1
                map[ey][ex][4][0] = LW1
                map[ey][ex][5][0] = LW1
            if "R" in layout[ey][ex]:
                map[ey][ex][3][10] = RW1
                map[ey][ex][4][10] = RW1
                map[ey][ex][5][10] = RW1
            if "U" in layout[ey][ex]:
                map[ey][ex][0][5] = BW1
            if "D" in layout[ey][ex]:
                map[ey][ex][8][5] = FW1
            ex += 1
            if ex == 3:
                ex = 0
        ey += 1

# Loads maps
def load_map():
    global loaditem, collideboxes, movelayer, moveroom
    collideboxes = []
    row = 1
    item = 0
    loaditem = map[movelayer][moveroom]
    if moveroom == -1:
        loaditem = roomS

    for _ in range(9):
        for _ in range(11):
            item += 1
            loadimage = loaditem[row - 1][item - 1]
            imag = pygame.image.load(loadimage).convert()
            image = pygame.transform.scale(imag, (64, 64))
            Display.blit(image, (item * 64 - 64, row * 64 - 64))
            if loadimage != FT1 and loadimage != FT2 and loadimage != FT3:
                collidebox = pygame.draw.rect(Surface, transparent, pygame.Rect(item * 64 - 64, row * 64 - 64, 64, 64))
                collideboxes.append(collidebox)
        item = 0
        row += 1


# Player character sprite
def player_character():
    global sprcontrol, sprcount, playerx, flip, playery, playerbox, playerattackbox, playerattackboxflip, direction, playerhp, playerdmg, playerAIdot, playerAIx, playerAIy
    playerimag = pygame.image.load("Player Sprites/PlayerAnim" + str(sprcontrol) + ".png").convert()
    playerimag2 = pygame.transform.scale(playerimag, (64, 64))
    playerimag2.convert_alpha()
    playerimag2.set_colorkey(0, 255)
    playerimag2flip = pygame.transform.flip(playerimag2, True, False)
    #Player hitboxes
    playerbox = pygame.Rect(playerx + 16, playery + 50, 32, 10)
    playerattackbox = pygame.Rect(playerx + 64, playery, 64, 64)
    playerattackboxflip = pygame.Rect(playerx - 64, playery, 64, 64)
    #Player dot used for AI tracking
    playerAIx = playerx + 32
    playerAIy = playery + 32
    playerAIdot = pygame.Rect(playerAIx, playerAIy, 1, 1)
    keys = pygame.key.get_pressed()
    # Detecting key presses
    if gameover == 1:
        pass
    else:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = "L"
                playerx -= movespeed
                if playerbox.collidelist(collideboxes) != -1:
                    playerx += movespeed
                flip = True
            elif event.key == pygame.K_RIGHT:
                direction = "R"
                playerx += movespeed
                flip = False
            elif event.key == pygame.K_UP:
                direction = "U"
                playery -= movespeed
            elif event.key == pygame.K_DOWN:
                direction = "D"
                playery += movespeed
    # Checks for collsiions with the walls(collideboxes)
    if playerbox.collidelist(collideboxes) != -1:
        if direction == "L":
            playerx += movespeed
        if direction == "R":
            playerx -= movespeed
        if direction == "U":
            playery += movespeed
        if direction == "D":
            playery -= movespeed

    if flip == True:
        Display.blit(playerimag2flip, (playerx, playery))
    else:
        Display.blit(playerimag2, (playerx, playery))


    sprcount += 1
    if sprcount == 15:
        sprcontrol += 1
        sprcount = 0
    if sprcontrol == 5:
        sprcontrol = 1


# Detection for room traversal
def Roomtraversal():
    global playerx, playery, movelayer, moveroom, enemyspawnlayer, enemyspawnroom, loaditem, floorcomplete
    #If there are enemies in the room, you cant go to a different room
    if lockedroom == True:
        if playerbox.colliderect(Left_box) or playerbox.colliderect(Right_box) or playerbox.colliderect(Up_box) or playerbox.colliderect(Down_box):
            Display.blit(lock, locktxt)
    #Going to a different room if there are no enemies in the room
    else:
        if playerbox.colliderect(Left_box):
            playerx = 630
            playery = 256
            moveroom -= 1
            enemyspawnroom -= 1
        elif playerbox.colliderect(Right_box):
            playerx = 10
            playery = 256
            moveroom += 1
            enemyspawnroom += 1
            if moveroom == 3:
                floorcomplete = 1
                moveroom = 2
            elif moveroom == 3:
                moveroom = 2
        elif playerbox.colliderect(Up_box):
            playerx = 320
            playery = 502
            movelayer -= 1
            enemyspawnlayer -= 1
        elif playerbox.colliderect(Down_box):
            playerx = 320
            playery = 10
            movelayer += 1
            enemyspawnlayer += 1
        if moveroom == -1 and (movelayer == 0 or movelayer == 2):
            moveroom = 0
        if (playerbox.colliderect(Down_box) or playerbox.colliderect(Up_box)) and (loaditem == roomS):
            moveroom = -1
            movelayer = 1


# Button Class, Just add:(text,textsize,xpos,ypos,width,height)
class Button:
    # Initialising attributes
    def __init__(self, text, textsize, textx, texty, xpos, ypos, width, height):
        self.text = text
        self.textx = textx
        self.texty = texty
        self.textsize = textsize
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height

    # Initialising Methods
    def draw(self):
        pos = pygame.mouse.get_pos()
        font = pygame.font.Font('freesansbold.ttf', self.textsize)
        button_text = font.render(self.text, True, green)
        button_rect = pygame.rect.Rect((self.xpos, self.ypos), (self.width, self.height))
        pygame.draw.rect(Display, black, pygame.Rect(self.xpos - 1, self.ypos - 1, self.width + 2, self.height + 2))
        # Makes it so that if button is hovered over, visual feedback is given
        if button_rect.collidepoint(pos):
            button_text = font.render(self.text, True, slgreen)
        else:
            button_text = font.render(self.text, True, green)
        # If button is clicked, it turns red
        if self.checkclick():
            pygame.draw.rect(Display, coolred, button_rect)
            button_text = font.render(self.text, True, slcoolred)
        else:
            if button_rect.collidepoint(pos):
                pygame.draw.rect(Display, slcoolgreen, button_rect)
            else:
                pygame.draw.rect(Display, coolgreen, button_rect)
        # Places text at X and Y coordinates proportional to a third of the button size
        Display.blit(button_text, (self.textx, self.texty))

    # Used to check if button is pressed or released
    def checkclick(self):
        pos = pygame.mouse.get_pos()
        button_rect = pygame.rect.Rect((self.xpos, self.ypos,), (self.width, self.height))
        if button_rect.collidepoint(pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
            elif event.type == pygame.MOUSEBUTTONUP:
                return False


# Enemy class(skeleton)
class Enemy():
    def __init__(self, maxhealth, damage, enemyx, enemyy):
        self.maxhealth = maxhealth
        self.damage = damage
        self.enemyx = enemyx
        self.enemyy = enemyy
        self.enemysprcontrol = 1
        self.enemysprcount = 0
        self.enemyflip = False
        self.alive = True
        self.health = self.maxhealth
        self.attackcooldown = 15
        self.aliveconfirm = 1

    def draw(self):
        global hpbarx, invincibleframe, attackcooldown, enemyclearconfirm, currency
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            self.alive = False
        enemyimag = pygame.image.load(f"Enemy Sprites/EnemyAnim{self.enemysprcontrol}.png").convert()
        enemyimag = pygame.transform.scale(enemyimag, (64, 64))
        enemyimag.convert_alpha()
        enemyimag.set_colorkey(0, 255)
        enemyimagflip = pygame.transform.flip(enemyimag, True, False)
        #Checks if the enemy is not alive
        if self.alive == False:
            if self.aliveconfirm == 1:
                self.aliveconfirm = 0
                enemyclearconfirm += 1
                currency += (5*floor)
                print(enemyclearconfirm)
        # Runs if eveny is alive
        elif self.alive == True:
            # Dot used for tracking enemy position for the AI
            enemyAIx = self.enemyx+32
            enemyAIy = self.enemyy+32
            enemyAIdot = pygame.Rect(enemyAIx, enemyAIy, 1, 1)
            # Enemy sight radius
            enemyradius = pygame.Rect(self.enemyx-128, self.enemyy-128, 320, 320)
            #Enemy hitboxes
            enemybox = pygame.Rect(self.enemyx, self.enemyy, 64, 64)
            enemycollidebox = pygame.Rect(self.enemyx + 16, self.enemyy + 50, 32, 10)
            if self.enemyflip == True:
                Display.blit(enemyimagflip, (self.enemyx, self.enemyy))
            else:
                Display.blit(enemyimag, (self.enemyx, self.enemyy))

            #Enemy Healthbars
            pygame.draw.rect(Display, black, pygame.Rect(self.enemyx, self.enemyy-15, 64, 10))
            pygame.draw.rect(Display, coolred, pygame.Rect(self.enemyx+2, self.enemyy-13, 60, 6))
            pygame.draw.rect(Display, coolgreen, pygame.Rect(self.enemyx+2, self.enemyy-13, 60*(self.health/self.maxhealth), 6))

            #AI calculations for making enemy move towards player
            if playerbox.colliderect(enemyradius):
                if enemyAIx-playerAIx > 0:
                    self.enemyx -= 1
                if enemyAIx-playerAIx < 0:
                    self.enemyx += 1
                if enemyAIy-playerAIy > 0:
                    self.enemyy -= 1
                if enemyAIy-playerAIy < 0:
                    self.enemyy += 1

            # Checks for collisions with enemies
            if playerbox.colliderect(enemybox) and invincibleframe == 60:
                hpbarx -= self.damage
                invincibleframe = 0
            elif invincibleframe < 60:
                invincibleframe += 1

            #Attacks have a 0.5 second cooldown
            if self.attackcooldown >= 15:
                # Checks for playerattack hitboxes colliding with the enemy hitbox and deducs hp from the enemy if true
                # Checks attacks using the hitbox when player is turned to the right(normal direction sprites)
                if event.type == pygame.MOUSEBUTTONDOWN and flip == False:
                    if playerattackbox.colliderect(enemybox):
                        self.enemyx += 10
                        self.enemyy += (random.randint(-3, 3))
                        self.health -= playerdmg
                        self.attackcooldown = 0
                #Checks attacks using the hitbox when player is turned to the left(flipped sprite)
                elif event.type == pygame.MOUSEBUTTONDOWN and flip == True:
                    if playerattackboxflip.colliderect(enemybox):
                        self.enemyx -= 10
                        self.enemyy += (random.randint(-3,3))
                        self.health -= playerdmg
                        self.attackcooldown = 0
            elif self.attackcooldown < 15:
                self.attackcooldown += 1

            #Cycles between animation frames
            self.enemysprcount += 1
            if self.enemysprcount == 15:
                self.enemysprcontrol += 1
                self.enemysprcount = 0
            if self.enemysprcontrol > 4:
                self.enemysprcontrol = 1


def enemyspawn():
    global enemies
    collide = True
    enemies = []
    for _ in range(random.randint(1,5)):
        collide = True
        while collide == True:
            randomx = random.randint(64, 576)
            randomy = random.randint(64, 448)
            enemycollide = pygame.Rect(randomx, randomy, 64, 64)
            if enemycollide.collidelist(collideboxes) != -1:
                collide = True
            else:
                collide = False
        enemies.append(Enemy(20+(floor*25),5+(floor*5) , randomx, randomy))

#Displays enemies on screen
def enemydraw():
    enemycount = 0
    while enemycount < len(enemies):
        enemies[enemycount].draw()
        enemycount += 1

#Controls when enemies can spawn
def enemyspawncontrol():
    global lockedroom, enemyclearconfirm
    if enemyspawnroom == -1 or enemyspawnroom == 3:
        pass
    else:
        if enemymap[enemyspawnlayer][enemyspawnroom] == "E":
            enemyspawn()
            enemymap[enemyspawnlayer][enemyspawnroom] = "C"
            lockedroom = True
        if enemyclearconfirm == len(enemies):
            lockedroom = False
            enemyclearconfirm = 0
        if moveroom == -1:
            pass
        else:
            enemydraw()

loop = True
while loop:
    left, middle, right = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            loop = False

    if menu == 1:
        # Printing the UI elements for the menu
        Display.fill(white)
        Display.blit(backimage2, (0, 0))
        titleimage = pygame.image.load("dungeondashers.png").convert()
        titleimage2 = pygame.transform.scale(titleimage, (400, 150))
        Display.blit(titleimage2, (150, 35))
        # Buttons(text,textsize,textx,texty,xpos,ypos,width,height)
        Play_button = Button('Play', 25, 328, 260, 282, 232, 150, 75)
        Play_button.draw()
        #Menu button for upgrades menu
        Upgrades_button = Button('Upgrades', 25, 300, 358, 282, 332, 150, 75)
        Upgrades_button.draw()
        # What the buttons do when clicked
        if Play_button.checkclick() == False:
            #Resets some variables to start all over again
            menu = 0
            lockedroom = False
            chosenupgrade = 0
            #The default player stats which can be boosted by permanent upgrades
            maxhpbarx = defaultmaxhp + (permmaxhp * 10)
            hpbarx = maxhpbarx
            playerdmg = defaultplayerdmg + (permstrength * 5)
            movespeed = defaultmovespeed + permmovespeed
            enemyspawnlayer = 1
            enemyspawnroom = -1
            enemyclearconfirm = 0
            floor = 1
        #Checks if upgrades button is pressed
        if Upgrades_button.checkclick() == False:
            upgradesmenu = 1
        if upgradesmenu == 1:
            upgrades()
    else:
        # Printing the UI elements for ingame
        if loadcontrol == 0:
            loading()
        else:
            if newmap == 1:
                generate_map()
                generate_map2()
                generate_map3()
                newmap = 0
            load_map()
            # Exit button(text,textsize,textx,texty,xpos,ypos,width,height)
            Exit_button3 = Button('X', 35, 662, 15, 654, 10, 40, 40)
            Exit_button3.draw()
            #For displaying the money counter
            pygame.draw.rect(Display, black, pygame.Rect(10, 60, 84, 44))
            pygame.draw.rect(Display, gold, pygame.Rect(12, 62, 80, 40))
            money = "$" + str(currency)
            balance2 = font5.render(money, True, dgold)
            balancetxt2 = balance2.get_rect()
            balancetxt2.center = (53, 82)
            Display.blit(balance2, balancetxt2)
            # Hitboxes
            hitboxleft()
            hitboxright()
            hitboxup()
            hitboxdown()
            # Player
            if hpbarx <= 0:
                hpbarx = 0
            player_character()
            # Enemy
            enemyspawncontrol()
            #Tutorial
            tutorial()
            # For dungeon upgrades you get every floor
            dungeonupgrade()
            # Function for when you want to exit the dungeon and click the Exit button3
            Quitdungeon()
            playerhpbar()
            Roomtraversal()
            if floorcomplete == 1:
                floorwinner()
            Gameover()
    # Refreshes display
    pygame.display.flip()
    pygame.time.Clock().tick(fps)


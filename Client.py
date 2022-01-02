import pygame
from Network import network

pygame.font.init()

width = 600
height = 730
red = (255, 0, 0)
pathColour = (100, 100, 100)
coordX = width / 2
coordY = 0
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
coordLists = [[300, 0, 0], [300, 30, 1], [300, 60, 2]]
backgroundColourRed = (255, 50, 50)
backgroundColourBlue = (0, 0, 255)
btnText = ""
backDrawn= False

class Button:
    def __init__(self, text, x, y, colour, buttonWidth, buttonHeight):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = buttonWidth
        self.height = buttonHeight

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, player, pos):
    global backDrawn
    if not (game.connected()):
        win.fill(backgroundColourBlue)
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Waiting for player...", True, (255, 0, 0), False)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        drawBackGround(window,game)
        for i in game.Enemies:
            i.draw(window)
        for i in game.Defenders:
            i.draw(window)
        if game.selected and player == 1:
            if btnText == "Kare":
                pygame.draw.rect(window, (255, 255, 255), pygame.Rect(pos[0], pos[1], 30, 30))
            elif btnText == "Daire":
                pygame.draw.circle(window, (255, 255, 255), pos, 12, 12)
            elif btnText == "Ucgen":
                pygame.draw.polygon(window, (255, 255, 255),
                                    [(pos[0] + 5, pos[1] + 25), (pos[0] + 15, pos[1] + 5), (pos[0] + 25, pos[1] + 25)])

        if player == 0:
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render("Attacker",False, (255, 0, 0), False)
            health = font.render("HP: "+str(game.player0H),False, (255,0,0))
            win.blit(text, (10, 120))
            win.blit(health,(150, 120))
        elif player ==1:
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render("Defender", False, (255, 0, 0), False)
            health = font.render("HP: "+str(game.player1H),False, (255,0,0))
            win.blit(text, (10, 120))
            win.blit(health,(150,120))
    pygame.display.update()


button = [Button("Back", 10, 10, (250, 0, 0), 250, 100), Button("Ucgen", 400, 0, (255, 0, 0), 100, 30),
          Button("Kare", 400, 35, (0, 255, 0), 100, 30), Button("Daire", 400, 70, (0, 0, 255), 100, 30),
          Button("del", 400, 105, (0, 0, 0), 100, 30)]


def drawBackGround(win, game):
    window.fill((0, 0, 0))
    for i in game.coordLists:
        pygame.draw.rect(window, pathColour, pygame.Rect(i[0], i[1], 30, 30))
    for btn in button:
        btn.draw(win)


def mainLoop():
    global btnText
    loop = True
    clock = pygame.time.Clock()
    n = network()
    player = int(n.getPlayer())
    print("player : ", player)
    while loop:
        clock.tick(60)
        try:
            try:
                pos = pygame.mouse.get_pos()
            except:
                pass
            game = n.sendStr("continue")
        except:
            loop = False
            print("Cant connect")
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in button:
                    if btn.click(pos) and game.connected():
                        if btn.text == "Back":
                            loop = False
                            break
                        else:
                            if player == 1:
                                btnText = btn.text
                                n.sendStr(btn.text + "T")
                            else:
                                n.sendStr(btn.text)
            elif game.selected and player == 1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pos = pygame.mouse.get_pos()
                        data = btnText + "D" + " " + str(pos[0]) + " " + str(pos[1])
                        n.sendStr(data)

        redrawWindow(window, game, player, pos)


def menuScreen(win):
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill(backgroundColourRed)
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Click to Play!", True, (0, 0, 0))
        win.blit(text, (100, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
            else:
                pass
        pygame.display.update()
    mainLoop()


while True:
    menuScreen(window)

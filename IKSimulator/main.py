import pygame, math, sys
from ai import AirHockeyAI
from code import InteractiveConsole
from threading import Thread
from model.line import Line
from model.point import Point
from model.circle import Circle

SCREEN_RESOLUTION = (750, 750)

class Application:
    def __init__(self):
        self.running = True
        self.mousePos = (1, 1)

        self.ai = AirHockeyAI()

    """
    Initializes the appropriate stuff.
    Starts the main loop.
    """
    def start(self):
        pygame.init()
        self.font = pygame.font.Font(None, 24)
        self.running = True
        self.initDisplay()

        self.consoleThread = Thread(target=self.startInteractiveShell)
        self.consoleThread.setDaemon(True)
        self.consoleThread.start()

        self.loop()

    """
    Starts interactive console.
    ai variable avaliable from console.
    """
    def startInteractiveShell(self):
        vars = globals()
        ai = self.ai

        p1 = Point(0, 0)
        p2 = Point(10, 10)
        l1 = Line(p1, p2)

        p1 = Point(1, 1)
        p2 = Point(11, 11)
        l2 = Line(p1, p2)

        p1 = Point(0, 0)
        c1 = Circle(p1, 2)

        vars.update(locals())
        shell = InteractiveConsole(vars)
        shell.interact()

    """
    See self.loop comment
    """
    def stop(self):
        self.running = False

    """
    Initializes the display with the appropriate screen resolution
    Called in self.start
    """
    def initDisplay(self):
        self.surface = pygame.display.set_mode(SCREEN_RESOLUTION)
        pygame.display.set_caption('Air Hockey Robot Simulation')

    """
    Main Loop
    Loops until self.running == false
    """
    def loop(self):
        while self.running:
            self.surface.fill((0, 0, 0))          #Fills display with white
            self.handleEvents()                         #Handles events

            self.drawQuadrants()
            self.drawArmAndMallet()
            self.drawAngleValues()

            pygame.display.flip()                       #Draws display buffer to display



        """
        Quitting procedure.
        """
        pygame.quit()
        sys.exit(0)

    """
    Handles pygame events.
    """
    def handleEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.MOUSEMOTION:
                self.mousePos = event.dict["pos"]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()

    def polarToCartesian(self, length, angle):
        x = length * math.cos(math.radians(angle))
        y = length * math.sin(math.radians(angle))
        return(x, y)

    def drawArmAndMallet(self):

        base = (0, 0)
        target = fromPygame(self.mousePos)

        """Gets angle to the midarm"""
        self.globalBaseAngle = self.ai.getBaseAngle(target)

        """Gets angle to the end arm"""
        self.globalMidArmAngle = self.ai.getMidArmAngle(target)

        """Deals with the coordinate mid arm"""
        midArm = self.polarToCartesian(self.ai.upperArmLength, self.globalBaseAngle)

        """ Deals with the coordinate for the end of the arm: essentially mathematical version of target"""
        cart = self.polarToCartesian(self.ai.lowerArmLength, self.globalMidArmAngle)
        endArm = midArm[0]+cart[0], midArm[1]+cart[1]

        pygame.draw.circle(self.surface, (255,0,0), (int(toPygame(endArm)[0]), int(toPygame(endArm)[1])), 20)
        pygame.draw.line(self.surface, (0, 255, 255), toPygame(base), toPygame(midArm), 3)
        pygame.draw.line(self.surface, (0, 255, 0), toPygame(midArm), toPygame(endArm), 3)

    def drawQuadrants(self):
        pygame.draw.line(self.surface, (255, 0, 0), (0, SCREEN_RESOLUTION[1]/2), (SCREEN_RESOLUTION[0], SCREEN_RESOLUTION[1]/2))
        pygame.draw.line(self.surface, (255, 0, 0), (SCREEN_RESOLUTION[0]/2, 0), (SCREEN_RESOLUTION[0]/2, SCREEN_RESOLUTION[1]))

    def drawAngleValues(self):
        baseAngle = self.globalBaseAngle
        midArmAngle = self.globalMidArmAngle

        baseAngleText = self.font.render("Base Servo Angle: " + str(baseAngle), True, (255,255,255))
        baseAngleTextBox = baseAngleText.get_rect()
        baseAngleTextBox.centerx = self.surface.get_rect().centerx
        self.surface.blit(baseAngleText, baseAngleTextBox)

        midAngleText = self.font.render("Elbow Servo Angle: " + str(midArmAngle - baseAngle + 360), True, (255,255,255))
        midAngleTextBox = midAngleText.get_rect()
        midAngleTextBox.centerx = self.surface.get_rect().centerx
        midAngleTextBox.centery += 30
        self.surface.blit(midAngleText, midAngleTextBox)

        targetText = self.font.render("Target Pos: " + str(fromPygame(self.mousePos)), True, (255,255,255))
        targetTextBox = targetText.get_rect()
        targetTextBox.centerx = self.surface.get_rect().centerx
        targetTextBox.centery += 60
        self.surface.blit(targetText, targetTextBox)



"""
Essentially makes the origin in the centre of the window, rather than top right.
"""
def toPygame(pos):
    return pos[0]+SCREEN_RESOLUTION[0]/2, (-pos[1]+SCREEN_RESOLUTION[1]/2)

def fromPygame(pos):
    return pos[0]-SCREEN_RESOLUTION[0]/2, -(pos[1]-SCREEN_RESOLUTION[1]/2)

"""
If this file was not imported, then start the application's code.
"""
if __name__ == "__main__":
    app = Application()
    app.start()
import pygame
import math

#Konstantos

PLOTIS, AUKSTIS = 800, 800
STULPAS, EILES = 8, 8
LANGAS = AUKSTIS//STULPAS
FPS = 60
APSKRITIMAS = 20

#Spalvos

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (210, 43, 43)
BROWN = (110, 38, 14)
PURPLE = ( 255, 0, 255)

class Zaidimas:
    def __init__(self):
        self.busena = "on"
        self.zaidejas = ["x", "o"]
        self.pasirinkimas = None
        self.ejimas = 1
        self.lenta =      [['x','-','x','-','x','-','x','-'],
                           ['-','x','-','x','-','x','-','x'],
                           ['x','-','x','-','x','-','x','-'],
                           ['-','-','-','-','-','-','-','-'],
                           ['-','-','-','-','-','-','-','-'],
                           ['-','o','-','o','-','o','-','o'],
                           ['o','-','o','-','o','-','o','-'],
                           ['-','o','-','o','-','o','-','o']]
        self.suolis = False
        self.x = 0
        self.y = 0

# Tikrina paspaudima

    def paspaudimas(self, pele):
        if self.busena == "on":
            eil, stu = xasis(pele), yasis(pele)
            # print(self.lenta[eil][stu])
            # print(eil, stu)
            if self.pasirinkimas:
                eiti = self.leidimas(self.zaidejas[self.ejimas % 2], self.pasirinkimas, eil, stu)
                if eiti[0]:
                    self.veiksmas(self.zaidejas[self.ejimas % 2], self.pasirinkimas, eil, stu, eiti[1])
                elif eil == self.pasirinkimas[0] and stu == self.pasirinkimas[1]:
                    self.pasirinkimas = None
                    if self.suolis:
                        self.suolis = False 
                        self.ejimogalas()
                else:
                    print("Negalimas veiksmas")
            else:
                if self.lenta[eil][stu] == self.zaidejas[self.ejimas % 2]:
                    self.pasirinkimas = [eil,stu]   
        elif self.busena == "Pabaiga":
            self.__init__() 
            
# Tikrina ar galimas veiksmas

    def leidimas(self, zaidejo, lokacija, ieile, istulp):
        iseiles = lokacija[0]
        isstulp = lokacija[1]
        if self.lenta[ieile][istulp] != '-':
            return False, None
        if(((zaidejo == "x" and ieile - iseiles == 1) or 
            (zaidejo == "o" and iseiles - ieile == 1)) and 
            abs(isstulp - istulp) == 1) and not self.suolis:
             return True, None
        if(((zaidejo == "x" and ieile - iseiles == 2) or 
            (zaidejo == "o" and iseiles - ieile == 2)) and 
            abs(isstulp - istulp) == 2):
            eile = round((ieile - iseiles) / 2 + iseiles)
            stulp = round((istulp - isstulp) / 2 + isstulp)
            if self.lenta[eile][stulp] not in [zaidejo, "-"]:
                return True, [eile, stulp]
        return False, None

# Atlieka veiksma

    def veiksmas(self, zaidejo, lokacija, ieile, istulp, suolis):
        iseiles = lokacija[0]
        isstulp = lokacija[1]
        laik = self.lenta[iseiles][isstulp]
        self.lenta[ieile][istulp] = laik
        self.lenta[iseiles][isstulp] = "-"
        if(zaidejo == "x" and ieile == 7) or (zaidejo == "o" and ieile == 0):
            self.lenta[ieile][istulp] = laik
        if suolis:
            self.lenta[suolis[0]][suolis[1]] = "-"
            self.pasirinkimas = [ieile, istulp]
            self.suolis = True
        else:
            self.pasirinkimas = None
            self.ejimogalas()
        laimetojas = self.arlaimejo()
        if laimetojas is None:
            pass
        elif laimetojas == "Lygiosios":
            pygame.display.set_caption("Lygiosios, paspausk ant lentos jei nori pradeti is pradziu")
            self.busena = 'Pabaiga'
        elif laimetojas == "x":
            pygame.display.set_caption("Juodi laimejo, paspausk ant lentos jei nori pradeti is pradziu")
            self.busena = 'Pabaiga'
        else:
            pygame.display.set_caption("Balti laimejo, paspausk ant lentos jei nori pradeti is pradziu")
            self.busena = 'Pabaiga'

# Ejimo uzbaigimas

    def ejimogalas(self):
        self.ejimas += 1
        if(self.zaidejas[self.ejimas % 2]) == "o":
            pygame.display.set_caption("Balto ejimas")
        else:
            pygame.display.set_caption("Juodo ejimas")
        
# Tikrinam ar laimejo kazkas

    def arlaimejo(self):
        x = sum([row.count('x') for row in self.lenta])
        if x == 0:
            return 'o'
        o = sum([row.count('o') for row in self.lenta])
        if o == 0:
            return 'x'
        if x == 1 and o == 1:
            return 'Lygiosios'
        return None

# Lentos piesimas

    def piesti(self, vaizdas):
        vaizdas.fill(RED)
        for eile in range(EILES):
            for stulp in range(eile % 2, EILES, 2):
                pygame.draw.rect(vaizdas, BROWN, (eile*LANGAS, stulp*LANGAS,LANGAS, LANGAS))
        for e in range(len(self.lenta)):
            for s in range(len(self.lenta[e])):
                saske = self.lenta[e][s]
                if saske != '-':
                    if saske == 'x':
                        spalva = BLACK
                    elif saske == "o":
                        spalva = WHITE
                    if self.pasirinkimas:
                        if self.pasirinkimas[0] == e and self.pasirinkimas[1] == s:
                            spalva = PURPLE
                    self.x = LANGAS * e + LANGAS // 2
                    self.y = LANGAS * s + LANGAS // 2
                    pygame.draw.circle(vaizdas, spalva, (self.y, self.x), 40)
    


run = True
vaizdas = pygame.display.set_mode((PLOTIS, AUKSTIS))
zaisti = Zaidimas()

# Koordinates

def yasis(pele):
    x = pele[0]
    for i in range(1,8):
        if x < i * PLOTIS / 8:
            return i -1
    return 7

def xasis(pele):
    y = pele[1]
    for i in range(1,8):
        if y < i * AUKSTIS / 8:
            return i - 1
    return 7

# Zaidimo loopas

while run:
    for veiksmas in pygame.event.get():
        if veiksmas.type == pygame.QUIT:
            run = False
        
        if veiksmas.type == pygame.MOUSEBUTTONDOWN:
            zaisti.paspaudimas((pygame.mouse.get_pos()))
            

    zaisti.piesti(vaizdas)
    pygame.display.update()

pygame.quit()

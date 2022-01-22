# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:30 2022

@author: rapha
"""
from vaisseau import vaisseau
from projectile import projectile

# --- Classe du vaisseau controllé par le joueur --- # 
class joueur(vaisseau):
    def __init__(self,gui,couleur, posX, posY, tag, entities):
        super().__init__(gui, couleur, posX, posY, tag)
        self.__couleur="bleu"
        #self.__difficulte=difficulte
        self.__entities=entities
        self.stats = (3, 1, 0)
        self.__vitesse=5
        self.__ally = []
        self.__can_shoot = True
        self.__enemies = entities[1]
        
    def set_entities(self, new_entities):
        self.__entities = new_entities
    def get_entities(self):
        return(self.__entities)
    def del_entities(self):
        del self.__entities
    entities = property(get_entities, set_entities, del_entities, 'Enemy seen from the player Property')
    
    
    def bonus(self,genre):
       if genre == "pv":
           self.__pv+=1
       elif genre == "dmg":
           self.__dmg+=1
           
    def get_ally(self):
        print("ally gain")
        gui = self.get_gui()
        (posX, posY) = self.pos
        print(self.__ally)
        if len(self.__ally) == 0 and len(self.__ally) != 1 :
            self.__ally.append(vaisseau(gui, "orange", posX, posY, "ally")) #Rajoute l'alié à l'attribut liste d'allié
            self.__ally[0].sprite = "Ally_Ship.png"
            self.__ally[0].follow((-1, self)) #Assure que l'allié suit le joueur
        elif len(self.__ally) == 1 and len(self.__ally) < 2:
            #ally = vaisseau(canevas, "orange", posX +40, posY, "ally")
            self.__ally.append(vaisseau(gui, "orange", posX, posY, "ally")) #Rajoute l'alié à l'attribut liste d'allié
            self.__ally[1].sprite = "Ally_Ship.png"
            self.__ally[1].follow((1, self)) #Assure que l'allié suit le joueur
            
    def mvmtP(self,event):
        (self.__posX, self.__posY) = self.pos
        gui = self.get_gui()
        canevas = gui.get_canevas()
        if event.keysym == 'Right':
            if self.__posX < 900:
                self.__posX += 20
                self.pos = (self.__posX, self.__posY)
                canevas.move("player", +20, 0)
        if event.keysym == 'Left':
            if self.__posX > 40:
                self.__posX -= 20
                self.pos = (self.__posX, self.__posY)
                canevas.move("player", -20, 0)
                #canevas.coords(self.__rectangle , self.__posX -20, self.__posY -20, self.__posX +20, self.__posY +20)
        if event.keysym == 'space':
            if self.__can_shoot == True:
                bullet = projectile(gui, self.__posX, self.__posY, 0, 'green', self.__entities)
                bullet.friendlyroutine()
                if len(self.__ally) != 0:
                    for a in self.__ally:
                        (posX_ally, posY_ally) = a.pos
                        ally_bullet = projectile(gui, a.pos[0], a.pos[1], 0, 'Orange', self.__entities)
                        ally_bullet.friendlyroutine()
                self.__can_shoot = False
                canevas.after(500, self.timer)
            
    def timer(self):
        self.__can_shoot = True

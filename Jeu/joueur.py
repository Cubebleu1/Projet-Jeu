# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:30 2022
Classe du vaisseau controllé par le joueur. On y retrouve des fonctions de déplacement rudimentaires (gauche/droite) et un tir
Le vaisseau devait normalement se déplacer en hauteur aussi, mais la fonction qui vérifiait si le vaisseau joueur entrait en
colision avec un des aliens n'a pas eut le temps d'être débuggée.

TO DO LIST :
    - Faire en sorte que le joueur puisse se déplacer en hauter aussi (+ conditions de défaite qui en découlent)
    - Possibilité d'esquiver rapidement une fois toutes les 5 secondes ? 
    
@author: Raphaël CAUDRON & Arthur JEZEQUEL
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
       
    # --- Ces fonctions permettent de récupérer/modifier les attributs de la classe joueur liés aux entités du jeu --- 
    def set_entities(self, new_entities):
        self.__entities = new_entities
    def get_entities(self):
        return(self.__entities)
    def del_entities(self):
        del self.__entities
    entities = property(get_entities, set_entities, del_entities, 'Enemy seen from the player Property')
    
     
    #Cette fonction permet au joueur d'obtenir un alié s'il a tué le bonus. Il peut en avaoir jusqu'à 2.      
    def get_ally(self):
        gui = self.get_gui()
        (posX, posY) = self.pos
        if len(self.__ally) == 0 and len(self.__ally) != 1 :
            self.__ally.append(vaisseau(gui, "orange", posX, posY, "ally")) #Rajoute l'alié à l'attribut liste d'allié
            self.__ally[0].sprite = "images/Ally_Ship.png"
            self.__ally[0].follow((-1, self)) #Assure que l'allié suit le joueur
        #Si on a déjà un alié, on en rajoute un deuxième
        elif len(self.__ally) == 1 and len(self.__ally) < 2:
            self.__ally.append(vaisseau(gui, "orange", posX, posY, "ally"))
            self.__ally[1].sprite = "images/Ally_Ship.png"
            self.__ally[1].follow((1, self))
        #Si on a déjà 2 aliés, rien ne se passe
            
    #Cette fonction représente le mouvement du joueur. Elle prend en argument la touche sur laquelle l'utilisateur appuye
    def mvmtP(self,event):
        (self.__posX, self.__posY) = self.pos
        gui = self.get_gui()
        canevas = gui.get_canevas()
        #Si l'on appuye sur la flèche droite, on va a droite
        if event.keysym == 'Right':
            if self.__posX < 900:
                self.__posX += 20
                self.pos = (self.__posX, self.__posY)
                canevas.move("player", +20, 0)
        #Si l'on appuye sur la flèche droite, on va a gauche
        if event.keysym == 'Left':
            if self.__posX > 40:
                self.__posX -= 20
                self.pos = (self.__posX, self.__posY)
                canevas.move("player", -20, 0)
        #Si l'on appuye sur la barre d'espace, on va a tir !
        if event.keysym == 'space':
            if self.__can_shoot == True:
                bullet = projectile(gui, self.__posX, self.__posY, 0, 'green', self.__entities)
                bullet.friendlyroutine()
                if len(self.__ally) != 0:
                    for a in self.__ally:
                        (posX_ally, posY_ally) = a.pos
                        ally_bullet = projectile(gui, a.pos[0], a.pos[1], 0, 'Orange', self.__entities)
                        ally_bullet.friendlyroutine()
                #Pour éviter de pouvoir tirer en boucle, on rajoute une variable qui fait office de timer
                self.__can_shoot = False
                canevas.after(500, self.timer)
    
    #Au bout de 0,5 secondes, on peut de nouveau tirer 
    def timer(self):
        self.__can_shoot = True

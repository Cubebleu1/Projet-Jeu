# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:31 2022

@author: rapha
"""

class projectile :
    def __init__(self, gui, POSX, POSY, angle, couleur, tout):
        self.__couleur = couleur 
        self.__angle = angle
        self.__gui = gui
        self.__canevas = gui.get_canevas()
        
        self.__player = tout[0]
        self.__enemies = tout[1]
        self.__protection = tout[2]
        self.__posX = POSX
        self.__posY = POSY
        self.__rectangle = self.__canevas.create_rectangle(self.__posX-2, self.__posY-5, self.__posX+5, self.__posY+2, tags="projo", width ='1', outline =couleur, fill=couleur)
    
    #Cette fonction régi le comportement d'un projectile hostile
    def routine(self):
        if self.__posY < 640 and self.__posY > 0: #On vérifie que le projectile est toujours dans le canevas
            self.__posY += 20
            self.__canevas.coords(self.__rectangle , self.__posX -2, self.__posY -5, self.__posX +2, self.__posY +5)
            #self.__canevas.update()
            if (self.__posY <  self.__player._vaisseau__posY +20 and self.__posY > self.__player._vaisseau__posY - 20) and (self.__posX > self.__player._vaisseau__posX - 20 and self.__posX < self.__player._vaisseau__posX + 20) :
                #On rentre dans cette boucle quand le projectile entre en contact avec le joueur
                self.__player.stats = (self.__player.stats[0] -1, self.__player.stats[1], self.__player.stats[2])
                self.__gui.set_lives(self.__player.stats[0]) #Le nombre de vie est mis à jour
                self.__canevas.delete(self.__rectangle)
            self.__canevas.after(30, self.routine)   #La fonction s'appelle récursivement                                 
        else :
            self.__canevas.delete(self.__rectangle)
    
    def get_pos(self):
        return ([self.__posX, self.__posY])
    def set_pos(self, pos):
        (self.__posX, self.__posY) = pos    
    def del_pos(self):
        del self.__posX
        del self.__posY     
    pos = property(get_pos, set_pos, del_pos, 'Position Property')
    
    def get_rectangle(self):
        return(self.__rectangle)
    
    #Cette fonction régi le comportement d'un projectile alié
    def friendlyroutine(self):
        Alien = self.__enemies
        #print(Alien, 'begin')
        if self.__posY < 640 and self.__posY > 0: 
            self.__posY -= 20
            self.__canevas.coords(self.__rectangle , self.__posX -5, self.__posY -5, self.__posX +5, self.__posY +5)
            self.is_enemy_shot()
            # for t in Alien:
            #     (posX, posY) = t.pos
            #     if (self.__posY <  posY +20 and self.__posY > posY - 20) and (self.__posX > posX - 20 and self.__posX < posX + 20) :
            #         #self.__canevas.delete(t.get_rectangle())
            #         print('touché :)')
            #         if t.stats[0] == 1: #Si l'ennemi n'avait plus que un point de vie, il meurt
            #             self.__canevas.delete(t.sprite)
            #             t.is_alive = False
            #             Alien.remove(t)
            #             self.__canevas.delete(self.get_rectangle())                        
            #             self.__gui.set_score(self.__gui.get_score() + t.stats[2])
            #             del t
            #         else:  #Si l'ennemi a plus que d'un point de vie, il en pert un mais continue d'exister
            #             self.__canevas.delete(self.get_rectangle())
            #             t.stats = (t.stats[0]-1, t.stats[1], t.stats[2])
            #             print(t.stats)
            #         return(None)  #pour sortir de la fonction et arreter le projectile
            self.is_projo_shot()
            self.__canevas.after(30, self.friendlyroutine) 
        else :
            self.__canevas.delete(self.__rectangle)

    def is_enemy_shot(self):
        for t in self.__enemies:
            (posX, posY) = t.pos
            if (self.__posY <  posY +20 and self.__posY > posY - 20) and (self.__posX > posX - 20 and self.__posX < posX + 20) :
                #self.__canevas.delete(t.get_rectangle())
                print('touché :)')
                if t.stats[0] == 1: #Si l'ennemi n'avait plus que un point de vie, il meurt
                    self.__canevas.delete(t.sprite)
                    t.is_alive = False
                    self.__enemies.remove(t)
                    self.__canevas.delete(self.get_rectangle())                        
                    self.__gui.set_score(self.__gui.get_score() + t.stats[2])
                    del t
                else:  #Si l'ennemi a plus que d'un point de vie, il en pert un mais continue d'exister
                    self.__canevas.delete(self.get_rectangle())
                    t.stats = (t.stats[0]-1, t.stats[1], t.stats[2])
                    print(t.stats)
                return(None)  #pour sortir de la fonction et arreter le projectile
            
    def is_projo_shot(self):
        for t in self.__protection:
            (posX, posY) = t.pos
            if (self.__posY <  posY +20 and self.__posY > posY - 20) and (self.__posX > posX - 20 and self.__posX < posX + 20) :
                #self.__canevas.delete(t.get_rectangle())
                print('touché :)')
                if t.stats == 1: #Si l'ennemi n'avait plus que un point de vie, il meurt
                    self.__canevas.delete(t.sprite)
                    t.is_alive = False
                    self.__protection.remove(t)
                    self.__canevas.delete(self.get_rectangle())                        
                    del t
                else:  #Si l'ennemi a plus que d'un point de vie, il en pert un mais continue d'exister
                    self.__canevas.delete(self.get_rectangle())
                    t.stats = t.stats-1
                    print(t.stats)
                return(None)  #pour sortir de la fonction et arreter le projectile
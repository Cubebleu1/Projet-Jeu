# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:05:31 2022
Cette classe est celle du jeu dans sa globalité : on y retrouve la gestion des entités, de leur création et de leur mouvement,
mais aussi toutes les fonctions qui permettent au jeu de fonctionement convenablement : gestion des niveaux, des conditions de victoire
ou d'echec.

TO DO LIST :
    - Optimiser tout cela !!
    - Implémenter plusieurs modes de jeu ou de difficulté
    - Plus de niveaux
    - Un semblant de trame scénaristique
    - Ca pourrait être super sympa d'avoir un fond différent à chaque niveau ! 
    - Plus d'animations ! (explosions, ect...)
    - DE LA MUSIQUE.

@author: Raphaël CAUDRON & Arthur JEZEQUEL
"""
from random import choices
import tkinter as tk
from PIL import Image, ImageTk
from joueur import joueur
from ilot import ilot
from mechantTire import mechantTire
from mechant import mechant
from bonusMechant import bonusMechant
from final_boss import final_boss
from bonusJeu import bonusJeu
#joueur ilot mechantTire bonusMechant mechant final_boss 

class game :
    def __init__(self, gui):
        self.__gameover = True
        self.__reverse = False
        self.__enemies = []
        self.__bonus = []
        self.__boss = []
        self.__protections = []
        self.__enemies_cara = []
        self.__level = 0
        self.__number_of_enemies = 0
        self.__enemies_per_line = 0
        self.__mode = 0
        self.__player = None
        self.__gui = gui
        self.__canevas = gui.get_canevas()
        
    # --- Game Properties --- #
        
    def get_entities(self):
        return([self.__player, self.__enemies, self.__protections, self.__bonus, self.__boss])
    def set_entities(self, entities):
        (self.__player, self.__enemies, self.__protections, self.__bonus, self.__boss) = entities   
    def del_entities(self):
        del self.__player
        del self.__enemies
        del self.__protections
        del self.__bonus
        del self.__boss
    entities = property(get_entities, set_entities, del_entities, 'Entities Property')
           
    def get_game_state(self):
        return([self.__gameover, self.__reverse, self.__level, self.__mode])
    def set_game_state(self, new_state):
        (self.__gameover, self.__reverse, self.__level, self.__mode) = new_state 
    def del_game_state(self):
        del self.__gameover
        del self.__reverse
        del self.__level
        del self.__mode
    game_state = property(get_game_state, set_game_state, del_game_state, 'Game Property')
        
    def get_level_state(self):
        return([self.__enemies_cara, self.__enemies_per_line, self.__number_of_enemies])
    def set_level_state(self, new_state):
        (self.__enemies_cara, self.__enemies_per_line, self.__number_of_enemies) = new_state     
    def del_level_state(self):
        del self.__enemies_per_line
        del self.__number_of_enemies
        del self.__enemies_cara
    level_state = property(get_level_state, set_level_state, del_level_state, 'Level Property')

    # --- Fonctions de déroulement du jeu --- #  
    
    #Cette fonction initie le début du jeu
    def game_begin(self):
        if self.__gameover == True :
            self.__canevas.delete('Greetings')
            self.__gui.set_lives(3)
            self.__gameover = False #Le jeu commence, et donc il n'y a plus "gameover"
            self.__enemies = []
            self.__player = joueur(self.__gui, "blue", 470, 620, "player", self.entities) #création d'un joueur
            self.__canevas.bind('<Key>', self.__player.mvmtP) #On bind le canevas au mouvement du vaisseau joueur
            
            #Chaque niveau a un nombre d'ennemis différents, jusqu'a à un boss final
            if self.__level == 0:
                self.__enemies_per_line = 7
                self.__number_of_enemies = 21
                self.__enemies = self.create_enemies()
                self.__bonus.append(bonusJeu(self.__gui, 'green', 20, -100, "bonus", self.entities))
                self.__protections.append(ilot(self.__gui, game, self.entities, 800, 525))
                self.__protections.append(ilot(self.__gui, game, self.entities, 150, 525))                
                self.__player.entities = self.entities #Mise à jour des enemis percus par le joueur
                self.whole_behavioral()
            elif self.__level == 1:
                self.__enemies_per_line = 10
                self.__number_of_enemies = 40
                self.__enemies = self.create_enemies()
                self.__bonus.append(bonusJeu(self.__gui, 'green', 20, -100, "bonus", self.entities))
                self.__protections.append(ilot(self.__gui, game, self.entities, 800, 525))
                self.__protections.append(ilot(self.__gui, game, self.entities, 150, 525))
                self.__player.entities = self.entities
                self.whole_behavioral()
            elif self.__level == 2:
                self.__enemies_per_line = 10
                self.__number_of_enemies = 80
                self.__enemies = self.create_enemies()
                self.__bonus.append(bonusJeu(self.__gui, 'green', 20, -100, "bonus", self.entities))
                self.__protections.append(ilot(self.__gui, game, self.entities, 800, 525))
                self.__protections.append(ilot(self.__gui, game, self.entities, 150, 525))                
                self.__player.entities = self.entities
                self.whole_behavioral()
            elif self.__level == 3:
                self.__enemies_per_line = 10
                self.__number_of_enemies = 40
                self.__enemies = self.create_enemies() 
                self.__boss.append(final_boss(self.__gui, 'osef', 470, 300, 'boss', self.entities))   
                self.__boss[0].final_boss_sprite() 
                self.__protections.append(ilot(self.__gui, game, self.entities, 800, 525))
                self.__protections.append(ilot(self.__gui, game, self.entities, 150, 525))   
                self.__player.entities = self.entities 
                self.whole_behavioral()                         
        else :
            return(None)
        
    #Cette fonction permet de créer les enemis de manière aléatoire au début des niveaux 
    def create_enemies(self):
        enemies = []
        L = []
        nbLignes = self.__number_of_enemies//self.__enemies_per_line #nombre de lignes
        for l in range(nbLignes):
            for k in range(self.__enemies_per_line):
                enemy_type = choices([0, 1, 2], weights=(40, 40, 20), k=1)[0] #Chaque entier représente un type d'enemi
                L.append([self.__gui,"red",60*(k+1),60*(-l+1), "enemy", enemy_type]) 
        #On sort par ligne le nombre de méchants désirés, L contient les attributs de chaque alien
        target = self.__player
        for k in range(self.__number_of_enemies):
            caraAlien=L.pop()
            if caraAlien[5] == 0:
                enemies.append(mechant(caraAlien[0],caraAlien[1],caraAlien[2],caraAlien[3], caraAlien[4]))
                enemies[k].set_sprite("images/AlienVert.png")
            elif caraAlien[5] == 1:
                enemies.append(mechantTire(caraAlien[0],caraAlien[1],caraAlien[2],caraAlien[3], caraAlien[4], self.entities))
                enemies[k].set_sprite("images/RedAlien.png")
            elif caraAlien[5] == 2:
                enemies.append(bonusMechant(caraAlien[0],caraAlien[1],caraAlien[2],caraAlien[3], caraAlien[4], self.entities))
                enemies[k].set_sprite("images/BlackAlien.png")
            #canevas.after(100, ligne[k].behavior)
        return(enemies)


    
    def restart(self):
        self.__gameover = True
        self.__canevas.delete("enemy")
        for e in self.__enemies:
            e.is_alive = False
        for e in self.__boss:
            e.is_alive = False
        self.__bonus=[]
        self.__enemies=[]
        self.__protections=[]
        self.__boss=[]
        self.__canevas.delete("projo")
        self.__canevas.delete("text")
        self.__canevas.delete("player")
        self.__canevas.delete("boss")
        self.__canevas.delete("bonus")
        self.__level = 0
        self.__gui.set_score(0)
        self.__gui.set_lives(3)
        self.__canevas.after(400, self.game_begin)
        
    def whole_behavioral(self):
        print("behavioral started")
        self.clockmove()
        self.check_victory()
        self.check_defeat()
        for m in self.__enemies:
            m.behavior()
        for m in self.__boss:
            m.behavior()
        for m in self.__bonus:
            m.behavior()

    # --- Fonctions de mouvement des entités --- #
    
    #Fonctions qui permet aux enemis de base de se déplacer de manière synchronisée et "retro"
    def clockmove(self):
        if self.__gameover == False:
            if self.check_limit(): 
                pass #on vérifie que les enemis ne sont pas en dehors du canevas, si ils le sont, ils changent de sens et sautent une ligne
            else :
                #On modifie les coordonnées des enemis pour qu'elles s'accordent au déplacement de leur sprite
                for m in self.__enemies:
                    alien = m
                    (posX, posY) = alien.pos
                    if self.__reverse == False:
                        #posX += 10
                        alien.pos = (posX +10, posY)
                    elif self.__reverse == True:
                        #posX -= 10
                        alien.pos = (posX-10, posY)                            
                #On déplace tous les sprites des enemies de manière synchronisée
                if not self.__reverse:
                    self.__canevas.move("enemy", 10, 0)
                elif self.__reverse :
                    self.__canevas.move("enemy", -10, 0)
            self.__canevas.after(200, self.clockmove)
            #sans lambda, la fonction clockmove est éxécutée en boucle sans fin et sans temporalisation (le .after n'a aucun effet)
        elif self.__gameover == True : 
            return(None)
        
    #Cette fonction permet aux enemis de sauter une ligne et donc d'avancer vers le joueur
    def jump(self, dir):
        self.__canevas.move("enemy", dir*40, 40)
        for m in self.__enemies:
            if dir == 1:
                (posX, posY) = m.pos
                m.pos = (posX+40, posY + 40)
            elif dir == -1:
                (posX, posY) = m.pos
                m.pos = (posX-40, posY + 40)

    #C'est cette fonction qui vérifie que les ennemis ne sont pas hors du canevas
    def check_limit(self):
        for m in self.__enemies:
            (posX, posY) = m.pos
            if posY >= 580:
                self.__player.stats = (0,0, 0)
                return(False)
            elif posX > 900:
                self.__reverse = not self.__reverse 
                self.jump(-1)
                return(True)
            elif posX < 30:
                self.__reverse = not self.__reverse
                self.jump(1)
                return(True)
    
    #Cette fonction vérifie les conditions de victoire (tous les enemis ont été vaincus) tout le long du jeu !
    def check_victory(self):
        if self.__gameover == True :
            return(None)
        elif self.__level == 3:
            if self.__boss==[] and self.__enemies == []:
                self.__gameover = True
                self.__player.is_alive = False 
                self.__canevas.delete(self.__player.sprite)
                self.__canevas.delete("protec")
                self.__canevas.delete("ally")
                victory = self.__canevas.create_text(475,320,fill="yellow",font="Times 40 italic bold", text="CONGRATULATIONS !", tag="text")               
                return(None)
            else :
                self.__canevas.after(50, self.check_victory)
        elif self.__enemies == []:
            self.__bonus = []
            self.__protections = []
            self.__player.is_alive = False
            self.__canevas.delete("ally")
            self.__canevas.delete("protec")
            self.__canevas.delete(self.__player.sprite)
            victory = self.__canevas.create_text(475,320,fill="yellow",font="Times 40 italic bold", text="Get ready for the next level", tag="text")
            self.__canevas.after(2000, lambda:self.__canevas.delete(victory))
            self.__level += 1
            self.__gameover = True
            self.__canevas.after(4000, lambda:self.__canevas.delete("text"))
            self.__canevas.after(4500, self.game_begin)
        else :
            self.__canevas.after(50, self.check_victory)
            
    #Cette fonction vérifie les conditions de défaite(les pv du joueur sont à 0) tout le long du jeu !
    def check_defeat(self):
        if self.__player.stats[0] == 0 :
            self.__player.is_alive = False
            for e in self.__enemies:
                e.is_alive = False
            self.__canevas.delete("enemy")
            self.__canevas.delete("projo")
            self.__canevas.delete("text")
            self.__canevas.delete("protec")
            self.__canevas.delete(self.__player.sprite)
            self.__canevas.delete("ally")
            self.__canevas.create_text(475,320,fill="red",font="Times 40 italic bold", text="DEFEAT", tag="text")
        else:
            self.__canevas.after(200, self.check_defeat)
            

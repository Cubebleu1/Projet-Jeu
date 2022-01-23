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
from joueur import joueur
from ilot import ilot
from mechantTire import mechantTire
from mechant import mechant
from bonusMechant import bonusMechant
from final_boss import final_boss
from bonusJeu import bonusJeu 

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
        
    # --- Si besoin, ces fonctions permettent de récuperer/modifier les entités dynamiques du jeu     
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
   
    # --- Si besoin, ces fonctions permettent de récuperer/modifier l'état du jeu (en cours ou non, niveau, mode)      
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
        
    # --- Si besoin, ces fonctions permettent de récuperer/modifier l'état du niveau et de ses enemis
    def get_level_state(self):
        return([self.__enemies_cara, self.__enemies_per_line, self.__number_of_enemies])
    def set_level_state(self, new_state):
        (self.__enemies_cara, self.__enemies_per_line, self.__number_of_enemies) = new_state     
    def del_level_state(self):
        del self.__enemies_per_line
        del self.__number_of_enemies
        del self.__enemies_cara
    level_state = property(get_level_state, set_level_state, del_level_state, 'Level Property')
 
    
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
        L = [] #L est la pile qui contiendra les informations sur les enemis générés aléatoirement
        nbLignes = self.__number_of_enemies//self.__enemies_per_line #nombre de lignes
        for l in range(nbLignes):
            for k in range(self.__enemies_per_line):
                enemy_type = choices([0, 1, 2], weights=(40, 40, 20), k=1)[0] #Chaque entier représente un type d'enemi
                L.append([self.__gui,"red",60*(k+1),60*(-l+1), "enemy", enemy_type]) 
        #On sort par ligne le nombre de méchants désirés, L contient les attributs de chaque alien
        target = self.__player
        for k in range(self.__number_of_enemies):
            caraAlien=L.pop()
            #En fonction du type d'alien, on crée des objets de classes différentes
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

    #Cette fonction réinitialise le jeu : toute entité est éffacée, et le niveau retourne à 0 
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
        self.__player._vaisseau__ally=[]
        self.__canevas.delete("ally")
        self.__canevas.delete("projo")
        self.__canevas.delete("text")
        self.__canevas.delete("protec")
        self.__canevas.delete("player")
        self.__canevas.delete("boss")
        self.__canevas.delete("bonus")
        self.__level = 0
        self.__gui.set_score(0)
        self.__gui.set_lives(3)
        self.__canevas.after(400, self.game_begin)
        
    #Cette fonction active la fonction comportementale (behavior) de chaque entité dynamique, mais inite aussi les fonctions
    #qui vérifient l'état du jeu (echec ou victoire)
    def whole_behavioral(self):
        self.clockmove() #mouvement des ennemis
        self.check_victory() #Vérification continue de si le joueur a gagné...
        self.check_defeat() #... ou perdu
        for m in self.__enemies:
            m.behavior()
        for m in self.__boss:
            m.behavior()
        for m in self.__bonus:
            m.behavior()

    
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
                #On déplace tous les sprites des ennemis de manière synchronisée
                if not self.__reverse:
                    self.__canevas.move("enemy", 10, 0)
                elif self.__reverse :
                    self.__canevas.move("enemy", -10, 0)
            self.__canevas.after(200, self.clockmove)
        elif self.__gameover == True : 
            return(None)
        
    #Cette fonction permet aux ennemis de sauter une ligne et donc d'avancer vers le joueur
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
            #Si les enemis sont trop proches du joueur, on considére qu'il a perdu : ses points de vie atteignent 0
            if posY >= 580:
                self.__player.stats = (0,0, 0)
                return(False)
            #En fonction de si les enemis touchent le bord droit ou gauche du canevas, on modifie la valeur de reverse
            #qui défini si les enemis vont à droite ou à gauche dans clockmove
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
        #Les conditions de victoire du niveau 3 sont spéciales : il faut avoir vaincu le boss
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
        #Dans les niveaux 0 à 2, si les ennemis sont tous vaincus, alors le joueur gagne et on passe au niveau suivant.
        elif self.__enemies == []:
            #On pense bien à reinitialiser l'état du jeu avant de passer au niveau suivant,et effacer toutes les entitiés du niveau précédent
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
            #Si le joueur a perdu, tout est reinitialisé, les entités sont éffacés et il faut appuyer sur recommencer
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
            

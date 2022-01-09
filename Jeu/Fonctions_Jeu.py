#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:43:08 2021

@author: arthur.jezequel
"""
#import Jeu
import tkinter as tk
from PIL import ImageTk, Image
from random import randint, choices

GameOver = True
Reverse = False
Ligne = 0
Alien = []
Level = 0

class game :
    def __init__(self, gui):
        self.__gameover = True
        self.__reverse = False
        self.__enemies = []
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
        return([self.__player, self.__enemies])
    def set_entities(self, entities):
        (self.__player, self.__enemies) = entities   
    def del_entities(self):
        del self.__player
        del self.__enemies
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
            self.__gameover = False #Le jeu commence, et donc il n'y a plus "gameover"
            self.__enemies = []
            self.__player = joueur(self.__gui, "blue", 470, 620, "player") #création d'un joueur
            self.__canevas.bind('<Key>', self.__player.mvmtP) #On bind le canevas au mouvement du vaisseau joueur
            
            #Chaque niveau a un nombre d'ennemis différents, jusqu'a à un boss final
            if self.__level == 0:
                self.__enemies_per_line = 7
                self.__number_of_enemies = 21
                self.__enemies = self.create_enemies()
                self.__player.enemies = self.entities[1] #Mise à jour des enemis percus par le joueur
                self.whole_behavioral()
            elif self.__level == 1:
                self.__enemies_per_line = 10
                self.__number_of_enemies = 40
                self.__enemies = self.create_enemies()
                self.__player.enemies = self.entities[1]
                self.whole_behavioral()
            elif self.__level == 2:
                self.__enemies_per_line = 10
                self.__number_of_enemies = 80
                self.__enemies = self.create_enemies()
                self.__player.enemies = self.entities[1]
                self.whole_behavioral()
            elif self.__level == 3:
                self.__enemies.append(final_boss(self.__gui, 'pink', 475, 300, "enemy", self.__player))
                self.__enemies[0].final_boss_sprite()
                self.__player.enemies = self.entities[1]
                self.__enemies[0].behavior()
                self.clockmove()
                self.check_victory()
                self.check_defeat()
        else :
            return(None)
        
    #Cette fonction permet de créer les enemis de manière aléatoire au début des niveaux 
    def create_enemies(self):
        7 #nombre d'aliens par ligne
        enemies = []
        L = []
        nbLignes = self.__number_of_enemies//self.__enemies_per_line #nombre de lignes
        print(nbLignes)
        for l in range(nbLignes):
            for k in range(self.__enemies_per_line):
                #enemy_type = randint(0, 2)
                enemy_type = choices([0, 1, 2], weights=(40, 40, 20), k=1)[0] #Chaque entier représente un type d'enemi
                print(enemy_type)
                L.append([self.__gui,"red",60*(k+1),60*(-l+1), "enemy", enemy_type]) 
        #On sort par ligne le nombre de méchants désirés, L contient les attributs de chaque alien
        target = self.__player
        for k in range(self.__number_of_enemies):
            caraAlien=L.pop()
            if caraAlien[5] == 0:
                enemies.append(mechant(caraAlien[0],caraAlien[1],caraAlien[2],caraAlien[3], caraAlien[4]))
                enemies[k].set_sprite("AlienVert.png")
            elif caraAlien[5] == 1:
                enemies.append(mechantTire(caraAlien[0],caraAlien[1],caraAlien[2],caraAlien[3], caraAlien[4], target))
                enemies[k].set_sprite("RedAlien.png")
            elif caraAlien[5] == 2:
                enemies.append(bonusMechant(caraAlien[0],caraAlien[1],caraAlien[2],caraAlien[3], caraAlien[4], target))
                enemies[k].set_sprite("BlackAlien.png")
            #canevas.after(100, ligne[k].behavior) 
        return(enemies)
        
    def display_enemies(self, L):
        target = self.__player
        for k in range(self.__number_of_enemies):
            caraAlien=L.pop()
            self.__enemies.append(mechantTire(caraAlien[0],caraAlien[1],caraAlien[2],caraAlien[3], caraAlien[4], target))

            #canevas.after(100, ligne[k].behavior) 

    
    def restart(self):
        self.__gameover = True
        self.__canevas.delete("enemy")
        for e in self.__enemies:
            e.is_alive = False
        self.__canevas.delete("projo")
        self.__canevas.delete("player")
        self.__level = 0
        self.game_begin()
        
    def whole_behavioral(self):
        print("behavioral started")
        self.clockmove()
        self.check_victory()
        self.check_defeat()
        for m in self.__enemies:
            m.behavior()

    # --- Fonctions de mouvement des entités --- #
    
    #Fonctions qui permet aux enemis de base de se déplacer de manière synchronisée et "retro"
    def clockmove(self):
        if self.check_limit(): 
            pass #on vérifie que les enemis ne sont pas en dehors du canevas, si ils le sont, ils changent de sens et sautent une ligne
        else :
            #On modifie les coordonnées des enemis pour qu'elles s'accordent au déplacement de leur sprite
            for m in self.__enemies:
                (posX, posY) = m.pos
                if self.__reverse == False:
                    posX += 10
                    m.pos = (posX, posY)
                elif self.__reverse == True:
                    posX -= 10
                    m.pos = (posX, posY)
            #On déplace tous les sprites des enemies de manière synchronisée
            if not self.__reverse:
                self.__canevas.move("enemy", 10, 0)
            elif self.__reverse :
                self.__canevas.move("enemy", -10, 0)
        self.__canevas.after(300, self.clockmove)
        #sans lambda, la fonction clockmove est éxécutée en boucle sans fin et sans temporalisation (le .after n'a aucun effet)
        
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
            if posX > 900:
                self.__reverse = not self.__reverse 
                self.jump(-1)
                return(True)
            elif posX < 60:
                self.__reverse = not self.__reverse
                self.jump(1)
                return(True)
    
    #Cette fonction vérifie les conditions de victoire (tous les enemis ont été vaincus) tout le long du jeu !
    def check_victory(self):
        if self.__gameover == True :
            return(None)
        elif self.__enemies == []:
            self.__player.is_alive = False
            self.__canevas.delete("ally")
            self.__canevas.delete(self.__player.sprite)
            victory = self.__canevas.create_text(475,320,fill="yellow",font="Times 40 italic bold", text="Get ready for the next level", tag="text")
            self.__canevas.after(2000, lambda:self.__canevas.delete(victory))
            self.__level += 1
            self.__canevas.after(4000, lambda:self.__canevas.delete("text"))
            self.__canevas.after(4500, self.game_begin)
        else :
            self.__canevas.after(50, self.check_victory)
            
    #Cette fonction vérifie les conditions de défaite(les pv du joueur sont à 0) tout le long du jeu !
    def check_defeat(self):
        if self.__player.stats[0] == 0:
            self.__player.is_alive = False
            for e in self.__enemies:
                e.is_alive = False
            self.__canevas.delete("enemy")
            self.__canevas.delete("projo")
            self.__canevas.delete("ally")
            self.__canevas.delete("text")
            self.__canevas.delete(self.__player.sprite)
            self.__canevas.create_text(475,320,fill="red",font="Times 40 italic bold", text="DEFEAT", tag="text")
            self.__gameover = True
        else:
            self.__canevas.after(50, self.check_defeat)
            
        

class GUI:
    def __init__(self, fenetre):
        self.__fenetre = fenetre
        
        self.__background = ImageTk.PhotoImage(file = 'Background.png')
        self.__canevas = tk.Canvas(self.__fenetre, width = 2*470, height = 2*320, bg ='darkblue')
        self.__canevas.create_image(0,0, anchor=tk.NW, image = self.__background)
        self.__canevas.focus_set()
        self.__canevas.pack(padx = 5, pady = 5)
        
        self.__exit_btn = tk.Button(self.__fenetre, text = 'Quitter', command = self.__fenetre.destroy)
        self.__exit_btn.pack(side = 'left', padx = 5, pady = 5)
        
        self.__game = game(self)
        self.__start_btn = tk.Button(self.__fenetre, text = 'Jouer', command =  self.__game.game_begin)
        self.__start_btn.pack(side = 'left', padx = 5, pady = 5)
        
        self.__reset_btn = tk.Button(self.__fenetre, text = 'Recommencer', command = self.__game.restart)
        self.__reset_btn.pack(side = 'left', padx = 5, pady = 5)

        #Vies & Score
        self.__main_frame = tk.Frame(self.__fenetre)
        self.__main_frame.pack(side ='right')
        self.__score = tk.StringVar()
        self.__score.set('Score : 0')
        self.__score_int = 0
        self.__score_label = tk.Label(self.__main_frame, textvariable=self.__score).pack(side = 'right', padx = 10, pady = 10)
        self.__lives = tk.StringVar()
        self.__lives.set('Vies : 3')
        self.__lives_label = tk.Label(self.__main_frame, textvariable=self.__lives).pack(side = 'right', padx = 10, pady = 10)
        
        self.__fenetre.mainloop()
        
    def set_score(self, new_score):
        self.__score.set("Score : " + str(new_score))
        self.__score_int = new_score
        
    def get_score(self):
        return(self.__score_int)
    def set_lives(self, new_lives):
        self.__lives.set("Lives : " + str(new_lives))
        
    def get_canevas(self):
        return(self.__canevas)


class vaisseau : ### ON PEUT VIRER COULEUR NON ?###
    def __init__(self,gui,couleur, posX, posY, tag):
        self.__alive = True
        self.__type = "None"
        self.__pv=0
        self.__dmg=0
        self.__gui = gui
        self.__canevas = gui.get_canevas()
        self.__tag = tag
        self.__couleur=couleur
        self.__points=0
        self.__posX = posX
        self.__posY = posY
        #self.__rectangle = self.__canevas.create_rectangle(self.__posX-20, self.__posY-20, self.__posX+20, self.__posY+20, tags = self.__tag, width ='1', outline =couleur)
        self.__sprite = ImageTk.PhotoImage((Image.open("PlayerSpaceShip.png")).resize((40,40), Image.ANTIALIAS))
        self.__display = self.__canevas.create_image(self.__posX -20,self.__posY-20, anchor=tk.NW, image=self.__sprite, tag = self.__tag)

    def follow(self, localisation):
        (direction, target_to_folow) = localisation
        (self.__posX, self.__posY) = target_to_folow.pos
        #self.__posX = target_to_folow[0]
        #self.__posY = target_to_folow[1]
        self.__canevas.coords(self.__display , self.__posX +60*direction, self.__posY -60)
        #canevas.coords(self.__rectangle , self.__posX -20, self.__posY -20, self.__posX +20, self.__posY +20)
        self.pos = (self.__posX +60*direction, self.__posY)
        self.__canevas.after(10, lambda : self.follow(localisation))
        #print(self.pos, "vue display")
        #sans lambda, la fonction follow est éxécutée en boucle sans fin et sans temporalisation (le .after n'a aucun effet)

     
    # --- Properties --- #
    def get_pos(self):
        return ([self.__posX, self.__posY])
    def set_pos(self, pos):
        (self.__posX, self.__posY) = pos       
    def del_pos(self):
        del self.__posX
        del self.__posY
    pos = property(get_pos, set_pos, del_pos, 'Position Property')
    
    def set_sprite(self, sprite_localisation):
        self.__canevas.delete(self.__display)
        self.__sprite = ImageTk.PhotoImage((Image.open(sprite_localisation)).resize((40,40), Image.ANTIALIAS))
        self.__display = self.__canevas.create_image(self.__posX -20,self.__posY-20, anchor=tk.NW, tag=self.__tag, image=self.__sprite)
    def get_sprite(self):
        return(self.__display)
    def del_sprite(self):
        del self.__display
    sprite = property(get_sprite, set_sprite, del_sprite, 'Sprite Property')
    
    def get_gui(self):
        return(self.__gui)
    
    def get_stats(self):
        return([self.__pv, self.__dmg, self.__points])
    def set_stats(self, new_stats):
        (self.__pv, self.__dmg, self.__points) = new_stats
    stats = property(get_stats, set_stats, None, 'Stats Property')
        
    
    def get_alive(self):
        return(self.__alive)
    def set_alive(self, Bool):
        self.__alive = Bool
    is_alive = property(get_alive, set_alive, None, 'Alive or not ?')
    
    
    
    
# --- Classe du vaisseau controllé par le joueur --- # 
class joueur(vaisseau):
    def __init__(self,gui,couleur, posX, posY, tag):
        super().__init__(gui, couleur, posX, posY, tag)
        self.__couleur="bleu"
        #self.__difficulte=difficulte
        self.stats = (3, 1, 0)
        self.__vitesse=5
        self.__ally = []
        self.__enemies = []
    #def pdv(self):
        #if joueur.difficulte == "NM":
            #self.__pv = 3
        #elif joueur.difficulte == "HCM":
            #self.__pv = 1
        #else:
            #self.__pv = 999
    
    def set_enemies(self, new_enemies):
        self.__enemies = new_enemies
    def get_enemies(self):
        return(self.__enemies)
    def del_enemies(self):
        del self.__enemies
    enemies = property(get_enemies, set_enemies, del_enemies, 'Enemy seen from the player Property')
    
    
    def bonus(self,genre):
       if genre == "pv":
           self.__pv+=1
       elif genre == "dmg":
           self.__dmg+=1
           
    def get_ally(self):
        gui = self.get_gui()
        canevas = gui.get_canevas()
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
        if event.keysym == 'Up':
            if self.__posY > 60 :
                self.__posY -= 20
                self.pos = (self.__posX, self.__posY)
                canevas.move("player", 0, -20)
        if event. keysym == 'Down':
            if self.__posY < 600:
                self.__posY += 20
                self.pos = (self.__posX, self.__posY) #On réinjecte les bonnes coordonnées à l'aide du SETTER
                canevas.move("player", 0, +20)
        if event.keysym == 'space':
            bullet = projectile(gui, self.__posX, self.__posY, 0, 'green', self, self.__enemies)
            bullet.friendlyroutine()
            if len(self.__ally) != 0:
                for a in self.__ally:
                    (posX_ally, posY_ally) = a.pos
                    ally_bullet = projectile(gui, a.pos[0], a.pos[1], 0, 'Orange', self, self.__enemies)
                    ally_bullet.friendlyroutine()
        
            
            
# --- Classes des différents aliens --- #

#Mechant de base, il ne tire pas.
class mechant(vaisseau):
    def __init__(self, gui,couleur, POSX, POSY, tag):
        super().__init__(gui, couleur, POSX, POSY, tag)
        self.__img="alienNoir.jpg"
        self.stats = (1, 1, 10)
        
    def behavior(self):
        pass


#Mechant qui peut tirer et blesser le joueur.      
class mechantTire(vaisseau):
    def __init__(self, gui,couleur, posX, posY, tag, player):
        super().__init__(gui, couleur, posX, posY, tag)
        self.__type = "Shoot"
        self.__img="alienRouge.jpg"
        self.stats = (2, 1, 25)
        #self.__tirer=True
        self.__projectileC = gui.get_canevas()
        self.__player = player
    def shoot(self):
        if self.is_alive == True :
            bullet = projectile(self._vaisseau__gui, self._vaisseau__posX, self._vaisseau__posY, 0, 'yellow', self.__player, None)
            bullet.routine()
            self.__projectileC.after(3000, self.shoot)
        else:
            return(None)
    

    def behavior(self):
        self.shoot()
    
#Classe du boss final, très dur a vaincre :(      
class final_boss(vaisseau):
    def __init__(self, gui, couleur, posX, posY, tag, player):
        super().__init__(gui, couleur, posX, posY, tag)
        self.__gui = gui
        self.__canevas = gui.get_canevas()
        self.stats = (40, 2, 5000)
        self.__player = player
        self.__posX = self.pos[0]
        self.__posY = self.pos[1]
    
    def final_boss_sprite(self):
        self.__canevas.delete(self.get_sprite())
        self.__sprite = ImageTk.PhotoImage((Image.open("BossGalaga.png")).resize((200,200), Image.ANTIALIAS))
        self.__display = self.__canevas.create_image(self.__posX -20,self.__posY-20, anchor=tk.CENTER, tag="Boss", image=self.__sprite)
    
    def spawn_minions(self):
        print('ye')
        minion = mechantTire(self.__gui, 'red', 100, 40, "enemy", self.__player )
        minion.set_sprite("RedAlien.png")
        self.__canevas.after(3000, self.spawn_minions)
        
    def super_shoot(self):    
        if self.is_alive == True :
            bullet1 = projectile(self.__gui, self.__posX -4, self.__posY, 2, 'orange', self.__player, None )
            bullet1.routine()
            bullet2 = projectile(self.__gui, self.__posX - 30, self.__posY, 2, 'orange', self.__player, None )
            bullet2.routine()
            self.__canevas.after(3000, self.super_shoot)
        else:
            return(None)    
        
    def behavior(self):
        self.super_shoot()
        self.spawn_minions()

#Classe d'un méchant rapide qui offre un super bonus si vaincu       
class bonusMechant(mechantTire):
    def __init__(self, canevas, couleur, posX, posY, tag, player):
        super().__init__(canevas, couleur, posX, posY, tag, player)
        self.__img="alienViolet.jpg"
        self.stats = (4, 1, 50)
        self.__points=150
        
        
#Classe d'une entité inofensive mais qui offre un bonus temporaire lorsque vaincu
class bonusJeu(vaisseau):
    def __init__(self):
        self.__img="alienBonus.jpg"
        self.__couleur="jaune"
    def meurt(self):
        return self.__genre
    
    
#Ilot Protecteurs
class ilot(vaisseau):
    def __init__(self,grosseur):
        self.__img="obstacle2"
        self.__pv=4
        self.__grosseur=grosseur
        
    

 
        
class projectile :
    def __init__(self, gui, POSX, POSY, angle, couleur, player, enemies):
        self.__couleur = couleur 
        self.__angle = angle
        self.__gui = gui
        self.__canevas = gui.get_canevas()
        self.__player = player
        self.__enemies = enemies
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
                print('décès')
                self.__player.stats = (self.__player.stats[0] -1, self.__player.stats[1], self.__player.stats[2])
                self.__gui.set_lives(self.__player.stats[0]) #Le nombre de vie est mis à jour
                self.__canevas.delete(self.__rectangle)
            self.__canevas.after(70, self.routine)   #La fonction s'appelle récursivement                                 
        else :
            self.__canevas.delete(self.__rectangle)
            print('OOB')
    
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
            for t in Alien:
                (posX, posY) = t.pos
                if (self.__posY <  posY +20 and self.__posY > posY - 20) and (self.__posX > posX - 20 and self.__posX < posX + 20) :
                    #self.__canevas.delete(t.get_rectangle())
                    print('touché :)')
                    if t.stats[0] == 1: #Si l'ennemi n'avait plus que un point de vie, il meurt
                        self.__canevas.delete(t.sprite)
                        t.is_alive = False
                        Alien.remove(t)
                        self.__canevas.delete(self.get_rectangle())                        
                        self.__gui.set_score(self.__gui.get_score() + t.stats[2])
                        del t
                    else:  #Si l'ennemi a plus que d'un point de vie, il en pert un mais continue d'exister
                        self.__canevas.delete(self.get_rectangle())
                        t.stats = (t.stats[0]-1, t.stats[1], t.stats[2])
                        print(t.stats)
                    return(None)  #pour sortir de la fonction et arreter le projectile
            self.__canevas.after(30, self.friendlyroutine) 
        else :
            self.__canevas.delete(self.__rectangle)
            print('OOB')


def jeu(game, canevas, mode):
    (player, enemies) = game.entities
    (gameover, reverse, level, mode) = game.game_state
    if not gameover:
        return(None)
    elif gameover:
        game.game_begin()
        
def restart(game, canevas, mode):
    print('hey')
    
        
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:28 2022
Cette classe est celle de l'interface utilisateur (UI), et on y retrouve tout les procédés qui créent les
boutons et le canevas. On y a aussi les labels qui permettent l'affichage dynamique du score et des vies restantes

TO DO LIST:
    - Faire en sorte que le menu Mode servent à changer la difficulté (facile = 3 vies, diffcile = 1 vie)
    - Faire en sorte que le menu Option fonctionne (Key bindings et mode plein écran)
    
@author: Raphaël CAUDRON & Arthur JEZEQUEL
"""
import tkinter as tk
from PIL import ImageTk,Image
from game import game

class GUI:
    def __init__(self, fenetre):
        #Création de l'interface grâce à TKinter
        self.__fenetre = fenetre
        self.__menu_main = tk.Menu(self.__fenetre)
        
        self.__menu_options = tk.Menu(self.__menu_main, tearoff = 0)
        self.__menu_main.add_cascade(label="Options", menu=self.__menu_options)
        self.__menu_options.add_command(label = 'Controle', command = self.__fenetre.destroy)
        self.__menu_options.add_command(label = 'PleinEcran', command = self.__fenetre.destroy)

        self.__menu_game = tk.Menu(self.__menu_main, tearoff = 0)
        self.__menu_main.add_cascade(label ="Modes de Jeu", menu=self.__menu_game)
        self.__menu_game.add_command(label = 'Hardcore Mode', command = self.__fenetre.destroy)
        self.__menu_game.add_command(label = 'Easy Mode', command = self.__fenetre.destroy)

        self.__fenetre.config(menu = self.__menu_main)
        
        #Création du canevas
        self.__background = ImageTk.PhotoImage(file = 'images/Background.png')
        self.__canevas = tk.Canvas(self.__fenetre, width = 2*470, height = 2*320, bg ='darkblue')
        self.__canevas.create_image(0,0, anchor=tk.NW, image = self.__background)
        self.__canevas.focus_set()
        self.__canevas.pack(padx = 5, pady = 5)
        
        #Petit message de bienvenue sur le jeu
        self.__greetings = ImageTk.PhotoImage((Image.open("images/Greetings.png")).resize((750,440), Image.ANTIALIAS))
        self.__greetings_img = self.__canevas.create_image(450,300, anchor=tk.CENTER, tag="Greetings", image=self.__greetings)
        
        #Bouton pour quitter le jeu
        self.__exit_btn = tk.Button(self.__fenetre, text = 'Quitter', command = self.__fenetre.destroy)
        self.__exit_btn.pack(side = 'left', padx = 5, pady = 5)
        
        #Bouton pour lancer le jeu
        self.__game = game(self)
        self.__start_btn = tk.Button(self.__fenetre, text = 'Jouer', command =  self.__game.game_begin)
        self.__start_btn.pack(side = 'left', padx = 5, pady = 5)
        
        #Bouton pour redémarer la partie
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
        
    # --- Si besoin, ces fonctions permettent de récuperer/modifier le score ou le nombre de vie
    def set_score(self, new_score):
        self.__score.set("Score : " + str(new_score))
        self.__score_int = new_score   
    def get_score(self):
        return(self.__score_int)
    def set_lives(self, new_lives):
        self.__lives.set("Lives : " + str(new_lives))
        
    def get_canevas(self):
        return(self.__canevas)

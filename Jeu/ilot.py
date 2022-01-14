# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 15:08:31 2022

@author: rapha
"""

#Ilot Protecteurs
class ilot:
    def __init__(self, gui, grosseur, posX, posY):
        self.__img="obstacle2"
        self.__pv=4
        self.__gui = gui
        self.__canevas = gui.get_canevas()
        self.__grosseur=grosseur
        self.__posX = posX
        self.__posY = posY
        self.__rectangle = self.__canevas.create_rectangle(self.__posX-50, self.__posY-12, self.__posX+50, self.__posY+12, tags="protec", width ='1', outline ="grey", fill="grey")

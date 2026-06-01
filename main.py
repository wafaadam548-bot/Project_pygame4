import pygame as pg
class Player:
    def __init__(self,name,image):
        self.image=image
        self.name=name
player_one_name=Player(input())
player_image=Player(pg.image.load(" "))
print("hellow",player_one_name.name)    
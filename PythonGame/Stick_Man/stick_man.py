# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from tkinter import *
import random
import time

class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("MR. Stick Man Race for the Exit!")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width = 500, height = 500, highlightthickness = 0 )
        #self.canvas.pack()
        #self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        self.bg = PhotoImage(file="Draws/background.gif")
        self.bg2 = PhotoImage(file="Draws/background2.gif")
        w = self.bg.width()
        h = self.bg.height()
        w2 = self.bg2.width()
        h2 = self.bg2.height()
        for x in range(0, 5):
            for y in range(0, 5):
                if ((x +y)%2) == 0:
                    self.canvas.create_image(x * w, y * h, image=self.bg, anchor='nw')
                else:
                    self.canvas.create_image(x * w2, y * h2, image=self.bg2, anchor='nw')
        self.sprites = []
        self.running = True
        self.canvas.pack()
        self.tk.update()

    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)
            
class Coords:
    def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2 =0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
            or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
            or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
            or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
        return True
    else:
        return False

def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
            or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
            or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
            or (co2.y2 > co1.y1 and co2.y2 < co1.y1) :
        return True
    else:
        return False
    
def collided_left(co1, co2):
    if within_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            return True
    return False

def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False

def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False

def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        y_calc=co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None
    def move(self):
        pass
    def coords(self):
        return self.coordinates

class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)

class StickFigureSprint(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [PhotoImage(file="Draws/figure-L1.gif"), PhotoImage(file="Draws/figure-L2.gif"), PhotoImage(file="Draws/figure-L3.gif")]
        self.images_right = [PhotoImage(file="Draws/figure-R1.gif"), PhotoImage(file="Draws/figure-R2.gif"), PhotoImage(file="Draws/figure-R3.gif")]
        self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2
            
    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2
    
    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0


if __name__ == "__main__":
    game = Game()
    platform1 = PlatformSprite(game, PhotoImage(file="Draws/platform1.gif"), 0, 480, 100, 10)
    game.sprites.append(platform1)
    platform2 = PlatformSprite(game, PhotoImage(file="Draws/platform1.gif"), 150, 440, 100, 10)
    game.sprites.append(platform2)
    platform3 = PlatformSprite(game, PhotoImage(file="Draws/platform1.gif"), 300, 400, 100, 10)
    game.sprites.append(platform3)
    platform4 = PlatformSprite(game, PhotoImage(file="Draws/platform1.gif"), 300, 160, 100, 10)
    game.sprites.append(platform4)
    platform5 = PlatformSprite(game, PhotoImage(file="Draws/platform2.gif"), 175, 350, 66, 10)
    game.sprites.append(platform5)
    platform1 = PlatformSprite(game, PhotoImage(file="Draws/platform2.gif"), 50, 300, 66, 10)
    game.sprites.append(platform1)
    platform1 = PlatformSprite(game, PhotoImage(file="Draws/platform2.gif"), 170, 120, 66, 10)
    game.sprites.append(platform1)
    platform1 = PlatformSprite(game, PhotoImage(file="Draws/platform2.gif"), 45, 60, 66, 10)
    game.sprites.append(platform1)
    platform1 = PlatformSprite(game, PhotoImage(file="Draws/platform3.gif"), 170, 250, 32, 10)
    game.sprites.append(platform1)
    platform1 = PlatformSprite(game, PhotoImage(file="Draws/platform3.gif"), 230, 200, 32, 10)
    game.sprites.append(platform1)
    game.mainloop()
  
from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill = color)
        self.canvas.move(self.id, 245, 100)
        self.starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(self.starts)
        self.x = self.starts[0]
        random.shuffle(self.starts)
        self.y = self.starts[0]
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3
    
    def start(self):
        self.canvas.coords(self.id, 245, 100, 260, 115)
        random.shuffle(self.starts)
        self.x = self.starts[0]
        random.shuffle(self.starts)
        self.y = self.starts[0]
        self.draw()
        pass
    
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3]>= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
            
            
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas. create_rectangle(0, 0, 100, 10, fill = color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width =self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.pos = self.canvas.coords(self.id)
        
    def update(self):
        self.pos = self.canvas.coords(self.id)
        self.canvas.move(self.id, self.x, 0)
    
    def turn_left(self, evt):
        if self.pos[0] <= 0:
            self.x = 0
        else:
            self.x = -5
        self.update()
        
    def turn_right(self, evt):
        if self.pos[2] >= self.canvas_width:
            self.x = 0
        else:
            self.x = 5
        self.update()
    
class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Game")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width = 500, height = 400, bd = 0, highlightthickness = 0)
        self.canvas.pack()
        self.tk.update()
        self.canvas.bind_all('<KeyPress>', self.key)
        self.pause = True
        self.paddle = Paddle(self.canvas, 'blue')
        self.ball = Ball(self.canvas, self.paddle, 'red')
        self.text_id = None
    
    def Draw(self):
        if self.ball.hit_bottom == True: 
            self.mach()
        if self.pause == False:
            if self.text_id is not None: 
                self.canvas.delete(self.text_id)
                self.text_id = None
            self.ball.draw()
    
    def mach(self):
        self.text_id = self.canvas.create_text(250, 200, text='Game Over', fill='black', font=('Courier', 42))
        #time.sleep(2)
        self.pause = True
        self.ball.hit_bottom = False
        self.ball.start()

    
    def GameState(self):
        self.tk.update_idletasks()
        self.tk.update()
        time.sleep(0.01)
          
    def key(self, event):
        if event.keysym == "space":
            self.pause = not self.pause

game = Game()
while 1:
    game.Draw()
    game.GameState()

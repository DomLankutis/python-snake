from tkinter import *
from tkinter.font import Font
from random import randint


class Snake:
    def __init__(self, startX, startY, blockSize):
        self.x = startX / blockSize
        self.y = startY / blockSize
        startX, startY = startX / blockSize // 2, startY / blockSize // 2
        self.snake = [[startX - 1, startY, 1], [startX, startY, 2], [startX + 1, startY, 3]]
        self.head = self.snake[-1:][0]

    def move(self, direction):
        self.snake.insert(len(self.snake), [(int(self.head[0]) + direction[0]) % self.x, (int(self.head[1]) + direction[1]) % self.y, 0])
        self.snake.pop(0)
        self.head = self.snake[-1:][0]

    def grow(self, direction):
        self.snake.insert(0, [(int(self.snake[0][0]) + -direction[0]) % self.x, (int(self.snake[0][1]) + -direction[1]) % self.y, 0])


class App(Frame):
    def __init__(self, x, y, master=None):
        super().__init__(master)
        self.blockSize = 10
        self.x = x * self.blockSize
        self.y = y * self.blockSize
        self.continueUpdating = True
        self.canvas = Canvas(master, width=self.x, height=self.y, bg="black")
        self.canvas.pack()
        self.snake = Snake(self.x, self.y, self.blockSize)
        self.foodExists = False
        self.foodVector = []
        self.currentDir = [1, 0] # 2D Vector [X, Y]
        self.keys = {"w": [0, -1], "s": [0, 1], "a": [-1, 0], "d": [1, 0]}
        self.collisionVector = []
        self.callgameupdate()

    def display(self):
        self.canvas.delete("all")
        color = "white"

        for index, vector in enumerate(self.snake.snake):
            if vector == self.collisionVector:
                color = "red"
            else:
                color = "white"
            self.snake.snake[index][2] = self.canvas.create_rectangle(vector[0] * self.blockSize, vector[1] * self.blockSize,
                                                                        (vector[0] + 1) * self.blockSize, (vector[1] + 1) * self.blockSize,
                                                                        fill=color)
        if self.continueUpdating:
            self.canvas.create_rectangle(self.foodVector[0] * self.blockSize, self.foodVector[1] * self.blockSize,
                                         (self.foodVector[0] + 1) * self.blockSize, (self.foodVector[1] + 1) * self.blockSize,
                                         fill=color)
        else:
            font = Font(self, family="Arial", size=56)
            self.canvas.create_text(self.x / 2, self.y / 2, text="Game Over", fill="white", font=font)

    def genfood(self):
        if not self.foodExists:
            pos = [randint(0, self.x / self.blockSize - 1), randint(0, self.y / self.blockSize - 1), 0]
            if pos not in self.snake.snake:
                self.foodExists = True
                self.foodVector = pos
            else:
                self.genfood()

    def callgameupdate(self):
        if self.continueUpdating:
            self.gameupdate(None)
            self.master.after(DELAY, self.callgameupdate)

    def gameupdate(self, event):
        if self.continueUpdating:
            self.genfood()
            if event:
                key = event.char.lower()
                if key in self.keys.keys() and self.continueUpdating:
                    for char, value in self.keys.items():
                        if key == char:
                            if self.currentDir != [-x for x in value]:
                                self.currentDir = value
            self.snake.move(self.currentDir)
            if [self.snake.head[0], self.snake.head[1]] == [self.foodVector[0], self.foodVector[1]]:
                self.snake.grow(self.currentDir)
                self.foodExists = False
            for vector in self.snake.snake[0:-1]:
                if vector[0:2] == self.snake.head[0:2]:
                    self.collisionVector = self.snake.head
                    self.continueUpdating = False
            self.display()


DELAY = 300
root = App(50, 50, Tk())
root.master.bind("<Key>", root.gameupdate)
root.mainloop()

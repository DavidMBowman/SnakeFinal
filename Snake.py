#import what I need
from tkinter import *
import random

#declare needed variables
gameWidth = 900     #width of game
gameHeight = 600    #height of game
gameSpeed = 100     #speed of the snake
itemSize = 30       #size of the indivdual squares of snake and the food
bodyWidth = 2       #starting body width
bodyColor = "purple"#body color
foodColor = "red"   #food color
backgroundColor = "black"   #background color

#create the starting menu
startScreen = Tk()
startScreen.geometry("1200x720+400+0")  #create size of starting menu
startScreen.configure(bg = "black")     #starting menu background color
startScreen.title("Start Screen")       #give the starting menu a title

#define the main loop
def mainLoop():
    global snake, Food, direction, points, pointsIncrement  #make variables global to avoid running into errors

    #define function for turning the snake
    def snakeTurn(snake, food):
        a, b = snake.coordonate[0]

        if direction == "up":           #check if player is going up
            b -= itemSize               #go up
        elif direction == "down":       #check if player pushed the down arrow
            b += itemSize               #go down
        elif direction == "left":       #check if player pushed the left arrow
            a -= itemSize               #go left
        elif direction == "right":      #check if player pushed the right arrow
            a += itemSize               #go right

        snake.coordonate.insert(0, (a, b))
        cube = objectCanvas.create_rectangle(a, b, a + itemSize, b + itemSize, fill = bodyColor)
        snake.cubes.insert(0, cube)
        if a == food.coordonate[0] and b == food.coordonate[1]:                 #check if snake coordinates match food cordinates
            global points                                                       #globalize points variable
            points += 1                                                         #add to points
            pointsIncrement.config(text="Points:{}".format(points))             #add point
            objectCanvas.delete("food")                                         #delete food
            food = Food()

        else:
            del snake.coordonate[-1]                                            
            objectCanvas.delete(snake.cubes[-1])                                #delete snake cube behind snake
            del snake.cubes[-1]                                                 #delete snake cube behind snake

        if checkCollisions(snake):
            gameOver()                                                             #if there is a collision end the game
        else:       
            gameScreen.after(gameSpeed - points * 2, snakeTurn, snake, food)       #increase snake speed

    #define function for finding the new direction and testing if you can (you can't if you move in the oppsite direction you are currently heading in)
    def changeMovement(newDirection):
        global direction                    #making direction variable global

        if newDirection == "left":          #testing if player pushed left button
            if direction != "right":        #test if player was going right (the new direction can't be the opposite of the current direction)
                direction = newDirection    #set the players new direction to the button they pushed
        elif newDirection == "right":       #testing if player pushed right button
            if direction != "left":         #test if player was going left (the new direction can't be the opposite of the current direction)
                direction = newDirection    #set the players new direction to the button they pushed
        elif newDirection == "up":          #testing if player pushed up button
            if direction != "down":         #test if player was going down (the new direction can't be the opposite of the current direction)
                direction = newDirection    #testing if player pushed up button
        elif newDirection == "down":        #testing if player pushed down button
            if direction != "up":           #test if player was going up (the new direction can't be the opposite of the current direction)
                direction = newDirection    #testing if player pushed up button

    #check for collisions
    def checkCollisions(snake):
        a, b = snake.coordonate[0]                              #define snake coordinates

        if a < 0 or a >= gameWidth:                             #if snake hits left or right wall then there was a collision
            return True
        elif b < 0 or b >= gameHeight:                          #if snake hits top or bottom wall then there was a collision
            return True
        for snake_body in snake.coordonate[1:]:
            if a == snake_body[0] and b == snake_body[1]:       #if snake hits itself then there was a collision
                return True

    #define a function for ending the game
    def gameOver():
        objectCanvas.delete(ALL)                                                                                                    #delete everything on the canvas
        objectCanvas.create_text(objectCanvas.winfo_width() / 2, objectCanvas.winfo_height() / 2, font=("", 90), text="GAME OVER",  #create the game over screen
        fill="red", tag="Game Over")
        closeButton.place(relx = 0.5, rely = 0.7, anchor = "center")                                                                #place the close button
        restartButton.place(relx = 0.5, rely = 0.8, anchor = "center")                                                              #place the restart button

    #define the function for closing the game (close button)
    def close():
        gameScreen.destroy()                                                                                                        #delete the game screen
        startScreen.destroy()                                                                                                       #delete the start menu
    
    #define a function for restarting the game (restart button)
    def restart():
        gameScreen.destroy()                                                                                                        #delete the game screen
        mainLoop()                                                                                                                  #rerun the main loop

    #make a class for the snake
    class snake:   
        def __init__(self):
            self.body_size = bodyWidth
            self.coordonate = []
            self.cubes = []

            for i in range(0, bodyWidth):
                self.coordonate.append([0, 0])

            for a, b in self.coordonate:
                cube = objectCanvas.create_rectangle(a, b, a + itemSize, b + itemSize, fill=bodyColor, tag="snake")
                self.cubes.append(cube)

    #make a class for the food
    class Food:
        def __init__(self):
            a = random.randint(0, (gameWidth / itemSize) - 1) * itemSize                                                        #randomize the x coordinate
            b = random.randint(0, (gameHeight / itemSize) - 1) * itemSize                                                       #randomize the y coordinate

            self.coordonate = [a, b]                                                                                            #set the coordinates to the random ones
            objectCanvas.create_oval(a, b, a + itemSize, b + itemSize, fill=foodColor, tag="food")                              #create the food
    
    gameScreen = Toplevel(startScreen)                                                                                          #create the game screen as a top level of the start screen
    gameScreen.title("Snake")                                                                                                   #title the game screen
    gameScreen.resizable(False, False)                                                                                          #make the game screen not resizable
    gameScreen.configure(bg = 'black')                                                                                          #set background color to black

    points = 0                                                                                                                  #define starting points as 0
    direction = "down"                                                                                                          #define starting direction as down

    gameBackGround = PhotoImage(file = 'grass.png')                                                                             #define the background image as the grass image

    pointsIncrement = Label(gameScreen, text = "Points:{}".format(points), font = ("consolas", 40), bg = 'black', fg = 'white') #display the player's points
    pointsIncrement.pack()

    objectCanvas = Canvas(gameScreen, bg = 'black', height = gameHeight, width = gameWidth)                                     #create the game screen canvas
    objectCanvas.pack()

    objectCanvas.create_image(0, 0, image = gameBackGround, anchor = 'center')                                                  #create background grass image
    objectCanvas.create_image(900, 600, image = gameBackGround, anchor = 'center')                                              #create background grass image
    objectCanvas.create_image(400, 200, image = gameBackGround, anchor = 'center')                                              #create background grass image
    objectCanvas.create_image(0, 800, image = gameBackGround, anchor = 'center')                                                #create background grass image

    gameScreen.update()

    gameScreen_width = gameScreen.winfo_width()                                                                                 #define game screen width
    gameScreen_height = gameScreen.winfo_height()                                                                               #define game screen height
    screen_width = gameScreen.winfo_screenwidth()                                                                               #define screen width
    screen_height = gameScreen.winfo_screenheight()                                                                             #define screen height

    a = int((screen_width / 2) - (gameScreen_width / 2))
    b = int((screen_height / 2) - (gameScreen_height / 2))

    gameScreen.geometry(f"{gameScreen_width}x{gameScreen_height}+{a}+{b}")                                                      #define screen size

    gameScreen.bind("<Left>", lambda event: changeMovement("left"))
    gameScreen.bind("<Right>", lambda event: changeMovement("right"))
    gameScreen.bind("<Up>", lambda event: changeMovement("up"))
    gameScreen.bind("<Down>", lambda event: changeMovement("down"))

    closeButton = Button(gameScreen, text = "Close", command = close)                                                           #create the close button and customize it
    restartButton = Button(gameScreen, text = "Restart", command = restart)                                                     #create the restart button and customize it

    snake = snake()                                                                                                             #the snake is equal to the snake class
    food = Food()                                                                                                               #the snake is equal to the snake class

    snakeTurn(snake, food)

    gameScreen.mainloop()

#define a function for quitting the game (quit button)
def quit():
    startScreen.destroy()                                                                                                       #destroy the start screen

snakeImg = PhotoImage(file = "SnakeTitleScreen.png")                                                                            #set the snakeImg variable as the SnakeTitleScreen image
snakeLabel = Label(startScreen, bg = "black", image = snakeImg)                                                                 #create a lable for the image
snakeLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)                                                                     #place the label for the image

#create the quite button, customize it, and place it on the start screen
quitButton = Button(startScreen, text="Quit", fg = "black", width = 20, height = 5, command = quit)
quitButton.place(x = 750, y = 600)

#create the start button, customize it, and place it on the start screen
startButton = Button(startScreen, text="Start Snake", fg = "black", width = 20, height = 5, command = mainLoop)
startButton.place(x = 550, y = 600)

#create the lable, for the instructions on the start screen, customize it, and place it
instructions = Label(startScreen, text = "Make sure to click on the window before the snake hits the wall and use arrow keys to move!", font=('Comic Sans MS', 15, 'bold'), bg = 'black', fg = 'white')
instructions.place(x = 150, y = 20)

#create the lable, that warns the player to click on the game screen in order to move on the start screen, customize it, and place it
warning = Label(startScreen, text = "The more points you get the faster it goes!", font=('Comic Sans MS', 15, 'bold'), bg = 'black', fg = 'white')
warning.place(x = 90, y = 635)

#create the lable, for telling the player good luck on the start screen, customize it, and place it
goodLuck = Label(startScreen, text = "Good Luck!", font=('Comic Sans MS', 15, 'bold'), bg = 'black', fg = 'white')
goodLuck.place(x = 900, y = 635)

#run the program
startScreen.mainloop()
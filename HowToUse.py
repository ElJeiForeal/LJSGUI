import pygame
from sys import exit
import os
import LJSGui

pygame.init()

fps = 60
clock = pygame.time.Clock()

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)

screenSize = screenWidth, screenHeight = (600,600)
screen = pygame.display.set_mode(screenSize)

#Fonts
font = pygame.font.SysFont("consolas", 25)
small_font = pygame.font.SysFont("consolas", 15)

#Textlabel
frame = LJSGui.Frame((200,50), (screenWidth/2, screenHeight/2), LIGHT_GRAY, "center", True, 10, GRAY)
textlabel = LJSGui.TextLabel((0,0), "Hello world!", frame)

#Button
buttonframe = LJSGui.Frame((100,50),(10,10), LIGHT_GRAY, bordercolor=GRAY)
printTextBoxes = LJSGui.Button("Print Textbox", buttonframe)

#TextBox
textbox_frame = LJSGui.Frame((200,50), (screenWidth/2, 4*screenHeight/5), LIGHT_GRAY, "center", True, 10, GRAY)
TextBox = LJSGui.TextBox(textbox_frame, 20,"Type something")

#SecondTextBox

textbox_frame2 = LJSGui.Frame((200,50), (screenWidth/2, 3.3*screenHeight/5), LIGHT_GRAY, "center", True, 10, GRAY)
TextBox2 = LJSGui.TextBox(textbox_frame2, 20,"Type something", clearOnFocus= False)

running = True
tick = 0


while running:
    tick +=1

    screen.fill(BLACK)

    frame.render(screen)
    textlabel.render(screen, font, BLACK, "center")

    LJSGui.TextLabel((screenWidth/2,screenHeight/3), "Textlabel").render(screen, font, GRAY, "center")

    printTextBoxes.render(screen, small_font, BLACK, "center")

    TextBox.render(screen, small_font, BLACK, "center")
    TextBox2.render(screen, small_font, BLACK, "center")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if printTextBoxes.clicked(event,1):
            os.system("cls")
            
            print("textbox1" , TextBox.text)
            print("textbox2" , TextBox2.text)

            pos = printTextBoxes.frame.rect.topleft
            printTextBoxes.frame.rect.topleft = (pos[0] + 10, pos[1])

        TextBox.activate(event)
        TextBox2.activate(event, focusNeeded= False)

    pygame.display.update()
    clock.tick(fps)



pygame.quit()
exit()

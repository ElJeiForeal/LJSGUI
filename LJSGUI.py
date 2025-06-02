import pygame

def IsPosModeNotValid(positionmode):
    return positionmode not in {"center", "topleft", "bottomright"}


class Frame():
    def __init__(self, size, position, framecolor, positionmode : str = "topleft", HasBorder : bool = True ,bordersize : float = 10.0, bordercolor : tuple = (0,0,0)):
        if IsPosModeNotValid(positionmode):
            raise ValueError(f"Invalid position mode: {positionmode}")
        
        self.rect = pygame.Rect(0,0, size[0], size[1])

        if positionmode == "center":
            self.rect.center = position
        if positionmode == "topleft":
            self.rect.topleft = position
        if positionmode == "bottomright":
            self.rect.bottomright = position
        
        self.framecolor = framecolor
        self.bordersize = bordersize
        self.bordercolor = bordercolor
        self.HasBorder = HasBorder

    def render(self, screen):
        if self.HasBorder:
            borderRect = self.rect.inflate(self.bordersize, self.bordersize)
            pygame.draw.rect(screen, self.bordercolor, borderRect)
        
        pygame.draw.rect(screen, self.framecolor, self.rect)

class TextLabel():
    def __init__(self, position, text, frame: object = None):
        self.position = position
        self.text = text

        self.frame = frame
    
    def render(self, screen, font, textcolor, textPosMode: str = "topleft"):
        if IsPosModeNotValid(textPosMode):
            raise ValueError(f"Invalid position mode: {textPosMode}")
        
        renderedfont = font.render(self.text, True, textcolor)
        txtrect = renderedfont.get_rect()
        
    
        if self.frame:
            self.frame.render(screen)

            if textPosMode == "topleft":
                txtrect.topleft = self.frame.rect.topleft
            elif textPosMode == "center":
                txtrect.center = self.frame.rect.center
            elif textPosMode == "bottomright":
                txtrect.bottomright = self.frame.rect.bottomright

        else:

            if textPosMode == "topleft":
                txtrect.topleft = self.position
            elif textPosMode == "center":
                txtrect.center = self.position
            elif textPosMode == "bottomright":
                txtrect.bottomright = self.position
            
        screen.blit(renderedfont, txtrect.topleft)


class Button():
    def __init__(self, text, frame):
        self.text = text
        self.frame = frame
        self.rect = frame.rect
    
    def render(self, screen, font, textcolor, textPosMode: str = "topleft"):
        if IsPosModeNotValid(textPosMode):
            raise ValueError(f"Invalid position mode: {textPosMode}")
        
        renderedfont = font.render(self.text, True, textcolor)
        txtrect = renderedfont.get_rect()
        
    
        self.frame.render(screen)

        if textPosMode == "topleft":
            txtrect.topleft = self.frame.rect.topleft
        elif textPosMode == "center":
            txtrect.center = self.frame.rect.center
        elif textPosMode == "bottomright":
            txtrect.bottomright = self.frame.rect.bottomright

        screen.blit(renderedfont, txtrect.topleft)

    def clicked(self, event, mousebutton:int = 1):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == mousebutton:
                return self.rect.collidepoint(pygame.mouse.get_pos())
        return False
    

class TextBox():
    def __init__(self, frame, max_characters, EmptyText :str = "", EmptyTextColor : tuple = (128, 128, 128), clearOnFocus :bool = True):
        self.EmptyTextColor = EmptyTextColor
        self.EmptyText = EmptyText
        self.frame = frame
        self.rect = frame.rect
        self.max_characters = max_characters
        self.clearOnFocus = clearOnFocus

        self.LastKey = ""

        self.text = ""
        self.focused = False
    
    def render(self, screen, font, textcolor, textPosMode: str = "topleft"):
        if IsPosModeNotValid(textPosMode):
            raise ValueError(f"Invalid position mode: {textPosMode}")
        
        texttorender = (self.text != "" and self.text) or self.EmptyText
        colortorender = (self.text == "" and self.EmptyTextColor) or textcolor

        renderedfont = font.render(texttorender, True, colortorender)
        txtrect = renderedfont.get_rect()
        
    
        self.frame.render(screen)

        if textPosMode == "topleft":
            txtrect.topleft = self.frame.rect.topleft
        elif textPosMode == "center":
            txtrect.center = self.frame.rect.center
        elif textPosMode == "bottomright":
            txtrect.bottomright = self.frame.rect.bottomright

        screen.blit(renderedfont, txtrect.topleft)

    def CheckIfFocused(self, event, mousebutton:int = 1):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == mousebutton:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.focused = True
                    if self.clearOnFocus:
                        self.text = ""
                    return
            self.focused = False
            return
    
    def type(self, event, focusNeeded : bool = True):
        if event.type == pygame.KEYDOWN:
            if (not self.focused) and focusNeeded:
                return

            char = event.unicode

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.LastKey = "backspace"
                return

            if event.key == pygame.K_RETURN:
                self.focused = False
                self.LastKey = "enter"
                return

            if len(self.text) < self.max_characters:
                self.text += char
                self.LastKey = char
    
    def activate(self,event, mousebutton:int = 1, focusNeeded : bool = True):
        self.CheckIfFocused(event, mousebutton)
        self.type(event, focusNeeded)
    
    def onKey(self, key: str = "enter", callback=None):
        if self.LastKey == key:
            self.LastKey = ""
            if callback:
                callback()
            return True
        return False
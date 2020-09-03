import pygame, random, os.path

pygame.init()

#Window attributes
screenWidth = 1000
screenHeight = 600
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Hangman Pygame")

# Text
buttonFont = pygame.font.SysFont('Calibri', 20, True)
wordFont = pygame.font.SysFont('Calibri', 36, True)
overFont = pygame.font.SysFont('Calibri', 56, True)

# Image for the hangman
hangPic = []
for x in range (7):
    pic = (pygame.image.load('assets/' +  str(x) + '.png').convert_alpha())
    hangPic.append(pic)

# FPS
clock = pygame.time.Clock()

class button(object):
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.radius = 30
        self.width = 40
        self.height = 40
    
    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.width, self.height))
        # pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), self.radius)
        text = buttonFont.render(self.name, 1, (0,0,255))
        win.blit(text, (self.x + 14, self.y + 11))

def handleMouseClick(mousePos):
    for btn in buttons:
        if mousePos[1] > btn.y and mousePos[1] < btn.y + btn.height:
            if mousePos[0] > btn.x and mousePos[0] < btn.x + btn.width:
                return btn.name.upper()
    return "-1"

def readWordFile():
    if os.path.exists("wordList.txt"):        
        fileName = open("wordList.txt", "r")
        wordList = []
        temp = fileName.readlines()
        fileName.close()

        for line in temp:
            if line[-1] == "\n":
                wordList.append(line[:-1])
            else:
                wordList.append(line)
        return wordList
    else:
        return False

def getWord(listForWord, wordsPlayed):
    returnWord = ''

    # If all words played already
    if len(listForWord) == len(wordsPlayed):
        wordsPlayed.clear()  
    while True:
        returnWord = random.choice(listForWord).upper()
        if returnWord not in wordsPlayed:
            return returnWord

def gameOver():
    gameOverText = overFont.render('Game Over!', 1, (0,0,0))
    textRect = gameOverText.get_rect()
    textRect.center = (screenWidth//2, screenHeight//2 - 25)

    descText = wordFont.render("Press right click to restart the game!", 1, (0,0,0))
    descRect = descText.get_rect()
    descRect.center = (screenWidth//2, screenHeight//2 + 25)

    pausing = True
    while (pausing):
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3: #Right click
                    return True
        
        win.fill((211, 211, 211))
        win.blit(gameOverText, textRect)
        win.blit(descText, descRect)
        pygame.display.update()

def correct():
    correctText = wordFont.render('Correct! Score +1', 1, (255,255,255))
    textRect = correctText.get_rect()
    textRect.center = (screenWidth//2, screenHeight//2 + 250)

    pausing = True
    while (pausing):
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return True
        
        #win.fill((211, 211, 211))
        win.blit(correctText, textRect)
        pygame.display.update()

def drawWindow(wordDisplay, tries, guessed_word, score, guessed):
    #Background
    win.fill((0,0,0))

    #Hangman
    hangRect = hangPic[tries].get_rect()
    hangRect.center = (250, 200) #to Center
    win.blit(hangPic[tries], hangRect)

    for button in buttons:
        if button.name not in guessed_word:
            button.draw(win)

    #Words being played
    for index, letter in enumerate(wordDisplay):
        text = wordFont.render(letter, 1, (255, 255, 255))
        win.blit(text, (430 + (index*50), 250)) #Make some space for x

    #Scores
    scoreText = wordFont.render('Score : ' + str(score), 1, (255,255,255))
    textRect = scoreText.get_rect()
    textRect.center = (screenWidth - 120, 50)
    win.blit(scoreText, textRect)

    #Show message
    if guessed:
        correct() 

    pygame.display.update()

# Initialize variables
buttons = []
for i in range(26):
    if i >= 13:
        buttons.append(button(65 + (i % 13)*70, 460, chr(65+i)))
    else:
        buttons.append(button(65 + (70*i), 370, chr(65+i)))

# Initialize words from file to a list first
wordsPlayed = []
wordList = readWordFile()
FPS = 30

if not wordList:
    errorText = wordFont.render("WordList file not found!", 1, (255,255,255))
    errorRect = errorText.get_rect()
    errorRect.center = (screenWidth//2, screenHeight//2)
    
    pausing = True
    while (pausing):
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        win.fill((255, 0, 0))
        win.blit(errorText, errorRect)
        pygame.display.update()

else:
    # All words in uppercase
    run = True
    stock_word = getWord(wordList, wordsPlayed)
    print(stock_word)
    guessed_word = []
    display_word = "_" * len(stock_word)
    tries = 0
    guessed = False
    score = 0

    while (run):
        clock.tick(FPS)

        if tries >= 6:
            guessed = gameOver()
            score = 0

        if guessed:
            stock_word = getWord(wordList, wordsPlayed)
            print(stock_word)
            display_word = "_" * len(stock_word)
            tries = 0
            guessed_word = []
            guessed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Validasi, kalo ga ada gameOver screen, biar tries ga > 6 (ga ada .png nya)
                if event.button == 1 and tries < 6: 
                    mouse = pygame.mouse.get_pos()
                    wordGuessing = handleMouseClick(mouse)

                    if wordGuessing != "-1" and wordGuessing not in guessed_word:
                        if wordGuessing in stock_word:
                            indices = [index for index, letter in enumerate(stock_word) if letter == wordGuessing]
                            for i in range(len(stock_word)):
                                if i in indices:
                                    display_word = display_word[:i] + wordGuessing + display_word[i+1:]
                        else:
                            tries += 1
                        guessed_word.append(wordGuessing)

        if display_word == stock_word:
            guessed = True
            score += 1
            wordsPlayed.append(stock_word)

        drawWindow(display_word, tries, guessed_word, score, guessed)


        
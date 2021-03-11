import pygame
import random
from time import sleep

#전역 변수
WHITE = (255, 255, 255)
RED = (255, 0, 0)
pad_width = 1024
pad_height = 512
background_width = 1024

aircraft_width = 90
aircraft_height = 78
bat_width = 110
bat_height = 135

fireball1_width = 140
fireball1_height = 60
fireball2_width = 86
fireball2_height = 60

heart_width = 40
heart_height = 40

#함수 코드부
def drawScore(count) : # 적이 화면 밖으로 지난 수 계산
    global gamepad

    font = pygame.font.SysFont(None, 50)
    text = font.render('Life:' + str(5-count), True, WHITE)
    gamepad.blit(text, (0, 0))

def drawShotScore(count) : # 적을 맞춘 수 계산
    global gamepade

    font = pygame.font.SysFont(None, 30)
    text = font.render('Score:' + str(count), True, WHITE)
    gamepad.blit(text, (100, 0))

def drawTime(count) :
    global gamepad

    font = pygame.font.SysFont(None, 30)
    text = font.render('Time:' + str(count), True, WHITE)
    gamepad.blit(text, (500, 0))

# 화면에 글씨 보이기
def textObj(text, font) :
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def disMessage(text) :
    global gamepad

    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((pad_width/2), pad_height/2)
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(2)
    runGame()
def gameOver() : # 게임오버 글씨 나오기
    global gamepad

    disMessage('GAME OVER')


def crah() : # 적과 충돌했을 시 글씨 나오기
    global gamepad, explosion_sound

    pygame.mixer.Sound.play(explosion_sound)
    disMessage('Crashed!')

def drawObject(obj, x, y) : # 객체 불러오는 함수
    global gamepad
    gamepad.blit(obj, (x, y))

############### 게임을 초기화하고 시작하는 함수 ########################

def initGame () :
    global gamepad, aircraft, clock, background1, background2
    global bat, fires, bullet, boom, enermy, heart
    global shot_sound, explosion_sound, start_time, elapsed_time

    start_time = 0
    elapsed_time = 0

    fires = []
    enermy = []

    pygame.init() # pygame 라이브러리 초기화
    gamepad = pygame.display.set_mode((pad_width,pad_height)) # 게임창 화면 크기
    pygame.display.set_caption('ShootingGame_JE') # 게임 타이틀 지정
    aircraft = pygame.image.load('images/plane.png') # 비행기 이미지
    background1 = pygame.image.load('images/bg1.png') # 배경이미지
    background2 = background1.copy()
    bat = pygame.image.load('images/bat.png')
    fires.append((0, pygame.image.load('images/fireball.png')))
    fires.append((0, pygame.image.load('images/fireball2.png')))

    boom = pygame.image.load('images/boom.png')

    for i in range(3) :
        fires.append((i+2, None))

    bullet = pygame.image.load('images/bullet.png')
    heart = pygame.image.load('images/heart.png')
    enermy.append(pygame.image.load('images/bat.png'))
    enermy.append(pygame.image.load('images/bat1.png'))
    enermy.append(pygame.image.load('images/bat2.png'))



    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(-1)
    shot_sound = pygame.mixer.Sound('shot.wav')
    explosion_sound = pygame.mixer.Sound('explosion.wav')

    clock = pygame.time.Clock() #게임 초당 프레임 설정
    runGame() # 게임 호출


############### 실제 게임이 구동되는 함수 ########################
def runGame() :
    global gamepad, aircraft, clock, background1, background2
    global bat, fires, bullet, boom, heart, enermy
    global shot_sound, start_time, elapsed_time

    enermypassed = 0 # 적이 지나간 수
    shot_count = 0 # 적을 맞춘 수

    start_time = pygame.time.get_ticks() # 게임 시작 시각 지정

    bullet_xy = []  # 무기 좌표를 위한 리스트 준비

    # 플레이어 초기 위치 (x, y) 설정
    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0  # 비행기가 위 아래로 움직이므로 y좌표 변화 표시

    # 배경 위치 지정
    background1_x = 0  # 배경 이미지의 좌상단 모서리의 x 좌표
    background2_x = background_width

    # 적(박쥐)의 초기 위치
    bat_x = pad_width
    bat_y = random.randrange(0, pad_height)
    bat_speed = 3

    #불 초기 위치
    fire_x = pad_width
    fire_y = random.randrange(0, pad_height)
    random.shuffle(fires)
    fire = fires[0]

    # 하트 초기 위치
    heart_x = pad_width
    heart_y = random.randrange((0, pad_height-heart_height/2))
    heart_speed = 2
    isheart = False

    # isShotBat = False
    # boom_count = 0
    #
    # bat_passed = 0

    crashed = False # 게임 종료
    while not crashed :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                crashed = True

            # 키보드 이벤트
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP :
                    y_change = -5
                elif event.key == pygame.K_DOWN :
                    y_change = 5

                elif event.key == pygame.K_LCTRL :
                    pygame.mixer.Sound.play(shot_sound)
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height/2
                    bullet_xy.append([bullet_x, bullet_y])

                elif event.key == pygame.K_SPACE :
                    sleep(5)

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                    y_change = 0

        # Clear gamepad
        gamepad.fill(WHITE)

        # Draw Background
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        if int(elapsed_time) == 10 :
            disMessage('stage2')
            background1 = pygame.image.load('images/bg2.png')
            background2 = background1.copy()
            enermy = []
            enermy.append(pygame.image.load('images/bird1.png'))
            enermy.append(pygame.image.load('images/bird2.png'))
            enermy.append(pygame.image.load('images/bird3.png'))

            # 적 초기 위치
            bat_x = pad_width
            bat_y = random.randrange(0, pad_height - bat_height / 2)
            bat_speed = 3

            # 불 초기 위치
            fire_x = pad_width
            fire_y = random.randrange(0, pad_height)
            random.shuffle(fires)
            fire = fires[0]

            # 하트 초기 위치
            heart_x = pad_width
            heart_y = random.randrange(0, pad_height - heart_height / 2)
            heart_speed = 2
            isheart = False

        background1_x -= 2
        background2_x -= 2

        if background1_x == -background_width :
            background1_x = background_width

        if background2_x == -background_width :
            background2_x = background_width


        drawObject(background1, background1_x, 0) # 배경 이미지의 최초 좌표값
        drawObject(background2, background2_x, 0)

        # 화면에 띄우기
        drawObject(aircraft, x, y)
        drawObject(fire, fire_x, fire_y)
        drawObject(bat, bat_x, bat_y)
        drawObject(heart, heart_x, heart_y)

        if int(elapsed_time) > 0 and int(elapsed_time)%11 == 0 :
            isheart = True

        if isheart :
            heart_x -= heart_speed

        if len(bullet_xy) != 0 :
            for bx, by in bullet_xy :
                drawObject(bullet, bx, by)

        drawScore(enermypassed)
        drawShotScore(shot_count)
        drawTime(str(int(elapsed_time)))

        # Aircraft Position
        y += y_change
        if y < 0:
            y = 0
        elif y > pad_height - aircraft_height:
            y = pad_height - aircraft_height

        #Check the number of BAT passed
        if bat_x < 0 :
            bat_x = pad_width
            bat_y = random.randrange(0, pad_height- bat_height)
            enermypassed += 1

        # fireball Position
        if fire == None:
            fire_x -= 30
        else:
            fire_x -= 15

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0, pad_height)
            random.shuffle(fires)
            fire = fires[0]

        if heart_x < 0 :
            heart_x = pad_width
            heart_y = random.randrange(0, pad_height - heart_height / 2)

        # Check aircraft crashed by BAT
        if x + aircraft_width > bat_x:
            if (y > bat_y and y < bat_y + bat_height) or (
                    y + aircraft_height > bat_y and y + aircraft_height < bat_y + bat_height):
                crah()

        # Check aircraft crashed by Fireball
        if fire[1] != None:
            if fire[0] == 0:
                fireball_width = fireball1_width
                fireball_height = fireball1_height
            elif fire[0] == 1:
                fireball_width = fireball2_width
                fireball_height = fireball2_height

            if x + aircraft_width > fire_x:
                if (y > fire_y and y < fire_y + fireball_height) or (
                        y + aircraft_height > fire_y and y + aircraft_height < fire_y + fireball_height):
                    crah()

        # Bullet Position
        if len(bullet_xy) != 0 :
            for i, bxy in enumerate(bullet_xy) :
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]
                # Check if bullet strike Bat
                if bxy[0] > bat_x :
                    if bxy[1] > bat_y and bxy[1] < bat_y + bat_height :
                        shot_count += 1
                        bullet_xy.remove(bxy)
                        isShotBat = True

                if bxy[0] >= pad_width :
                    try :
                        bullet_xy.remove(bxy)
                    except :
                        pass
        if shot_count % 5 == 0 & shot_count > 0  :
            bat_speed += 5

        if x + aircraft_width > bat_x:  # 적이 플레이어의 x 위치에 접근 했을 때
            if (y < bat_y and bat_y < y + aircraft_height) or \
                    (y < bat_y + bat_height and bat_y + bat_height < y + aircraft_height):
                pygame.mixer.Sound.play(explosion_sound)
                drawObject(boom, bat_x, bat_y)
                bat_x = pad_width
                bat_y = random.randrange(0, pad_height - bat_height / 2)
                enermypassed += 1

        if x + aircraft_width > fire_x:
            if (y < fire_y and fire_y < y + aircraft_height) or \
                    (y < fire_y and fire_y < y + aircraft_height):
                fire_x = pad_width
                fire_y = random.randrange(0, pad_height)
                enermypassed += 1

        if x + aircraft_width > fire2_x:
            if (y < fire2_y and fire2_y < y + aircraft_height) or \
                    (y < fire2_y and fire2_y < y + aircraft_height):
                fire2_x = pad_width + 130
                fire2_y = random.randrange(30, pad_height)
                enermypassed += 1

            # 하트를 먹으면 Life +1
        if heart_x < 0:
            heart_x = pad_width
            heart_y = random.randrange(0, pad_height - heart_height)

        if x + aircraft_width >= heart_x:
            if (y > heart_y and y < heart_y + heart_height) or \
                    (y + aircraft_height >= heart_y and y < heart_y + heart_height):
                isheart = False
                heart_x = pad_width
                heart_y = random.randrange(0, pad_height - heart_height)
                enermypassed -= 1

        if enermypassed == 10:
            gameOver()

        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]

                if bxy[0] > bat_x:
                    if bxy[1] > bat_y and bxy[1] < bat_y + bat_height:
                        bullet_xy.remove(bxy)
                        shot_count += 1
                        drawObject(boom, bat_x, bat_y)
                        bat_x = pad_width
                        bat_y = random.randrange(0, pad_height - bat_height)
                        if shot_count % 3 == 1:
                            bat = enermy[0]
                        elif shot_count % 3 == 2:
                            bat = enermy[1]
                            if bat_speed < 10:
                                bat_speed += 1
                            else:
                                bat_speed = 10
                        else:
                            bat = enermy[2]
                if bxy[0] >= pad_width:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

# if __name__ == '__main__':
initGame()
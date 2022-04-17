from pygame import *
from random import randint
#переменные с модельками игроков
back = 'background.png'
first_model = '1model.png'
second_model = '2model.png'
model_ball = 'ball.png'
model_heart1 = 'heart1.png'
model_heart2 = 'heart2.png'
model_heart3 = 'heart3.png'
#переменные, отвечающие за перемещение мяча
dx = 10
dy = 10
#переменные отвечающие за жизни игроков 
lifes1 = 3
lifes2 = 3

#шрифты и надписи
font.init()
font1 = font.SysFont('Arial', 80)
win1 = font1.render('Green player, you win!!!', True, (255,255,255))
win2 = font1.render('Red player, you win!!!', True, (255,255,255))
lose1 = font1.render('Green player, you lose!!!', True, (100,0,0))
lose2 = font1.render('Red player, you lose!!!', True, (100,0,0))
font2 = font.SysFont('Arial', 36)
#классы
#класс родитель
class GameSprite(sprite.Sprite):
    #конструктор
    def __init__(self,player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        #свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #свойство rect- прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#классы наследники (два игрока)
class Player_First(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Player_Second(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed  

#класс мяч
class Ball(GameSprite):
    #движение врага
    def update(self):
        global lifes1
        global lifes2
        #исчезает если доходит до края экрана
        if self.rect.x >= win_width:
            self.rect.x = win_width/2
            self.rect.y = win_height/2
            lifes1 = lifes1 - 1
        if self.rect.x <= 0:
            self.rect.x = win_width/2
            self.rect.y = win_height/2
            lifes2 = lifes2 - 1
#создание окна
win_width = 1080
win_height = 720
window = display.set_mode((win_width, win_height))
display.set_caption('Ping-Pong')
background = transform.scale(image.load(back), (win_width, win_height))
clock = time.Clock()
#создание спрайтов
player1 = Player_First(first_model, 80, win_height/2, 25, 60, 15)
player2 = Player_Second(second_model, win_width - 80, win_height/2, 25, 60, 15)
ball = Ball(model_ball, win_width/2, win_height/2, 50, 50, 6)
first_heart1 = Player_First(model_heart1, win_width - 100, 20, 70, 40, 0)
first_heart2 = Player_First(model_heart2, win_width - 150, 20, 125, 75, 0)
first_heart3 = Player_First(model_heart3, win_width - 200, 20, 200, 150, 0)
second_heart1 = Player_First(model_heart1, 150, 20, 70, 40, 0)
second_heart2 = Player_First(model_heart2, 100, 20, 125, 75, 0)
second_heart3 = Player_First(model_heart3, 50, 20, 200, 150, 0)

#переменная отвечающая за цикл игры
game = True

#переменная отвечающая за конец игры
finish = False

#переменная, отвечающая за частоту обновления кадров
fps = 120

#цикл игры
while game:
    #если нажат крестик закрытия, переменная game = False и игра закрывается 
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    
    if not finish:
        #обновление фона 
        window.blit(background, (0,0))

        #движение мяча
        ball.rect.x += dx
        ball.rect.y += dy

        if ball.rect.y >= win_height or ball.rect.y <= 0:
            dy *= -1

        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
            dx *= -1
        #отображение жизней
        #игрок1
        if lifes1 == 3:
            first_heart3.reset()
        if lifes1 == 2:
            first_heart2.reset()
        if lifes1 == 1:
            first_heart1.reset()
        #игрок2
        if lifes2 == 3:
            second_heart3.reset()
        if lifes2 == 2:
            second_heart2.reset()
        if lifes2 == 1:
            second_heart1.reset()
        #отображение спрайтов
        player1.update()
        player2.update()
        ball.update()

        player1.reset()
        player2.reset()
        ball.reset()
        #проверка проигрышей 
        if lifes1 <= 0:
            #проиграл игрок1, ставим фон больше и больше не управляем спрайтами
            finish = True
            window.blit(lose1, (200,200))
            window.blit(win2, (200, 300))

        if lifes2 <= 0:
            #проиграл игрок2, ставим фон больше и больше не управляем спрайтами
            finish = True
            window.blit(lose2, (200,200))
            window.blit(win1, (200,300)) 
    #автоматический перезапуск
    else:
        #подождать 3секунды перед перезапуском
        time.delay(3000)
        finish = False
        lifes1 = 3
        lifes2 = 3
    display.update()
    clock.tick(fps)
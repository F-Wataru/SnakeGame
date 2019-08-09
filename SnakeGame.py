import pygame
import random

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
YELLO = (255,255,0)
WHITE = (255,255,255)
GRAY = (128,128,128)

BLOCK_SIZE = 20
X = 640 #画面のx座標の大きさ
Y = 480 #画面のy座標の大きさ

class Snake():
    x = X/2 #蛇の頭のx座標
    y = Y/2 #蛇の頭のy座標
    head = 0
    body = []
    body_color = GREEN
    length = 0 #胴体の長さ
    x_speed = 0
    y_speed = 0

    def __init__(self):
        direction = random.randint(0, 3) #0~3のいずれかを生成
        if(direction == 0):
            self.x_speed = BLOCK_SIZE
        elif(direction == 1):
            self.x_speed = -BLOCK_SIZE
        elif(direction == 2):
            self.y_speed = BLOCK_SIZE
        elif(direction == 3):
            self.y_speed = -BLOCK_SIZE

    def move(self):
        press = pygame.key.get_pressed()
        #左が押されたとき
        if(press[pygame.K_LEFT]):
            #進行方向の逆向きに進まないようにする
            if(self.x_speed <= 0):
                self.x_speed = -BLOCK_SIZE
                self.y_speed = 0
        #右が押されたとき
        elif(press[pygame.K_RIGHT]):
            if(self.x_speed >= 0):
                self.x_speed = BLOCK_SIZE
                self.y_speed = 0
        #上が押されたとき
        elif(press[pygame.K_UP]):
            if(self.y_speed <= 0):
                self.x_speed = 0
                self.y_speed = -BLOCK_SIZE
        #下が押されたとき
        elif(press[pygame.K_DOWN]):
            if(self.y_speed >= 0):
                self.x_speed = 0
                self.y_speed = BLOCK_SIZE

    def draw_head(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, RED, self.head) #蛇の頭を生成

    def eat_food(self, food):
        #頭とえさとの衝突判定
        if(self.x == food.x and self.y == food.y):
            food.generate()
            self.length += 1
            self.body.append(self.head.copy())

    def draw_body(self):
        j = 0
        previous_body = []
        for i in range(self.length):
            previous_body.append(self.body[i]) #previous_body[j]にbody[i]を保存
            #body[0]はheadの真後ろに描画
            if(i == 0):
                if(self.x_speed < 0):
                    self.body[i] = pygame.Rect(self.x+BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)
                elif(self.x_speed > 0):
                    self.body[i] = pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)
                elif(self.y_speed < 0):
                    self.body[i] = pygame.Rect(self.x, self.y+BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                elif(self.y_speed > 0):
                    self.body[i] = pygame.Rect(self.x, self.y-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            else:
                self.body[i] = previous_body[j-1]

            pygame.draw.rect(screen, self.body_color, self.body[i])
            j += 1

    def collide_wall(self):
        global playing
        #頭と壁との衝突判定
        if (self.x < 0 or self.x > X-BLOCK_SIZE or self.y < 0 or self.y > Y-BLOCK_SIZE):
            show.gameover()
            playing = False

    def collide_me(self):
        global playing
        #頭と体の衝突判定
        for i in range(self.length):
            if(self.head.clip(self.body[i])):
                show.gameover()
                playing = False


class Food():
    x = 0
    y = 0

    def __init__(self):
        self.generate()

    def draw(self):
        food = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, GREEN, food) #えさを生成

    def generate(self):
        self.x = random.randint(0, (X - BLOCK_SIZE)/BLOCK_SIZE)*BLOCK_SIZE
        self.y = random.randint(0, (Y - BLOCK_SIZE)/BLOCK_SIZE)*BLOCK_SIZE


class Show():
    def score(self, length):
        score_font = pygame.font.SysFont(None, 40)
        score = score_font.render("score:{}".format(str(length)), True, WHITE)
        screen.blit(score, (10, 10)) #得点の表示

    def gameover(self):
        gameover_font = pygame.font.SysFont(None, 80)
        gameover = gameover_font.render("GAME OVER", False, RED)
        screen.blit(gameover, ((X-gameover.get_width())/2, Y/2)) #GAMEOVERの表示
        pygame.display.flip()
        pygame.time.wait(1000) #1秒待つ


class Hiddencommand():
    def line(self):
        if(L_lock == True):
            for i in range(0, X, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (i,0), (i,Y))
            for i in range(0, Y, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (0,i), (X,i))

    def color(self):
        if(C_lock == True):
            snake.body_color = YELLO
        else:
            snake.body_color = GREEN

 
playing = True
pygame.init() #pygameの初期化
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("SnakeGame")
clock = pygame.time.Clock()

snake = Snake()
food = Food()
show = Show()
hiddencomand = Hiddencommand()

L_lock = False
C_lock = False

while playing:
    for event in pygame.event.get():
        #閉じるボタンが押されたら終了
        if event.type == pygame.QUIT:
            playing = False

    press = pygame.key.get_pressed()

    if(press[pygame.K_l]):
        L_lock = not L_lock #True,Falseを交互に代入
    if(press[pygame.K_c]):
        C_lock = not C_lock

    screen.fill(BLACK)
    show.score(snake.length)

    hiddencomand.line()
    hiddencomand.color()

    snake.move()
    snake.draw_head()
    snake.eat_food(food)
    snake.draw_body()
    snake.collide_wall()
    snake.collide_me()

    food.draw()

    pygame.display.flip()
    clock.tick(10 + snake.length/2)


pygame.quit()
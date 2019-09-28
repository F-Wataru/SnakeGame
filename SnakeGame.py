import pygame
import random
import numpy as np
import gif_creater #外部ファイル

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
GOLD = (255,215,0)
SILVER = (194,200,206)
BRONZE = (196,112,34)

X = 640 #画面のx座標の大きさ
Y = 480 #画面のy座標の大きさ
BLOCK_SIZE = 20

pygame.init() #pygameの初期化
pygame.display.set_caption("SnakeGame")
screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()

#gif_create = gif_creater.create() #外部ファイルのクラスのインスタンスを生成

class Snake():
    x = X/2 #蛇の頭のx座標
    y = Y/2 #蛇の頭のy座標
    head = 0
    body = []
    body_color = GREEN
    x_speed = 0
    y_speed = 0
    move_distance = 0

    def __init__(self):
        self.body.clear()
        self.body.append(True) #蛇の体を1つ分生成
        
        direction = random.randint(0, 3) #0~3のいずれかを生成
        if direction == 0:
            self.x_speed = BLOCK_SIZE
        elif direction == 1:
            self.x_speed = -BLOCK_SIZE
        elif direction == 2:
            self.y_speed = BLOCK_SIZE
        elif direction == 3:
            self.y_speed = -BLOCK_SIZE

    def move(self):
        press = pygame.key.get_pressed()
        #左が押されたとき
        if press[pygame.K_LEFT]:
            #進行方向の逆向きに進まないようにする
            if self.x_speed <= 0:
                self.x_speed = -BLOCK_SIZE
                self.y_speed = 0
        #右が押されたとき
        elif press[pygame.K_RIGHT]:
            if self.x_speed >= 0:
                self.x_speed = BLOCK_SIZE
                self.y_speed = 0
        #上が押されたとき
        elif press[pygame.K_UP]:
            if self.y_speed <= 0:
                self.x_speed = 0
                self.y_speed = -BLOCK_SIZE
        #下が押されたとき
        elif press[pygame.K_DOWN]:
            if self.y_speed >= 0:
                self.x_speed = 0
                self.y_speed = BLOCK_SIZE

    def draw_head(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, RED, self.head) #蛇の頭を生成

    def draw_face(self):
        face = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
                         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
                         [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])        
        #頭とえさとの衝突して進んだ距離が2以下のとき
        if (self.x == food.x and self.y == food.y) or (self.move_distance >= 1 and self.move_distance <= 2):
            face[10:,:] = 0
            self.move_distance += 1
        else:
            self.move_distance = 0
        #進む方向によりfaceを回転する
        if self.x_speed < 0:
            face = np.fliplr(face)
        elif self.y_speed < 0:
            face = np.rot90(face, k=1)
        elif self.y_speed > 0:
            face = np.rot90(face, k=-1)
        #faceの描画
        for i in range(len(face)):
            for j in range(len(face[i])):
                if face[i][j] == 1:
                    pygame.draw.circle(screen, BLACK, (int(self.x+j), int(self.y+i)), 1)
        
    def eat_food(self, food):
        #頭とえさとの衝突判定
        if self.x == food.x and self.y == food.y:
            food.generate()
            self.body.append(True)

    def draw_body(self):
        j = 0
        previous_body = []
        for i in range(len(self.body)):
            previous_body.append(self.body[i]) #previous_body[j]にbody[i]を保存
            #body[0]はheadの真後ろに描画
            if i == 0:
                if self.x_speed < 0:
                    self.body[i] = pygame.Rect(self.x+BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)
                elif self.x_speed > 0:
                    self.body[i] = pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)
                elif self.y_speed < 0:
                    self.body[i] = pygame.Rect(self.x, self.y+BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                elif self.y_speed > 0:
                    self.body[i] = pygame.Rect(self.x, self.y-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            else:
                self.body[i] = previous_body[j-1]

            pygame.draw.rect(screen, self.body_color, self.body[i])
            j += 1

    def collide_wall(self):
        #頭と壁との衝突判定
        if self.x < 0 or self.x > X-BLOCK_SIZE or self.y < 0 or self.y > Y-BLOCK_SIZE:
            write.gameover()

    def collide_me(self):
        #頭と体の衝突判定
        for i in range(len(self.body)):
            if self.head.clip(self.body[i]):
                write.gameover()


class Food():
    x = 0
    y = 0

    def __init__(self):
        self.generate()

    def draw(self):
        food = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, GREEN, food) #えさを生成

    def generate(self):
        self.x = random.randint(0, (X-BLOCK_SIZE)/BLOCK_SIZE)*BLOCK_SIZE
        self.y = random.randint(0, (Y-BLOCK_SIZE)/BLOCK_SIZE)*BLOCK_SIZE


class Write():
    def score(self):
        score_font = pygame.font.SysFont(None, 40)
        score = score_font.render("score:{}".format(str(len(snake.body)-1)), True, WHITE)
        screen.blit(score, (10, 10)) #得点の表示

    def gameover(self):
        global play_screen
        global continue_screen
        gameover_font = pygame.font.SysFont(None, 80)
        gameover = gameover_font.render("GAME OVER", True, RED)
        screen.blit(gameover, ((X-gameover.get_width())/2, Y/2)) #GAMEOVERの表示
        #duration=100より10個分の画像を保存
        #for count in range(10):
        #    gif_create.image(screen)
        pygame.display.flip()
        pygame.time.wait(1000) #1秒待つ
        save.score()
        play_screen = False
        continue_screen = True
        
    def ranking(self):
        ranking_font = pygame.font.SysFont(None, 100)
        ranking = ranking_font.render("RANKING", True, RED)
        screen.blit(ranking, ((X-ranking.get_width())/2, 40)) #ランキングの表示

    def first(self):
        first_font = pygame.font.SysFont(None, 65)
        first = first_font.render("1st{:>5}".format(str(save.high_scores[0].rstrip('\n'))), True, GOLD)
        screen.blit(first, (X/4, 140))
        
    def second(self):
        second_font = pygame.font.SysFont(None, 56)
        second = second_font.render("2nd{:>5}".format(str(save.high_scores[1].rstrip('\n'))), True, SILVER)
        screen.blit(second, (X/4, 220))
        
    def third(self):
        third_font = pygame.font.SysFont(None, 60)
        third = third_font.render("3rd{:>5}".format(str(save.high_scores[2].rstrip('\n'))), True, BRONZE)
        screen.blit(third, (X/4, 300))
        
    def Continue(self, left):
        Continue_font = pygame.font.SysFont(None, 40)
        if left == True:
            Continue = Continue_font.render("Continue", True, GREEN)
        else:
            Continue = Continue_font.render("Continue", True, GRAY)
        screen.blit(Continue, (400, 400))
        
    def quit(self, right):
        quit_font = pygame.font.SysFont(None, 40)
        if right == True:
            quit = quit_font.render("Quit", True, GREEN)
        else:
            quit = quit_font.render("Quit", True, GRAY)
        screen.blit(quit, (540, 400))


class Save():
    high_scores = []
    
    def __init__(self):
        self.high_scores.clear()
    
    def score(self):
        #ファイルの読み込み
        f1 = open("high_scores.txt", "r")
        rewrite = False
        for row in f1:
            if len(snake.body)-1 > int(row) and rewrite == False:
                self.high_scores.append(str(len(snake.body)-1)+"\n")
                self.high_scores.append(row)
                rewrite = True
            else:
                self.high_scores.append(row)
        f1.close
        #ファイルの書き込み
        f2 = open("high_scores.txt", "w")
        for i in range(3):
            f2.write(self.high_scores[i])
        f2.close

        
class Select():
    left = True
    right = False

    #ゲームを終えるか選ぶ
    def quit(self):
        global play_screen
        global continue_screen
        
        press = pygame.key.get_pressed()
        if press[pygame.K_LEFT]:
            self.left = True
            self.right = False
        elif press[pygame.K_RIGHT]:
            self.left = False
            self.right = True
            
        write.Continue(self.left)
        write.quit(self.right)
        
        if press[pygame.K_RETURN]:
            if self.left == True:
                play_screen = True
                continue_screen = False
            else:
                continue_screen = False
          

class Hiddencommand():
    L_lock = False
    C_lock = False

    def line(self):
        press = pygame.key.get_pressed()
        if press[pygame.K_l]:
            self.L_lock = not self.L_lock #True,Falseを交互に代入
            
        if self.L_lock == True:
            for i in range(0, X, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (i,0), (i,Y))
            for i in range(0, Y, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (0,i), (X,i))

    def color(self):
        press = pygame.key.get_pressed()
        if press[pygame.K_c]:
            self.C_lock = not self.C_lock
            
        if self.C_lock == True:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            snake.body_color = (r,g,b)
        else:
            snake.body_color = GREEN


playing = True
play_screen = True
continue_screen = True

while playing:
    snake = Snake()
    food = Food()
    write = Write()
    save = Save()
    select = Select()
    hiddencomand = Hiddencommand()

    while play_screen:
        for event in pygame.event.get():
            #閉じるボタンが押されたら終了
            if event.type == pygame.QUIT:
                play_screen = False
                continue_screen = False

        screen.fill(BLACK)
        write.score()

        hiddencomand.line()
        hiddencomand.color()

        snake.move()
        snake.draw_head()
        snake.draw_face()
        snake.eat_food(food)
        snake.draw_body()
        snake.collide_wall()
        snake.collide_me()

        food.draw()
        
        #gif_create.image(screen)
        pygame.display.flip() #画面の更新
        clock.tick(10 + len(snake.body)/2)
    
    while continue_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continue_screen = False
                
        screen.fill(BLACK)
        
        write.ranking()
        write.first()
        write.second()
        write.third()
        select.quit()
        
        #gif_create.image(screen)
        pygame.display.flip()
        clock.tick(10)
        
    if play_screen == False and continue_screen == False:
        #gif_create.gif()
        playing = False

        
pygame.quit()
import pygame
import random
import numpy as np
import sys
from gif_creater import Gif #外部ファイル

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
gif = Gif() #外部ファイルのクラス

class Snake():
    def __init__(self):
        self.x = X/2 #蛇の頭のx座標
        self.y = Y/2 #蛇の頭のy座標
        self.head = 0
        self.bodys = [True] #蛇の体を1つ分生成
        self.body_color = GREEN
        self.x_speed = 0
        self.y_speed = 0
        self.move_distance = 0
        self.direction()

    def direction(self):
        """最初の進行方向をランダムに決定"""
        way = random.choice(("left", "right", "up", "down"))
        if way == "left":
            self.x_speed = -BLOCK_SIZE
        elif way == "right":
            self.x_speed = BLOCK_SIZE
        elif way == "up":
            self.y_speed = -BLOCK_SIZE
        elif way == "down":
            self.y_speed = BLOCK_SIZE

    def move(self):
        """x方向とy方向のスピードの決定"""
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
        """頭の描画"""
        self.x += self.x_speed
        self.y += self.y_speed
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, RED, self.head) #蛇の頭を生成

    def draw_face(self):
        """顔の描画"""
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
        #進む方向によりfaceを回転
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
        """頭とえさとの衝突判定"""
        if self.x == food.x and self.y == food.y:
            food.generate()
            self.bodys.append(True)

    def draw_body(self):
        """胴体の描画"""
        previous_bodys = []
        for i in range(len(self.bodys)):
            previous_bodys.append(self.bodys[i]) #previous_bodys[i]にbodys[i]を保存
            #bodys[0]はheadの真後ろに描画
            if i == 0:
                if self.x_speed < 0:
                    self.bodys[i] = pygame.Rect(self.x+BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)
                elif self.x_speed > 0:
                    self.bodys[i] = pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)
                elif self.y_speed < 0:
                    self.bodys[i] = pygame.Rect(self.x, self.y+BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                elif self.y_speed > 0:
                    self.bodys[i] = pygame.Rect(self.x, self.y-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            else:
                self.bodys[i] = previous_bodys[i-1]
            #bodys[i]の描画
            pygame.draw.rect(screen, self.body_color, self.bodys[i])

    def collide_wall(self):
        """頭と壁との衝突判定"""
        if self.x < 0 or self.x > X-BLOCK_SIZE or self.y < 0 or self.y > Y-BLOCK_SIZE:
            write.gameover()

    def collide_me(self):
        """頭と体の衝突判定"""
        if len(self.bodys) >= 4:
            for body in self.bodys:
                if self.head.clip(body):
                    write.gameover()


class Food():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.apple = pygame.image.load("./apple.png")
        self.generate()

    def generate(self):
        """えさの位置をランダムに決定"""
        self.x = random.randint(0, (X-BLOCK_SIZE)/BLOCK_SIZE)*BLOCK_SIZE
        self.y = random.randint(0, (Y-BLOCK_SIZE)/BLOCK_SIZE)*BLOCK_SIZE

    def draw(self):
        """えさの描画"""
        apple = pygame.transform.scale(self.apple, (BLOCK_SIZE, BLOCK_SIZE))
        screen.blit(apple, (self.x, self.y))


class Write():
    def score(self):
        """得点の表示"""
        score_font = pygame.font.SysFont(None, 40)
        score = score_font.render("score:{}".format(str(len(snake.bodys)-1)), True, WHITE)
        screen.blit(score, (10, 10))

    def gameover(self):
        """ゲームオーバーの文字を1秒間表示"""
        global game_state
        gameover_font = pygame.font.SysFont(None, 80)
        gameover = gameover_font.render("GAME OVER", True, RED)
        screen.blit(gameover, ((X-gameover.get_width())/2, Y/2))
        #Gifクラスのduration=100より10個分の画像を保存
        for i in range(10):
            gif.save(screen)
        pygame.display.flip()
        pygame.time.wait(1000) #1秒待つ
        save.score()
        game_state = RANKING

    def ranking(self):
        """ランキングの文字を表示"""
        ranking_font = pygame.font.SysFont(None, 100)
        ranking = ranking_font.render("RANKING", True, RED)
        screen.blit(ranking, ((X-ranking.get_width())/2, 40))

    def first(self):
        """1位の表示"""
        first_font = pygame.font.SysFont(None, 65)
        first = first_font.render("1st{:>5}".format(str(save.high_scores[0].rstrip('\n'))), True, GOLD)
        screen.blit(first, (X/4, 140))

    def second(self):
        """2位の表示"""
        second_font = pygame.font.SysFont(None, 56)
        second = second_font.render("2nd{:>5}".format(str(save.high_scores[1].rstrip('\n'))), True, SILVER)
        screen.blit(second, (X/4, 220))

    def third(self):
        """3位の表示"""
        third_font = pygame.font.SysFont(None, 60)
        third = third_font.render("3rd{:>5}".format(str(save.high_scores[2].rstrip('\n'))), True, BRONZE)
        screen.blit(third, (X/4, 300))

    def restart(self, left):
        """Restartの文字を表示"""
        restart_font = pygame.font.SysFont(None, 40)
        if left == True:
            restart = restart_font.render("Restart", True, GREEN)
        else:
            restart = restart_font.render("Restart", True, GRAY)
        screen.blit(restart, (420, 400))

    def quit(self, right):
        """Quitの文字を表示"""
        quit_font = pygame.font.SysFont(None, 40)
        if right == True:
            quit = quit_font.render("Quit", True, GREEN)
        else:
            quit = quit_font.render("Quit", True, GRAY)
        screen.blit(quit, (540, 400))


class Save():
    def __init__(self):
        self.high_scores = []

    def score(self):
        """上位3つの得点をファイルに保存"""
        #ファイルの読み込み
        f1 = open("./high_scores.txt", "r")
        rewrite = False
        for row in f1:
            if len(snake.bodys)-1 > int(row) and rewrite == False:
                self.high_scores.append(str(len(snake.bodys)-1)+"\n")
                self.high_scores.append(row)
                rewrite = True
            else:
                self.high_scores.append(row)
        f1.close
        #ファイルの書き込み
        f2 = open("./high_scores.txt", "w")
        for i in range(3):
            f2.write(self.high_scores[i])
        f2.close


class Select():
    def __init__(self):
        self.left = True
        self.right = False

    def quit(self):
        """ゲームを終えるか選ぶ"""
        global game_state
        #←か→が押されたとき
        press = pygame.key.get_pressed()
        if press[pygame.K_LEFT]:
            self.left = True
            self.right = False
        elif press[pygame.K_RIGHT]:
            self.left = False
            self.right = True
        #文字の表示
        write.restart(self.left)
        write.quit(self.right)
        #Enterが押されたとき
        if press[pygame.K_RETURN]:
            if self.left == True:
                game_state = PLAY
            else:
                game_state = END


class Hiddencommand():
    def __init__(self):
        self.G_lock = False

    def grid(self):
        """「g」が押されたら線を碁盤目状に描画"""
        press = pygame.key.get_pressed()
        if press[pygame.K_g]:
            self.G_lock = not self.G_lock #TrueとFalseを交互に代入
        #G_lockがTrueのとき
        if self.G_lock == True:
            for i in range(0, X, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (i,0), (i,Y))
            for i in range(0, Y, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (0,i), (X,i))

    def color(self):
        """「c」が押されたとき蛇の胴体の色をランダムに変化させる"""
        press = pygame.key.get_pressed()
        if press[pygame.K_c]:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            snake.body_color = (r,g,b)


playing = True
PLAY, RANKING, END = (0, 1, 2) #ゲーム状態
game_state = PLAY

while playing:
    snake = Snake()
    food = Food()
    write = Write()
    save = Save()
    select = Select()
    hiddencomand = Hiddencommand()

    while game_state == PLAY:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = END

        screen.fill(BLACK)
        write.score()

        hiddencomand.grid()
        hiddencomand.color()

        food.draw()

        snake.move()
        snake.draw_head()
        snake.draw_face()
        snake.eat_food(food)
        snake.draw_body()
        snake.collide_wall()
        snake.collide_me()

        gif.save(screen)
        pygame.display.flip()
        clock.tick(10 + len(snake.bodys)/2)

    while game_state == RANKING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = END

        screen.fill(BLACK)

        write.ranking()
        write.first()
        write.second()
        write.third()
        select.quit()

        gif.save(screen)
        pygame.display.flip()
        clock.tick(10)

    if game_state == END:
        gif.create(False) #引数がTrueのときgifの作成
        playing = False


pygame.quit()
sys.exit()
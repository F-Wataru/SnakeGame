import pygame

class create:
    count = 0

    def __init__(self):
        import os
        os.mkdir("screenshot") #ディレクトリの作成

    #スクリーンショットの保存
    def image(self, screen):
        pygame.image.save(screen, "screenshot/SnakeGame{}.jpg".format(self.count))
        self.count += 1

    #jpgからgifを作成
    def gif(self):
        from natsort import natsorted
        import glob
        from PIL import Image
        import shutil
        files = natsorted(glob.glob("screenshot/*.jpg")) #自然順に取り出す
        images = list(map(lambda file: Image.open(file), files))
        images[0].save("SnakeGame.gif", save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)
        shutil.rmtree("screenshot") #ディレクトリの削除
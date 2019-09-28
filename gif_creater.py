import pygame

class Gif:
    def __init__(self):
        import os
        os.mkdir("./screenshot") #フォルダの作成
        self.count = 0

    def save(self, screen):
        """スクリーンショットの保存"""
        pygame.image.save(screen, "./screenshot/{}.jpg".format(self.count))
        self.count += 1

    def create(self, reply):
        """jpgからgifを作成"""
        from PIL import Image
        import shutil
        if reply == True:
            images = []
            for i in range(self.count):
                images.append(Image.open("./screenshot/{}.jpg".format(i)))
            images[0].save("SnakeGame.gif", save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)
        shutil.rmtree("./screenshot") #フォルダの削除
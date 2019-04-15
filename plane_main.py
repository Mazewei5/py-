import pygame as pg
import Plane_sprites as Ps

pg.mixer.init()
class PlaneGame(object):

    def __init__(self):
        print("游戏初始化")
        self.screen = pg.display.set_mode(Ps.SCREEN_RECT.size)
        self.clock = pg.time.Clock()
        self.__creat_sprites()
        pg.time.set_timer(Ps.CREATE_ENEMY_EVENT,1000)
        pg.time.set_timer(Ps.HERO_FIRE_EVENT,500)
        pg.time.set_timer(Ps.BOSS_MOVE_EVENT,1500)
        pg.time.set_timer(Ps.BOSS_FIRE_EVENT,4000)
        pg.time.set_timer(Ps.BOSS_UP,10000)
  #      pg.time.set_timer(Ps.BOSS_TRACK_EVENT,500)
        self.Boss_blood = 20
        self.fenshu = 0
        self.boss_come = False
        self.bullets_sound = pg.mixer.Sound("./sound/bullet.wav")
        self.bullets_sound.set_volume(0.3)
        self.bgm_01 = pg.mixer.Sound("./sound/bgm_zhandou1.wav")
        self.bgm_01.set_volume(0.3)
        self.Boss_bullets = pg.mixer.Sound("./sound/ssz_03.wav")
        self.Boss_bullets.set_volume(1)
        self.enemy_Sum = 1
    def __event_handler(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.__gameover()
            if event.type == Ps.CREATE_ENEMY_EVENT:
         #       print("敌机出场")
                self.enemy = Ps.Enemy()
         #       pg.time.set_timer(Ps.ENEMY_FIRE_EVENT+self.enemy_Sum,3000)
                self.enemy_Sum += 1

                self.enemy_Group.add(self.enemy)
            if event.type == Ps.HERO_FIRE_EVENT:
                self.hero.fire()
             #   self.bullets_sound.play()
            if event.type == Ps.ENEMY_FIRE_EVENT:
                self.enemy.fire()
            if event.type == Ps.BOSS_UP:
                if self.boss_come == False:
                    self.boss_come = True
                    print("Boss登场!!")
                    self.boss = Ps.Boss()

                    self.Boss_Group.add(self.boss)
       #     if event.type == Ps.BOSS_TRACK_EVENT:
        #        if self.boss_come:
        #            self.boss.track(self.hero.rect.centerx,self.hero.rect.y)

            if event.type == Ps.BOSS_FIRE_EVENT and self.boss_come:
                self.boss.fire()
                self.Boss_bullets.play()
            if event.type == Ps.BOSS_MOVE_EVENT and self.boss_come:
                self.boss.move()

        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_RIGHT]:
            self.hero.speed_x = Ps.HERO_SPEED
        elif keys_pressed[pg.K_LEFT]:
            self.hero.speed_x = -Ps.HERO_SPEED
        elif keys_pressed[pg.K_UP]:
            self.hero.speed_y = -Ps.HERO_SPEED
        elif keys_pressed[pg.K_DOWN]:
            self.hero.speed_y = Ps.HERO_SPEED
        else:
            if not keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_RIGHT]:
                self.hero.speed_x = 0
            if not keys_pressed[pg.K_UP] or keys_pressed[pg.K_DOWN]:
                self.hero.speed_y = 0
        pass
    def __check_collide(self):


        bo = pg.sprite.groupcollide(self.Boss_Group,self.hero.bullets,False,True)
        if bo:
            self.Boss_blood -= 1
            print("Boss剩余血量 %d" % self.Boss_blood)
        if  self.Boss_blood == 0:
            print("boss Killed!")
            self.boss.kill()
            self.Boss_blood = 20
            self.boss_come = False
            self.fenshu += 10

      #  try:
        if self.boss_come:
            f = pg.sprite.groupcollide(self.hero_Group,self.boss.bullets,True,True)
            if f:
                print("被击中!")
                self.__gameover()
       # except:


      #  if d:
      #     self.hero.kill()
      #      self.__gameover()
     #   except:
     #       print("boss没有出现")
    #    finally:
        a = pg.sprite.groupcollide(self.hero.bullets,self.enemy_Group,True,True)
        if a:
            self.fenshu += 1
        b = pg.sprite.spritecollide(self.hero,self.enemy_Group,True)
        if b:
            self.hero.kill()
            self.__gameover()
    def __update_sprites(self):
        self.bg_Group.update()
        self.bg_Group.draw(self.screen)

        self.enemy_Group.update()
        self.enemy_Group.draw(self.screen)

        self.hero_Group.update()
        self.hero_Group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        self.Boss_Group.update()
        self.Boss_Group.draw(self.screen)
        try:
            if self.boss_come:
                self.boss.bullets.update()
                self.boss.bullets.draw(self.screen)
        except:
            pass
    #@staticmethod
    def __gameover(self):
        pg.quit()
        print(self.fenshu)
        exit()
    def start_game(self):


        print("游戏开始")
        while True:
            self.clock.tick(Ps.GAME_FPS)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            pg.display.update()
    def __creat_sprites(self):
        bg1 = Ps.Background()
        bg2 = Ps.Background(True)
    #    bg2.rect.y = -bg2.rect.height
        self.bg_Group = pg.sprite.Group(bg1,bg2)

        self.enemy_Group = pg.sprite.Group()
        self.hero = Ps.Hero()
        self.hero_Group = pg.sprite.Group(self.hero)
        self.Boss_Group = pg.sprite.Group()
if __name__ == '__main__':

    game = PlaneGame()
    game.bgm_01.play()
    game.start_game()


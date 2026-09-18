import pygame as pg
import random
import math

pg.init()
pg.mixer.init()

pg.mixer.music.load("Âm-Thanh/NhạcNền.mp3")
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play(-1)
Bắn = pg.mixer.Sound("Âm-Thanh/Bắn.mp3")
Nạp_Đạn = pg.mixer.Sound("Âm-Thanh/NạpĐạn.wav")

screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Monster Killer")

gun_gốc = pg.image.load("Vũ-Khí/Súng.png").convert_alpha()
gun_gốc = pg.transform.scale(gun_gốc, (75, 75))

x_gun = 0
y_gun = 0
goc_rad = 0   # lưu góc theo radian
goc_deg = 0   # lưu góc theo độ

max_đạn = 25
đạn = max_đạn

chéo = pg.image.load("Số/chéo.png")
chéo = pg.transform.scale(chéo,(15, 25))

tên = pg.image.load("Tên.png").convert_alpha()
tên = pg.transform.scale(tên, (400, 400))
y_tên = 100

số_đạn = {
    số: pg.transform.scale(
        pg.image.load(f"Số/{số}.png").convert_alpha(),
        (15, 25),
    )
    for số in range(10)
}

monster_max = 15
monster_spawn = 0
monster_animation = 1
monster_animation_load = f"Quái-Vật/{monster_animation}.png"
monster_lật = False

player_idle_frames = [
    pg.transform.scale(
        pg.image.load(f"Chuyển-Động/Đứng-Yên/{frame}.png").convert_alpha(),
        (100, 100),
    )
    for frame in range(1, 5)
]
player_run_frames = [
    pg.transform.scale(
        pg.image.load(f"Chuyển-Động/Chạy/{frame}.png").convert_alpha(),
        (100, 100),
    )
    for frame in range(1, 7)
]
monster_frames = [
    pg.transform.scale(
        pg.image.load(f"Quái-Vật/{frame}.png").convert_alpha(),
        (100, 100),
    )
    for frame in range(1, 7)
]

size_start = 50
start_gốc = pg.image.load("start.png").convert_alpha()
start = pg.transform.scale(start_gốc, (size_start, size_start))
xoay_start_1 = 0
xoay_start_2 = 5
y_start = 300
start.set_alpha(0)

Máu_player = 100
thanh_máu = pg.image.load("hp/full.png")
che_máu = pg.image.load("hp/trắng.png")
load_máu = False

chuột_bth = pg.transform.scale(
    pg.image.load("Chuột/bth.png").convert_alpha(),
    (30, 30),
)
chuột_bắn = pg.transform.scale(
    pg.image.load("Chuột/bắn.png").convert_alpha(),
    (30, 30),
)
chuột_load = pg.transform.scale(
    pg.image.load("Chuột/load.png").convert_alpha(),
    (25, 25),
)
chuột = chuột_bth

x_player = 350
y_player = 250
player_lật = False
animation_index = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAP_COLOR = (10, 10, 10)

click = False
Start = False

cutdown = 0
class Monster(pg.sprite.Sprite):
    quái_gốc = monster_frames[0]

    def __init__(self, x, y):
        super().__init__()
        self.image = Monster.quái_gốc
        self.rect = self.image.get_rect(center=(x, y))
        self.x = float(x)
        self.y = float(y)
        self.hp = 100
        self.speed = 100

    def update(self, dt, monster_image):
        self.x_cũ = self.x
        dx = x_player - self.x
        dy = y_player - self.y
        goc_rad = math.atan2(dy, dx)

        self.x += self.speed * dt * math.cos(goc_rad)
        self.y += self.speed * dt * math.sin(goc_rad)
        self.rect.center = (int(self.x), int(self.y))

        if self.x - self.x_cũ < 0:
            monster_lật = True
        else:   
            monster_lật = False

        self.image = pg.transform.flip(monster_image, monster_lật, False)
                            
        if self.hp <= 0:
            self.kill()

class Bullet(pg.sprite.Sprite):
    đạn_gốc = pg.image.load("Vũ-Khí/Đạn.png").convert_alpha()
    đạn_gốc = pg.transform.scale(đạn_gốc, (14, 7))

    def __init__(self, x, y, speed, goc_rad):
        super().__init__()
        goc_deg = -math.degrees(goc_rad)
        self.image = pg.transform.rotate(Bullet.đạn_gốc, goc_deg)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.x = float(x)
        self.y = float(y)
        self.goc_rad = goc_rad
        self.killtime = 1
        self.hit = False

    def update(self, dt):
        self.x += self.speed * dt * math.cos(self.goc_rad)
        self.y += self.speed * dt * math.sin(self.goc_rad)
        self.rect.center = (int(self.x), int(self.y))

        if self.killtime <= 0.05:
            self.killtime -= dt
            if self.killtime <= 0:
                self.kill()
        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600:
            self.kill()

bullet_group = pg.sprite.Group()
monster_group = pg.sprite.Group()
clock = pg.time.Clock()

running = True
while running:
    dt = clock.tick(60) / 1000 
    chuột_x, chuột_y = pg.mouse.get_pos()

    x_gun = x_player + 50
    y_gun = y_player + 65
    dx = chuột_x - x_gun
    dy = chuột_y - y_gun
    goc_rad = math.atan2(dy, dx)
    goc_deg = -math.degrees(goc_rad)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            print("Lí Do: Đóng Game")
            running = False
        
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            click = True
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            click = False

    pg.display.set_caption(f"Monster Killer - FPS: {clock.get_fps():.1f}")

    if not Start:
        pg.mouse.set_visible(True)
        screen.fill(BLACK)
        screen.blit(tên, (200, y_tên))
        screen.blit(start, (400 - size_start // 2, y_start))
        
        if y_tên > 0:
            y_tên -= 100 * dt
        else:
            y_tên = 0
            start.set_alpha(255)
            if y_start < 350:
                y_start += 100 * dt
                size_start += 250 * dt
                start = pg.transform.scale(start_gốc, (int(size_start), int(size_start)))
            else:
                y_start = 350
                start = pg.transform.scale(start_gốc, (int(size_start), int(size_start)))
                
                if -100 < 400 - chuột_x < 100 and -25 < 450 - chuột_y < 100:
                    start = pg.transform.rotate(start, xoay_start_1)
                    start.set_alpha(200)
                    if xoay_start_1 > 5:
                        xoay_start_2 = -30 * dt
                    elif xoay_start_1 < -5:
                        xoay_start_2 = 30 * dt
                    xoay_start_1 += xoay_start_2
                    
                    if click:
                        pg.mouse.set_visible(False)
                        Start = True
                else:
                    xoay_start_1 = 0
                    start.set_alpha(255)
                    start = pg.transform.rotate(start, xoay_start_1)

    else:
        screen.fill(MAP_COLOR)

        if cutdown > 0:
            cutdown -= dt
        else:
            cutdown = 0

        keys = pg.key.get_pressed()
        is_moving = keys[pg.K_w] or keys[pg.K_s] or keys[pg.K_a] or keys[pg.K_d]

        if keys[pg.K_w]: y_player -= 150 * dt
        if keys[pg.K_s]: y_player += 150 * dt
        if keys[pg.K_a]: x_player -= 150 * dt
        if keys[pg.K_d]: x_player += 150 * dt

        if keys[pg.K_a] and not keys[pg.K_d]:
            player_lật = True
        elif keys[pg.K_d] and not keys[pg.K_a]:
            player_lật = False


        max_anim = 6 if is_moving else 4
        anim_speed = 8 if is_moving else 5
        folder = "Chuyển-Động/Chạy/" if is_moving else "Chuyển-Động/Đứng-Yên/"

        animation_index += anim_speed * dt
        if animation_index >= max_anim + 1 or animation_index < 1:
            animation_index = 1

        frames = player_run_frames if is_moving else player_idle_frames
        player_img = frames[int(animation_index) - 1]
        player_img = pg.transform.flip(player_img, player_lật, False)

        if x_player < 50: x_player = 50
        if x_player > 750: x_player = 750
        if y_player < 50: y_player = 50
        if y_player > 550: y_player = 550
        player_rect = player_img.get_rect(center=(x_player, y_player))
        screen.blit(player_img, player_rect)

        if len(monster_group) < monster_max:
            if monster_spawn <= 0:
                while True:
                    x_monster = random.randint(60, 740)
                    y_monster = random.randint(60, 540)
                    khoang_cach = math.hypot(
                        x_monster - (x_player + 50),
                        y_monster - (y_player + 50),
                    )
                    if khoang_cach > 180:
                        break
                monster = Monster(x_monster, y_monster)
                monster_group.add(monster)
                monster_spawn = random.randint(1,2)
            else:
                monster_spawn -= dt
                if monster_spawn < 0:
                    monster_spawn = 0

        monster_animation += 8 * dt
        if monster_animation >= len(monster_frames) + 1:
            monster_animation = 1
        monster_image = monster_frames[int(monster_animation) - 1]

        monster_group.update(dt, monster_image)
        monster_group.draw(screen)

        x_gun = x_player
        y_gun = y_player + 17
        dx = chuột_x - x_gun
        dy = chuột_y - y_gun
        goc_rad = math.atan2(dy, dx)
        goc_deg = -math.degrees(goc_rad)

        if dx < 0:
            gun_xu_ly = pg.transform.flip(gun_gốc, False, True)
        else:
            gun_xu_ly = gun_gốc

        if pg.mouse.get_pressed()[0] and cutdown == 0:
            if đạn > 0:
                bullet = Bullet(x_gun, y_gun, 500, goc_rad)
                bullet_group.add(bullet)
                cutdown = 0.25
                Bắn.play()
                đạn -= 1

            else:
                cutdown = 1.25
                Nạp_Đạn.play()
                đạn = max_đạn

        bullet_group.update(dt)
        va_cham = pg.sprite.groupcollide(
            bullet_group,
            monster_group,
            False,
            False,
        )
        for bullet, monsters in va_cham.items():
            if not bullet.hit:
                for monster in monsters:
                    monster.hp -= 25
                bullet.hit = True
                bullet.killtime = 0.05
                if đạn != 0:
                    chuột = chuột_bắn

        if not va_cham:
            chuột = chuột_bth

        if cutdown > 0.25:
            chuột = chuột_load
        
        bullet_group.draw(screen)

        gun_xoay = pg.transform.rotate(gun_xu_ly, goc_deg)
        gun_rect = gun_xoay.get_rect(center=(x_gun, y_gun))
        screen.blit(gun_xoay, gun_rect.topleft)

        hàng_chục, hàng_đơn_vị = divmod(đạn, 10)
        max_hàng_chục, max_hàng_đơn_vị = divmod(max_đạn, 10)

        screen.blit(số_đạn[hàng_chục], (10, 40))
        screen.blit(số_đạn[hàng_đơn_vị], (30, 40))
        screen.blit(chéo,(50,40))
        screen.blit(số_đạn[max_hàng_chục], (70, 40))
        screen.blit(số_đạn[max_hàng_đơn_vị], (90, 40))

        chuột_rect = chuột.get_rect(center=(chuột_x, chuột_y))
        screen.blit(chuột, chuột_rect)

    pg.display.update()

pg.quit()
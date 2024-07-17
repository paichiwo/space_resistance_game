import math
import random
from src.helpers import import_assets
from src.config import *
from src.timer import Timer
from src.sprites import Shot, Explosion


class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, screen, sound_manager, player, data, group):
        super().__init__(group)

        self.screen = screen
        self.sound_manager = sound_manager
        self.player = player
        self.group = group
        self.animation_speed = 20

        self.frames = import_assets(data['frames'])
        self.index = 0
        self.energy = data['energy']
        self.bump_power = data['bump_power']
        self.shot_score = data['shot_score']
        self.kill_score = data['kill_score']
        self.can_shoot = data['can_shoot']

        self.shots_group = pygame.sprite.Group()
        self.shot_power = 20
        # self.shoot_timer = Timer(5000, self.shoot, repeat=True, autostart=True)

        self.image = self.frames[self.index]

    def animate(self, dt):
        self.index += self.animation_speed * dt
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def shoot(self):
        if self.can_shoot:
            if 1 == random.choice([0, 0, 0, 0, 1]):
                dx = self.player.rect.centerx - self.rect.centerx
                dy = self.player.rect.centery - self.rect.centery
                direction = pygame.math.Vector2(dx, dy).normalize()
                Shot(self.rect, self.shots_group, 'enemy', direction)

    def collisions(self):
        if not self.player.god_mode:
            for sprite in self.group[0].sprites():
                for shot in sprite.shots_group:
                    if pygame.sprite.collide_mask(shot, self.player):
                        shot.kill()
                        self.player.current_energy -= sprite.shot_power
                        Explosion(shot.rect.center, self.group[1])
                        self.sound_manager.play_sound(SOUND_EFFECTS['explosion'])

    def deduct_energy(self, player_shot_power):
        self.energy -= player_shot_power
        if self.energy <= 0:
            self.kill()

    def kill_off_screen(self):
        if self.rect.top > HEIGHT * 2 or self.rect.right < -30 or self.rect.left > WIDTH + 50:
            self.kill()

    def update(self, dt):
        # self.shoot_timer.update()
        self.animate(dt)
        # self.shoot()

        self.shots_group.update(dt)
        self.shots_group.draw(self.screen)
        self.collisions()


class Enemy(EnemyBase):
    def __init__(self, screen, sound_manager, player, enemy_type, enemy_speed, waypoints, group):
        data = ENEMY_DATA[enemy_type]
        super().__init__(screen, sound_manager, player, data, group)

        self.enemy_type = enemy_type
        self.enemy_speed = enemy_speed
        self.waypoints = waypoints
        self.current_waypoint = 0

        self.pos = pygame.math.Vector2(waypoints[0])
        self.rect = self.image.get_rect(center=self.pos)

        # self.waypoints = [
        #     pygame.math.Vector2(random.randint(10, WIDTH - 10), random.randint(10, HEIGHT))
        #     for _ in range(3)
        # ]
        # self.current_waypoint = 0

    # def move(self, dt):
    #     if self.current_waypoint < len(self.waypoints):
    #         target = self.waypoints[self.current_waypoint]
    #         direction = target - self.pos
    #         distance = direction.length()
    #
    #         if distance > 0:
    #             direction.normalize_ip()
    #             self.pos += direction * self.enemy_speed * dt
    #             self.rect.midbottom = round(self.pos)
    #
    #             if distance < self.enemy_speed * dt:
    #                 self.current_waypoint += 1
    #     else:
    #         self.pos.y += self.enemy_speed * dt
    #         self.rect.midbottom = round(self.pos)

    def move(self, dt):
        if self.current_waypoint < len(self.waypoints):
            target_x, target_y = self.waypoints[self.current_waypoint]
            dx, dy = target_x - self.pos.x, target_y - self.pos.y
            dist = math.hypot(dx, dy)

            if dist != 0:
                dx, dy = dx / dist, dy / dist
                self.pos.x += dx * self.enemy_speed * dt
                self.pos.y += dy * self.enemy_speed * dt

                self.rect.x = self.pos.x
                self.rect.y = self.pos.y

            if dist < self.enemy_speed * dt:
                self.current_waypoint += 1

    def update(self, dt):
        super().update(dt)
        self.move(dt)
        self.kill_off_screen()
        # print(self.pos)


class Boss(EnemyBase):
    def __init__(self, screen, player, sound_manager, group):
        data = ENEMY_DATA['boss']
        super().__init__(screen, sound_manager, player, data, group)

        self.pos = pygame.math.Vector2(WIDTH / 2, 25)
        self.rect = self.image.get_rect(center=self.pos)

        self.direction = 1
        self.vert_speed = 40

    def move(self, dt):
        if self.pos.y >= 70:
            self.direction = -1
        elif self.pos.y <= 25:
            self.direction = 1

        self.pos.y += self.direction * self.vert_speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        super().update(dt)
        self.move(dt)
